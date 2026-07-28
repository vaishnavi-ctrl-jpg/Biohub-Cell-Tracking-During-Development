"""
Config manager for parsing YAML configuration files into validated Pydantic schemas.
"""

from pathlib import Path
import yaml
from cell_tracking.config.schema import BaselineConfig


class ConfigManager:
    """Parses and validates configuration files."""

    @staticmethod
    def load_config(config_path: str) -> BaselineConfig:
        """Load YAML configuration file and validate against BaselineConfig schema."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        with open(path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f) or {}

        return BaselineConfig(**raw_data)
