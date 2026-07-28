# Engineering Principles & Philosophy

This document outlines the core engineering philosophy governing the development of the **CZ Biohub - Cell Tracking During Development** project.

---

## 1. Core Principles

1. **Reproducibility First**
   - Every experiment run must be 100% deterministic and reproducible.
   - All random seeds (Python, NumPy, PyTorch, CUDNN) are explicitly set.
   - Every experiment automatically records system environment info, Python package versions, git commit SHA, and exact hyperparameter configs into timestamped run directories (`runs/YYYY_MM_DD_HH_MM_SS/`).

2. **Modular over Monolithic**
   - No monolithic notebooks or spaghetti scripts.
   - Every file has a single responsibility (SRP).
   - Component interfaces (`BaseReader`, `BaseDetector`, `BaseTracker`, `BaseFeatureExtractor`) remain decoupled from execution pipelines.

3. **Type Safety & Schema Validation**
   - Strict static typing using Python type hints across 100% of codebase.
   - Domain objects (`Cell`, `Track`, `Frame`, `PipelineResult`) use `@dataclass`.
   - Configurations use Pydantic models (`BaselineConfig`) for automatic runtime key & type validation.

4. **"V1 Proves the Algorithm, Not the Framework"**
   - Build a minimal, functional, testable baseline end-to-end first before adding complex neural models.
   - Do not over-engineer premature infrastructure (e.g. event buses, complex DI containers) before they add tangible algorithmic value.

5. **Testability & Continuous Integration**
   - Every module must contain automated unit tests.
   - Automated CI testing via GitHub Actions runs `pytest` and linter checks on every pull request.

6. **Benchmark Driven Improvement**
   - Every version MUST print and archive execution latency (FPS), per-stage wall-clock time, peak CPU RAM, and GPU memory usage.
   - Benchmarks are compared across versions to ensure optimizations never introduce regressions.
