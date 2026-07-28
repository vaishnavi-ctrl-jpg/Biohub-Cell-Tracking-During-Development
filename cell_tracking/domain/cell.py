"""
Cell domain schema.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


@dataclass
class Cell:
    """Represents a single detected cell candidate within a 3D time frame."""

    cell_id: int
    frame_idx: int
    centroid: Tuple[float, float, float]  # (z, y, x)
    bbox: Tuple[int, int, int, int, int, int]  # (z_min, y_min, x_min, z_max, y_max, x_max)
    volume_voxels: int
    area_pixels: int
    mean_intensity: float
    max_intensity: float
    confidence: float = 1.0
    track_id: Optional[int] = None
    mask_id: Optional[int] = None
    features: Dict[str, float] = field(default_factory=dict)
