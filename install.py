#!/usr/bin/env python3
"""
Unified Web Search - 交互式安装脚本

引导用户完成配置，包括：
- 代理设置
- API key 配置
- Claude Code skill 安装
"""

import json
import sys
import os
from pathlib import Path


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


def ask_choice(question: str, choices: list[str], default: str = "") -> str:
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


def install_claude_skill(config_path: Path) -> bool:
    """安装为 Claude Code skill"""
    skill_dir = Path.home() / ".claude" / "skills" / "web-search"
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建 skill 配置
    skill_config = {
        "name": "web-search",
        "description": "统一搜索工具，支持多个搜索提供商（Tavily、Exa 等），全局 key 池轮询。",
        "command": f"python3 {Path(__file__).parent / 'search.py'}",
        "config_path": str(config_path),
    }

    skill_file = skill_dir / "skill.json"
    with open(skill_file, "w") as f:
        json.dump(skill_config, f, indent=2)

    # 创建启动脚本
    launch_script = skill_dir / "search.py"
    with open(launch_script, "w") as f:
        f.write(f'''#!/usr/bin/env python3
"""Claude Code skill 启动脚本"""
import sys
sys.path.insert(0, "{Path(__file__).parent}")
from search import main
if __name__ == "__main__":
    main()
''')
    launch_script.chmod(0o755)

    return True


def main():
    print_header("Unified Web Search 安装向导")

    print("本向导将帮助您完成以下配置：")
    print("  1. 代理设置（可选）")
    print("  2. API key 配置")
    print("  3. Claude Code skill 安装（可选）")

    # ============ 代理配置 ============
    print_step("代理配置")

    use_proxy = ask_yes_no("是否需要配置代理？", default=False)

    proxy_config = {
        "enabled": False,
        "url": "http://localhost:7897"
    }

    if use_proxy:
        print("\n常见代理地址：")
        print_info("Clash: http://localhost:7897")
        print_info("V2Ray: http://localhost:10809")
        print_info("Shadowsocks: http://localhost:1080")

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
        print("\n⚠ 未添加任何 API key，您可以稍后使用以下命令添加：")
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

    # ============ Claude Code 安装 ============
    print_step("Claude Code 集成")

    install_skill = ask_yes_no("是否安装为 Claude Code skill？", default=True)

    if install_skill:
        if install_claude_skill(config_path):
            print_success("Claude Code skill 已安装")
            print_info("使用方法: ~/.claude/skills/web-search/search.py \"搜索内容\"")
    else:
        print_info("跳过 Claude Code skill 安装")

    # ============ 完成 ============
    print_header("安装完成！")

    print("配置摘要：")
    print(f"  配置文件: {config_path}")
    print(f"  API keys: {len(keys)} 个")
    print(f"  代理: {'启用' if proxy_config['enabled'] else '禁用'}")
    print(f"  故障转移: {'启用' if fallback else '禁用'}")

    print("\n使用方法：")
    print_info(f"python3 {Path(__file__).parent / 'search.py'} \"搜索内容\"")
    print_info(f"python3 {Path(__file__).parent / 'search.py'} --check")

    if install_skill:
        print("\nClaude Code 中使用：")
        print_info("~/.claude/skills/web-search/search.py \"搜索内容\"")

    print("\n更多选项请查看 README.md")


if __name__ == "__main__":
    main()
