"""
Unit tests for domain schema classes.
"""

from cell_tracking.domain.cell import Cell
from cell_tracking.domain.track import Track
from cell_tracking.domain.frame import Frame
import numpy as np


def test_cell_dataclass():
    cell = Cell(
        cell_id=1,
        frame_idx=0,
        centroid=(2.0, 10.0, 10.0),
        bbox=(1, 8, 8, 3, 12, 12),
        volume_voxels=25,
        area_pixels=25,
        mean_intensity=0.85,
        max_intensity=0.95,
    )
    assert cell.cell_id == 1
    assert cell.frame_idx == 0
    assert cell.centroid == (2.0, 10.0, 10.0)


def test_track_properties():
    c1 = Cell(1, 0, (2.0, 10.0, 10.0), (1, 8, 8, 3, 12, 12), 25, 25, 0.8, 0.9)
    c2 = Cell(1, 1, (2.2, 10.5, 10.2), (1, 8, 8, 3, 12, 12), 25, 25, 0.8, 0.9)

    track = Track(track_id=10, cells=[c1, c2])
    assert track.track_id == 10
    assert track.start_frame == 0
    assert track.end_frame == 1
    assert track.length == 2
