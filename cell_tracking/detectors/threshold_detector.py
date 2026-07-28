"""
Classical thresholding & connected components 3D cell candidate detector.
"""

from typing import List, Any
import numpy as np
from scipy.ndimage import gaussian_filter, label

from cell_tracking.domain.cell import Cell
from cell_tracking.domain.frame import Frame
from cell_tracking.detectors.base import BaseDetector, register_detector
from cell_tracking.features.geometry import GeometryExtractor
from cell_tracking.features.intensity import IntensityExtractor


@register_detector("threshold")
class ThresholdDetector(BaseDetector):
    """Classical 3D cell detector using intensity thresholding and connected components."""

    def __init__(
        self,
        threshold_value: float = 0.4,
        gaussian_sigma: float = 1.0,
        min_volume_voxels: int = 10,
        max_volume_voxels: int = 5000,
        **kwargs: Any,
    ):
        self.threshold_value = threshold_value
        self.gaussian_sigma = gaussian_sigma
        self.min_volume_voxels = min_volume_voxels
        self.max_volume_voxels = max_volume_voxels

        self.geom_extractor = GeometryExtractor()
        self.intens_extractor = IntensityExtractor()

    def detect(self, frame: Frame) -> List[Cell]:
        vol = frame.data

        # 1. 3D Gaussian pre-smoothing
        if self.gaussian_sigma > 0:
            smoothed = gaussian_filter(vol, sigma=self.gaussian_sigma)
        else:
            smoothed = vol

        # 2. Binary thresholding
        binary_mask = smoothed > self.threshold_value

        # 3. 3D Connected component labeling
        labeled_array, num_features = label(binary_mask)

        detected_cells: List[Cell] = []
        cell_id_counter = 1

        # 4. Feature extraction and candidate object construction
        for obj_idx in range(1, num_features + 1):
            obj_mask = (labeled_array == obj_idx).astype(np.uint8)
            vol_voxels = int(np.sum(obj_mask))

            # Filter out spurious noise or oversized blobs
            if vol_voxels < self.min_volume_voxels or vol_voxels > self.max_volume_voxels:
                continue

            # Extract features
            geom_feats = self.geom_extractor.extract(obj_mask, vol)
            intens_feats = self.intens_extractor.extract(obj_mask, vol)
            bbox = self.geom_extractor.get_bbox(obj_mask)

            centroid = (
                geom_feats["centroid_z"],
                geom_feats["centroid_y"],
                geom_feats["centroid_x"],
            )

            all_features = {**geom_feats, **intens_feats}

            cell = Cell(
                cell_id=cell_id_counter,
                frame_idx=frame.frame_idx,
                centroid=centroid,
                bbox=bbox,
                volume_voxels=vol_voxels,
                area_pixels=vol_voxels,  # 3D volume proxy
                mean_intensity=intens_feats["mean_intensity"],
                max_intensity=intens_feats["max_intensity"],
                confidence=1.0,
                mask_id=obj_idx,
                features=all_features,
            )
            detected_cells.append(cell)
            cell_id_counter += 1

        return detected_cells
