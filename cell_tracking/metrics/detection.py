"""
Detection quality metrics evaluation.
"""

from typing import List, Tuple, Dict, Any
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from cell_tracking.domain.cell import Cell


def evaluate_detection(
    detected_cells: List[Cell],
    gt_centroids: List[Tuple[float, float, float]],
    match_threshold: float = 10.0,
) -> Dict[str, Any]:
    """Computes Detection Precision, Recall, F1 score, and mean spatial error."""
    if not gt_centroids and not detected_cells:
        return {"precision": 1.0, "recall": 1.0, "f1_score": 1.0, "tp": 0, "fp": 0, "fn": 0}
    if not detected_cells:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0, "tp": 0, "fp": 0, "fn": len(gt_centroids)}
    if not gt_centroids:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0, "tp": 0, "fp": len(detected_cells), "fn": 0}

    pred_arr = np.array([c.centroid for c in detected_cells])
    gt_arr = np.array(gt_centroids)

    cost_matrix = cdist(gt_arr, pred_arr)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    tp = 0
    errors = []
    for r, c in zip(row_ind, col_ind):
        dist = cost_matrix[r, c]
        if dist <= match_threshold:
            tp += 1
            errors.append(dist)

    fp = len(detected_cells) - tp
    fn = len(gt_centroids) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    mean_err = float(np.mean(errors)) if errors else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "mean_centroid_error": round(mean_err, 4),
    }
