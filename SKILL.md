---
name: web-search
description: |
  统一搜索工具，支持 Tavily、Exa 等多个搜索提供商，全局 key 池轮询。
  当用户需要搜索网页、获取实时信息、查找文档时使用此 skill。
  支持代理配置，适用于 Claude Code、Codex、Cursor 等主流 AI 工具。
---

# Web Search - 统一搜索工具

## 快速开始

```bash
# 搜索
python3 ~/.claude/skills/web-search/search.py "Python best practices"

# 指定提供商
python3 ~/.claude/skills/web-search/search.py "React hooks" --provider exa

# 查看配置
python3 ~/.claude/skills/web-search/search.py --check
```

## 安装配置

用户可通过 AI 对话完成安装：

```
用户: 帮我安装 web-search skill
AI: 运行 python3 install.py，按提示配置
```

## 功能特性

- **全局 Key 池**：所有 key 统一轮询，不区分提供商
- **多提供商**：Tavily（返回答案）、Exa（语义搜索）
- **故障转移**：主 key 失败自动切换下一个
- **代理支持**：HTTP/HTTPS 代理配置
- **并发限制**：
  - Tavily: 100 RPM（每分钟请求数）
  - Exa: 1000 RPM

## 使用场景

| 场景 | 命令 |
|------|------|
| 搜索文档 | `search.py "Python async tutorial"` |
| 获取最新信息 | `search.py "2024 AI trends"` |
| 查找代码示例 | `search.py "React hooks example" --provider exa` |
| 深度搜索 | `search.py "machine learning" --depth advanced` |

## 配置文件

位置：`~/.config/unified-web-search/config.json`

```json
{
  "proxy": { "enabled": false, "url": "http://localhost:7897" },
  "keys": [
    { "provider": "tavily", "key": "tvly-xxx" },
    { "provider": "exa", "key": "exa-xxx" }
  ],
  "default_count": 5,
  "default_depth": "basic",
  "fallback": true
}
```

## 管理命令

```bash
# 添加 key
search.py --add-key tavily "tvly-xxx"
search.py --add-key exa "exa-xxx"

# 移除 key
search.py --remove-key tavily "tvly-xxx"

# 查看状态
search.py --check
```

## 提供商对比

| 提供商 | 免费额度 | RPM | 特点 |
|--------|---------|-----|------|
| Tavily | 1000 次/月 | 100 | 返回 AI 答案 |
| Exa | 1000 次/月 | 1000 | 语义搜索 |

## 详细文档

- [README.md](README.md) - 完整使用说明
- [config.example.json](config.example.json) - 配置示例
