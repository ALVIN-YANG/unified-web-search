"""Key 池管理 - 全局轮询"""

import json
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass

from .config import KeyConfig


@dataclass
class PoolEntry:
    """池中的 key 条目"""
    provider: str
    key: str
    index: int


class KeyPool:
    """全局 Key 池 - 轮询管理"""

    def __init__(self, state_path: Optional[Path] = None):
        self.state_path = state_path or Path.home() / ".claude" / "skills" / "web-search" / "state.json"
        self._current_index: int = 0
        self._load_state()

    def _load_state(self):
        """加载状态"""
        if self.state_path.exists():
            try:
                with open(self.state_path, "r") as f:
                    state = json.load(f)
                    self._current_index = state.get("current_index", 0)
            except (json.JSONDecodeError, KeyError):
                self._current_index = 0

    def _save_state(self):
        """保存状态"""
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_path, "w") as f:
            json.dump({"current_index": self._current_index}, f)

    def get_next(self, keys: list[KeyConfig]) -> Optional[Tuple[str, str]]:
        """
        获取下一个 key（轮询）

        Returns:
            (provider, key) 或 None
        """
        if not keys:
            return None

        index = self._current_index % len(keys)
        entry = keys[index]

        self._current_index = index + 1
        self._save_state()

        return (entry.provider, entry.key)

    def reset(self):
        """重置计数器"""
        self._current_index = 0
        self._save_state()

    @property
    def current_index(self) -> int:
        return self._current_index
