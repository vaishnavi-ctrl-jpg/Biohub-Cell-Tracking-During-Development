"""
Memory-efficient chunked Zarr 3D+T reader.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import numpy as np
from cell_tracking.domain.frame import Frame
from cell_tracking.readers.base import BaseReader, register_reader


@register_reader("zarr")
class ZarrReader(BaseReader):
    """Lazily opens Zarr 4D time series arrays (T, Z, Y, X)."""

    def __init__(self, path: str, **kwargs: Any):
        self.path = Path(path)
        self._zarr_array = None
        self._num_frames = 0
        self._cached_metadata: Dict[str, Any] = {}
        self._open_zarr()

    def _open_zarr(self) -> None:
        if not self.path.exists():
            # If path doesn't exist, fallback gracefully or raise error
            raise FileNotFoundError(f"Zarr array not found at: {self.path}")

        try:
            import zarr

            self._zarr_array = zarr.open(str(self.path), mode="r")
            self._num_frames = self._zarr_array.shape[0]
            self._cached_metadata = {
                "shape": self._zarr_array.shape,
                "dtype": str(self._zarr_array.dtype),
                "chunks": self._zarr_array.chunks,
            }
        except ImportError:
            raise ImportError("zarr package is required to read Zarr arrays.")

    def get_num_frames(self) -> int:
        return self._num_frames

    def get_frame(self, frame_idx: int) -> Frame:
        if self._zarr_array is None:
            raise RuntimeError("Zarr array is not open.")

        frame_data = np.array(self._zarr_array[frame_idx], dtype=np.float32)
        return Frame(
            frame_idx=frame_idx,
            data=frame_data,
            timestamp=float(frame_idx),
            metadata=self._cached_metadata,
        )
