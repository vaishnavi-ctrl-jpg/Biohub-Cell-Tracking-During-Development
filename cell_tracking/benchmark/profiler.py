"""
Stage performance, timing, and memory profiling utilities.
"""

import time
import os
from typing import Dict, Any


class StageProfiler:
    """Tracks execution time and memory usage per pipeline stage."""

    def __init__(self) -> None:
        self.stage_times: Dict[str, float] = {}
        self.start_times: Dict[str, float] = {}

    def start_stage(self, name: str) -> None:
        self.start_times[name] = time.perf_counter()

    def stop_stage(self, name: str) -> float:
        if name in self.start_times:
            elapsed = time.perf_counter() - self.start_times[name]
            self.stage_times[name] = round(elapsed, 4)
            return elapsed
        return 0.0

    def get_summary(self) -> Dict[str, Any]:
        total_time = sum(self.stage_times.values())
        return {
            "stage_times_sec": self.stage_times,
            "total_time_sec": round(total_time, 4),
            "peak_ram_mb": self._get_ram_usage_mb(),
        }

    def _get_ram_usage_mb(self) -> float:
        try:
            import psutil

            process = psutil.Process(os.getpid())
            return round(process.memory_info().rss / (1024 * 1024), 2)
        except Exception:
            return 0.0
