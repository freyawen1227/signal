#!/bin/bash
# AI资讯自动更新脚本
# 使用方法: ./run_update.sh

cd /Users/freya/Desktop/AI资讯

# 激活虚拟环境
source venv/bin/activate

# 运行更新脚本
python3 scripts/update_news.py

# 记录日志
mkdir -p logs
echo "[$(date)] 更新完成" >> logs/update.log
