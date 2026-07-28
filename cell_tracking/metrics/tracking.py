"""
Tracking quality evaluation metrics.
"""

from typing import List, Dict, Any
from cell_tracking.domain.track import Track


def evaluate_tracking(tracks: List[Track]) -> Dict[str, Any]:
    """Computes trajectory length statistics and track counts."""
    if not tracks:
        return {
            "num_tracks": 0,
            "mean_track_length": 0.0,
            "max_track_length": 0,
            "min_track_length": 0,
        }

    lengths = [tr.length for tr in tracks]

    return {
        "num_tracks": len(tracks),
        "mean_track_length": round(sum(lengths) / len(lengths), 2),
        "max_track_length": max(lengths),
        "min_track_length": min(lengths),
    }
