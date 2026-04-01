# SIGNAL — AI播客收录站

YouTube 上最有价值的 AI 播客，翻译、深度解读为中文长文。

## 收录频道

Lex Fridman / All-In Podcast / 20VC / No Priors / BG2 Pod / Lenny's Podcast / Lightcone (YC)

## 项目结构

```
signal/
├── product-preview.html   # Landing page
├── app.html               # 文章列表页
├── article.html           # 文章详情页
├── articles/              # 文章数据（JSON）
│   ├── index.json         # 文章索引（元数据，按日期倒序）
│   └── {id}.json          # 单篇文章完整数据
├── scripts/
│   ├── publish.py         # 发布新文章
│   └── update_news.py     # 数据源更新
└── skills/                # Claude Code skills
```

## 本地开发

```bash
python3 -m http.server 8000
# 访问 http://localhost:8000/product-preview.html
```

## 发布新文章

```bash
python scripts/publish.py <article-id> \
  --title "标题" --date 2026-03-30 \
  --source "频道名" --category interview \
  --tags "Tag1,Tag2" --content output.md
```

## 文章格式

每篇解读包含：总结 → 核心洞察(Insight) → 全文意译 + 名词解释

## License

MIT
