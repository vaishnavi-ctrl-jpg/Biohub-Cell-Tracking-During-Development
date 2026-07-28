"""
Intensity feature extractor for 3D cell candidates.
"""

from typing import Dict
import numpy as np
from cell_tracking.features.base import BaseFeatureExtractor


class IntensityExtractor(BaseFeatureExtractor):
    """Computes pixel intensity statistics within cell mask."""

    def extract(self, mask: np.ndarray, intensity_vol: np.ndarray) -> Dict[str, float]:
        voxels = intensity_vol[mask > 0]
        if len(voxels) == 0:
            return {
                "mean_intensity": 0.0,
                "max_intensity": 0.0,
                "min_intensity": 0.0,
                "std_intensity": 0.0,
            }

        return {
            "mean_intensity": float(np.mean(voxels)),
            "max_intensity": float(np.max(voxels)),
            "min_intensity": float(np.min(voxels)),
            "std_intensity": float(np.std(voxels)),
        }
