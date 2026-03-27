#!/usr/bin/env python3
"""
AI资讯自动抓取脚本
从配置的来源抓取最新 AI 新闻，使用 Claude 处理后保存为 JSON
"""

import os
import json
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv

# 配置路径
BASE_DIR = Path(__file__).parent.parent  # 项目根目录
ARTICLES_DIR = BASE_DIR / "docs" / "data" / "articles"
INDEX_FILE = BASE_DIR / "docs" / "data" / "index.json"
PROCESSED_FILE = BASE_DIR / "docs" / "data" / ".processed_urls.json"
AI_NEWS_DIR = BASE_DIR / "docs" / "ai-news"
NEWS_JSON_FILE = BASE_DIR / "docs" / "data" / "news.json"

# 加载环境变量
load_dotenv(BASE_DIR / ".env")

OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "anthropic/claude-sonnet-4")

# 要抓取的来源（RSS feeds 和 API endpoints）
SOURCES = [
    # AI 公司官方博客
    {"name": "Anthropic", "url": "https://www.anthropic.com/news", "type": "web"},
    {"name": "OpenAI", "url": "https://openai.com/blog", "type": "web"},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog", "type": "web"},

    # 科技媒体 RSS
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "type": "rss"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/ai/feed/", "type": "rss"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "type": "rss"},

    # 中文媒体
    {"name": "机器之心", "url": "https://www.jiqizhixin.com/", "type": "web"},
    {"name": "量子位", "url": "https://www.qbitai.com/", "type": "web"},
]


def load_processed_urls():
    """加载已处理的 URL 列表"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)
    return {}


def save_processed_urls(processed):
    """保存已处理的 URL 列表"""
    with open(PROCESSED_FILE, "w") as f:
        json.dump(processed, f, indent=2)


def fetch_rss(url):
    """获取 RSS feed 内容"""
    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  获取 RSS 失败: {e}")
        return None


def fetch_webpage(url):
    """获取网页内容"""
    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  获取网页失败: {e}")
        return None


def call_claude(prompt, max_tokens=4096):
    """调用 Claude API"""
    if not OPENROUTER_API_KEY:
        print("错误: 未设置 OPENROUTER_API_KEY")
        return None

    try:
        response = requests.post(
            f"{OPENROUTER_BASE_URL}chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-startup-news.local",
                "X-Title": "AI Startup News Crawler"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  调用 Claude 失败: {e}")
        return None


def extract_articles_from_content(source_name, content, content_type):
    """使用 Claude 从内容中提取文章"""
    prompt = f"""分析以下来自 {source_name} 的{content_type}内容，提取最近7天内发布的 AI 相关新闻文章。

内容：
{content[:15000]}

请提取文章并以 JSON 数组格式返回，每篇文章包含：
- title: 文章标题
- url: 文章链接
- date: 发布日期 (YYYY-MM-DD 格式)
- summary: 简短摘要 (1-2句话)

只返回 JSON 数组，不要其他内容。如果没有找到相关文章，返回空数组 []。
示例格式：
[{{"title": "...", "url": "...", "date": "2026-01-28", "summary": "..."}}]
"""

    result = call_claude(prompt)
    if not result:
        return []

    # 解析 JSON
    try:
        # 尝试提取 JSON 部分
        json_match = re.search(r'\[[\s\S]*\]', result)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        print(f"  解析 JSON 失败")
    return []


def process_article(article_info, source_name):
    """处理单篇文章，生成完整的中英文内容"""
    title = article_info.get('title', '').lower()
    summary = article_info.get('summary', '').lower()

    # 判断是否为投资类文章（排除诉讼类）
    investment_keywords = ['funding', 'raised', 'investment', 'valuation', 'ipo', 'series a', 'series b', 'series c',
                          'investor', '融资', '估值', '投资', '上市', 'seed round']
    exclude_keywords = ['sue', 'lawsuit', 'litigation', '诉讼', '起诉', 'copyright', 'infringement']

    has_investment = any(kw in title or kw in summary for kw in investment_keywords)
    has_exclude = any(kw in title or kw in summary for kw in exclude_keywords)
    is_investment = has_investment and not has_exclude

    if is_investment:
        # 投资类文章 prompt
        prompt = f"""生成投资新闻的JSON（直接返回，不要代码块）。

标题: {article_info.get('title', '')}
摘要: {article_info.get('summary', '')}

JSON格式：
{{"title_zh":"标题","title_en":"Title","tags":["tag1","tag2"],"content_zh":"正文","content_en":"content"}}

中文正文结构：
## 背景信息
介绍公司背景和本轮融资基本情况

## 总结
完整分析融资意义、资金用途、市场反应，把事情讲清楚

## Insight
**对创业者**：2点启示，每点一句话
**对投资人**：1点分析

要求：语气专业严谨，突出关键数据，分析要有深度"""
    else:
        # AI 动态类文章 prompt
        prompt = f"""生成AI新闻的JSON（直接返回，不要代码块）。

标题: {article_info.get('title', '')}
摘要: {article_info.get('summary', '')}

JSON格式：
{{"title_zh":"标题","title_en":"Title","tags":["tag1","tag2"],"content_zh":"正文","content_en":"content"}}

中文正文结构：
## 背景信息
介绍事件背景和相关方

## 总结
完整分析核心内容，把事情的来龙去脉讲清楚，专业但易懂

## Insight
**对创业者**：2点启示，每点一句话
**对行业**：1点趋势判断

要求：语气专业稳重，解释清楚技术或商业逻辑，有独到见解"""

    # 尝试最多3次
    for attempt in range(3):
        result = call_claude(prompt, max_tokens=8192)
        if not result:
            continue

        try:
            # 清理可能的 markdown 代码块
            result = re.sub(r'^```json\s*', '', result.strip())
            result = re.sub(r'\s*```$', '', result)
            return json.loads(result)
        except json.JSONDecodeError as e:
            if attempt < 2:
                print(f"  第{attempt+1}次解析失败，重试...")
            else:
                print(f"  处理文章失败: {e}")
                print(f"  原始返回内容前300字符: {result[:300]}")

    return None


def get_next_id():
    """获取下一个文章 ID"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)
            if index["articles"]:
                return max(a["id"] for a in index["articles"]) + 1
    return 1


def save_article(article_data, article_info, source_name):
    """保存文章到 JSON 文件"""
    next_id = get_next_id()
    date = article_info.get("date", datetime.now().strftime("%Y-%m-%d"))

    # 生成 slug
    slug_base = re.sub(r'[^\w\s-]', '', article_data["title_en"].lower())
    slug_base = re.sub(r'[-\s]+', '-', slug_base).strip('-')[:50]
    slug = f"{date}-{slug_base}"

    # 完整文章数据
    full_article = {
        "id": next_id,
        "slug": slug,
        "date": date,
        "category": "ai-news",
        "source": source_name,
        "source_url": article_info.get("url", ""),
        "tags": article_data.get("tags", []),
        "title_zh": article_data["title_zh"],
        "title_en": article_data["title_en"],
        "content_zh": article_data["content_zh"],
        "content_en": article_data["content_en"],
        "created_at": f"{date}T00:00:00Z",
        "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # 保存文章文件
    article_file = ARTICLES_DIR / f"{slug}.json"
    with open(article_file, "w", encoding="utf-8") as f:
        json.dump(full_article, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 保存: {slug}")
    return full_article


def update_index():
    """更新索引文件"""
    articles = []
    for article_file in ARTICLES_DIR.glob("*.json"):
        with open(article_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            articles.append({
                "id": data["id"],
                "slug": data["slug"],
                "date": data["date"],
                "category": data.get("category", "ai-news"),
                "title_zh": data.get("title_zh") or data.get("zh", {}).get("title", ""),
                "title_en": data.get("title_en") or data.get("en", {}).get("title", ""),
                "tags": data.get("tags", []),
                "updated_at": data.get("updated_at", "")
            })

    # 按日期排序
    articles.sort(key=lambda x: x["date"], reverse=True)

    index_data = {
        "total": len(articles),
        "last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "articles": articles
    }

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    print(f"\n索引已更新: {len(articles)} 篇文章")


def main():
    """主函数"""
    print("=" * 50)
    print(f"AI资讯自动抓取 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # 确保目录存在
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

    # 加载已处理的 URL
    processed = load_processed_urls()
    new_articles = 0

    for source in SOURCES:
        print(f"\n抓取: {source['name']}")

        # 获取内容
        if source["type"] == "rss":
            content = fetch_rss(source["url"])
            content_type = "RSS"
        else:
            content = fetch_webpage(source["url"])
            content_type = "网页"

        if not content:
            continue

        # 提取文章列表
        articles = extract_articles_from_content(source["name"], content, content_type)
        print(f"  找到 {len(articles)} 篇文章")

        for article_info in articles:
            url = article_info.get("url", "")
            if not url:
                continue

            # 检查是否已处理
            url_hash = hashlib.md5(url.encode()).hexdigest()
            if url_hash in processed:
                print(f"  跳过已处理: {article_info.get('title', '')[:30]}...")
                continue

            # 处理文章
            print(f"  处理: {article_info.get('title', '')[:40]}...")
            article_data = process_article(article_info, source["name"])

            if article_data:
                save_article(article_data, article_info, source["name"])
                processed[url_hash] = {
                    "url": url,
                    "title": article_info.get("title", ""),
                    "processed_at": datetime.now().isoformat()
                }
                new_articles += 1

    # 保存已处理的 URL
    save_processed_urls(processed)

    # 更新索引
    update_index()

    print(f"\n完成! 新增 {new_articles} 篇文章")
    print("=" * 50)


if __name__ == "__main__":
    main()
