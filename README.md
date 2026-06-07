# Unified Web Search

统一搜索工具，支持多个搜索提供商（Tavily、Exa 等），全局 key 池轮询。

## ✨ 特性

- ✅ **全局 Key 池**：所有 key 统一管理，轮询使用
- ✅ **多提供商**：支持 Tavily、Exa，易于扩展
- ✅ **故障转移**：主 key 失败自动切换下一个
- ✅ **代理支持**：HTTP/HTTPS 代理配置
- ✅ **零硬编码**：所有配置外置
- ✅ **交互式安装**：引导式配置向导

## 🚀 快速开始

### 方式一：交互式安装（推荐）

```bash
# 克隆项目
git clone https://github.com/ALVIN-YANG/unified-web-search.git
cd unified-web-search

# 运行安装向导
python3 install.py
```

安装向导会引导你完成：
1. **选择 AI 工具**（支持多选）
2. 代理配置
3. API key 添加
4. 自动安装到对应工具

### 支持的 AI 工具

| 工具 | 安装路径 |
|------|---------|
| **Claude Code** | `~/.claude/skills/web-search/` |
| **Codex (OpenAI)** | `~/.codex/tools/web-search/` |
| **OpenClaw** | `~/.openclaw/tools/web-search/` |
| **Cursor** | `~/.cursor/tools/web-search/` |
| **Windsurf** | `~/.windsurf/tools/web-search/` |
| **Continue** | `~/.continue/tools/web-search/` |

### 方式二：手动安装

```bash
# 克隆项目
git clone https://github.com/ALVIN-YANG/unified-web-search.git
cd unified-web-search

# 复制配置示例
cp config.example.json config.json

# 编辑配置
vim config.json

# 测试运行
python3 search.py --check
```

## ⚙️ 代理配置

如果你的网络环境需要代理才能访问外部 API，请按以下步骤配置。

### 常见代理软件端口

| 代理软件 | 默认端口 | 代理地址 |
|---------|---------|---------|
| **Clash** | 7897 | `http://localhost:7897` |
| **Clash Verge** | 7897 | `http://localhost:7897` |
| **V2Ray** | 10809 | `http://localhost:10809` |
| **Shadowsocks** | 1080 | `http://localhost:1080` |
| **Surge** | 6152 | `http://localhost:6152` |
| **Quantumult X** | 9090 | `http://localhost:9090` |

### 配置方式

#### 方式一：使用安装向导

```bash
python3 install.py
# 在代理配置步骤选择"是"并输入代理地址
```

#### 方式二：手动编辑配置文件

编辑 `config.json`：

```json
{
  "proxy": {
    "enabled": true,
    "url": "http://localhost:7897"
  }
}
```

#### 方式三：命令行参数

```bash
# 临时使用代理（开发中）
python3 search.py --proxy http://localhost:7897 "搜索内容"
```

### 验证代理

```bash
# 测试代理连接
curl -x http://localhost:7897 https://api.tavily.com --connect-timeout 5

# 测试搜索
python3 search.py "test" --check
```

### 代理故障排查

1. **检查代理是否运行**
   ```bash
   # Clash
   curl http://localhost:7897
   
   # 或查看进程
   ps aux | grep clash
   ```

2. **检查代理端口**
   ```bash
   lsof -i :7897
   ```

3. **测试代理连接**
   ```bash
   curl -x http://localhost:7897 https://www.google.com
   ```

4. **查看代理日志**
   - Clash: 查看 `~/.config/clash/` 目录
   - V2Ray: 查看日志文件

## 🔑 API Key 配置

### 获取 API Key

#### Tavily（免费 1000 次/月）

1. 访问 https://app.tavily.com/home
2. 注册账号
3. 在 Dashboard 获取 API key

#### Exa（免费 1000 次/月）

1. 访问 https://exa.ai
2. 注册账号
3. 在 Dashboard 获取 API key

### 添加 Key

```bash
# 使用安装向导
python3 install.py

# 或命令行添加
python3 search.py --add-key tavily "tvly-dev-xxx"
python3 search.py --add-key exa "exa-xxx"

# 查看当前配置
python3 search.py --check
```

### 配置文件格式

```json
{
  "proxy": {
    "enabled": true,
    "url": "http://localhost:7897"
  },
  "keys": [
    {
      "provider": "tavily",
      "key": "tvly-dev-xxx"
    },
    {
      "provider": "exa",
      "key": "exa-xxx"
    }
  ],
  "default_count": 5,
  "default_depth": "basic",
  "fallback": true
}
```

## 📖 使用方法

### 命令行

```bash
# 基本搜索（使用默认提供商）
python3 search.py "Python best practices"

# 指定提供商
python3 search.py "React hooks" --provider exa

# 指定结果数量
python3 search.py "Docker tutorial" --count 10

# 深度搜索
python3 search.py "AI trends" --depth advanced

# JSON 输出
python3 search.py "搜索内容" --json

# 查看配置状态
python3 search.py --check

# 添加 key
python3 search.py --add-key tavily "tvly-dev-xxx"

# 移除 key
python3 search.py --remove-key tavily "tvly-dev-xxx"
```

### Python API

```python
from src.search import UnifiedSearch

# 初始化（自动加载配置）
search = UnifiedSearch()

# 搜索
result = search.search("Python best practices", count=5)

# 打印答案（Tavily 返回）
if result.get("answer"):
    print(f"答案: {result['answer']}")

# 打印结果
for r in result.get("results", []):
    print(f"- {r['title']}: {r['url']}")
```

### 各 AI 工具使用方法

所有工具统一使用相同的命令格式，只是路径不同：

```bash
# Claude Code
~/.claude/skills/web-search/search.py "搜索内容"

# Codex (OpenAI)
~/.codex/tools/web-search/search.py "搜索内容"

# Cursor
~/.cursor/tools/web-search/search.py "搜索内容"

# Windsurf
~/.windsurf/tools/web-search/search.py "搜索内容"

# Continue
~/.continue/tools/web-search/search.py "搜索内容"

# OpenClaw
~/.openclaw/tools/web-search/search.py "搜索内容"
```

或者直接使用项目目录：

```bash
python3 search.py "搜索内容"
```

## 🔄 轮询机制

所有 key 存储在统一池中，按顺序轮询：

```
keys[0] → keys[1] → keys[2] → ... → keys[n] → keys[0]
```

**示例：**

假设有 3 个 key：
- `tavily-key-1`
- `exa-key-1`
- `tavily-key-2`

轮询顺序：
1. `tavily-key-1`
2. `exa-key-1`
3. `tavily-key-2`
4. `tavily-key-1`（循环）

不区分提供商，全局轮询。

## 🔁 故障转移

当 `fallback: true` 时：

1. 主 key 请求失败
2. 自动尝试下一个 key
3. 直到成功或所有 key 都失败

## 🛠️ 扩展提供商

### 1. 创建提供商类

```python
# src/providers/new_provider.py
from .base import BaseProvider, SearchResponse, SearchResult

class NewProvider(BaseProvider):
    name = "new_provider"
    api_url = "https://api.new-provider.com/search"

    def search(self, query: str, api_key: str, count: int = 5, **kwargs) -> SearchResponse:
        # 实现搜索逻辑
        results = [SearchResult(title="...", url="...", content="...")]
        return SearchResponse(provider=self.name, results=results)
```

### 2. 注册提供商

编辑 `src/providers/__init__.py`：

```python
from .new_provider import NewProvider

PROVIDERS = {
    "tavily": TavilyProvider,
    "exa": ExaProvider,
    "new_provider": NewProvider,  # 添加这行
}
```

### 3. 添加 API key

```bash
python3 search.py --add-key new_provider "your-api-key"
```

## 📁 项目结构

```
unified-web-search/
├── README.md              # 使用说明
├── LICENSE                # MIT 许可证
├── .gitignore            # Git 忽略规则
├── config.example.json   # 配置示例
├── setup.py              # 包安装配置
├── install.py            # 交互式安装脚本
├── search.py             # 主入口脚本
└── src/
    ├── __init__.py
    ├── config.py         # 配置管理
    ├── key_pool.py       # 全局 key 池轮询
    ├── search.py         # 统一搜索类
    └── providers/
        ├── __init__.py
        ├── base.py       # 提供商基类
        ├── tavily.py     # Tavily 实现
        └── exa.py        # Exa 实现
```

## 📊 API 限制

| 提供商 | 免费额度 | RPM 限制 | 特点 |
|--------|---------|---------|------|
| **Tavily** | 1,000 次/月 | 100 | 返回 AI 答案 |
| **Exa** | 1,000 次/月 | 1,000 | 语义搜索 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT
