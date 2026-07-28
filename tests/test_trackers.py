"""
Unit tests for NearestNeighborTracker.
"""

from cell_tracking.domain.cell import Cell
from cell_tracking.trackers.nearest_neighbor import NearestNeighborTracker


def test_nearest_neighbor_tracking():
    # Frame 0 cells
    c0_1 = Cell(1, 0, (2.0, 10.0, 10.0), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    c0_2 = Cell(2, 0, (4.0, 20.0, 20.0), (3, 18, 18, 5, 22, 22), 20, 20, 0.8, 0.9)

    # Frame 1 cells (slightly drifted)
    c1_1 = Cell(1, 1, (2.1, 10.5, 10.2), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    c1_2 = Cell(2, 1, (4.2, 20.3, 20.1), (3, 18, 18, 5, 22, 22), 20, 20, 0.8, 0.9)

    detections = [[c0_1, c0_2], [c1_1, c1_2]]

    tracker = NearestNeighborTracker(max_linking_distance=10.0)
    tracks = tracker.track(detections)

    assert len(tracks) == 2
    assert tracks[0].length == 2
    assert tracks[1].length == 2
    assert tracks[0].cells[0].track_id == tracks[0].cells[1].track_id
