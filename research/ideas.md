# Research Ideas & Hypothesis Backlog

- **Hypothesis 1**: Anisotropic 3D Gaussian pre-smoothing matched to physical voxel spacing ($\Delta z \neq \Delta x = \Delta y$) will reduce false positive nucleus detections by >15%.
- **Hypothesis 2**: Combining 3D Euclidean Distance Transform with Marker-Controlled Watershed (V2) will resolve overlapping nuclei in dense early embryo developmental stages.
- **Hypothesis 3**: 3D ResUNet trained with combined Dice + Focal loss (V3) will outperform classical thresholding by >20% F1-score on weak signal cell boundaries.
- **Hypothesis 4**: Graph Neural Network edge classification (V4) combining cell geometric distance and deep appearance embeddings will eliminate >80% of ID switches.
- **Hypothesis 5**: Formulating temporal cell trajectory linking as a global Min-Cost Max-Flow / ILP optimization problem solved via HiGHS (V5) will enforce global topological lineage DAG constraints.
