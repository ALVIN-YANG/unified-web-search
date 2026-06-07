---
name: web-search
description: |
  统一搜索工具，支持 Tavily、Exa 等多个搜索提供商，全局 key 池轮询。
  当用户需要搜索网页、获取实时信息、查找文档时使用此 skill。
---

# Web Search

> 详细使用说明请查看 [skills/web-search/SKILL.md](skills/web-search/SKILL.md)

## 快速开始

```bash
# 搜索
search.py "Python best practices"

# 指定提供商
search.py "React hooks" --provider exa

# 查看配置
search.py --check
```

## 安装

```bash
git clone https://github.com/ALVIN-YANG/unified-web-search.git /tmp/unified-web-search
cd /tmp/unified-web-search && python3 install.py
```
