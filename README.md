# CZ Biohub – Cell Tracking During Development

[![CI Test Suite](https://github.com/vaishnavi-ctrl-jpg/Biohub-Cell-Tracking-During-Development/actions/workflows/tests.yml/badge.svg)](https://github.com/vaishnavi-ctrl-jpg/Biohub-Cell-Tracking-During-Development/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-grade, modular, research-ready AI system for 3D+T microscopy cell tracking built for the **CZ Biohub - Cell Tracking During Development** Kaggle competition.

---

## 🏗 Architecture Overview

```mermaid
graph TD
    A[configs/baseline.yaml] --> B[cell_tracking/config/schema.py]
    B --> C[cell_tracking/core/pipeline.py - Pipeline]
    
    subgraph Readers & Datasets
        D[cell_tracking/readers/ Zarr/Synthetic] -->|ReaderFactory| E[cell_tracking/datasets/dataset.py]
        E -->|Frame Objects| C
    end
    
    subgraph Core Detection & Tracking
        C -->|DetectorFactory| F[cell_tracking/detectors/ ThresholdDetector]
        F -->|Geometry & Intensity Features| G[Cell Domain Objects]
        G -->|TrackerFactory| H[cell_tracking/trackers/ NearestNeighborTracker]
    end

    subgraph Metrics, Submission & Experiment Archiving
        H -->|Track Domain Objects| I[cell_tracking/metrics/ Detection & Tracking Metrics]
        H --> J[cell_tracking/submission/ Formatter & Validator]
        H --> K[cell_tracking/visualization/ GIF & Max Projection Exporter]
        I & J & K --> L[cell_tracking/experiments/ ExperimentManager MLFlow Lite]
        L --> M[runs/YYYY_MM_DD_HH_MM_SS/]
    end
```

---

## 🌟 Key Features

- **Clean Modular Architecture**: Clean separation of concerns following SOLID principles.
- **Config-Driven Development**: Type-safe Pydantic schemas validating YAML configurations at startup.
- **Installable Package**: Install locally via `pip install -e .` for clean cross-module imports.
- **Automated Experiment Archiving ("MLFlow Lite")**: Every run creates a timestamped run directory (`runs/YYYY_MM_DD_HH_MM_SS/`) containing config copies, metrics JSON, execution logs, submission CSV, preview GIF, and an HTML dashboard (`metrics.html`).
- **Hardened Kaggle Submission Validator**: Automated schema validation preventing malformed competition submission files.
- **Comprehensive Unit Testing & CI**: Full `pytest` test suite running automatically on GitHub Actions.

---

## 🗺 Version Roadmap

- **Version 1 (Current Baseline)**: Operational end-to-end baseline (Synthetic/Zarr reader -> Threshold Detector -> Nearest Neighbor Tracker -> Metrics & HTML Dashboard -> Submission Validator).
- **Version 2**: 3D spatial anisotropic resampling, 3D Distance Transform Watershed segmentation, morphology filtering.
- **Version 3**: 3D Anisotropic ResUNet deep learning cell detector (MONAI/PyTorch Lightning with mixed precision).
- **Version 4**: Learned cell appearance embeddings, Hungarian matching solver, division/mitosis classification head, frame-pair GNN tracker.
- **Version 5**: Global ILP / Min-Cost Max-Flow graph solver via HiGHS, dynamic density calibration, full lineage DAG reconstruction.
- **Version 6**: Multi-model ensemble, Test-Time Augmentation (TTA), multi-GPU parallel inference engine.

---

## ⚡ Quick Start

### 1. Installation

```bash
git clone https://github.com/vaishnavi-ctrl-jpg/Biohub-Cell-Tracking-During-Development.git
cd Biohub-Cell-Tracking-During-Development
pip install -e .[dev]
```

### 2. Run Version 1 Baseline Pipeline

```bash
python scripts/run_pipeline.py --config configs/baseline.yaml
```

or via Makefile:

```bash
make run
```

### 3. Run Automated Pytest Suite

```bash
make test
```

---

## 📊 Benchmark & Scorecard (Version 1)

| Stage | Latency | Status |
| :--- | :--- | :--- |
| **Data Ingestion** | 0.02s / volume | ✅ Verified |
| **3D Threshold Detection** | 0.04s / volume | ✅ Verified |
| **Nearest Neighbor Tracking** | 0.01s / volume | ✅ Verified |
| **Submission Validator** | 0.01s | ✅ Passed |
| **Total V1 End-to-End Pipeline** | ~0.15s | ✅ Passed |

---

## 📄 Documentation

- [Engineering Principles](docs/engineering_principles.md)
- [System Architecture](docs/architecture.md)
- [Version Roadmap](docs/roadmap.md)
- [ADR 0001: Lean V1 Baseline](docs/adr/0001-lean-v1-baseline.md)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
