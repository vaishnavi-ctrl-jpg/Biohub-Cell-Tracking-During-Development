"""
Unit tests for submission formatter and schema validator.
"""

from cell_tracking.domain.cell import Cell
from cell_tracking.domain.track import Track
from cell_tracking.submission.formatter import SubmissionFormatter
from cell_tracking.submission.validator import SubmissionValidator


def test_submission_formatting_and_validation(tmp_path):
    c1 = Cell(1, 0, (2.0, 10.0, 10.0), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    c2 = Cell(1, 1, (2.1, 10.1, 10.1), (1, 8, 8, 3, 12, 12), 20, 20, 0.8, 0.9)
    t = Track(track_id=10, cells=[c1, c2])

    out_file = tmp_path / "submission.csv"
    SubmissionFormatter.save([t], str(out_file))

    assert out_file.exists()
    assert SubmissionValidator.validate(out_file) is True
