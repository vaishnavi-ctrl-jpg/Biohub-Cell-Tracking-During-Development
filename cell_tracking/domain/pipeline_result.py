"""
PipelineResult domain schema.
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from cell_tracking.domain.track import Track


@dataclass
class PipelineResult:
    """Encapsulates the complete result of an end-to-end cell tracking pipeline execution."""

    run_id: str
    run_dir: str
    tracks: List[Track]
    total_cells_detected: int
    metrics: Dict[str, Any]
    submission_path: str
    preview_path: str
    dashboard_path: str
    benchmark_stats: Dict[str, float]
