#!/usr/bin/env python3
"""
Unified Web Search - 交互式安装脚本

支持多个 AI 工具：
- Claude Code
- Codex (OpenAI)
- OpenClaw
- Cursor
- Windsurf
- Continue
- 其他支持 MCP/自定义工具的 AI
"""

import json
import sys
import os
from pathlib import Path
from typing import Optional


# ============ AI 工具定义 ============

AI_TOOLS = {
    "claude": {
        "name": "Claude Code",
        "skill_dir": "~/.claude/skills/web-search",
        "config_format": "skill",
        "description": "Anthropic Claude Code CLI",
    },
    "codex": {
        "name": "Codex (OpenAI)",
        "skill_dir": "~/.codex/tools/web-search",
        "config_format": "mcp",
        "description": "OpenAI Codex CLI",
    },
    "openclaw": {
        "name": "OpenClaw",
        "skill_dir": "~/.openclaw/tools/web-search",
        "config_format": "mcp",
        "description": "OpenClaw AI assistant",
    },
    "cursor": {
        "name": "Cursor",
        "skill_dir": "~/.cursor/tools/web-search",
        "config_format": "mcp",
        "description": "Cursor AI editor",
    },
    "windsurf": {
        "name": "Windsurf",
        "skill_dir": "~/.windsurf/tools/web-search",
        "config_format": "mcp",
        "description": "Windsurf AI editor",
    },
    "continue": {
        "name": "Continue",
        "skill_dir": "~/.continue/tools/web-search",
        "config_format": "mcp",
        "description": "Continue VS Code extension",
    },
    "generic": {
        "name": "通用 MCP 服务器",
        "skill_dir": "~/.config/unified-web-search",
        "config_format": "mcp",
        "description": "支持 MCP 协议的任意 AI 工具",
    },
}


def ask_question(question: str, default: str = "") -> str:
    """询问用户问题"""
    if default:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "

    try:
        answer = input(prompt).strip()
        return answer if answer else default
    except (EOFError, KeyboardInterrupt):
        print("\n安装已取消")
        sys.exit(0)


def ask_yes_no(question: str, default: bool = True) -> bool:
    """询问是/否问题"""
    hint = "Y/n" if default else "y/N"
    answer = ask_question(f"{question} ({hint})")
    if not answer:
        return default
    return answer.lower() in ["y", "yes", "是"]


def ask_choice(question: str, choices: list, default: str = "") -> str:
    """询问选择问题"""
    print(f"\n{question}")
    for i, choice in enumerate(choices, 1):
        marker = "→" if choice == default else " "
        print(f"  {marker} {i}. {choice}")

    answer = ask_question("请选择", str(choices.index(default) + 1) if default else "")
    try:
        index = int(answer) - 1
        if 0 <= index < len(choices):
            return choices[index]
    except ValueError:
        pass

    return default


def ask_multiple_choice(question: str, choices: list) -> list:
    """询问多选问题"""
    print(f"\n{question}（输入序号，多个用逗号分隔，如 1,2,3）")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")

    answer = ask_question("请选择（可多选）")
    if not answer:
        return []

    selected = []
    for part in answer.split(","):
        try:
            index = int(part.strip()) - 1
            if 0 <= index < len(choices):
                selected.append(choices[index])
        except ValueError:
            pass

    return selected


def print_header(text: str):
    """打印标题"""
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}\n")


def print_step(text: str):
    """打印步骤"""
    print(f"\n▸ {text}")


def print_success(text: str):
    """打印成功信息"""
    print(f"  ✓ {text}")


def print_info(text: str):
    """打印信息"""
    print(f"  ℹ {text}")


def print_warning(text: str):
    """打印警告"""
    print(f"  ⚠ {text}")


# ============ 安装函数 ============

def install_claude_code(project_dir: Path, config_path: Path) -> bool:
    """安装为 Claude Code skill"""
    skill_dir = Path.home() / ".claude" / "skills" / "web-search"
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建 SKILL.md
    skill_md = skill_dir / "SKILL.md"
    with open(skill_md, "w") as f:
        f.write(f'''---
name: web-search
description: |
  统一搜索工具，支持多个搜索提供商（Tavily、Exa 等），全局 key 池轮询。
  当用户需要搜索网页、获取实时信息时使用此 skill。
---

# Unified Web Search

使用方法：运行 `{project_dir / 'search.py'} "搜索内容"`

配置文件：`{config_path}`
''')

    # 创建启动脚本
    launch_script = skill_dir / "search.py"
    with open(launch_script, "w") as f:
        f.write(f'''#!/usr/bin/env python3
"""Claude Code skill 启动脚本"""
import sys
sys.path.insert(0, "{project_dir}")
from search import main
if __name__ == "__main__":
    main()
''')
    launch_script.chmod(0o755)

    return True


def install_codex(project_dir: Path, config_path: Path) -> bool:
    """安装为 Codex 工具"""
    tool_dir = Path.home() / ".codex" / "tools" / "web-search"
    tool_dir.mkdir(parents=True, exist_ok=True)

    # 创建工具配置
    tool_config = {
        "name": "web-search",
        "description": "统一搜索工具，支持 Tavily、Exa 等多个搜索提供商",
        "command": f"python3 {project_dir / 'search.py'}",
        "args": ["{{query}}"],
        "env": {
            "WEB_SEARCH_CONFIG": str(config_path),
        },
    }

    config_file = tool_dir / "tool.json"
    with open(config_file, "w") as f:
        json.dump(tool_config, f, indent=2)

    # 创建启动脚本
    launch_script = tool_dir / "run.sh"
    with open(launch_script, "w") as f:
        f.write(f'''#!/bin/bash
cd "{project_dir}"
python3 search.py "$@"
''')
    launch_script.chmod(0o755)

    return True


def install_mcp_server(project_dir: Path, config_path: Path, tool_name: str) -> bool:
    """安装为 MCP 服务器"""
    # 创建 MCP 服务器脚本
    mcp_script = project_dir / "mcp_server.py"

    if not mcp_script.exists():
        with open(mcp_script, "w") as f:
            f.write('''#!/usr/bin/env python3
"""
MCP Server for Unified Web Search

支持 Cursor、Windsurf、Continue 等 MCP 客户端
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "''' + str(project_dir) + '''")

from src.search import UnifiedSearch


def handle_request(request: dict) -> dict:
    """处理 MCP 请求"""
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "web_search",
                    "description": "搜索网页内容",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索查询"
                            },
                            "provider": {
                                "type": "string",
                                "enum": ["tavily", "exa"],
                                "description": "搜索提供商（可选）"
                            },
                            "count": {
                                "type": "integer",
                                "description": "结果数量（默认 5）"
                            },
                        },
                        "required": ["query"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "web_search":
            search = UnifiedSearch(config_path="''' + str(config_path) + '''")
            result = search.search(
                query=arguments.get("query", ""),
                provider=arguments.get("provider"),
                count=arguments.get("count", 5),
            )
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, ensure_ascii=False, indent=2)
                    }
                ]
            }

    return {"error": "Unknown method"}


def main():
    """MCP 服务器主循环"""
    # 读取 stdin，写入 stdout
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON"}), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)


if __name__ == "__main__":
    main()
''')
        mcp_script.chmod(0o755)

    return True


def install_generic(project_dir: Path, config_path: Path) -> bool:
    """通用安装（创建配置文件和使用说明）"""
    config_dir = Path.home() / ".config" / "unified-web-search"
    config_dir.mkdir(parents=True, exist_ok=True)

    # 创建使用说明
    readme = config_dir / "README.md"
    with open(readme, "w") as f:
        f.write(f'''# Unified Web Search - 通用配置

## 使用方法

```bash
# 直接运行
python3 {project_dir / 'search.py'} "搜索内容"

# 指定配置文件
python3 {project_dir / 'search.py'} --config {config_path} "搜索内容"
```

## 环境变量

```bash
export WEB_SEARCH_CONFIG="{config_path}"
```

## 配置文件位置

{config_path}
''')

    return True


# ============ 主安装流程 ============

def main():
    print_header("Unified Web Search 安装向导")

    print("本向导将帮助您完成以下配置：")
    print("  1. AI 工具选择")
    print("  2. 代理设置（可选）")
    print("  3. API key 配置")
    print("  4. 工具安装")

    # ============ AI 工具选择 ============
    print_step("选择 AI 工具")

    print("\n支持的 AI 工具：")
    tool_names = []
    tool_keys = []
    for key, tool in AI_TOOLS.items():
        tool_names.append(f"{tool['name']} - {tool['description']}")
        tool_keys.append(key)

    selected_indices = ask_multiple_choice(
        "请选择要安装的 AI 工具（可多选）",
        tool_names
    )

    if not selected_indices:
        print_warning("未选择任何工具，将仅生成配置文件")
        selected_tools = ["generic"]
    else:
        selected_tools = []
        for name in selected_indices:
            index = tool_names.index(name)
            selected_tools.append(tool_keys[index])

    print_success(f"已选择: {', '.join([AI_TOOLS[t]['name'] for t in selected_tools])}")

    # ============ 代理配置 ============
    print_step("代理配置")

    use_proxy = ask_yes_no("是否需要配置代理？", default=False)

    proxy_config = {
        "enabled": False,
        "url": "http://localhost:7897"
    }

    if use_proxy:
        print("\n常见代理软件端口：")
        print_info("Clash / Clash Verge: http://localhost:7897")
        print_info("V2Ray: http://localhost:10809")
        print_info("Shadowsocks: http://localhost:1080")
        print_info("Surge: http://localhost:6152")
        print_info("Quantumult X: http://localhost:9090")

        proxy_url = ask_question("请输入代理地址", "http://localhost:7897")
        proxy_config["enabled"] = True
        proxy_config["url"] = proxy_url
        print_success(f"代理已配置: {proxy_url}")
    else:
        print_info("跳过代理配置")

    # ============ API Key 配置 ============
    print_step("API Key 配置")

    print("\n支持的搜索提供商：")
    print_info("Tavily - 免费 1000 次/月 - https://app.tavily.com/home")
    print_info("Exa    - 免费 1000 次/月 - https://exa.ai")

    keys = []

    # Tavily 配置
    print("\n--- Tavily ---")
    add_tavily = ask_yes_no("是否添加 Tavily API key？", default=True)

    if add_tavily:
        while True:
            key = ask_question("请输入 Tavily API key (输入空行完成)")
            if not key:
                break
            keys.append({"provider": "tavily", "key": key})
            print_success(f"已添加 Tavily key: {key[:20]}...")

            add_more = ask_yes_no("是否继续添加 Tavily key？", default=False)
            if not add_more:
                break

    # Exa 配置
    print("\n--- Exa ---")
    add_exa = ask_yes_no("是否添加 Exa API key？", default=True)

    if add_exa:
        while True:
            key = ask_question("请输入 Exa API key (输入空行完成)")
            if not key:
                break
            keys.append({"provider": "exa", "key": key})
            print_success(f"已添加 Exa key: {key[:20]}...")

            add_more = ask_yes_no("是否继续添加 Exa key？", default=False)
            if not add_more:
                break

    if not keys:
        print_warning("未添加任何 API key，您可以稍后使用以下命令添加：")
        print_info("python3 search.py --add-key tavily \"your-key\"")
        print_info("python3 search.py --add-key exa \"your-key\"")

    # ============ 高级设置 ============
    print_step("高级设置")

    default_count = ask_question("默认搜索结果数量", "5")
    default_depth = ask_choice("默认搜索深度", ["basic", "advanced"], "basic")
    fallback = ask_yes_no("是否启用故障转移？（主 key 失败自动切换）", default=True)

    # ============ 生成配置 ============
    print_step("生成配置")

    # 确定配置文件路径
    config_dir = Path.home() / ".config" / "unified-web-search"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"

    config = {
        "proxy": proxy_config,
        "keys": keys,
        "default_count": int(default_count),
        "default_depth": default_depth,
        "fallback": fallback,
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print_success(f"配置已保存: {config_path}")

    # ============ 安装到 AI 工具 ============
    print_step("安装到 AI 工具")

    project_dir = Path(__file__).parent

    for tool_key in selected_tools:
        tool = AI_TOOLS[tool_key]
        print(f"\n安装 {tool['name']}...")

        try:
            if tool_key == "claude":
                success = install_claude_code(project_dir, config_path)
            elif tool_key == "codex":
                success = install_codex(project_dir, config_path)
            elif tool_key in ["openclaw", "cursor", "windsurf", "continue"]:
                success = install_mcp_server(project_dir, config_path, tool_key)
            else:
                success = install_generic(project_dir, config_path)

            if success:
                print_success(f"{tool['name']} 安装完成")
            else:
                print_warning(f"{tool['name']} 安装失败")
        except Exception as e:
            print_warning(f"{tool['name']} 安装出错: {e}")

    # ============ 完成 ============
    print_header("安装完成！")

    print("配置摘要：")
    print(f"  配置文件: {config_path}")
    print(f"  API keys: {len(keys)} 个")
    print(f"  代理: {'启用' if proxy_config['enabled'] else '禁用'}")
    print(f"  故障转移: {'启用' if fallback else '禁用'}")

    print("\n已安装的 AI 工具：")
    for tool_key in selected_tools:
        print(f"  ✓ {AI_TOOLS[tool_key]['name']}")

    print("\n使用方法：")
    print_info(f"python3 {project_dir / 'search.py'} \"搜索内容\"")
    print_info(f"python3 {project_dir / 'search.py'} --check")

    if "claude" in selected_tools:
        print("\nClaude Code 中使用：")
        print_info("~/.claude/skills/web-search/search.py \"搜索内容\"")

    print("\n更多选项请查看 README.md")


if __name__ == "__main__":
    main()
