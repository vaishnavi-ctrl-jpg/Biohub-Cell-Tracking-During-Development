"""
Self-contained Experiment Manager ("MLFlow Lite") archiving timestamped runs.
"""

from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys
from typing import Dict, Any

import yaml
from cell_tracking.config.schema import BaselineConfig


class ExperimentManager:
    """Manages creation and artifact archiving for timestamped experiment runs."""

    @staticmethod
    def create_run_directory(base_dir: str = "runs", prefix: str = "run") -> Path:
        now_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        run_name = f"{prefix}_{now_str}"
        run_path = Path(base_dir) / run_name
        run_path.mkdir(parents=True, exist_ok=True)
        return run_path

    @classmethod
    def archive_run(
        cls,
        run_dir: Path,
        config: BaselineConfig,
        metrics: Dict[str, Any],
        benchmark_stats: Dict[str, Any],
    ) -> None:
        # 1. Save Config
        config_path = run_dir / "config.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config.model_dump(), f, default_flow_style=False)

        # 2. Save System & Git Metadata
        meta_info = {
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version,
            "git_commit_sha": cls._get_git_commit_sha(),
        }

        # 3. Save Metrics JSON
        full_metrics = {
            "metadata": meta_info,
            "benchmark": benchmark_stats,
            "metrics": metrics,
        }
        metrics_path = run_dir / "metrics.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(full_metrics, f, indent=2)

    @staticmethod
    def _get_git_commit_sha() -> str:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
            )
            return res.stdout.strip()
        except Exception:
            return "unknown_or_uncommitted"
