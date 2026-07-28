"""
Track domain schema.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from cell_tracking.domain.cell import Cell


@dataclass
class Track:
    """Represents a continuous trajectory of a cell across multiple time frames."""

    track_id: int
    cells: List[Cell] = field(default_factory=list)
    parent_id: Optional[int] = None

    @property
    def start_frame(self) -> int:
        return self.cells[0].frame_idx if self.cells else 0

    @property
    def end_frame(self) -> int:
        return self.cells[-1].frame_idx if self.cells else 0

    @property
    def length(self) -> int:
        return len(self.cells)
