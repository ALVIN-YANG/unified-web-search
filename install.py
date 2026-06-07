#!/usr/bin/env python3
"""
Unified Web Search - 交互式安装脚本

支持多个 AI 工具，统一使用 skill/tool 方式安装
"""

import json
import sys
import os
from pathlib import Path


# ============ AI 工具定义 ============

AI_TOOLS = {
    "claude": {
        "name": "Claude Code",
        "skill_dir": "~/.claude/skills/web-search",
    },
    "codex": {
        "name": "Codex (OpenAI)",
        "skill_dir": "~/.codex/tools/web-search",
    },
    "openclaw": {
        "name": "OpenClaw",
        "skill_dir": "~/.openclaw/tools/web-search",
    },
    "cursor": {
        "name": "Cursor",
        "skill_dir": "~/.cursor/tools/web-search",
    },
    "windsurf": {
        "name": "Windsurf",
        "skill_dir": "~/.windsurf/tools/web-search",
    },
    "continue": {
        "name": "Continue",
        "skill_dir": "~/.continue/tools/web-search",
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


def install_skill(project_dir: Path, config_path: Path, tool_key: str) -> bool:
    """安装为 skill/tool"""
    tool = AI_TOOLS[tool_key]
    skill_dir = Path(os.path.expanduser(tool["skill_dir"]))
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建启动脚本
    launch_script = skill_dir / "search.py"
    with open(launch_script, "w") as f:
        f.write(f'''#!/usr/bin/env python3
"""{tool["name"]} skill 启动脚本"""
import sys
sys.path.insert(0, "{project_dir}")
from search import main
if __name__ == "__main__":
    main()
''')
    launch_script.chmod(0o755)

    # 创建配置文件（指向主配置）
    skill_config = {
        "name": "web-search",
        "description": "统一搜索工具，支持 Tavily、Exa 等多个搜索提供商",
        "command": str(launch_script),
        "config": str(config_path),
    }

    config_file = skill_dir / "skill.json"
    with open(config_file, "w") as f:
        json.dump(skill_config, f, indent=2)

    return True


def main():
    print_header("Unified Web Search 安装向导")

    print("本向导将帮助您完成以下配置：")
    print("  1. AI 工具选择")
    print("  2. 代理设置（可选）")
    print("  3. API key 配置")
    print("  4. 自动安装到对应工具")

    # ============ AI 工具选择 ============
    print_step("选择 AI 工具")

    print("\n支持的 AI 工具：")
    tool_names = []
    tool_keys = []
    for key, tool in AI_TOOLS.items():
        tool_names.append(tool["name"])
        tool_keys.append(key)

    selected_indices = ask_multiple_choice(
        "请选择要安装的 AI 工具（可多选）",
        tool_names
    )

    if not selected_indices:
        print_warning("未选择任何工具")
        selected_tools = []
    else:
        selected_tools = []
        for name in selected_indices:
            index = tool_names.index(name)
            selected_tools.append(tool_keys[index])

    if selected_tools:
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
    default_depth = "basic" if ask_yes_no("默认使用基础搜索？（否则为深度搜索）", default=True) else "advanced"
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
    if selected_tools:
        print_step("安装到 AI 工具")

        project_dir = Path(__file__).parent

        for tool_key in selected_tools:
            tool = AI_TOOLS[tool_key]
            print(f"\n安装 {tool['name']}...")

            try:
                success = install_skill(project_dir, config_path, tool_key)
                if success:
                    skill_dir = Path(os.path.expanduser(tool["skill_dir"]))
                    print_success(f"{tool['name']} 安装完成")
                    print_info(f"路径: {skill_dir / 'search.py'}")
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

    if selected_tools:
        print("\n已安装的 AI 工具：")
        for tool_key in selected_tools:
            tool = AI_TOOLS[tool_key]
            skill_dir = Path(os.path.expanduser(tool["skill_dir"]))
            print(f"  ✓ {tool['name']}: {skill_dir / 'search.py'}")

    print("\n使用方法：")
    print_info(f"python3 {project_dir / 'search.py'} \"搜索内容\"")
    print_info(f"python3 {project_dir / 'search.py'} --check")

    print("\n更多选项请查看 README.md")


if __name__ == "__main__":
    main()
