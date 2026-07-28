"""
Kaggle competition submission formatter and exporter.
"""

from pathlib import Path
from typing import List
import pandas as pd
from cell_tracking.domain.track import Track


class SubmissionFormatter:
    """Formats cell trajectory tracks into official Kaggle submission CSV schemas."""

    @staticmethod
    def to_dataframe(tracks: List[Track]) -> pd.DataFrame:
        rows = []
        for track in tracks:
            parent_id = track.parent_id if track.parent_id is not None else -1
            for cell in track.cells:
                z, y, x = cell.centroid
                rows.append(
                    {
                        "cell_id": cell.cell_id,
                        "frame": cell.frame_idx,
                        "z": round(z, 3),
                        "y": round(y, 3),
                        "x": round(x, 3),
                        "parent_id": parent_id,
                        "track_id": track.track_id,
                    }
                )

        if not rows:
            return pd.DataFrame(
                columns=["cell_id", "frame", "z", "y", "x", "parent_id", "track_id"]
            )

        df = pd.DataFrame(rows)
        return df.sort_values(by=["frame", "cell_id"]).reset_index(drop=True)

    @classmethod
    def save(cls, tracks: List[Track], output_path: str) -> str:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        df = cls.to_dataframe(tracks)
        df.to_csv(out_file, index=False)
        return str(out_file)
