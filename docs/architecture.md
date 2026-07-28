# Technical System Architecture

## Architecture Diagram

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

## Modular Layer Breakdown

1. **`cell_tracking/domain/`**: Immutable schema definitions (`Cell`, `Track`, `Frame`, `PipelineResult`).
2. **`cell_tracking/readers/`**: Extensible multi-modal IO readers (`ZarrReader`, `SyntheticReader`).
3. **`cell_tracking/detectors/`**: 3D cell detection algorithms (`ThresholdDetector`).
4. **`cell_tracking/trackers/`**: Temporal cell association engines (`NearestNeighborTracker`).
5. **`cell_tracking/features/`**: Candidate object feature extractors (`GeometryExtractor`, `IntensityExtractor`).
6. **`cell_tracking/metrics/`**: Evaluation metrics and HTML dashboard generator (`DashboardGenerator`).
7. **`cell_tracking/submission/`**: Submission formatting and schema validation (`SubmissionValidator`).
8. **`cell_tracking/experiments/`**: Local experiment tracking and artifact archiving (`ExperimentManager`).
