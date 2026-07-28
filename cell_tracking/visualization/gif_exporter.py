"""
Animated GIF exporter for cell track trajectory preview.
"""

from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from PIL import Image, ImageDraw

from cell_tracking.datasets.dataset import CellDataset
from cell_tracking.domain.track import Track
from cell_tracking.visualization.preview_2d import render_max_projection


class GifExporter:
    """Exports animated preview GIF showing cell tracks over time."""

    @staticmethod
    def export_gif(
        dataset: CellDataset,
        tracks: List[Track],
        output_path: str,
        fps: int = 4,
    ) -> str:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        # Build map: (frame_idx) -> List[(x, y, track_id)]
        tracks_per_frame: Dict[int, List[Tuple[float, float, int]]] = {}
        for track in tracks:
            for cell in track.cells:
                f_idx = cell.frame_idx
                if f_idx not in tracks_per_frame:
                    tracks_per_frame[f_idx] = []
                _, y, x = cell.centroid
                tracks_per_frame[f_idx].append((x, y, track.track_id))

        images: List[Image.Image] = []
        colors = [
            (255, 50, 50),
            (50, 255, 50),
            (50, 50, 255),
            (255, 255, 50),
            (255, 50, 255),
            (50, 255, 255),
            (255, 150, 50),
        ]

        for frame in dataset:
            proj = render_max_projection(frame.data, axis=0)
            # Normalize 0-255
            p_min, p_max = proj.min(), proj.max()
            if p_max > p_min:
                norm_proj = ((proj - p_min) / (p_max - p_min) * 255.0).astype(np.uint8)
            else:
                norm_proj = (proj * 255.0).clip(0, 255).astype(np.uint8)

            img_rgb = Image.fromarray(norm_proj).convert("RGB")
            draw = ImageDraw.Draw(img_rgb)

            # Draw centroids and track labels
            if frame.frame_idx in tracks_per_frame:
                for x, y, tid in tracks_per_frame[frame.frame_idx]:
                    color = colors[tid % len(colors)]
                    r = 3
                    draw.ellipse([x - r, y - r, x + r, y + r], outline=color, width=2)
                    draw.text((x + 4, y - 4), f"T{tid}", fill=color)

            images.append(img_rgb)

        if images:
            images[0].save(
                out_file,
                save_all=True,
                append_images=images[1:],
                duration=int(1000 / fps),
                loop=0,
            )

        return str(out_file)
