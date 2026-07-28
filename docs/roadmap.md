# Project Version Roadmap (V1 – V6)

## Version 1: Operational Baseline (Completed)
- Clean modular package architecture (`cell_tracking`).
- Type-safe Pydantic configuration (`configs/baseline.yaml`).
- Synthetic 3D+T movie reader & chunked Zarr reader.
- 3D intensity threshold detector + Connected Component candidate object extraction.
- Geometric & intensity feature computation.
- Nearest-neighbor temporal tracking with distance cutoffs.
- Offline metrics evaluation (Detection F1, Precision, Recall, Track Length stats).
- Automated submission generation & Kaggle schema validator.
- Animated GIF preview exporter & HTML dashboard (`metrics.html`).
- Self-contained local Experiment Manager ("MLFlow Lite").
- Complete Pytest suite & CI runner.

## Version 2: Advanced Classical Detection & Preprocessing
- 3D spatial anisotropic voxel resampling ($z$-axis alignment to $x$-$y$).
- 3D Euclidean Distance Transform Watershed segmentation.
- 3D morphology filters (rolling ball background subtraction, top-hat filter).
- Advanced morphological & texture feature extractors.

## Version 3: Deep Learning Cell Detector
- 3D Anisotropic ResUNet / MONAI SwinUNETR segmentation backbone.
- PyTorch Lightning training loop with mixed-precision (FP16/BF16).
- Focal / Dice loss combination for imbalanced cell segmentation.
- Automated model checkpointing & validation loss monitoring.

## Version 4: Deep Tracking & Feature Embeddings
- Spatial-temporal cell appearance feature embeddings.
- Cost matrix matching incorporating appearance similarity + motion model prediction.
- Cell division / mitosis event classification head.
- Frame-pair Graph Neural Network (GNN) tracker.

## Version 5: Global Graph Optimization
- Global Integer Linear Programming (ILP) / Min-Cost Max-Flow graph solver via HiGHS.
- Multi-frame temporal window global trajectory optimization.
- Dynamic cell density calibration & mitosis tree DAG reconstruction.

## Version 6: Competition Ensemble & Production Pipeline
- Multi-model ensemble (3D ResUNet + Watershed + Cellpose wrappers).
- Test-Time Augmentation (TTA) for 3D volumes.
- Parallel multi-GPU streaming inference engine.
- Final submission optimizer.
