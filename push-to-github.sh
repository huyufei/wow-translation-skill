#!/bin/bash

# GitHub 推送脚本
# 仓库地址: https://github.com/huyufei/wow-translation-skill

echo "🚀 开始推送到 GitHub..."
echo ""

# 检查远程仓库
echo "📋 检查远程仓库配置..."
git remote -v

echo ""
echo "📤 推送到 GitHub..."
git push -u origin main

echo ""
if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
    echo ""
    echo "🌐 查看仓库: https://github.com/huyufei/wow-translation-skill"
else
    echo "❌ 推送失败，请检查网络连接或手动执行:"
    echo "   git push -u origin main"
fi
