"""
Dataset wrapper providing iterable frame sequence access over readers.
"""

from typing import Iterator
from cell_tracking.domain.frame import Frame
from cell_tracking.readers.base import BaseReader


class CellDataset:
    """Provides sequence iteration and indexing over 3D+T microscopy readers."""

    def __init__(self, reader: BaseReader):
        self.reader = reader

    def __len__(self) -> int:
        return self.reader.get_num_frames()

    def __getitem__(self, frame_idx: int) -> Frame:
        return self.reader.get_frame(frame_idx)

    def __iter__(self) -> Iterator[Frame]:
        for idx in range(len(self)):
            yield self[idx]
