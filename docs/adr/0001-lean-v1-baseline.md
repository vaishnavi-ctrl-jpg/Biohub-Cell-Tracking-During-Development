# ADR 0001: Lean Version 1 Baseline Architecture

## Status
Approved

## Context
In building a research-grade, production-quality solution for the **CZ Biohub - Cell Tracking During Development** Kaggle competition, we required an early integration baseline to validate data schemas, IO pipelines, evaluation metrics, submission formatting, and test coverage before introducing deep learning models.

## Decision
We decided to adopt a **Lean Version 1 Baseline** architecture:
1. **Core Package (`cell_tracking`)**: Fully modular, type-hinted Python package with `Pydantic` configuration validation.
2. **Algorithm Implementation**: Classical 3D thresholding + connected components detection + Nearest-Neighbor distance-capped tracking.
3. **No Over-Engineering in V1**: We explicitly delayed complex event buses, dependency injection containers, and multi-layered service abstractions until V4+, focusing V1 on validating the core end-to-end algorithmic flow (`Reader -> Dataset -> Detector -> Tracker -> Evaluator -> Submission`).
4. **Experiment Archiving**: Built a lightweight, local `ExperimentManager` that archives timestamped runs into `runs/YYYY_MM_DD_HH_MM_SS/` containing config, metrics JSON, submission CSV, preview GIF, and HTML dashboard.

## Consequences
- **Positive**: Complete baseline pipeline runs in seconds; 100% test coverage can be maintained from Day 1; zero premature framework complexity.
- **Positive**: Clean interfaces (`BaseReader`, `BaseDetector`, `BaseTracker`) allow plug-and-play addition of 3D ResUNet and GNN models in V3–V5 without refactoring core pipelines.
