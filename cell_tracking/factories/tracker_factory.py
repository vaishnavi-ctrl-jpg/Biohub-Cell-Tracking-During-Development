"""
TrackerFactory implementation.
"""

from cell_tracking.config.schema import TrackerConfig
from cell_tracking.trackers.base import BaseTracker, TRACKER_REGISTRY


class TrackerFactory:
    """Instantiates cell trackers registered in TRACKER_REGISTRY."""

    @staticmethod
    def create(config: TrackerConfig) -> BaseTracker:
        tracker_name = config.name
        if tracker_name not in TRACKER_REGISTRY:
            raise KeyError(
                f"Tracker '{tracker_name}' not found in registry. Available: {list(TRACKER_REGISTRY.keys())}"
            )
        cls = TRACKER_REGISTRY[tracker_name]
        return cls(**config.model_dump())
