"""
Base tracker contract and dynamic registry decorator.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Type
from cell_tracking.domain.cell import Cell
from cell_tracking.domain.track import Track

TRACKER_REGISTRY: Dict[str, Type["BaseTracker"]] = {}


def register_tracker(name: str):
    """Decorator to register a new cell tracking implementation."""

    def decorator(cls: Type["BaseTracker"]):
        TRACKER_REGISTRY[name] = cls
        return cls

    return decorator


class BaseTracker(ABC):
    """Abstract base class for temporal cell tracking models."""

    @abstractmethod
    def track(self, detections_per_frame: List[List[Cell]]) -> List[Track]:
        """Link frame-level cell candidates across time into continuous Track objects."""
        pass
