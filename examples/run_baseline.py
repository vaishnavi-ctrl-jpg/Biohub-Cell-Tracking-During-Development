#!/usr/bin/env python3
"""
Standalone runnable example demonstrating V1 Baseline Cell Tracking.
"""

from cell_tracking.config.schema import BaselineConfig, DatasetConfig, DetectorConfig, TrackerConfig
from cell_tracking.core.pipeline import Pipeline


def main():
    print("=== CZ Biohub Cell Tracking: Baseline Example ===")

    # Define inline configuration
    config = BaselineConfig(
        experiment_name="example_baseline_run",
        dataset=DatasetConfig(
            reader_type="synthetic",
            num_frames=5,
            shape_z=12,
            shape_y=48,
            shape_x=48,
            num_cells=4,
        ),
        detector=DetectorConfig(threshold_value=0.3),
        tracker=TrackerConfig(max_linking_distance=15.0),
    )

    # Initialize and execute pipeline
    pipeline = Pipeline(config)
    result = pipeline.run()

    print("\n=== Example Execution Results ===")
    print(f"Run ID                : {result.run_id}")
    print(f"Cells Detected        : {result.total_cells_detected}")
    print(f"Tracks Formed         : {len(result.tracks)}")
    print(f"Submission Exported To: {result.submission_path}")


if __name__ == "__main__":
    main()
