"""
2D Max Projection rendering helper.
"""

import numpy as np


def render_max_projection(vol: np.ndarray, axis: int = 0) -> np.ndarray:
    """Computes 2D Max Intensity Projection along specified axis."""
    if vol.ndim == 3:
        return np.max(vol, axis=axis)
    return vol
