"""
HTML Metrics Dashboard generator for experiment run inspection.
"""

from pathlib import Path
from typing import Dict, Any


class DashboardGenerator:
    """Renders HTML metrics dashboard file (metrics.html)."""

    @staticmethod
    def generate_html(metrics_dict: Dict[str, Any], output_path: str) -> str:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Biohub Cell Tracking - Run Dashboard</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 20px; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 10px; }}
        .card {{ background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .metric-item {{ background: #0f172a; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #334155; }}
        .metric-val {{ font-size: 24px; font-weight: bold; color: #4ade80; margin-top: 5px; }}
        .metric-label {{ font-size: 14px; color: #94a3b8; }}
        img {{ max-width: 100%; border-radius: 8px; border: 1px solid #334155; }}
    </style>
</head>
<body>
    <h1>CZ Biohub Cell Tracking — Version 1 Dashboard</h1>
    
    <div class="card">
        <h2>Run Summary & Metrics</h2>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-label">Detection F1-Score</div>
                <div class="metric-val">{metrics_dict.get('detection', {}).get('f1_score', 'N/A')}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Precision / Recall</div>
                <div class="metric-val">{metrics_dict.get('detection', {}).get('precision', 0)} / {metrics_dict.get('detection', {}).get('recall', 0)}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Total Tracks Created</div>
                <div class="metric-val">{metrics_dict.get('tracking', {}).get('num_tracks', 'N/A')}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Mean Track Length</div>
                <div class="metric-val">{metrics_dict.get('tracking', {}).get('mean_track_length', 'N/A')} frames</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Total Execution Time</div>
                <div class="metric-val">{metrics_dict.get('benchmark', {}).get('total_time_sec', 'N/A')}s</div>
            </div>
        </div>
    </div>

    <div class="card">
        <h2>Trajectory Visualization Preview</h2>
        <p>Preview of 3D cell tracks over time:</p>
        <img src="preview.gif" alt="Cell Tracks Preview GIF">
    </div>
</body>
</html>
"""
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(out_file)
