<p align="center">
  <h1 align="center">Unified Web Search</h1>
  <p align="center">
    <em>AI-powered web search with multi-provider key rotation</em>
  </p>
</p>

<p align="center">
  <a href="https://github.com/ALVIN-YANG/unified-web-search/stargazers"><img src="https://img.shields.io/github/stars/ALVIN-YANG/unified-web-search?style=for-the-badge&logo=github&labelColor=1e293b&color=fbbf24" alt="GitHub stars"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-fbbf24?style=for-the-badge&labelColor=1e293b" alt="MIT License"/></a>
  <a href="#providers"><img src="https://img.shields.io/badge/Providers-Tavily%20·%20Exa-111827?style=for-the-badge&labelColor=1e293b" alt="Supported providers"/></a>
</p>

---

Unified web search tool for AI agents. Supports multiple search providers (Tavily, Exa) with **global key pool rotation**, automatic failover, and HTTP proxy support.

<p align="center">
  <a href="#installing">Install</a> · <a href="#quick-start">Quick Start</a> · <a href="#providers">Providers</a> · <a href="#configuration">Configuration</a> · <a href="#api-keys">API Keys</a> · <a href="#proxy-setup">Proxy</a> · <a href="#faq">FAQ</a>
</p>

---

## Installing

### Option 1: AI Conversation (Recommended)

Copy this to your AI assistant:

```
Please install the web-search skill:
git clone https://github.com/ALVIN-YANG/unified-web-search.git /tmp/unified-web-search
cd /tmp/unified-web-search && python3 install.py
```

### Option 2: Manual Install

```bash
git clone https://github.com/ALVIN-YANG/unified-web-search.git /tmp/unified-web-search
cd /tmp/unified-web-search && python3 install.py
```

### Option 3: Using npx skills

```bash
npx skills add https://github.com/ALVIN-YANG/unified-web-search
```

---

## Quick Start

```bash
# Basic search
search.py "Python best practices"

# Specify provider
search.py "React hooks" --provider exa

# Advanced depth
search.py "machine learning" --depth advanced

# JSON output
search.py "async tutorial" --json

# Check configuration
search.py --check
```

---

## Providers

| Provider | Strengths | Free Tier | RPM |
|----------|-----------|-----------|-----|
| **Tavily** | General search, AI-generated answers | 1,000 req/month | 100 |
| **Exa** | Semantic search, code examples, highlights | 1,000 req/month | 1,000 |

### How Key Rotation Works

```
┌─────────────────────────────────────────┐
│           Global Key Pool               │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │Key 1│ │Key 2│ │Key 3│ │Key 4│ ...   │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
│      ↓       ↓       ↓       ↓         │
│    Tavily  Exa   Tavily   Exa          │
└─────────────────────────────────────────┘
         Round-Robin Rotation
```

- All keys stored in single pool (not per-provider)
- Sequential rotation across all keys
- Automatic failover if key fails
- Counter persists across restarts

---

## Configuration

Config file: `~/.config/unified-web-search/config.json`

```json
{
  "proxy": {
    "enabled": true,
    "http": "http://localhost:7897",
    "https": "http://localhost:7897"
  },
  "keys": [
    {
      "provider": "tavily",
      "key": "tvly-dev-xxx"
    },
    {
      "provider": "exa",
      "key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ]
}
```

---

## API Keys

### Get Free Keys

| Provider | Get Key |
|----------|---------|
| Tavily | [tavily.com](https://tavily.com) |
| Exa | [exa.ai](https://exa.ai) |

### Manage Keys

```bash
# Add keys
search.py --add-key tavily "tvly-dev-xxx"
search.py --add-key exa "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Remove key
search.py --remove-key tavily "tvly-dev-xxx"

# View all keys
search.py --check
```

### Why Multiple Keys?

- **Higher throughput**: More keys = more requests per minute
- **Fault tolerance**: If one key fails, others continue
- **Load distribution**: Spread requests across keys

---

## Proxy Setup

If you're behind a firewall or using Clash Verge:

### During Installation

The install script will ask:
```
需要配置代理吗？(y/n): y
HTTP 代理地址: http://localhost:7897
HTTPS 代理地址: http://localhost:7897
```

### Manual Configuration

Edit `~/.config/unified-web-search/config.json`:

```json
{
  "proxy": {
    "enabled": true,
    "http": "http://localhost:7897",
    "https": "http://localhost:7897"
  }
}
```

### Common Proxy Ports

| Tool | Default Port |
|------|--------------|
| Clash Verge | 7897 |
| V2Ray | 10809 |
| Shadowsocks | 1080 |

---

## Supported AI Tools

| Tool | Install Location |
|------|------------------|
| Claude Code | `~/.claude/skills/web-search` |
| Codex | `~/.codex/tools/web-search` |
| OpenClaw | `~/.openclaw/tools/web-search` |
| Cursor | `~/.cursor/tools/web-search` |
| Windsurf | `~/.windsurf/tools/web-search` |
| Continue | `~/.continue/tools/web-search` |

---

## FAQ

**Q: How many keys should I register?**

A: Start with 2-3 keys. Each Tavily key = 1,000 req/month, each Exa key = 1,000 req/month.

**Q: Which provider is better?**

A: Tavily returns AI-generated answers (good for summaries). Exa is better for semantic/code search.

**Q: Can I use both providers?**

A: Yes! Keys from all providers are in one pool. The tool automatically uses the next available key.

**Q: What if a key fails?**

A: The tool automatically tries the next key in the pool. No manual intervention needed.

**Q: How do I change proxy settings?**

A: Edit `~/.config/unified-web-search/config.json` or re-run `python3 install.py`.

---

## Project Structure

```
unified-web-search/
├── skills/
│   ├── web-search/
│   │   └── SKILL.md        # AI skill instructions
│   └── llms.txt            # Quick index for AI
├── src/
│   ├── providers/
│   │   ├── base.py         # Base provider class
│   │   ├── tavily.py       # Tavily implementation
│   │   └── exa.py          # Exa implementation
│   ├── config.py           # Configuration manager
│   ├── key_pool.py         # Key rotation logic
│   └── search.py           # Unified search engine
├── search.py               # CLI entry point
├── install.py              # Installation script
├── skill.sh                # Local skill registry
├── config.example.json     # Example configuration
└── README.md               # This file
```

---

## License

[MIT License](LICENSE) · Copyright (c) 2026 ALVIN-YANG
