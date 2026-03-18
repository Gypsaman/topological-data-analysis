# TDA Algorithms and Software

## Overview

This document covers the computational algorithms underlying TDA, their complexity, and the software ecosystem. Understanding which tool to use — and why — is essential for practical TDA work.

---

## 1. Persistence Algorithms

### 1.1 Standard Algorithm (Edelsbrunner–Letscher–Zomorodian 2002)

The foundational algorithm for computing persistent homology via **left-to-right column reduction** of the boundary matrix.

**Setup:**
- Order all $m$ simplices: $\sigma_1, \ldots, \sigma_m$ (consistent with filtration)
- Build boundary matrix $D$: $D[i,j] = 1$ iff $\sigma_i$ is a codimension-1 face of $\sigma_j$
- Work over $\mathbb{Z}/2\mathbb{Z}$ (field with 2 elements) for speed; $\mathbb{Z}/p\mathbb{Z}$ or $\mathbb{Q}$ for richer information

**Algorithm:**
```
R = D   (copy of boundary matrix)
V = I   (identity matrix)
for j = 1 to m:
    while low(R, j) = low(R, j') for some j' < j:
        R[:, j] += R[:, j']
        V[:, j] += V[:, j']
end for
```

**Reading results:** Column $j$ of reduced $R$ with pivot $i = \text{low}(j)$ gives persistence pair $(\sigma_i, \sigma_j)$.

**Complexity:** $O(m^3)$ worst case (tight); practically much faster due to sparsity.

### 1.2 Twist / Clearing Algorithm (Chen & Kerber, 2011)

**Key insight:** The boundary of a boundary is zero ($\partial^2 = 0$). If simplex $\sigma_j$ is **born** (creates a cycle in some dimension $k$), then all faces of $\sigma_j$ in dimension $k-1$ are automatically boundaries — their corresponding columns in the boundary matrix can be **cleared** without reduction.

**Algorithm:** Process dimensions from highest to lowest. After identifying persistence pairs in dimension $k$, zero out the paired columns in dimension $k-1$ before processing that dimension.

**Effect:** Reduces the number of columns requiring explicit reduction, yielding major speedups in practice. This is the basis of the clearing optimization in Ripser.

### 1.3 Apparent and Emergent Pairs (Bauer, 2021 — Ripser)

Ripser's key innovation: identifying **apparent pairs** that can be resolved without any matrix operations.

- **Apparent pair:** A simplex $\sigma$ of dimension $k+1$ and its lowest-index facet $\tau$ of dimension $k$ form an apparent pair if $\tau$ is also the lowest facet of $\sigma$ under the coboundary ordering. These constitute $\sim$99% of all persistence pairs and are entirely free to compute.
- **Emergent pair:** Identified via the column structure without explicit reduction.

Combined with cohomological computation (working with the transpose matrix), Ripser achieves state-of-the-art performance.

### 1.4 Chunk Algorithm (Bauer, Kerber, Reininghaus, 2013)

A **parallel-friendly** approach that divides the boundary matrix into chunks and processes each chunk locally before combining:
1. Split the filtered complex into consecutive chunks
2. Compute local persistence pairs within each chunk
3. Compress/eliminate locally paired simplices
4. Reduce the remaining global boundary matrix

Enables multi-core computation. The PHAT library implements this and other algorithms with swappable matrix representations.

### 1.5 Discrete Morse Theory Approach (Mischaikow & Nanda, 2013 — Perseus)

Based on **Forman's discrete Morse theory** (1998): a discrete gradient vector field on a simplicial complex pairs simplices, collapsing the complex to a smaller **Morse complex** with the same homology.

1. Construct a discrete gradient on the filtered complex (acyclic matching of pairs $(\sigma^k, \tau^{k+1})$)
2. Collapse paired cells — can reduce complex size by orders of magnitude
3. Run standard reduction on the small Morse complex

Most effective on cubical complexes (image data) and regularly structured inputs.

### 1.6 Zigzag Persistence (Carlsson & de Silva, 2010)

For non-monotone sequences $K_0 \leftrightarrow K_1 \leftrightarrow K_2 \leftrightarrow \cdots$, where arrows can go backward (deletions). By Gabriel's theorem for $A_n$ quivers, zigzag persistence modules still decompose into interval modules.

**Algorithm:** Each insertion/deletion induces a matrix update, maintaining the barcode dynamically. Cost: $O(m^2)$ per update in the worst case.

**Applications:** Moving point clouds, bootstrapping for statistical inference, level-set persistence.

---

## 2. Multidimensional Persistence

For filtrations over $\mathbb{R}^n$ ($n \geq 2$) — e.g., filtering by both density AND scale simultaneously.

**Core problem (Carlsson & Zomorodian, 2009):** There is **no complete discrete invariant** for 2-parameter persistence modules analogous to barcodes. The module structure over a multivariate polynomial ring is of "wild" representation type — infinitely many indecomposable types, no finite classification.

**Current practical approaches:**

| Invariant | Completeness | Computability | Software |
|-----------|-------------|---------------|---------|
| Rank invariant / Hilbert function | Incomplete | Polynomial | RIVET |
| Bigraded Betti numbers | Incomplete | Polynomial | RIVET |
| Fibered barcode (1D slices) | Incomplete | Polynomial | RIVET |
| Signed barcodes (Botnan et al., 2024) | Richer | Research stage | — |
| Interval approximations | Approximate | Polynomial | — |

**RIVET** (Lesnick & Wright, 2015–present): Software for interactive 2-parameter persistence visualization. Computes persistence over all linear 1D slices through the 2D parameter space.

---

## 3. Computational Complexity and Scalability

### 3.1 Complexity Analysis

| Task | Complexity | Notes |
|------|-----------|-------|
| Standard reduction | $O(m^3)$ | $m$ = number of simplices; rarely achieved |
| Ripser (Rips, with optimizations) | $\sim O(m^{1.5})$ practical | Much faster in practice |
| Alpha complex construction | $O(n \log n)$ ($d \leq 3$) | $n$ = number of points |
| Rips complex size (dim $k$, $n$ pts) | $O(n^{k+1})$ | Exponential in $k$ |

### 3.2 Memory Constraints

For $n$ points in a Rips filtration:
- **Distance matrix:** $O(n^2)$. At $n = 10,000$ with float64: ~800 MB
- **Number of simplices (dim 2):** $O(n^3/6)$. At $n = 1,000$: ~167 million triangles

Ripser avoids storing the full boundary matrix by recomputing columns on demand, enabling much larger inputs.

**Practical limits (dense Euclidean data):**
- Ripser: $n \sim 5,000$–$10,000$ for $H_1/H_2$
- Alpha complex (low $d$): $n \sim 100,000+$
- Cubical complexes (images): limited by image size (typically feasible)

### 3.3 Scalability Solutions

| Challenge | Solution | Tool |
|-----------|----------|------|
| Exponential Rips complex | Dimension cutoff + Sparse Rips | Ripser.py |
| Large distance matrix | Sparse input format, greedy subsampling | Ripser, GUDHI |
| High ambient dimension | Witness complex (landmark-based) | JavaPlex, GUDHI |
| Large inputs | Edge collapse preprocessing | GUDHI |
| Sequential bottleneck | Parallel chunk algorithm | PHAT, giotto-ph |
| Single-core performance | GPU acceleration | Ripser++ |

**Sparse Rips approximation (Sheehy 2012; Cavanna et al. 2015):** Constructs a filtered complex with $O(n \cdot \varepsilon^{-O(d)})$ simplices that gives a $(1+\varepsilon)$-approximation to the full Rips barcode in bottleneck distance.

---

## 4. The Mapper Algorithm

### 4.1 Overview

Mapper (Singh, Mémoli, Carlsson — 2007) builds a topological graph summarizing the *shape* of high-dimensional data, providing an interpretable, visual summary distinct from persistence diagrams.

**Mathematical basis:** Mapper approximates the **Reeb graph** — the quotient of a space $X$ by connected components of levelsets of a function $f: X \to \mathbb{R}$.

### 4.2 Construction

Given a point cloud $P$ and a **filter/lens function** $f: P \to Z$:

**Step 1 — Choose filter $f$:**
Common choices:
- First PCA component (captures geometric spread)
- Density estimate (highlights dense vs. sparse regions)
- $L^\infty$-eccentricity (distance from centroid)
- Domain-specific score (e.g., survival time in genomics)

**Step 2 — Cover the codomain:**
Choose a cover $\mathcal{U} = \{U_\alpha\}$ of the image $f(P)$ by overlapping intervals (1D) or rectangles (2D).

Parameters:
- **Resolution** (number of intervals): controls coarseness
- **Gain/overlap** (typically 20–50%): controls connectivity

**Step 3 — Cluster each preimage:**
For each $U_\alpha$, cluster the data $f^{-1}(U_\alpha)$ using a standard algorithm (single-linkage, DBSCAN, etc.). Each cluster becomes a node.

**Step 4 — Build the nerve:**
Add an edge between two nodes if their clusters share at least one data point. Build higher simplices for mutual intersections.

**Step 5 — Visualize/analyze the output graph.**

### 4.3 Reading Mapper Output

| Topological feature | Data interpretation |
|--------------------|---------------------|
| Loops/cycles | Circular processes, periodicity |
| Flares/tendrils | Extreme subgroups, outliers |
| Branching points | Distinct subpopulations diverging from a common structure |
| Isolated components | Disconnected subgroups |

Node size/color can be mapped to density, class label, outcome variable, etc.

### 4.4 Stability

Mapper outputs are stable under perturbations of the filter function and data (formal stability results exist under technical conditions). In practice, sensitivity analysis over parameter choices is always recommended.

---

## 5. Software Ecosystem

### 5.1 Ripser

**Use for:** Fastest Vietoris-Rips persistent homology for point clouds / distance matrices.

- **Author:** Ulrich Bauer (TU Munich)
- **Language:** ~1,000 lines C++11; Python bindings via `ripser.py`
- **Algorithm:** Persistent cohomology + clearing + apparent/emergent pairs
- **Filtrations:** Vietoris-Rips (primary); lower-star for images (extension)
- **Coefficients:** $\mathbb{Z}/2$ (default); $\mathbb{Z}/p$ via compile flag
- **Performance:** ~40× faster and 15× more memory-efficient than prior tools (Dionysus, GUDHI, PHAT) on standard benchmarks
- **License:** MIT
- **Limitations:** Only Rips filtrations; no zigzag; memory limits for large $n$

```python
import ripser
import numpy as np

X = np.random.rand(100, 3)
result = ripser.ripser(X, maxdim=2)
diagrams = result['dgms']
```

**Paper:** Bauer, U. *Ripser: efficient computation of Vietoris–Rips persistence barcodes.* J. Applied and Computational Topology, 2021.

---

### 5.2 GUDHI

**Use for:** Comprehensive TDA library — multiple filtration types, statistical tools, ML integration.

- **Developers:** INRIA (Chazal, Rouvreau, Maria, et al.)
- **Language:** C++ core; Python + scikit-learn + TensorFlow bindings
- **Filtrations:** VR, Sparse Rips, Alpha complex, Čech, Cubical, Weighted Rips, Tangential, Cover/Mapper
- **Distances:** Bottleneck, Wasserstein (with barycenter computation)
- **Vectorizations:** Persistence landscapes, images, Betti curves, heat kernels, silhouettes
- **Statistical tools:** Confidence bands, bootstrap
- **Differentiable PH:** TensorFlow lower-star layers (for topological optimization)
- **Edge collapse:** Preprocessing to reduce flag filtration size
- **License:** MIT/GPL
- **URL:** https://gudhi.inria.fr

```python
import gudhi
import numpy as np

X = np.random.rand(50, 2)
rips = gudhi.RipsComplex(points=X, max_edge_length=2.0)
simplex_tree = rips.create_simplex_tree(max_dimension=2)
simplex_tree.compute_persistence()
diag = simplex_tree.persistence()
```

---

### 5.3 giotto-tda

**Use for:** Full TDA pipeline in Python with scikit-learn compatibility.

- **Developers:** L2F SA / Giotto-AI
- **Language:** Python with C++ backends; strictly scikit-learn API
- **Homology:** `VietorisRipsPersistence`, `WeightedRipsPersistence`, `WeakAlphaPersistence`, `CubicalPersistence`, `FlagserPersistence` (directed graphs)
- **Diagrams:** Persistence landscapes, images, Betti curves, heat kernels, amplitudes, entropy features
- **Time series:** Takens/sliding window embedding, stationarity testing
- **Mapper:** Full pipeline with interactive Plotly visualization
- **Parallel:** `giotto-ph` backend for multicore computation
- **License:** GNU AGPL v3
- **URL:** https://giotto-ai.github.io/gtda-docs/

```python
from gtda.homology import VietorisRipsPersistence
from gtda.diagrams import PersistenceImage
import numpy as np

X = np.random.rand(10, 50, 3)  # 10 point clouds, 50 points, 3D
VR = VietorisRipsPersistence(homology_dimensions=[0, 1, 2])
diagrams = VR.fit_transform(X)
PI = PersistenceImage()
images = PI.fit_transform(diagrams)
```

---

### 5.4 Dionysus 2

**Use for:** Zigzag persistence, vineyard updates, research flexibility.

- **Author:** Dmitriy Morozov (Lawrence Berkeley Lab)
- **Language:** C++ with Python bindings
- **Key features:**
  - Full zigzag persistence support
  - Vineyard algorithm (dynamic persistence as filtration values change)
  - Gradient computation for topological optimization
- **URL:** https://mrzv.org/software/dionysus2/

---

### 5.5 PHAT

**Use for:** Algorithmic research and benchmarking; custom algorithm selection.

- **Authors:** Bauer, Kerber, Reininghaus, Wagner
- **Language:** C++ header-only; Python bindings
- **Algorithms:** Standard, Row, Twist (default), Chunk, Spectral sequence
- **Matrix representations:** 8 options (vector_vector, bit_tree_pivot_column, heap, etc.)
- **Input:** User-provided boundary matrix (field $\mathbb{Z}/2$)
- **Key limitation:** Only $\mathbb{Z}/2$; no filtration construction built-in
- **Paper:** Bauer et al. *PHAT – Persistent Homology Algorithms Toolbox.* ICMS 2014.

---

### 5.6 Ripser++ (GPU)

**Use for:** GPU-accelerated Rips persistence.

- **Authors:** Zhang, Xiao, Wang
- **Key innovation:** Apparent pairs (~99% of all pairs) are embarrassingly parallel on GPU; reduces CPU memory by 2×; up to 30× speedup over Ripser
- **Paper:** Zhang et al. *GPU-Accelerated Computation of Vietoris-Rips Persistence Barcodes.* SoCG 2020.

---

### 5.7 Cubical Ripser

**Use for:** Persistent homology of image/volume data (cubical complexes).

- **Authors:** Kaji, Sudo, Ahara
- **Algorithm:** Lower-star filtration on cubical complexes
- **Inputs:** 2D images, 3D volumes, time series (as 1D cubical complexes)
- **Performance:** Currently fastest and most memory-efficient for cubical PH
- **URL:** https://github.com/shizuo-kaji/CubicalRipser_3dim
- **Paper:** Kaji et al. arXiv:2005.12692, 2020.

---

### 5.8 RIVET

**Use for:** 2-parameter persistent homology visualization and computation.

- **Authors:** Lesnick, Wright (and contributors)
- **Computes:** Fibered barcodes (persistence over all linear 1D projections), Hilbert function, bigraded Betti numbers
- **Visualization:** Interactive GUI for exploring the 2-parameter persistence landscape
- **URL:** https://github.com/rivetTDA/rivet

---

### 5.9 KeplerMapper

**Use for:** Mapper algorithm with rich visualization.

- **Language:** Python; part of scikit-tda ecosystem
- **Features:** Many filter functions, customizable covers, pluggable clustering, interactive HTML visualization
- **URL:** https://kepler-mapper.scikit-tda.org

---

### 5.10 TDA (R Package)

**Use for:** Statistical inference on persistence diagrams; R integration.

- **Authors:** Fasy, Kim, Lecci, Maria, Millman, Rouvreau
- **Backend:** Wraps GUDHI, Dionysus, PHAT via Rcpp
- **Statistical methods:** Confidence bands, bootstrap, kernel density estimation, distance-to-measure
- **License:** GPL-3
- **Paper:** Fasy et al. arXiv:1411.1830, 2014.

---

### 5.11 Oineus

**Use for:** Lock-free parallel PH + differentiable TDA (PyTorch integration).

- **Authors:** Morozov, Nigmetov (Lawrence Berkeley Lab)
- **Key features:** Lock-free shared-memory parallel reduction; image/kernel/cokernel persistence; differentiable filtrations for topological optimization in PyTorch
- **URL:** https://github.com/anigmetov/oineus
- **Papers:** Morozov & Nigmetov, SPAA 2020; Nigmetov & Morozov, 2022.

---

### 5.12 JavaPlex

**Use for:** Education, MATLAB integration, zigzag and cohomology research.

- **Authors:** Stanford Computational Topology group
- **Language:** Java; MATLAB interface
- **Features:** PH/cohomology over $\mathbb{Z}/p$ and $\mathbb{Q}$, zigzag, witness complexes, incremental algorithms
- **URL:** https://appliedtopology.github.io/javaplex/

---

## 6. Tool Selection Guide

| Use case | Best tool |
|----------|-----------|
| Fastest Rips PH (point cloud) | Ripser / Ripser.py |
| GPU-accelerated Rips | Ripser++ |
| Multicore parallel Rips | giotto-ph (5+ cores beats GPU) |
| Image / volume (cubical) PH | Cubical Ripser or GUDHI cubical |
| Alpha complex (Euclidean) | GUDHI |
| Full scikit-learn TDA pipeline | giotto-tda |
| Statistical inference (R) | TDA R package |
| Zigzag persistence | Dionysus 2 or JavaPlex |
| 2-parameter persistence | RIVET |
| Mapper algorithm | KeplerMapper / giotto-tda |
| Algorithm comparison / research | PHAT |
| Topological optimization (ML) | Oineus |
| Education / MATLAB | JavaPlex |

---

## 7. Benchmarking Reference

**"A Roadmap for the Computation of Persistent Homology"** (Otter, Porter, Tillmann, Grindrod, Harrington — EPJ Data Science, 2017; arXiv:1506.08903) systematically benchmarks all major TDA software tools across multiple dataset types. Essential reading before choosing a tool for a new application.

---

*Previous: [02_persistent_homology.md](02_persistent_homology.md) | Next: [04_applications.md](04_applications.md)*
