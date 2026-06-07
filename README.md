# Unified Web Search

统一搜索工具，支持 Tavily、Exa 等多个搜索提供商，全局 key 池轮询。

## ✨ 特性

- ✅ **全局 Key 池**：所有 key 统一轮询
- ✅ **多提供商**：Tavily、Exa
- ✅ **故障转移**：自动切换失败的 key
- ✅ **代理支持**：HTTP/HTTPS 代理
- ✅ **多 AI 工具**：Claude Code、Codex、Cursor 等

## 📊 并发限制

| 提供商 | 免费额度 | RPM | 说明 |
|--------|---------|-----|------|
| **Tavily** | 1000 次/月 | 100 | 每分钟 100 请求 |
| **Exa** | 1000 次/月 | 1000 | 每分钟 1000 请求 |

> **RPM** = Requests Per Minute（每分钟请求数）

## 🚀 快速开始

### 方式一：AI 对话安装（推荐）

直接告诉你的 AI 助手：

```
帮我安装 web-search skill
```

AI 会引导你完成配置。

### 方式二：命令行安装

```bash
git clone https://github.com/ALVIN-YANG/unified-web-search.git
cd unified-web-search
python3 install.py
```

### 方式三：手动配置

```bash
# 1. 克隆项目
git clone https://github.com/ALVIN-YANG/unified-web-search.git

# 2. 创建配置目录
mkdir -p ~/.config/unified-web-search

# 3. 复制配置文件
cp config.example.json ~/.config/unified-web-search/config.json

# 4. 编辑配置
vim ~/.config/unified-web-search/config.json

# 5. 安装到 AI 工具
ln -s "$(pwd)" ~/.claude/skills/web-search
```

## ⚙️ 代理配置

如果需要代理访问外部 API：

### 常见代理端口

| 代理软件 | 端口 | 地址 |
|---------|------|------|
| Clash / Clash Verge | 7897 | `http://localhost:7897` |
| V2Ray | 10809 | `http://localhost:10809` |
| Shadowsocks | 1080 | `http://localhost:1080` |
| Surge | 6152 | `http://localhost:6152` |

### 配置方法

编辑 `~/.config/unified-web-search/config.json`：

```json
{
  "proxy": {
    "enabled": true,
    "url": "http://localhost:7897"
  }
}
```

### 验证代理

```bash
curl -x http://localhost:7897 https://api.tavily.com
```

## 🔑 获取 API Key

### Tavily（免费 1000 次/月）

1. 访问 https://app.tavily.com/home
2. 注册账号
3. 获取 API key

### Exa（免费 1000 次/月）

1. 访问 https://exa.ai
2. 注册账号
3. 获取 API key

## 📖 使用方法

### 命令行

```bash
# 基本搜索
search.py "Python best practices"

# 指定提供商
search.py "React hooks" --provider exa

# 深度搜索
search.py "AI trends" --depth advanced

# 查看配置
search.py --check
```

### 管理 Key

```bash
# 添加
search.py --add-key tavily "tvly-xxx"
search.py --add-key exa "exa-xxx"

# 移除
search.py --remove-key tavily "tvly-xxx"
```

### 各 AI 工具路径

```bash
# Claude Code
~/.claude/skills/web-search/search.py "搜索内容"

# Codex
~/.codex/tools/web-search/search.py "搜索内容"

# Cursor
~/.cursor/tools/web-search/search.py "搜索内容"

# Windsurf
~/.windsurf/tools/web-search/search.py "搜索内容"

# Continue
~/.continue/tools/web-search/search.py "搜索内容"
```

## 🔄 轮询机制

所有 key 统一池管理，按顺序轮询：

```
key1 → key2 → key3 → key1 → ...
```

不区分提供商，全局轮询。

## 🔁 故障转移

当 `fallback: true` 时：
1. 主 key 失败
2. 自动尝试下一个 key
3. 直到成功或全部失败

## 📁 项目结构

```
unified-web-search/
├── SKILL.md              # Skill 说明
├── README.md             # 完整文档
├── install.py            # 安装脚本
├── search.py             # 主入口
├── config.example.json   # 配置示例
└── src/
    ├── config.py         # 配置管理
    ├── key_pool.py       # Key 池轮询
    ├── search.py         # 搜索逻辑
    └── providers/        # 提供商实现
        ├── tavily.py
        └── exa.py
```

## 🛠️ 扩展提供商

```python
# src/providers/new_provider.py
from .base import BaseProvider, SearchResponse

class NewProvider(BaseProvider):
    name = "new_provider"

    def search(self, query, api_key, count=5, **kwargs):
        # 实现搜索
        return SearchResponse(provider=self.name, results=[...])
```

注册：编辑 `src/providers/__init__.py`

## 📄 License

MIT
