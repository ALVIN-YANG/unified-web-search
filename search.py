#!/usr/bin/env python3
"""
Unified Web Search - 统一搜索工具

支持多个搜索提供商（Tavily、Exa 等），全局 key 池轮询。

Usage:
    python search.py "搜索内容"
    python search.py "搜索内容" --provider exa
    python search.py "搜索内容" --count 10 --depth advanced
    python search.py --add-key tavily "tvly-dev-xxx"
    python search.py --check
"""

import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from src.search import UnifiedSearch
from src.config import ConfigManager


def format_output(result: dict, show_provider: bool = True) -> str:
    """格式化输出"""
    lines = []

    if "error" in result:
        return f"错误: {result['error']}"

    if show_provider and result.get("provider"):
        provider = result["provider"].upper()
        fallback = " (备用)" if result.get("fallback") else ""
        lines.append(f"🔍 [{provider}]{fallback}\n")

    if result.get("answer"):
        lines.append(f"📝 {result['answer']}\n")

    for i, r in enumerate(result.get("results", []), 1):
        lines.append(f"{i}. {r.get('title', '无标题')}")
        lines.append(f"   {r.get('url', '')}")
        if r.get("content"):
            content = r["content"]
            if len(content) > 200:
                content = content[:200] + "..."
            lines.append(f"   {content}")
        lines.append("")

    return "\n".join(lines)


def format_status(status: dict) -> str:
    """格式化状态输出"""
    lines = ["=== 配置状态 ===\n"]

    lines.append("提供商:")
    for provider, count in status["providers"].items():
        lines.append(f"  {provider}: {count} 个 key")

    lines.append(f"\n总 key 数: {status['total_keys']}")
    lines.append(f"故障转移: {'启用' if status['fallback_enabled'] else '禁用'}")
    lines.append(f"代理: {'启用' if status['proxy_enabled'] else '禁用'}")
    if status["proxy_enabled"]:
        lines.append(f"代理地址: {status['proxy_url']}")
    lines.append(f"当前索引: {status['current_index']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Unified Web Search - 统一搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search.py "Python best practices"
  python search.py "React hooks" --provider exa
  python search.py "Docker tutorial" --count 10
  python search.py --add-key tavily "tvly-dev-xxx"
  python search.py --check
        """,
    )

    parser.add_argument("query", nargs="*", help="搜索查询")
    parser.add_argument("--provider", "-p", help="指定提供商")
    parser.add_argument("--count", "-n", type=int, help="结果数量")
    parser.add_argument("--depth", "-d", choices=["basic", "advanced"], help="搜索深度")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 格式输出")
    parser.add_argument("--check", "-c", action="store_true", help="检查配置状态")
    parser.add_argument("--add-key", nargs=2, metavar=("PROVIDER", "KEY"), help="添加 API key")
    parser.add_argument("--remove-key", nargs=2, metavar=("PROVIDER", "KEY"), help="移除 API key")
    parser.add_argument("--config", help="配置文件路径")

    args = parser.parse_args()

    # 初始化
    search = UnifiedSearch(config_path=args.config)
    config_manager = search.config_manager

    # 检查状态
    if args.check:
        status = search.get_status()
        print(format_status(status))
        return

    # 添加 key
    if args.add_key:
        provider, key = args.add_key
        if provider not in ["tavily", "exa"]:
            print(f"错误: 不支持的提供商 {provider}，可用: tavily, exa", file=sys.stderr)
            sys.exit(1)
        if config_manager.add_key(provider, key):
            print(f"已添加 {provider} key: {key[:20]}...")
        else:
            print("该 key 已存在")
        return

    # 移除 key
    if args.remove_key:
        provider, key = args.remove_key
        if config_manager.remove_key(provider, key):
            print(f"已移除 {provider} key")
        else:
            print("未找到该 key")
        return

    # 搜索
    if not args.query:
        parser.print_help()
        return

    query = " ".join(args.query)
    result = search.search(
        query=query,
        provider=args.provider,
        count=args.count,
        depth=args.depth,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
