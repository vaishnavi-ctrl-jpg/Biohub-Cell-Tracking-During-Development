"""
Unit tests for ThresholdDetector and DetectorFactory.
"""

from cell_tracking.detectors.threshold_detector import ThresholdDetector
from cell_tracking.factories.detector_factory import DetectorFactory
from cell_tracking.config.schema import DetectorConfig


def test_threshold_detector_detection(sample_frame):
    detector = ThresholdDetector(threshold_value=0.5, min_volume_voxels=2)
    cells = detector.detect(sample_frame)
    assert len(cells) == 2
    assert cells[0].frame_idx == 0
    assert cells[0].volume_voxels > 0


def test_detector_factory():
    cfg = DetectorConfig(name="threshold", threshold_value=0.4)
    detector = DetectorFactory.create(cfg)
    assert isinstance(detector, ThresholdDetector)
