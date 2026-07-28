"""
Base detector contract and dynamic registry decorator.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Type
from cell_tracking.domain.cell import Cell
from cell_tracking.domain.frame import Frame

DETECTOR_REGISTRY: Dict[str, Type["BaseDetector"]] = {}


def register_detector(name: str):
    """Decorator to register a new cell detector implementation."""

    def decorator(cls: Type["BaseDetector"]):
        DETECTOR_REGISTRY[name] = cls
        return cls

    return decorator


class BaseDetector(ABC):
    """Abstract base class for 3D cell detection models."""

    @abstractmethod
    def detect(self, frame: Frame) -> List[Cell]:
        """Detect cell candidates within a 3D frame and return Cell domain objects."""
        pass
