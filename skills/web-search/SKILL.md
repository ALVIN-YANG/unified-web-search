---
name: web-search
description: Unified web search with Tavily/Exa providers and global key pool rotation. Use when the user needs to search the web, find documentation, get real-time information, or research topics.
---

# Web Search Skill

> Search the web using Tavily or Exa APIs with automatic key rotation and failover.

---

## When to Use

- User asks to search, look up, or research something
- User needs current information, documentation, or examples
- User wants to find code examples, tutorials, or references
- `WebSearch` or `WebFetch` tools are unavailable or failing

---

## How It Works

1. **Global key pool**: All API keys (Tavily + Exa) are stored in one pool
2. **Round-robin rotation**: Each request uses the next key in sequence
3. **Automatic failover**: If a key fails, tries the next one
4. **Proxy support**: Routes through HTTP proxy if configured

---

## Usage

### Basic Search

```bash
search.py "your search query"
```

### With Options

```bash
# Specify provider
search.py "query" --provider tavily
search.py "query" --provider exa

# Search depth
search.py "query" --depth basic      # Fast, fewer results
search.py "query" --depth advanced   # Thorough, more results

# JSON output (for programmatic use)
search.py "query" --json
```

### Check Configuration

```bash
search.py --check
```

---

## Response Format

### Default Output

```
[1] Title of result
    URL: https://example.com
    Snippet: Brief description...

[2] Another result
    URL: https://another.com
    Snippet: Another description...
```

### JSON Output

```json
{
  "provider": "tavily",
  "query": "your query",
  "results": [
    {
      "title": "Title",
      "url": "https://example.com",
      "snippet": "Description..."
    }
  ],
  "answer": "Tavily-generated answer (if available)"
}
```

---

## Provider Differences

| Provider | Best For | RPM Limit |
|----------|----------|-----------|
| Tavily | General search, returns AI answer | 100 |
| Exa | Semantic/code search, highlights | 1000 |

---

## Managing Keys

```bash
# Add a key
search.py --add-key tavily "tvly-dev-xxx"
search.py --add-key exa "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# Remove a key
search.py --remove-key tavily "tvly-dev-xxx"

# List all keys
search.py --check
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No API keys configured | Run `search.py --add-key <provider> <key>` |
| Connection timeout | Check proxy settings in `~/.config/unified-web-search/config.json` |
| Rate limit exceeded | Wait or add more keys to the pool |
| Invalid key | Remove and re-add the key |

---

## Integration with AI Tools

When the user asks you to search for something:

1. Run `search.py "query" --json`
2. Parse the JSON output
3. Summarize the results for the user
4. Cite sources with URLs

Example prompt to user:
> "I found several relevant results. Here's a summary based on [source](url)..."
