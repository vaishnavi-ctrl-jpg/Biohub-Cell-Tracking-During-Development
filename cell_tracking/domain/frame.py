"""
Frame domain schema.
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Any
import numpy as np


@dataclass
class Frame:
    """Represents a single 3D image volume slice at time index t."""

    frame_idx: int
    data: np.ndarray  # 3D array (Z, Y, X)
    timestamp: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def shape(self) -> Tuple[int, ...]:
        return self.data.shape
