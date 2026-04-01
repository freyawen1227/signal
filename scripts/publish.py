#!/usr/bin/env python3
"""
publish.py — 发布新文章到 SIGNAL

用法:
  python scripts/publish.py <article-id> \
    --title "文章标题" \
    --date 2026-03-30 \
    --source "Lex Fridman Podcast" \
    --category interview \
    --tags "Tag1,Tag2,Tag3" \
    --content content.md \
    [--video-url "https://youtube.com/..."]

功能:
  1. 创建 articles/<id>.json（完整文章）
  2. 更新 articles/index.json（添加元数据，按日期倒序）
"""

import argparse
import json
import os
import sys

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'articles')


def main():
    parser = argparse.ArgumentParser(description='发布新文章到 SIGNAL')
    parser.add_argument('id', help='文章ID (如 huang-lex-fridman)')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--date', required=True, help='日期 YYYY-MM-DD')
    parser.add_argument('--source', required=True, help='来源频道')
    parser.add_argument('--category', required=True, choices=['interview', 'debate', 'tech', 'keynote'])
    parser.add_argument('--tags', required=True, help='标签，逗号分隔')
    parser.add_argument('--content', required=True, help='Markdown内容文件路径')
    parser.add_argument('--video-url', default='', help='YouTube视频链接')

    args = parser.parse_args()

    # Read content
    with open(args.content, 'r', encoding='utf-8') as f:
        content = f.read()

    tags = [t.strip() for t in args.tags.split(',') if t.strip()]

    # Build article object
    article = {
        'id': args.id,
        'title': args.title,
        'date': args.date,
        'source': args.source,
        'category': args.category,
        'tags': tags,
        'videoUrl': args.video_url,
        'content': content,
    }

    # Write individual article file
    article_path = os.path.join(ARTICLES_DIR, f'{args.id}.json')
    if os.path.exists(article_path):
        print(f'⚠ 文章 {args.id} 已存在，将覆盖')

    with open(article_path, 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)

    # Update index.json
    index_path = os.path.join(ARTICLES_DIR, 'index.json')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = []

    # Remove existing entry with same id
    index = [e for e in index if e['id'] != args.id]

    # Add new entry (no content)
    index.append({
        'id': args.id,
        'title': args.title,
        'date': args.date,
        'source': args.source,
        'category': args.category,
        'tags': tags,
        'videoUrl': args.video_url,
    })

    # Sort by date descending
    index.sort(key=lambda x: x['date'], reverse=True)

    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f'✓ 已发布: articles/{args.id}.json')
    print(f'✓ 索引已更新: {len(index)} 篇文章')


if __name__ == '__main__':
    main()
