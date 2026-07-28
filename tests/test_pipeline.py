"""
Integration tests for full Pipeline execution.
"""

from cell_tracking.config.schema import BaselineConfig, DatasetConfig
from cell_tracking.core.pipeline import Pipeline
from cell_tracking.domain.pipeline_result import PipelineResult


def test_full_pipeline_run(sample_config, tmp_path):
    sample_config.output_dir = str(tmp_path / "runs")
    pipeline = Pipeline(sample_config)
    result = pipeline.run()

    assert isinstance(result, PipelineResult)
    assert result.total_cells_detected > 0
    assert len(result.tracks) > 0
    assert "detection" in result.metrics
    assert "tracking" in result.metrics
