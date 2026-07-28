"""
Hardened Kaggle submission format validator.
"""

from pathlib import Path
from typing import Union
import pandas as pd


class SubmissionValidator:
    """Validates submission files for Kaggle compliance."""

    REQUIRED_COLUMNS = ["cell_id", "frame", "z", "y", "x", "parent_id", "track_id"]

    @classmethod
    def validate(cls, submission: Union[str, Path, pd.DataFrame]) -> bool:
        if isinstance(submission, (str, Path)):
            path = Path(submission)
            if not path.exists():
                raise FileNotFoundError(f"Submission file does not exist: {path}")
            df = pd.read_csv(path)
        else:
            df = submission

        # 1. Check required columns
        for col in cls.REQUIRED_COLUMNS:
            if col not in df.columns:
                raise ValueError(f"Missing required column in submission: {col}")

        # 2. Check non-empty (if data frames processed)
        if df.empty:
            raise ValueError("Submission DataFrame is empty!")

        # 3. Check null values
        if df[cls.REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError("Submission contains null/NaN values!")

        return True
