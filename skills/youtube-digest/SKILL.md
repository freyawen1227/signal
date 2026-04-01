---
name: youtube-digest
description: Generate SIGNAL platform articles from YouTube videos. Takes a YouTube URL, downloads transcript, and produces a structured Chinese analysis article. Outputs markdown and publishes to articles/ JSON directory via publish.py. Use when user provides a YouTube URL and wants to create content for the SIGNAL platform.
---

# AI Insider — YouTube 视频解读生成器

从 YouTube AI 视频自动生成 AI Insider 平台的结构化解读文章。

## 支持平台

| URL Pattern | Platform | Method |
|-------------|----------|--------|
| youtube.com, youtu.be | YouTube | 字幕 → Whisper fallback |
| twitter.com, x.com | Twitter/X | Whisper (自动) |

## 文件组织

```
transcripts/
└── {video-title}/
    ├── audio.mp3          # 音频文件（Whisper fallback时）
    ├── transcript.txt     # 清洗后的原始字幕
    ├── output.md          # AI Insider 格式的解读文章
    └── metadata.json      # 文章元数据（用于 publish.py）
```

## 完整工作流

```
1. 创建文件夹: transcripts/{sanitized-title}/
2. 获取字幕（优先字幕文件，fallback Whisper）
3. 清洗并保存 transcript.txt
4. 生成 AI Insider 格式的 output.md
5. 用 publish.py 发布到 articles/ 目录
6. [可选] 同步到飞书
```

## 选题标准

面向 AI 创业者的内容筛选指南。满足**任一**收录条件即可。

### 收录

- **人物维度**：嘉宾是 AI / 科技公司创始人、CEO、核心高管、知名研究员
- **话题维度**：涉及 AI 应用落地、产品策略、技术趋势、融资、增长、商业模式
- **事件维度**：科技行业重大事件（发布会、并购、政策）的深度讨论
- **方法论维度**：创业方法论、产品思维、组织管理——即使标题不带"AI"，只要嘉宾或内容与科技/AI生态强相关即可（如 Figma CEO 聊产品设计变革）

### 排除

- 纯娱乐 / 纯政治 / 纯宏观经济（除非直接影响 AI 行业，如芯片禁令、能源政策）
- 短于 15 分钟的片段式内容
- 旧视频重新上传或剪辑合集

### 频道扫描建议

搜索时不要只用 "AI" 关键词，应浏览频道最近一周的所有视频标题，根据嘉宾身份和话题相关性判断是否收录。

## Step 1: 环境准备 & 获取视频信息

```bash
# 检查 yt-dlp
which yt-dlp || brew install yt-dlp

# 获取视频标题（文件名安全处理）
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '' | cut -c1-80)

# 获取频道名和时长
CHANNEL=$(yt-dlp --print "%(channel)s" "URL")
DURATION=$(yt-dlp --print "%(duration_string)s" "URL")

# 创建输出文件夹
mkdir -p "transcripts/${VIDEO_TITLE}"
cd "transcripts/${VIDEO_TITLE}"
```

## Step 2: 获取字幕

### YouTube
```bash
# 优先尝试字幕文件
yt-dlp --write-auto-sub --skip-download --output "temp" "URL"

# 如果有 VTT 文件，清洗它
if ls temp*.vtt 1>/dev/null 2>&1; then
    VTT_FILE=$(ls temp*.vtt | head -n 1)
    python3 -c "
import re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > transcript.txt
    rm temp*.vtt
else
    # Fallback: 下载音频 + Whisper
    yt-dlp -x --audio-format mp3 --output "audio.%(ext)s" "URL"
    command -v whisper || pip3 install openai-whisper --break-system-packages -q
    whisper audio.mp3 --model base --output_format txt --output_dir .
    mv audio.txt transcript.txt
fi
```

### Twitter/X（全自动）
```bash
yt-dlp -x --audio-format mp3 --output "audio.%(ext)s" "URL"
command -v whisper || pip3 install openai-whisper --break-system-packages -q
whisper audio.mp3 --model base --output_format txt --output_dir .
mv audio.txt transcript.txt
```

## Step 3: 生成中文解读

读取 transcript.txt，生成 output.md：

```markdown
# {视频标题}

**来源**: {URL}
**平台**: YouTube / Twitter
**时长**: {duration}

---

## 总结
{500 字以内}

## Insight
{个人成长启发，务实直白}
{加分项：强相关时补充业务启发，不硬凑}

## 全文意译

### {段落标题}
{意译内容}

【名词解释】{术语}: {解释}
```

### 翻译原则

- **意译优先**：按逻辑重组，不逐句翻译
- **术语必解释**：专业名词用括号或单独段落解释
- **补充背景**：主动补充视频默认观众已知的背景
- **通俗易懂**：假设读者无技术背景

## Step 4: 发布文章到 articles/ 目录

生成完 output.md 后，使用 publish.py 将文章发布到 JSON 数据目录：

```bash
python scripts/publish.py {article-id} \
  --title "{解读标题}" \
  --date {YYYY-MM-DD} \
  --source "{频道名}" \
  --category {interview|debate|tech|keynote} \
  --tags "Tag1,Tag2,Tag3" \
  --content "transcripts/{video-title}/output.md" \
  --video-url "{YouTube URL}"
```

这会自动：
1. 创建 `articles/{article-id}.json`
2. 更新 `articles/index.json`（按日期倒序）

### 分类规则

| category | catLabel | 适用场景 |
|----------|----------|---------|
| interview | 深度访谈 | 1对1 播客访谈、长对话 |
| keynote | 大会演讲 | 产品发布会、大会演讲 |
| debate | 圆桌激辩 | 多人讨论、辩论 |
| tech | 技术解析 | 技术教学、论文解读、Demo |
| tutorial | 教程 | 动手教程、工具使用 |

### article-id 命名规则

`{嘉宾姓氏小写}-{主题关键词}`，如 `altman-agi`、`huang-ces2026`、`karpathy-llm`

## Step 5: [可选] 同步到飞书

```bash
python3 scripts/feishu_sync.py \
  --markdown "output.md" \
  --title "{视频标题}" \
  --url "{原视频URL}"
```

## 用户背景

参考 [references/user-context.md](references/user-context.md) 自定义输出风格。

## 飞书配置

创建 `config/feishu.json`（参考 `config/feishu.example.json`）：

```json
{
  "app_id": "YOUR_FEISHU_APP_ID",
  "app_secret": "YOUR_FEISHU_APP_SECRET",
  "open_id": "YOUR_FEISHU_OPEN_ID"
}
```
