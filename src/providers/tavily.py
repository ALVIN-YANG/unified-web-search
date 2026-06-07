"""Tavily 搜索提供商"""

import json
from typing import Optional

from .base import BaseProvider, SearchResponse, SearchResult


class TavilyProvider(BaseProvider):
    """Tavily 搜索提供商"""

    name = "tavily"
    api_url = "https://api.tavily.com/search"

    def search(
        self,
        query: str,
        api_key: str,
        count: int = 5,
        depth: str = "basic",
        **kwargs,
    ) -> SearchResponse:
        """执行 Tavily 搜索"""
        import urllib.request

        data = json.dumps({
            "api_key": api_key,
            "query": query,
            "max_results": count,
            "search_depth": depth,
            "include_answer": True,
        }).encode("utf-8")

        opener = self._get_opener()
        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={"Content-Type": "application/json"},
        )

        try:
            with opener.open(req, timeout=15) as response:
                result = json.loads(response.read().decode("utf-8"))

                results = []
                for r in result.get("results", []):
                    results.append(SearchResult(
                        title=r.get("title", ""),
                        url=r.get("url", ""),
                        content=r.get("content", "")[:500],
                    ))

                return SearchResponse(
                    provider=self.name,
                    results=results,
                    answer=result.get("answer"),
                    raw=result,
                )
        except Exception as e:
            raise RuntimeError(f"Tavily search failed: {e}")
