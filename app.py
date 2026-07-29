"""
Streamlit Web Application & Interactive 3D Microscopy Dashboard
CZ Biohub - Cell Tracking During Development
"""

import os
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from cell_tracking.config.schema import (
    BaselineConfig,
    DatasetConfig,
    DetectorConfig,
    TrackerConfig,
    EvaluationConfig,
    SubmissionConfig,
)
from cell_tracking.core.pipeline import Pipeline
from cell_tracking.visualization.preview_2d import render_max_projection

# Page configuration
st.set_page_config(
    page_title="CZ Biohub - Cell Tracking Workbench",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for dark mode UI
st.markdown(
    """
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.0rem; color: #94a3b8; margin-bottom: 1.5rem; }
    .metric-card { background-color: #1e293b; border-radius: 10px; padding: 15px; border: 1px solid #334155; text-align: center; }
    .metric-title { font-size: 0.85rem; color: #94a3b8; font-weight: 500; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #38bdf8; }
</style>
""",
    unsafe_allow_scope=True,
)

st.markdown('<div class="main-header">🔬 CZ Biohub — 3D+T Cell Tracking Workbench</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Interactive 3D Microscopy Cell Detection, Trajectory Tracking & Submission Portal</div>',
    unsafe_allow_html=True,
)

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Pipeline Configuration")

# Dataset Controls
st.sidebar.subheader("1. Dataset Options")
reader_type = st.sidebar.selectbox("Data Reader Type", ["synthetic", "zarr"], index=0)

if reader_type == "synthetic":
    num_frames = st.sidebar.slider("Number of Frames (T)", 3, 30, 10)
    num_cells = st.sidebar.slider("Number of Simulated Cells", 2, 20, 6)
    drift_scale = st.sidebar.slider("Cell Drift Velocity Scale", 0.5, 5.0, 2.5)
    data_path = "data/raw/synthetic"
else:
    data_path = st.sidebar.text_input("Zarr Dataset Path", "data/raw/cell_sequence.zarr")
    num_frames = 10
    num_cells = 5
    drift_scale = 2.0

# Detector Controls
st.sidebar.subheader("2. Cell Detector Settings")
threshold_val = st.sidebar.slider("Intensity Threshold", 0.1, 0.9, 0.35, step=0.05)
gaussian_sigma = st.sidebar.slider("3D Gaussian Smoothing (σ)", 0.0, 3.0, 1.0, step=0.5)
min_vol = st.sidebar.number_input("Min Cell Volume (voxels)", 1, 50, 5)

# Tracker Controls
st.sidebar.subheader("3. Temporal Tracker Settings")
max_linking_dist = st.sidebar.slider("Max Linking Distance (voxels)", 5.0, 50.0, 20.0, step=2.5)

run_button = st.sidebar.button("🚀 Run Pipeline", type="primary", use_container_width=True)

# Session State Cache for Pipeline Result
if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None
if "config" not in st.session_state:
    st.session_state["config"] = None

if run_button or st.session_state["pipeline_result"] is None:
    config = BaselineConfig(
        experiment_name="ui_workbench_run",
        dataset=DatasetConfig(
            reader_type=reader_type,
            path=data_path,
            num_frames=num_frames,
            num_cells=num_cells,
            drift_scale=drift_scale,
        ),
        detector=DetectorConfig(
            threshold_value=threshold_val,
            gaussian_sigma=gaussian_sigma,
            min_volume_voxels=min_vol,
        ),
        tracker=TrackerConfig(max_linking_distance=max_linking_dist),
    )

    with st.spinner("Processing 3D+T volumes, detecting cells, and building trajectories..."):
        pipeline = Pipeline(config)
        result = pipeline.run()

    st.session_state["pipeline_result"] = result
    st.session_state["config"] = config
    st.session_state["pipeline_obj"] = pipeline

result = st.session_state["pipeline_result"]
pipeline_obj = st.session_state.get("pipeline_obj")

# --- Key Metrics Header ---
col1, col2, col3, col4, col5 = st.columns(5)

det_metrics = result.metrics.get("detection", {})
tr_metrics = result.metrics.get("tracking", {})
bench_stats = result.metrics.get("benchmark", {})

with col1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Total Cells Detected</div><div class="metric-value">{result.total_cells_detected}</div></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Active Cell Tracks</div><div class="metric-value">{len(result.tracks)}</div></div>',
        unsafe_allow_html=True,
    )
with col3:
    f1 = det_metrics.get("f1_score", "N/A")
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Detection F1 Score</div><div class="metric-value">{f1}</div></div>',
        unsafe_allow_html=True,
    )
with col4:
    precision = det_metrics.get("precision", "N/A")
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Precision / Recall</div><div class="metric-value">{precision}</div></div>',
        unsafe_allow_html=True,
    )
with col5:
    runtime = bench_stats.get("total_time_sec", "N/A")
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Pipeline Runtime</div><div class="metric-value">{runtime}s</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- Main Workbench Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🌌 3D & 2D Microscopy Viewer",
    "📈 Trajectories & Analytics",
    "📑 Kaggle Submission Portal",
    "📋 Experiment Metrics & Logs",
])

# TAB 1: 3D/2D Microscopy Viewer
with tab1:
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("2D Max Intensity Projection (Per Frame)")
        selected_frame_idx = st.slider("Select Time Frame (T)", 0, len(pipeline_obj.dataset) - 1, 0)
        frame_data = pipeline_obj.dataset[selected_frame_idx]
        max_proj = render_max_projection(frame_data.data, axis=0)

        # Plot 2D projection with cell overlays
        fig_2d = px.imshow(
            max_proj,
            color_continuous_scale="Viridis",
            title=f"Time Frame {selected_frame_idx} (Max Z Projection)",
        )

        # Overlay detected centroids for this frame
        frame_cells = [
            c for track in result.tracks for c in track.cells if c.frame_idx == selected_frame_idx
        ]
        if frame_cells:
            xs = [c.centroid[2] for c in frame_cells]
            ys = [c.centroid[1] for c in frame_cells]
            tids = [f"Track {c.track_id}" for c in frame_cells]

            fig_2d.add_trace(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="markers+text",
                    marker=dict(size=12, color="red", symbol="circle-open", line=dict(width=2)),
                    text=tids,
                    textposition="top center",
                    name="Detected Cells",
                )
            )

        st.plotly_chart(fig_2d, use_container_width=True)

    with col_right:
        st.subheader("Interactive 3D Trajectory Graph")
        # Build 3D scatter plot of all cell centroids over time
        all_3d_points = []
        for track in result.tracks:
            for cell in track.cells:
                z, y, x = cell.centroid
                all_3d_points.append(
                    {
                        "X": x,
                        "Y": y,
                        "Z": z,
                        "Time": cell.frame_idx,
                        "Track ID": f"Track {track.track_id}",
                        "Volume": cell.volume_voxels,
                    }
                )

        if all_3d_points:
            df_3d = pd.DataFrame(all_3d_points)
            fig_3d = px.scatter_3d(
                df_3d,
                x="X",
                y="Y",
                z="Z",
                color="Track ID",
                size="Volume",
                hover_data=["Time", "Volume"],
                title="Full 3D Cell Trajectories Across Time",
            )
            fig_3d.update_layout(scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"))
            st.plotly_chart(fig_3d, use_container_width=True)

# TAB 2: Trajectories & Analytics
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Track Length Distribution")
        lengths = [tr.length for tr in result.tracks]
        df_len = pd.DataFrame({"Track Length (frames)": lengths})
        fig_hist = px.histogram(
            df_len, x="Track Length (frames)", nbins=10, color_discrete_sequence=["#38bdf8"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        st.subheader("Cell Count per Frame")
        counts_per_frame = [
            sum(1 for tr in result.tracks for c in tr.cells if c.frame_idx == t)
            for t in range(len(pipeline_obj.dataset))
        ]
        df_counts = pd.DataFrame(
            {"Time Frame": list(range(len(pipeline_obj.dataset))), "Cell Count": counts_per_frame}
        )
        fig_line = px.line(
            df_counts,
            x="Time Frame",
            y="Cell Count",
            markers=True,
            color_discrete_sequence=["#4ade80"],
        )
        st.plotly_chart(fig_line, use_container_width=True)

# TAB 3: Submission Export
with tab3:
    st.subheader("Kaggle Submission Export File")
    if os.path.exists(result.submission_path):
        df_sub = pd.read_csv(result.submission_path)
        st.dataframe(df_sub, use_container_width=True)

        with open(result.submission_path, "rb") as f:
            st.download_button(
                label="📥 Download Submission CSV",
                data=f,
                file_name="submission.csv",
                mime="text/csv",
                type="primary",
            )

# TAB 4: Metrics & Logs
with tab4:
    st.subheader("Run Metrics JSON")
    st.json(result.metrics)

    st.subheader("Generated Artifact File Paths")
    st.code(
        f"""
Run Directory  : {result.run_dir}
Submission CSV : {result.submission_path}
Preview GIF    : {result.preview_path}
Metrics HTML   : {result.dashboard_path}
""",
        language="yaml",
    )
