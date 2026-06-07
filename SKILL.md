---
name: web-search
description: |
  统一搜索工具，支持 Tavily、Exa 等多个搜索提供商，全局 key 池轮询。
  当用户需要搜索网页、获取实时信息、查找文档时使用此 skill。
---

# Web Search

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

**手动安装：**
```bash
git clone https://github.com/ALVIN-YANG/unified-web-search.git /tmp/unified-web-search
cd /tmp/unified-web-search && python3 install.py
```

**AI 对话安装：**
复制以下内容给 AI：
```
请执行：git clone https://github.com/ALVIN-YANG/unified-web-search.git /tmp/unified-web-search && cd /tmp/unified-web-search && python3 install.py
```

## 功能

- **全局 Key 池**：所有 key 统一轮询
- **多提供商**：Tavily（返回答案）、Exa（语义搜索）
- **故障转移**：自动切换失败的 key
- **代理支持**：HTTP/HTTPS 代理

## 使用场景

| 场景 | 命令 |
|------|------|
| 搜索文档 | `search.py "Python async tutorial"` |
| 查找代码 | `search.py "React hooks example"` |
| 深度搜索 | `search.py "machine learning" --depth advanced` |

## 并发限制

| 提供商 | 免费额度 | RPM |
|--------|---------|-----|
| Tavily | 1000 次/月 | 100 |
| Exa | 1000 次/月 | 1000 |

## 管理 Key

```bash
search.py --add-key tavily "tvly-xxx"
search.py --add-key exa "exa-xxx"
search.py --remove-key tavily "tvly-xxx"
```

## 详细文档

- [README.md](README.md) - 完整说明
- [config.example.json](config.example.json) - 配置示例
