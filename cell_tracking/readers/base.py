"""
Base reader contract and dynamic registry decorator.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type
from cell_tracking.domain.frame import Frame

READER_REGISTRY: Dict[str, Type["BaseReader"]] = {}


def register_reader(name: str):
    """Decorator to register a new file reader implementation."""

    def decorator(cls: Type["BaseReader"]):
        READER_REGISTRY[name] = cls
        return cls

    return decorator


class BaseReader(ABC):
    """Abstract base class for all image sequence readers."""

    @abstractmethod
    def get_num_frames(self) -> int:
        """Return total number of time frames."""
        pass

    @abstractmethod
    def get_frame(self, frame_idx: int) -> Frame:
        """Return Frame object at given time index."""
        pass
