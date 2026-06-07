#!/usr/bin/env python3
"""配置管理测试"""

import json
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import ConfigManager, Config, KeyConfig, ProxyConfig


def test_config_roundtrip():
    """测试配置读写"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_path = Path(f.name)

    try:
        # 创建配置
        config = Config()
        config.keys = [
            KeyConfig(provider="tavily", key="tvly-test"),
            KeyConfig(provider="exa", key="exa-test"),
        ]
        config.proxy = ProxyConfig(enabled=True, url="http://localhost:7897")

        # 保存
        manager = ConfigManager(config_path)
        manager._config = config
        manager.save()

        # 重新加载
        manager2 = ConfigManager(config_path)
        loaded = manager2.load()

        assert len(loaded.keys) == 2
        assert loaded.keys[0].provider == "tavily"
        assert loaded.keys[0].key == "tvly-test"
        assert loaded.proxy.enabled is True
        assert loaded.proxy.url == "http://localhost:7897"
        print("✓ Config roundtrip test passed")
    finally:
        config_path.unlink(missing_ok=True)


def test_add_remove_key():
    """测试添加和删除 key"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{}')
        f.flush()
        config_path = Path(f.name)

    try:
        manager = ConfigManager(config_path)

        # 添加 key
        assert manager.add_key("tavily", "tvly-1") is True
        assert manager.add_key("tavily", "tvly-1") is False  # 重复
        assert manager.add_key("exa", "exa-1") is True

        assert len(manager.config.keys) == 2

        # 删除 key
        assert manager.remove_key("tavily", "tvly-1") is True
        assert manager.remove_key("tavily", "tvly-1") is False  # 不存在

        assert len(manager.config.keys) == 1
        print("✓ Add/Remove key test passed")
    finally:
        config_path.unlink(missing_ok=True)


if __name__ == "__main__":
    test_config_roundtrip()
    test_add_remove_key()
    print("\nAll config tests passed!")
