"""统一搜索模块"""

from typing import Optional, Dict, Any, List

from .config import ConfigManager, Config
from .key_pool import KeyPool
from .providers import get_provider, PROVIDERS
from .providers.base import SearchResponse


class UnifiedSearch:
    """统一搜索类"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化统一搜索

        Args:
            config_path: 配置文件路径（可选）
        """
        from pathlib import Path

        path = Path(config_path) if config_path else None
        self.config_manager = ConfigManager(path)
        self.config = self.config_manager.load()
        self.key_pool = KeyPool()

    def search(
        self,
        query: str,
        provider: Optional[str] = None,
        count: Optional[int] = None,
        depth: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        执行搜索

        Args:
            query: 搜索查询
            provider: 指定提供商（可选，默认轮询）
            count: 结果数量
            depth: 搜索深度

        Returns:
            搜索结果字典
        """
        count = count or self.config.default_count
        depth = depth or self.config.default_depth

        # 获取要使用的 key 列表
        if provider:
            # 指定提供商
            keys = [k for k in self.config.keys if k.provider == provider]
            if not keys:
                return {"error": f"No keys found for provider: {provider}"}
            # 从该提供商的 key 中轮询
            key_config = keys[self.key_pool.current_index % len(keys)]
            provider_name = key_config.provider
            api_key = key_config.key
            # 更新全局索引
            self.key_pool._current_index += 1
            self.key_pool._save_state()
        else:
            # 全局轮询
            result = self.key_pool.get_next(self.config.keys)
            if not result:
                return {"error": "No API keys configured"}
            provider_name, api_key = result

        # 执行搜索
        try:
            provider_class = get_provider(provider_name)
            proxy_url = self.config.proxy.url if self.config.proxy.enabled else None
            provider_instance = provider_class(proxy_url=proxy_url)

            response = provider_instance.search(
                query=query,
                api_key=api_key,
                count=count,
                depth=depth,
                **kwargs,
            )

            return response.to_dict()

        except Exception as e:
            # 故障转移
            if self.config.fallback:
                return self._fallback_search(query, provider_name, api_key, count, depth, **kwargs)
            return {"error": str(e), "provider": provider_name}

    def _fallback_search(
        self,
        query: str,
        failed_provider: str,
        failed_key: str,
        count: int,
        depth: str,
        **kwargs,
    ) -> Dict[str, Any]:
        """故障转移搜索 - 尝试所有其他 key（包括同 provider 的其他 key）"""
        for key_config in self.config.keys:
            # 跳过刚才失败的 key
            if key_config.provider == failed_provider and key_config.key == failed_key:
                continue
            try:
                provider_class = get_provider(key_config.provider)
                proxy_url = self.config.proxy.url if self.config.proxy.enabled else None
                provider_instance = provider_class(proxy_url=proxy_url)

                response = provider_instance.search(
                    query=query,
                    api_key=key_config.key,
                    count=count,
                    depth=depth,
                    **kwargs,
                )

                result = response.to_dict()
                result["fallback"] = True
                return result

            except Exception:
                continue

        return {"error": "All keys failed"}

    def get_status(self) -> Dict[str, Any]:
        """获取配置状态"""
        provider_counts = {}
        for key in self.config.keys:
            provider_counts[key.provider] = provider_counts.get(key.provider, 0) + 1

        return {
            "providers": provider_counts,
            "total_keys": len(self.config.keys),
            "proxy_enabled": self.config.proxy.enabled,
            "proxy_url": self.config.proxy.url if self.config.proxy.enabled else None,
            "fallback_enabled": self.config.fallback,
            "current_index": self.key_pool.current_index,
        }
