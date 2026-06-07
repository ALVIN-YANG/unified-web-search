"""配置管理"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class KeyConfig:
    """Key 配置"""
    provider: str
    key: str


@dataclass
class ProxyConfig:
    """代理配置"""
    enabled: bool = False
    url: str = "http://localhost:7897"


@dataclass
class Config:
    """主配置"""
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    keys: List[KeyConfig] = field(default_factory=list)
    default_count: int = 5
    default_depth: str = "basic"
    fallback: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proxy": asdict(self.proxy),
            "keys": [asdict(k) for k in self.keys],
            "default_count": self.default_count,
            "default_depth": self.default_depth,
            "fallback": self.fallback,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        proxy = ProxyConfig(**data.get("proxy", {}))
        keys = [KeyConfig(**k) for k in data.get("keys", [])]
        return cls(
            proxy=proxy,
            keys=keys,
            default_count=data.get("default_count", 5),
            default_depth=data.get("default_depth", "basic"),
            fallback=data.get("fallback", True),
        )


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".claude" / "skills" / "web-search" / "config.json",
        Path.home() / ".config" / "unified-web-search" / "config.json",
        Path("config.json"),
    ]

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._find_config()
        self._config: Optional[Config] = None

    def _find_config(self) -> Path:
        """查找配置文件"""
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path
        # 默认使用第一个路径
        return self.DEFAULT_CONFIG_PATHS[0]

    def load(self) -> Config:
        """加载配置"""
        if self._config:
            return self._config

        if not self.config_path.exists():
            self._config = Config()
            self.save()
            return self._config

        with open(self.config_path, "r") as f:
            data = json.load(f)

        self._config = Config.from_dict(data)
        return self._config

    def save(self):
        """保存配置"""
        if not self._config:
            return

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self._config.to_dict(), f, indent=2)

    @property
    def config(self) -> Config:
        if not self._config:
            self.load()
        return self._config

    def add_key(self, provider: str, key: str) -> bool:
        """添加 key"""
        config = self.config

        # 检查是否已存在
        for k in config.keys:
            if k.provider == provider and k.key == key:
                return False

        config.keys.append(KeyConfig(provider=provider, key=key))
        self.save()
        return True

    def remove_key(self, provider: str, key: str) -> bool:
        """移除 key"""
        config = self.config
        original_len = len(config.keys)
        config.keys = [k for k in config.keys if not (k.provider == provider and k.key == key)]
        if len(config.keys) < original_len:
            self.save()
            return True
        return False

    def get_keys_for_provider(self, provider: str) -> List[str]:
        """获取指定提供商的所有 key"""
        return [k.key for k in self.config.keys if k.provider == provider]

    def get_all_keys(self) -> List[KeyConfig]:
        """获取所有 key"""
        return self.config.keys
