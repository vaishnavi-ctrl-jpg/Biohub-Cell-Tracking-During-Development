"""
ReaderFactory implementation.
"""

from cell_tracking.config.schema import DatasetConfig
from cell_tracking.readers.base import BaseReader, READER_REGISTRY


class ReaderFactory:
    """Instantiates image sequence readers registered in READER_REGISTRY."""

    @staticmethod
    def create(config: DatasetConfig) -> BaseReader:
        reader_type = config.reader_type
        if reader_type not in READER_REGISTRY:
            raise KeyError(
                f"Reader '{reader_type}' not found in registry. Available: {list(READER_REGISTRY.keys())}"
            )
        cls = READER_REGISTRY[reader_type]
        return cls(**config.model_dump())
