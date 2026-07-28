"""
Unit tests for SyntheticReader and ReaderFactory.
"""

from cell_tracking.readers.synthetic_reader import SyntheticReader
from cell_tracking.factories.reader_factory import ReaderFactory
from cell_tracking.config.schema import DatasetConfig


def test_synthetic_reader_frames(synthetic_reader):
    assert synthetic_reader.get_num_frames() == 3
    frame0 = synthetic_reader.get_frame(0)
    assert frame0.frame_idx == 0
    assert frame0.shape == (8, 32, 32)
    assert "gt_centroids" in frame0.metadata


def test_reader_factory():
    cfg = DatasetConfig(reader_type="synthetic", num_frames=5)
    reader = ReaderFactory.create(cfg)
    assert isinstance(reader, SyntheticReader)
    assert reader.get_num_frames() == 5
