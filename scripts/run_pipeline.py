#!/usr/bin/env python3
"""
CLI entrypoint to run the cell tracking pipeline driven by configuration.

Usage:
    python scripts/run_pipeline.py --config configs/baseline.yaml
"""

import argparse
import sys
from cell_tracking.config.manager import ConfigManager
from cell_tracking.core.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description="CZ Biohub Cell Tracking Pipeline Runner")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/baseline.yaml",
        help="Path to YAML configuration file",
    )
    args = parser.parse_args()

    print(f"[CLI] Loading configuration from: {args.config}")
    config = ConfigManager.load_config(args.config)
    pipeline = Pipeline(config)
    result = pipeline.run()

    print(f"[CLI] Execution Complete!")
    print(f"      Run Directory   : {result.run_dir}")
    print(f"      Total Cells     : {result.total_cells_detected}")
    print(f"      Total Tracks    : {len(result.tracks)}")
    print(f"      Submission CSV  : {result.submission_path}")
    print(f"      Preview GIF     : {result.preview_path}")
    print(f"      Metrics HTML    : {result.dashboard_path}")


if __name__ == "__main__":
    main()
