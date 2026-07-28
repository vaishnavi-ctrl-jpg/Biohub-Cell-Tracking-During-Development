"""
Base feature extractor interface.
"""

from abc import ABC, abstractmethod
from typing import Dict
import numpy as np


class BaseFeatureExtractor(ABC):
    """Abstract interface for cell candidate feature computation."""

    @abstractmethod
    def extract(self, mask: np.ndarray, intensity_vol: np.ndarray) -> Dict[str, float]:
        """Extract scalar features given a binary 3D mask and intensity volume."""
        pass
