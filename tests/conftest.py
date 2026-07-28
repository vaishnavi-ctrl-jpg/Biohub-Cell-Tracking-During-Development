"""
Shared Pytest fixtures for synthetic data, frames, and configuration.
"""

import pytest
import numpy as np
from cell_tracking.config.schema import BaselineConfig, DatasetConfig, DetectorConfig, TrackerConfig
from cell_tracking.domain.frame import Frame
from cell_tracking.readers.synthetic_reader import SyntheticReader


@pytest.fixture
def sample_config() -> BaselineConfig:
    return BaselineConfig(
        experiment_name="test_run",
        dataset=DatasetConfig(
            reader_type="synthetic",
            num_frames=3,
            shape_z=8,
            shape_y=32,
            shape_x=32,
            num_cells=3,
        ),
        detector=DetectorConfig(threshold_value=0.3),
        tracker=TrackerConfig(max_linking_distance=15.0),
    )


@pytest.fixture
def synthetic_reader() -> SyntheticReader:
    return SyntheticReader(num_frames=3, shape=(8, 32, 32), num_cells=3, seed=42)


@pytest.fixture
def sample_frame() -> Frame:
    vol = np.zeros((8, 32, 32), dtype=np.float32)
    # Put two 3D blobs
    vol[2:5, 10:14, 10:14] = 0.8
    vol[4:7, 20:24, 20:24] = 0.9
    return Frame(frame_idx=0, data=vol, timestamp=0.0)
