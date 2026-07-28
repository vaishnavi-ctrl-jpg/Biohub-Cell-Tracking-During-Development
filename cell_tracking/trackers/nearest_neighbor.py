"""
Nearest Neighbor temporal cell tracker using distance-capped bipartite matching.
"""

from typing import List, Dict, Any
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

from cell_tracking.domain.cell import Cell
from cell_tracking.domain.track import Track
from cell_tracking.trackers.base import BaseTracker, register_tracker


@register_tracker("nearest_neighbor")
class NearestNeighborTracker(BaseTracker):
    """Links frame-by-frame 3D cell centroids using Euclidean distance bipartite matching."""

    def __init__(
        self,
        max_linking_distance: float = 20.0,
        weight_distance: float = 1.0,
        **kwargs: Any,
    ):
        self.max_linking_distance = max_linking_distance
        self.weight_distance = weight_distance

    def track(self, detections_per_frame: List[List[Cell]]) -> List[Track]:
        if not detections_per_frame:
            return []

        active_tracks: Dict[int, Track] = {}
        next_track_id = 1
        all_completed_tracks: List[Track] = []

        # 1. Initialize tracks for frame 0
        frame_0_cells = detections_per_frame[0]
        active_cell_map: Dict[int, Cell] = {}  # track_id -> last_cell

        for cell in frame_0_cells:
            cell.track_id = next_track_id
            new_track = Track(track_id=next_track_id, cells=[cell])
            active_tracks[next_track_id] = new_track
            active_cell_map[next_track_id] = cell
            next_track_id += 1

        # 2. Iterate sequentially t = 1 ... T-1
        for t in range(1, len(detections_per_frame)):
            current_cells = detections_per_frame[t]
            if not current_cells:
                continue

            active_ids = list(active_cell_map.keys())
            if not active_ids:
                # If no active tracks, start all current cells as new tracks
                for cell in current_cells:
                    cell.track_id = next_track_id
                    new_track = Track(track_id=next_track_id, cells=[cell])
                    active_tracks[next_track_id] = new_track
                    active_cell_map[next_track_id] = cell
                    next_track_id += 1
                continue

            prev_centroids = np.array([active_cell_map[tid].centroid for tid in active_ids])
            curr_centroids = np.array([c.centroid for c in current_cells])

            # Compute Euclidean distance cost matrix
            cost_matrix = cdist(prev_centroids, curr_centroids, metric="euclidean")

            # Bipartite matching via Hungarian algorithm
            row_ind, col_ind = linear_sum_assignment(cost_matrix)

            matched_prev = set()
            matched_curr = set()

            for r, c in zip(row_ind, col_ind):
                dist = cost_matrix[r, c]
                if dist <= self.max_linking_distance:
                    prev_tid = active_ids[r]
                    curr_cell = current_cells[c]

                    # Assign track ID
                    curr_cell.track_id = prev_tid
                    active_tracks[prev_tid].cells.append(curr_cell)
                    active_cell_map[prev_tid] = curr_cell

                    matched_prev.add(r)
                    matched_curr.add(c)

            # Unmatched active tracks are terminated
            for r, tid in enumerate(active_ids):
                if r not in matched_prev:
                    all_completed_tracks.append(active_tracks[tid])
                    del active_tracks[tid]
                    del active_cell_map[tid]

            # Unmatched current cells start new tracks
            for c, cell in enumerate(current_cells):
                if c not in matched_curr:
                    cell.track_id = next_track_id
                    new_track = Track(track_id=next_track_id, cells=[cell])
                    active_tracks[next_track_id] = new_track
                    active_cell_map[next_track_id] = cell
                    next_track_id += 1

        # Add remaining active tracks
        all_completed_tracks.extend(active_tracks.values())
        all_completed_tracks.sort(key=lambda tr: tr.track_id)

        return all_completed_tracks
