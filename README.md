# Unified Web Search

统一搜索工具，支持多个搜索提供商（Tavily、Exa 等），全局 key 池轮询。

## 特性

- ✅ **全局 Key 池**：所有 key 统一管理，轮询使用
- ✅ **多提供商**：支持 Tavily、Exa，易于扩展
- ✅ **故障转移**：主 key 失败自动切换下一个
- ✅ **代理支持**：HTTP/HTTPS 代理配置
- ✅ **零硬编码**：所有配置外置

## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/unified-web-search.git
cd unified-web-search

# 创建符号链接到 Claude skills 目录
ln -s "$(pwd)" ~/.claude/skills/web-search
```

## 配置

首次运行会自动创建配置文件 `~/.claude/skills/web-search/config.json`：

```json
{
  "proxy": {
    "enabled": false,
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

### 添加 Key

```bash
# 添加 Tavily key
python3 search.py --add-key tavily "tvly-dev-xxx"

# 添加 Exa key
python3 search.py --add-key exa "exa-xxx"
```

## 使用

### 命令行

```bash
# 基本搜索
python3 search.py "Python best practices"

# 指定提供商
python3 search.py "React hooks" --provider exa

# 指定结果数量
python3 search.py "Docker tutorial" --count 10

# 深度搜索
python3 search.py "AI trends" --depth advanced

# JSON 输出
python3 search.py "搜索内容" --json

# 查看配置
python3 search.py --check
```

### Python

```python
from src.search import UnifiedSearch

search = UnifiedSearch()
result = search.search("Python best practices", count=5)

print(result["answer"])  # Tavily 返回的答案
for r in result["results"]:
    print(f"- {r['title']}: {r['url']}")
```

## 轮询机制

所有 key 存储在统一池中，按顺序轮询：

```
keys[0] → keys[1] → keys[2] → keys[0] → ...
```

不区分提供商，全局轮询。

## 故障转移

当某个 key 请求失败时，自动尝试下一个 key。

## 扩展提供商

在 `src/providers/` 目录添加新提供商：

```python
# src/providers/new_provider.py
from .base import BaseProvider

class NewProvider(BaseProvider):
    name = "new_provider"

    def search(self, query: str, count: int, **kwargs) -> dict:
        # 实现搜索逻辑
        pass
```

然后在 `src/providers/__init__.py` 注册。

## License

MIT
