# AI创业资讯 / AI Startup News

面向AI创业者的权威资讯聚合平台 | Authoritative news aggregation platform for AI entrepreneurs

## 快速开始 / Quick Start

### 安装依赖 / Install Dependencies

```bash
npm install
```

### 本地开发 / Local Development

```bash
npm run dev
```

访问 http://localhost:5173 查看网站。

### 构建 / Build

```bash
npm run build
```

### 预览构建结果 / Preview Build

```bash
npm run preview
```

## 项目结构 / Project Structure

```
AI资讯/
├── package.json
├── docs/
│   ├── .vitepress/
│   │   ├── config.ts          # 站点配置 / Site configuration
│   │   └── theme/
│   │       ├── index.ts       # 主题入口 / Theme entry
│   │       └── custom.css     # 自定义样式 / Custom styles
│   ├── index.md               # 首页 / Home page
│   ├── sources.md             # 信息来源 / Information sources
│   ├── industry/              # 行业动态 / Industry news
│   ├── technology/            # 技术进展 / Technology
│   ├── products/              # 产品动向 / Products
│   ├── investment/            # 投资市场 / Investment
│   └── en/                    # 英文版本 / English version
└── README.md
```

## 添加新文章 / Adding New Articles

在对应分类目录下创建 Markdown 文件，使用以下模板：

Create a Markdown file in the corresponding category directory using this template:

```markdown
---
title: 文章标题 / Article Title
date: 2025-01-28
category: technology
tags: [tag1, tag2]
source: https://example.com/article
source_name: Source Name
lang: zh  # or 'en'
---

# 文章标题 / Article Title

## 核心要点 / Key Points
- Point 1
- Point 2

## 详细内容 / Details
...

## 原文链接 / Original Link
[Source Name](https://example.com/article)
```

## 分类说明 / Categories

- **industry** - 行业动态 / Industry News
- **technology** - 技术进展 / Technology
- **products** - 产品动向 / Products
- **investment** - 投资市场 / Investment

## 部署 / Deployment

### Vercel

1. 将代码推送到 GitHub
2. 在 Vercel 中导入项目
3. 构建命令设置为 `npm run build`
4. 输出目录设置为 `docs/.vitepress/dist`

### Netlify

1. 将代码推送到 GitHub
2. 在 Netlify 中导入项目
3. 构建命令设置为 `npm run build`
4. 发布目录设置为 `docs/.vitepress/dist`

## 技术栈 / Tech Stack

- [VitePress](https://vitepress.dev/) - 静态网站生成器
- [Vue 3](https://vuejs.org/) - 前端框架
- [Markdown](https://www.markdownguide.org/) - 内容编写

## License

MIT
