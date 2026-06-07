"""Exa 搜索提供商"""

import json
from typing import Optional

from .base import BaseProvider, SearchResponse, SearchResult


class ExaProvider(BaseProvider):
    """Exa 搜索提供商"""

    name = "exa"
    api_url = "https://api.exa.ai/search"

    # 搜索类型映射
    DEPTH_MAP = {
        "basic": "auto",
        "advanced": "deep",
    }

    def search(
        self,
        query: str,
        api_key: str,
        count: int = 5,
        depth: str = "basic",
        **kwargs,
    ) -> SearchResponse:
        """执行 Exa 搜索"""
        import urllib.request

        search_type = self.DEPTH_MAP.get(depth, "auto")

        data = json.dumps({
            "query": query,
            "type": search_type,
            "numResults": count,
            "contents": {
                "highlights": True,
            },
        }).encode("utf-8")

        opener = self._get_opener()
        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/json",
            },
        )

        try:
            with opener.open(req, timeout=15) as response:
                result = json.loads(response.read().decode("utf-8"))

                results = []
                for r in result.get("results", []):
                    highlights = r.get("highlights", [])
                    content = highlights[0] if highlights else ""
                    results.append(SearchResult(
                        title=r.get("title", ""),
                        url=r.get("url", ""),
                        content=content[:500],
                    ))

                return SearchResponse(
                    provider=self.name,
                    results=results,
                    raw=result,
                )
        except Exception as e:
            raise RuntimeError(f"Exa search failed: {e}")
