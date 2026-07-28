"""
Geometric feature extractor for 3D cell candidates.
"""

from typing import Dict, Tuple
import numpy as np
from cell_tracking.features.base import BaseFeatureExtractor


class GeometryExtractor(BaseFeatureExtractor):
    """Computes geometric features: volume, centroid, bounding box, and radius."""

    def extract(self, mask: np.ndarray, intensity_vol: np.ndarray) -> Dict[str, float]:
        indices = np.argwhere(mask > 0)
        if len(indices) == 0:
            return {
                "volume": 0.0,
                "centroid_z": 0.0,
                "centroid_y": 0.0,
                "centroid_x": 0.0,
                "radius": 0.0,
            }

        z_coords, y_coords, x_coords = indices[:, 0], indices[:, 1], indices[:, 2]
        volume = float(len(indices))
        cz = float(np.mean(z_coords))
        cy = float(np.mean(y_coords))
        cx = float(np.mean(x_coords))

        # Equivalent sphere radius
        radius = float((3.0 * volume / (4.0 * np.pi)) ** (1.0 / 3.0))

        return {
            "volume": volume,
            "centroid_z": cz,
            "centroid_y": cy,
            "centroid_x": cx,
            "radius": radius,
        }

    @staticmethod
    def get_bbox(mask: np.ndarray) -> Tuple[int, int, int, int, int, int]:
        """Compute 3D bounding box (z_min, y_min, x_min, z_max, y_max, x_max)."""
        indices = np.argwhere(mask > 0)
        if len(indices) == 0:
            return (0, 0, 0, 0, 0, 0)
        z_min, y_min, x_min = indices.min(axis=0)
        z_max, y_max, x_max = indices.max(axis=0) + 1
        return (int(z_min), int(y_min), int(x_min), int(z_max), int(y_max), int(x_max))
