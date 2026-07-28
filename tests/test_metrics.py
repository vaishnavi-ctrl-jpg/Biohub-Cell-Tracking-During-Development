"""
Unit tests for detection and tracking evaluation metrics.
"""

from cell_tracking.domain.cell import Cell
from cell_tracking.domain.track import Track
from cell_tracking.metrics.detection import evaluate_detection
from cell_tracking.metrics.tracking import evaluate_tracking


def test_evaluate_detection_perfect():
    c1 = Cell(1, 0, (2.0, 10.0, 10.0), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    gt = [(2.0, 10.0, 10.0)]

    metrics = evaluate_detection([c1], gt, match_threshold=5.0)
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1_score"] == 1.0


def test_evaluate_tracking():
    c1 = Cell(1, 0, (2.0, 10.0, 10.0), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    c2 = Cell(1, 1, (2.1, 10.1, 10.1), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    t = Track(track_id=1, cells=[c1, c2])

    metrics = evaluate_tracking([t])
    assert metrics["num_tracks"] == 1
    assert metrics["mean_track_length"] == 2.0
