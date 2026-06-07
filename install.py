#!/usr/bin/env python3
"""
Unified Web Search - 安装脚本

支持通过 AI 对话完成安装配置
"""

import json
import sys
import os
from pathlib import Path


# AI 工具配置
AI_TOOLS = {
    "claude": "~/.claude/skills/web-search",
    "codex": "~/.codex/tools/web-search",
    "openclaw": "~/.openclaw/tools/web-search",
    "cursor": "~/.cursor/tools/web-search",
    "windsurf": "~/.windsurf/tools/web-search",
    "continue": "~/.continue/tools/web-search",
}


def ask(question, default=""):
    """询问用户"""
    prompt = f"{question} [{default}]: " if default else f"{question}: "
    try:
        answer = input(prompt).strip()
        return answer if answer else default
    except (EOFError, KeyboardInterrupt):
        print("\n已取消")
        sys.exit(0)


def ask_yes_no(question, default=True):
    """询问是/否"""
    hint = "Y/n" if default else "y/N"
    answer = ask(f"{question} ({hint})")
    return answer.lower() in ["y", "yes", "是", ""] if default else answer.lower() in ["y", "yes", "是"]


def print_step(text):
    """打印步骤"""
    print(f"\n▸ {text}")


def print_ok(text):
    """打印成功"""
    print(f"  ✓ {text}")


def print_info(text):
    """打印信息"""
    print(f"  ℹ {text}")


def install_to_tool(project_dir, config_path, tool_name):
    """安装到指定 AI 工具"""
    skill_dir = Path(os.path.expanduser(AI_TOOLS[tool_name]))
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建启动脚本
    script = skill_dir / "search.py"
    with open(script, "w") as f:
        f.write(f'''#!/usr/bin/env python3
import sys
sys.path.insert(0, "{project_dir}")
from search import main
if __name__ == "__main__":
    main()
''')
    script.chmod(0o755)

    # 创建配置链接
    config_link = skill_dir / "config.json"
    if not config_link.exists():
        config_link.symlink_to(config_path)

    return True


def main():
    print("\n" + "="*50)
    print("  Unified Web Search 安装向导")
    print("="*50)

    project_dir = Path(__file__).parent

    # 选择 AI 工具
    print_step("选择 AI 工具")
    print("\n支持的工具：")
    for i, name in enumerate(AI_TOOLS.keys(), 1):
        print(f"  {i}. {name}")

    answer = ask("请选择（多个用逗号分隔）", "1")
    selected = []
    for part in answer.split(","):
        try:
            idx = int(part.strip()) - 1
            if 0 <= idx < len(AI_TOOLS):
                selected.append(list(AI_TOOLS.keys())[idx])
        except:
            pass

    if not selected:
        selected = ["claude"]

    print_ok(f"已选择: {', '.join(selected)}")

    # 代理配置
    print_step("代理配置")
    use_proxy = ask_yes_no("需要配置代理吗？", False)

    proxy = {"enabled": False, "url": "http://localhost:7897"}
    if use_proxy:
        print("\n常见代理端口：")
        print_info("Clash: http://localhost:7897")
        print_info("V2Ray: http://localhost:10809")
        proxy["url"] = ask("代理地址", "http://localhost:7897")
        proxy["enabled"] = True
        print_ok(f"代理: {proxy['url']}")

    # API Key
    print_step("API Key 配置")
    print("\n获取免费 key：")
    print_info("Tavily: https://app.tavily.com/home (1000次/月)")
    print_info("Exa: https://exa.ai (1000次/月)")

    keys = []

    # Tavily
    print("\n--- Tavily ---")
    if ask_yes_no("添加 Tavily key？", True):
        while True:
            key = ask("Tavily API key（空行完成）")
            if not key:
                break
            keys.append({"provider": "tavily", "key": key})
            print_ok(f"已添加: {key[:20]}...")

    # Exa
    print("\n--- Exa ---")
    if ask_yes_no("添加 Exa key？", True):
        while True:
            key = ask("Exa API key（空行完成）")
            if not key:
                break
            keys.append({"provider": "exa", "key": key})
            print_ok(f"已添加: {key[:20]}...")

    # 高级设置
    print_step("高级设置")
    count = int(ask("默认结果数", "5"))
    depth = "basic" if ask_yes_no("基础搜索？", True) else "advanced"
    fallback = ask_yes_no("启用故障转移？", True)

    # 生成配置
    config_dir = Path.home() / ".config" / "unified-web-search"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"

    config = {
        "proxy": proxy,
        "keys": keys,
        "default_count": count,
        "default_depth": depth,
        "fallback": fallback,
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print_ok(f"配置: {config_path}")

    # 安装到工具
    print_step("安装 Skill")
    for tool in selected:
        try:
            install_to_tool(project_dir, config_path, tool)
            skill_dir = Path(os.path.expanduser(AI_TOOLS[tool]))
            print_ok(f"{tool}: {skill_dir}/search.py")
        except Exception as e:
            print(f"  ✗ {tool}: {e}")

    # 完成
    print("\n" + "="*50)
    print("  安装完成！")
    print("="*50)
    print(f"\n配置: {config_path}")
    print(f"Keys: {len(keys)} 个")
    print(f"代理: {'启用' if proxy['enabled'] else '禁用'}")

    print("\n使用方法：")
    for tool in selected:
        skill_dir = Path(os.path.expanduser(AI_TOOLS[tool]))
        print(f"  {tool}: {skill_dir}/search.py \"搜索内容\"")


if __name__ == "__main__":
    main()
