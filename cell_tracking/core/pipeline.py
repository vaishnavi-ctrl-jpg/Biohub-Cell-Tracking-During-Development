"""
Main pipeline orchestrator class executing end-to-end cell tracking runs.
"""

from typing import List, Dict, Any
from pathlib import Path

from cell_tracking.config.schema import BaselineConfig
from cell_tracking.domain.cell import Cell
from cell_tracking.domain.track import Track
from cell_tracking.domain.pipeline_result import PipelineResult
from cell_tracking.factories.reader_factory import ReaderFactory
from cell_tracking.factories.detector_factory import DetectorFactory
from cell_tracking.factories.tracker_factory import TrackerFactory
from cell_tracking.datasets.dataset import CellDataset
from cell_tracking.metrics.detection import evaluate_detection
from cell_tracking.metrics.tracking import evaluate_tracking
from cell_tracking.metrics.dashboard import DashboardGenerator
from cell_tracking.submission.formatter import SubmissionFormatter
from cell_tracking.submission.validator import SubmissionValidator
from cell_tracking.visualization.gif_exporter import GifExporter
from cell_tracking.experiments.manager import ExperimentManager
from cell_tracking.benchmark.profiler import StageProfiler
from cell_tracking.utils.logger import get_logger
from cell_tracking.utils.seed import set_seed

logger = get_logger("cell_tracking.pipeline")


class Pipeline:
    """End-to-End cell tracking pipeline executing Reader -> Detector -> Tracker -> Evaluator -> Submission."""

    def __init__(self, config: BaselineConfig):
        self.config = config
        set_seed(config.seed)

        # Instantiate components via Factories
        self.reader = ReaderFactory.create(config.dataset)
        self.dataset = CellDataset(self.reader)
        self.detector = DetectorFactory.create(config.detector)
        self.tracker = TrackerFactory.create(config.tracker)
        self.profiler = StageProfiler()

    def run(self) -> PipelineResult:
        logger.info(f"=== Starting Pipeline Run: '{self.config.experiment_name}' ===")

        # 1. Create Timestamped Experiment Directory
        run_dir = ExperimentManager.create_run_directory(
            base_dir=self.config.output_dir, prefix=self.config.experiment_name
        )
        logger.info(f"Run directory created: {run_dir}")

        # 2. Frame-by-Frame Detection
        self.profiler.start_stage("detection")
        logger.info(f"Processing {len(self.dataset)} frame(s) for cell detection...")

        detections_per_frame: List[List[Cell]] = []
        gt_centroids_all: List[List] = []
        total_cells_count = 0

        for frame in self.dataset:
            cells = self.detector.detect(frame)
            detections_per_frame.append(cells)
            total_cells_count += len(cells)

            if "gt_centroids" in frame.metadata:
                gt_centroids_all.append(frame.metadata["gt_centroids"])

        det_time = self.profiler.stop_stage("detection")
        logger.info(
            f"Detection completed in {det_time:.2f}s | Total Cells Detected: {total_cells_count}"
        )

        # 3. Temporal Cell Tracking
        self.profiler.start_stage("tracking")
        logger.info("Executing temporal cell tracking...")
        tracks: List[Track] = self.tracker.track(detections_per_frame)
        track_time = self.profiler.stop_stage("tracking")
        logger.info(f"Tracking completed in {track_time:.2f}s | Tracks Created: {len(tracks)}")

        # 4. Metric Evaluation
        self.profiler.start_stage("evaluation")
        eval_metrics: Dict[str, Any] = {}

        if self.config.evaluation.enabled and gt_centroids_all:
            # Flatten ground truths and predictions for detection metric
            all_pred_cells = [c for frame_cells in detections_per_frame for c in frame_cells]
            all_gt_centroids = [
                c for frame_gt in gt_centroids_all for c in frame_gt
            ]
            det_metrics = evaluate_detection(
                all_pred_cells,
                all_gt_centroids,
                match_threshold=self.config.evaluation.match_distance_threshold,
            )
            tr_metrics = evaluate_tracking(tracks)
            eval_metrics = {"detection": det_metrics, "tracking": tr_metrics}
            logger.info(f"Evaluation Metrics: F1={det_metrics['f1_score']} | Tracks={tr_metrics['num_tracks']}")

        self.profiler.stop_stage("evaluation")

        # 5. Formatter & Validator Submission CSV
        self.profiler.start_stage("submission")
        sub_path = str(run_dir / self.config.submission.output_filename)
        SubmissionFormatter.save(tracks, sub_path)
        SubmissionValidator.validate(sub_path)
        self.profiler.stop_stage("submission")
        logger.info(f"Submission generated and validated at: {sub_path}")

        # 6. Visualization (GIF preview)
        self.profiler.start_stage("visualization")
        preview_path = str(run_dir / "preview.gif")
        GifExporter.export_gif(self.dataset, tracks, preview_path)
        self.profiler.stop_stage("visualization")
        logger.info(f"Preview GIF exported to: {preview_path}")

        # 7. Benchmark stats & Dashboard HTML
        benchmark_stats = self.profiler.get_summary()
        eval_metrics["benchmark"] = benchmark_stats
        dashboard_path = str(run_dir / "metrics.html")
        DashboardGenerator.generate_html(eval_metrics, dashboard_path)

        # 8. Archive Experiment Artifacts
        ExperimentManager.archive_run(run_dir, self.config, eval_metrics, benchmark_stats)

        logger.info(f"=== Pipeline Run Completed Successfully in {benchmark_stats['total_time_sec']}s ===")

        return PipelineResult(
            run_id=run_dir.name,
            run_dir=str(run_dir),
            tracks=tracks,
            total_cells_detected=total_cells_count,
            metrics=eval_metrics,
            submission_path=sub_path,
            preview_path=preview_path,
            dashboard_path=dashboard_path,
            benchmark_stats=benchmark_stats,
        )
