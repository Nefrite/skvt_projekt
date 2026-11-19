"""Konfigurace instance `Maintenance/config.yaml` (zadání 13, kap. 4).

Chybějící klíč = výchozí hodnota z taxonomy/defaults.yaml; neznámý klíč = varování.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path

from . import CORE_ROOT
from .errors import ConfigError
from .taxonomy import load_yaml

CONFIG_REL = Path("Maintenance") / "config.yaml"


@dataclass
class Config:
    data: dict
    path: Path | None
    warnings: list = field(default_factory=list)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    @property
    def thresholds(self) -> dict:
        return self.data.get("thresholds") or {}


def _merge(defaults: dict, local: dict, prefix: str, warnings: list) -> dict:
    out = copy.deepcopy(defaults)
    for k, v in local.items():
        if k not in defaults:
            warnings.append(f"Neznámý klíč konfigurace: {prefix}{k}")
            out[k] = v
        elif isinstance(defaults[k], dict) and isinstance(v, dict):
            out[k] = _merge(defaults[k], v, f"{prefix}{k}.", warnings)
        else:
            out[k] = v
    return out


def load(vault: Path, core_root: Path = CORE_ROOT) -> Config:
    defaults = load_yaml(core_root / "taxonomy" / "defaults.yaml") or {}
    path = Path(vault) / CONFIG_REL
    warnings: list = []
    if path.is_file():
        local = load_yaml(path) or {}
        if not isinstance(local, dict):
            raise ConfigError(f"Konfigurace není mapa: {path}")
        data = _merge(defaults, local, "", warnings)
    else:
        data = copy.deepcopy(defaults)
        path = None
    if data.get("hestia_config") != 1:
        raise ConfigError(f"Nepodporovaná verze konfigurace hestia_config={data.get('hestia_config')!r}")
    if not isinstance(data.get("game_layer"), bool):
        raise ConfigError(f"game_layer musí být true nebo false, je {data.get('game_layer')!r}")
    return Config(data, path, warnings)
