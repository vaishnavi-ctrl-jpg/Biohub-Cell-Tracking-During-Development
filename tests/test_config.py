"""
Unit tests for configuration schemas and manager.
"""

import pytest
from cell_tracking.config.schema import BaselineConfig, DatasetConfig
from cell_tracking.config.manager import ConfigManager


def test_baseline_config_defaults():
    cfg = BaselineConfig()
    assert cfg.experiment_name == "v1_baseline"
    assert cfg.seed == 42
    assert cfg.dataset.reader_type == "synthetic"


def test_config_validation_error():
    with pytest.raises(Exception):
        # Invalid type
        DatasetConfig(num_frames="invalid_int")
