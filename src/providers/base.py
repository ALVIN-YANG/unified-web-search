"""提供商基类"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List


class SearchResult:
    """搜索结果"""

    def __init__(self, title: str, url: str, content: str = ""):
        self.title = title
        self.url = url
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
        }


class SearchResponse:
    """搜索响应"""

    def __init__(
        self,
        provider: str,
        results: List[SearchResult],
        answer: Optional[str] = None,
        raw: Optional[Dict[str, Any]] = None,
    ):
        self.provider = provider
        self.results = results
        self.answer = answer
        self.raw = raw

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "answer": self.answer,
            "results": [r.to_dict() for r in self.results],
        }


class BaseProvider(ABC):
    """提供商基类"""

    name: str = "base"

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url

    @abstractmethod
    def search(
        self,
        query: str,
        api_key: str,
        count: int = 5,
        depth: str = "basic",
        **kwargs,
    ) -> SearchResponse:
        """
        执行搜索

        Args:
            query: 搜索查询
            api_key: API key
            count: 结果数量
            depth: 搜索深度 (basic/advanced)

        Returns:
            SearchResponse 对象
        """
        pass

    def _get_opener(self):
        """获取 URL opener（带代理支持）"""
        import urllib.request

        if self.proxy_url:
            proxy_handler = urllib.request.ProxyHandler({
                "http": self.proxy_url,
                "https": self.proxy_url,
            })
            return urllib.request.build_opener(proxy_handler)
        return urllib.request.build_opener()
