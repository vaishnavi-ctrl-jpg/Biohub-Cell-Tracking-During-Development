"""
DetectorFactory implementation.
"""

from cell_tracking.config.schema import DetectorConfig
from cell_tracking.detectors.base import BaseDetector, DETECTOR_REGISTRY


class DetectorFactory:
    """Instantiates cell detectors registered in DETECTOR_REGISTRY."""

    @staticmethod
    def create(config: DetectorConfig) -> BaseDetector:
        detector_name = config.name
        if detector_name not in DETECTOR_REGISTRY:
            raise KeyError(
                f"Detector '{detector_name}' not found in registry. Available: {list(DETECTOR_REGISTRY.keys())}"
            )
        cls = DETECTOR_REGISTRY[detector_name]
        return cls(**config.model_dump())
