"""搜索提供商模块"""

from .base import BaseProvider
from .tavily import TavilyProvider
from .exa import ExaProvider

# 提供商注册表
PROVIDERS = {
    "tavily": TavilyProvider,
    "exa": ExaProvider,
}

def get_provider(name: str) -> BaseProvider:
    """获取提供商类"""
    provider_class = PROVIDERS.get(name)
    if not provider_class:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDERS.keys())}")
    return provider_class

def register_provider(name: str, provider_class: type):
    """注册新提供商"""
    PROVIDERS[name] = provider_class

__all__ = ["BaseProvider", "TavilyProvider", "ExaProvider", "PROVIDERS", "get_provider", "register_provider"]
