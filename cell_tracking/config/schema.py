"""
Pydantic configuration schemas for type-safe parameter validation.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DatasetConfig(BaseModel):
    reader_type: str = "synthetic"  # "synthetic" or "zarr"
    path: str = "data/raw/synthetic"
    num_frames: int = 10
    shape_z: int = 16
    shape_y: int = 64
    shape_x: int = 64
    num_cells: int = 5
    drift_scale: float = 2.0


class DetectorConfig(BaseModel):
    name: str = "threshold"
    threshold_value: float = 0.5
    gaussian_sigma: float = 1.0
    min_volume_voxels: int = 10
    max_volume_voxels: int = 5000


class TrackerConfig(BaseModel):
    name: str = "nearest_neighbor"
    max_linking_distance: float = 15.0
    weight_distance: float = 1.0
    weight_intensity: float = 0.0
    weight_volume: float = 0.0


class EvaluationConfig(BaseModel):
    enabled: bool = True
    match_distance_threshold: float = 10.0


class SubmissionConfig(BaseModel):
    output_filename: str = "submission.csv"


class BaselineConfig(BaseModel):
    experiment_name: str = "v1_baseline"
    seed: int = 42
    output_dir: str = "runs"
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    detector: DetectorConfig = Field(default_factory=DetectorConfig)
    tracker: TrackerConfig = Field(default_factory=TrackerConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    submission: SubmissionConfig = Field(default_factory=SubmissionConfig)
