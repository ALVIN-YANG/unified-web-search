#!/usr/bin/env python3
"""Key 池轮询测试"""

import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.key_pool import KeyPool
from src.config import KeyConfig


def test_round_robin():
    """测试轮询逻辑"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        state_path = Path(f.name)

    try:
        pool = KeyPool(state_path=state_path)

        keys = [
            KeyConfig(provider="tavily", key="k1"),
            KeyConfig(provider="exa", key="k2"),
            KeyConfig(provider="tavily", key="k3"),
        ]

        # 轮询顺序
        result1 = pool.get_next(keys)
        assert result1 == ("tavily", "k1")

        result2 = pool.get_next(keys)
        assert result2 == ("exa", "k2")

        result3 = pool.get_next(keys)
        assert result3 == ("tavily", "k3")

        # 循环
        result4 = pool.get_next(keys)
        assert result4 == ("tavily", "k1")

        print("✓ Round-robin test passed")

        # 验证状态持久化（4次调用后 index=1，因为轮询 3 个 key）
        pool2 = KeyPool(state_path=state_path)
        assert pool2.current_index == 1, f"Expected 1, got {pool2.current_index}"
        print("✓ State persistence test passed")
    finally:
        state_path.unlink(missing_ok=True)


def test_empty_keys():
    """测试空 key 列表"""
    pool = KeyPool()
    result = pool.get_next([])
    assert result is None
    print("✓ Empty keys test passed")


if __name__ == "__main__":
    test_round_robin()
    test_empty_keys()
    print("\nAll key pool tests passed!")
