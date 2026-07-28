"""
Synthetic 3D+T movie generator reader for offline testing and verification.
"""

from typing import Tuple, List, Dict, Any
import numpy as np
from cell_tracking.domain.frame import Frame
from cell_tracking.readers.base import BaseReader, register_reader


@register_reader("synthetic")
class SyntheticReader(BaseReader):
    """Generates synthetic 3D cell volume sequences with moving 3D Gaussian blobs."""

    def __init__(
        self,
        num_frames: int = 10,
        shape: Tuple[int, int, int] = (16, 64, 64),
        num_cells: int = 5,
        drift_scale: float = 2.0,
        seed: int = 42,
        **kwargs: Any,
    ):
        self.num_frames = num_frames
        self.shape = shape
        self.num_cells = num_cells
        self.drift_scale = drift_scale
        self.seed = seed

        # Generate initial ground-truth centroids and trajectories
        rng = np.random.RandomState(seed)
        z_max, y_max, x_max = shape

        # Initial cell centroids
        self.initial_centroids = np.zeros((num_cells, 3))
        self.initial_centroids[:, 0] = rng.uniform(3, z_max - 3, num_cells)
        self.initial_centroids[:, 1] = rng.uniform(8, y_max - 8, num_cells)
        self.initial_centroids[:, 2] = rng.uniform(8, x_max - 8, num_cells)

        # Precompute trajectories over T
        self.gt_trajectories: List[np.ndarray] = [self.initial_centroids.copy()]
        current = self.initial_centroids.copy()
        for t in range(1, num_frames):
            drift = rng.normal(0, drift_scale, size=(num_cells, 3))
            current = current + drift
            # Clip within boundaries
            current[:, 0] = np.clip(current[:, 0], 2, z_max - 3)
            current[:, 1] = np.clip(current[:, 1], 4, y_max - 5)
            current[:, 2] = np.clip(current[:, 2], 4, x_max - 5)
            self.gt_trajectories.append(current.copy())

    def get_num_frames(self) -> int:
        return self.num_frames

    def get_frame(self, frame_idx: int) -> Frame:
        if frame_idx < 0 or frame_idx >= self.num_frames:
            raise IndexError(f"Frame index {frame_idx} out of range [0, {self.num_frames-1}]")

        vol = np.zeros(self.shape, dtype=np.float32)
        centroids = self.gt_trajectories[frame_idx]
        z_grid, y_grid, x_grid = np.ogrid[
            0 : self.shape[0], 0 : self.shape[1], 0 : self.shape[2]
        ]

        # Render 3D Gaussian blobs
        for cz, cy, cx in centroids:
            dist_sq = (
                ((z_grid - cz) / 1.5) ** 2
                + ((y_grid - cy) / 3.0) ** 2
                + ((x_grid - cx) / 3.0) ** 2
            )
            blob = np.exp(-dist_sq)
            vol = np.maximum(vol, blob)

        # Add background noise
        rng = np.random.RandomState(self.seed + frame_idx)
        vol += rng.normal(0, 0.05, size=self.shape).astype(np.float32)
        vol = np.clip(vol, 0.0, 1.0)

        metadata: Dict[str, Any] = {
            "gt_centroids": centroids.tolist(),
            "shape": self.shape,
            "num_cells": self.num_cells,
        }

        return Frame(frame_idx=frame_idx, data=vol, timestamp=float(frame_idx), metadata=metadata)
