# TDA Applications Across Scientific Domains

## Overview

TDA has found applications across an unusually broad range of scientific domains. In each case, topological features reveal structure that traditional methods (pairwise statistics, clustering, Fourier analysis) cannot detect. This document surveys landmark applications organized by domain.

**Why TDA detects what other methods miss:**

| Standard method | What it misses | What TDA reveals |
|----------------|----------------|-----------------|
| Pairwise correlation / pair distribution functions | Higher-order structural motifs | Triangles, rings, voids |
| k-means / hierarchical clustering | Thin bridges, geometric separation | Topological subgroups (Mapper flares) |
| Fourier transform / autocorrelation | Non-stationary, transient periodicity | Quantitative loop structure (H1) |
| Graph modularity | Persistent cycles across scales | Multi-scale loop structure |
| Landmark-based shape analysis | Requires correspondence | Coordinate-free, alignment-free |
| Order parameter curves | Requires prior knowledge | Topology-derived order parameters |

---

## 1. Biology and Medicine

### 1.1 Cancer Genomics — The Landmark Study

**Nicolau, M., Levine, A.J., Carlsson, G.** "Topology based data analysis identifies a subgroup of breast cancers with a unique mutational profile and excellent survival." *PNAS*, 108(17):7265–7270, 2011.

**Method:** Mapper algorithm applied to gene expression microarray data from 295 breast tumors. Filter functions: Disease-Specific Genomic Analysis (DSGA) residuals projected onto first SVD component.

**Discovery:** A previously undetected **flare** (topological branch) in the Mapper graph corresponded to a c-MYB-overexpressing, ER+ subgroup with **100% survival and zero metastatic events** across the cohort — completely invisible to hierarchical clustering, which requires dense local clusters.

**Key insight:** The subgroup was geometrically separated from the main tumor mass (requiring global topology to detect) but not forming its own dense cluster (making local methods blind to it). This is the canonical TDA proof-of-concept paper.

---

### 1.2 Brain Connectivity and Neuroscience

**Giusti, C., Pastalkova, E., Curto, C., Itskov, V.** "Clique topology reveals intrinsic geometric structure in neural correlations." *PNAS*, 112(44):13455–13460, 2015.

**Method:** Computed Betti numbers $\beta_1$, $\beta_2$ of clique complexes built from pairwise correlation matrices of hippocampal CA1 neurons in freely behaving rats.

**Discovery:** Real neural data showed **dramatically more topological complexity** than random controls — specifically, Betti number scaling consistent with activity living on a **torus** (product of two circular spaces encoding position and head direction). Detected purely from the topology of correlations, without assuming any spatial model.

**Follow-up applications:**
- Alzheimer's disease: Fewer 1-cycles and 2-cycles in functional connectivity vs. healthy controls; regions align with known AD signatures (hippocampus, precuneus)
- Schizophrenia: Different Betti curve profiles in frontal-temporal axis (Stolz et al., 2021)
- Brain networks have hyperbolic geometric character detectable via Betti curves (Caputi et al., 2024)

---

### 1.3 Protein Structure and Drug Discovery

**Wei group (Michigan State):** Element-specific persistent homology (ESPH) — separate Vietoris-Rips filtrations for each pair of atomic species (C-C, C-N, C-O, ...) in a molecule.

**Cang, Z., Wei, G.-W.** "TopologyNet: Topology based deep convolutional and multi-task neural networks for biomolecular property predictions." *PLOS Computational Biology*, 2017.

**Key results:**
- ESPH-based features achieved **state-of-the-art on CASF protein-ligand binding affinity benchmark**, outperforming fingerprint-based and 3D CNN methods
- Multi-scale: encodes covalent bonding topology (short-persistence) AND long-range van der Waals networks (long-persistence) simultaneously
- Wins in D3R Grand Challenges (blind drug binding affinity prediction)
- Forecast SARS-CoV-2 variants ~2 months in advance from spike protein mutation topology

---

### 1.4 Single-Cell RNA Sequencing

**Spectral-distance PH (Damrich, Berens, Kobak — NeurIPS workshop, 2023):**

Standard TDA on high-dimensional scRNA-seq fails (Euclidean distances dominated by noise). Using spectral distances (diffusion maps, Laplacian eigenmaps) as metric before computing PH robustly detected **cell cycle loops** — circular trajectories in gene expression space where Euclidean-distance PH produces noise.

**scGeom:** Persistent homology + Ollivier-Ricci curvature on kNN graphs detects transition cells at differentiation bifurcation points — cells that don't cluster cleanly with any fate, visible only via H1 features.

---

### 1.5 Medical Imaging

**Clough et al.** "A Topological Loss Function for Deep-Learning Based Image Segmentation Using Persistent Homology." *IEEE TPAMI*, 2022.

Topological loss function enforces correct topology (right number of connected components, no spurious holes) in neural network segmentations of cardiac MRI and road networks. Topology-preserving constraints are clinically essential: a segmented ventricle with a hole is useless for volume estimation.

---

## 2. Machine Learning and Artificial Intelligence

### 2.1 Persistence Images for ML

**Adams, H. et al.** "Persistence Images: A Stable Vector Representation of Persistent Homology." *JMLR*, 18(8):1–35, 2017.

Maps persistence diagrams to 2D images via Gaussian kernels on the birth-persistence plane. Proved stable under 1-Wasserstein distance. Applied to:
- Linked twist map: near-perfect parameter inference from trajectories
- Anisotropic Kuramoto-Sivashinsky PDE: predicts PDE parameters from spatial patterns

---

### 2.2 Topological Regularization in Neural Networks

**Brüel-Gabrielsson et al.** "A Topology Layer for Machine Learning." *AISTATS* 2020.

Differentiable persistent homology layer in PyTorch. Applications:
- **Topological regularization of autoencoders:** Penalizes latent representations with topological complexity inconsistent with a prior (e.g., data on a sphere should have trivial H1)
- **Topological GAN loss:** Enforces generated samples match Betti numbers of real data, preventing topology-destroying mode collapse
- **Topological adversarial attacks:** Perturbs input to change persistence diagram of feature layers

**Moor, M. et al.** "Topological Autoencoders." *ICML* 2020.

Minimizes Wasserstein distance between PH of input and latent representations. Preserves loops, connected components, and multi-scale connectivity in the latent space — achieving topology-preserving dimensionality reduction.

---

### 2.3 Neural Network Loss Landscapes

**Barannikov et al.** "Loss Barcode: A Topological Measure of Escapability in Loss Landscapes." arXiv:2011.14639, 2020.

**Method:** Sublevel-set persistent H0 of the neural network loss function over parameter space. The barcode encodes connected components of $\{\theta : L(\theta) \leq c\}$.

**Discovery:** Adam produces loss landscapes with fewer, shallower topological obstructions than SGD — a topological explanation for Adam's convergence advantage. Better-performing models consistently have topologically simpler loss landscapes.

**Rieck et al.** "Neural Persistence: A Complexity Measure for Deep Neural Networks Using Algebraic Topology." *ICLR* 2019.

Neural Persistence (sum of H0 persistence values across layers) *decreases during training* and correlates with generalization — providing a topology-based model complexity measure.

---

### 2.4 Graph Neural Networks and Topology

**Hofer, C., Graf, F., Rieck, B., et al.** "Graph Filtration Learning." *ICML* 2020.

End-to-end learning of parametric filtrations on graphs. Topological features from learned filtrations matched or exceeded GNN baselines on molecular graph classification tasks (MUTAG, PROTEINS, NCI1) where cycle structure is discriminative.

**Recent (2025):** Frequent Subgraph Filtration combining frequent pattern mining with PH yields 0.4–21% performance gains when integrated with GNN architectures for molecular property prediction.

---

### 2.5 TDA for Understanding LLMs

Rapidly emerging area (2023–2025). Topology of transformer representations reveals structure invisible to standard probing:

- **Gardinazzi et al. (ICML 2025):** Zigzag PH on activation spaces across transformer layers reveals distinct representational phases; enables topology-guided layer pruning
- **"Understanding Chain-of-Thought via TDA" (arXiv:2512.19135, 2024):** TDA analyzes reasoning traces in LLMs
- **Deepfake text detection:** Short-PHD uses PH to detect LLM-generated text (COLM 2025)
- Survey: "Unveiling Topological Structures from Language" (arXiv:2411.10298, 2024)

---

## 3. Materials Science and Physics

### 3.1 Amorphous Materials and Glass Structure

**Nakamura, T. et al.** "Persistent Homology and Many-Body Atomic Structure for Medium-Range Order in the Glass." *Nanotechnology*, 26:304001, 2015.

**Method:** Alpha complex filtration on atomic positions from MD simulations of amorphous silica. H1 features = ring structures; H2 features = cage structures.

**Discovery:** Persistence diagrams for amorphous materials occupy a **different region of diagram space** than both crystalline and completely random configurations. Captured **medium-range order** (structural correlations at 0.5–2 nm) invisible to pair distribution functions — the standard tool in amorphous materials characterization.

**Follow-up (Minamitani et al., JCP 2021):** H1 ring features predict thermal conductivity of amorphous silicon with high accuracy. Inverse analysis identified ring types that reduce thermal conductivity, providing design guidelines for thermal insulators.

**Hiraoka et al.** "Hierarchical structures of amorphous solids characterized by persistent homology." *PNAS*, 113(26):7035–7040, 2016.

Different glassy materials (silica, Cu-Zr metallic glass) have topologically distinct persistence diagram signatures — tetrahedral rings vs. icosahedral cages. Persistent across different cooling rates, intrinsic to bonding network.

---

### 3.2 Phase Transitions

**Cole, A., Loges, G., Shiu, G.** "Quantitative and Interpretable Order Parameters for Phase Transitions from Persistent Homology." *Physical Review Research*, 3:043059, 2021.

**Method:** PH on spin configurations from Ising and XY models. H0: ferromagnetic ordering; H1: vortex structures (BKT transition).

**Discovery:** Persistence images + logistic regression recovered known physics (magnetization, vortex density) as topological order parameters **without prior knowledge of the order parameter**. For the Berezinskii-Kosterlitz-Thouless transition (notoriously hard to characterize), H1 persistence detected vortex proliferation at $T_c$.

**Sale, N. et al.** "Probing Center Vortices and Deconfinement in SU(2) Lattice Gauge Theory with Persistent Homology." *Physical Review D*, 2023.

PH on 4D lattice gauge configurations accurately determined the critical temperature of the QCD deconfinement phase transition.

---

### 3.3 Cosmological Data Analysis

**Cole, A., Biagetti, M., Shiu, G.** "Topological Echoes of Primordial Physics in the Universe at Large Scales." *Physical Review Letters*, 126:101305, 2021.

Used PH on simulated matter distributions to detect **primordial non-Gaussianity** at 97.5% confidence — departures from Gaussian initial conditions that are invisible to the power spectrum alone.

**Wilding, G. et al.** "Persistent Homology of the Cosmic Web: Hierarchical Topology in ΛCDM Cosmologies." *MNRAS*, 2021.

H0 = galaxy clusters, H1 = filament loops, H2 = void walls. Persistence diagrams provided significantly more information about structure formation than standard two-point statistics.

**Elbers, W. & van de Weygaert, R.** *MNRAS*, 2022: H1 features dominate during cosmic reionization — ionized bubbles form a percolating network with non-trivial loop structure before fully overlapping.

---

## 4. Time Series and Dynamical Systems

### 4.1 Sliding Window Embeddings and Periodicity

**Perea, J.A. & Harer, J.** "Sliding Windows and Persistence: An Application of Topological Methods to Signal Analysis." *Foundations of Computational Mathematics*, 15:799–838, 2015.

**Method:** **Sliding window embedding** (Takens delay embedding): for time series $f(t)$, construct point cloud $\{[f(t), f(t+\tau), \ldots, f(t+(d-1)\tau)]\}$. For periodic signals, this concentrates near a circle; H1 detects the dominant loop.

**Key theorem:** For periodic functions, the maximum H1 persistence of the sliding window embedding is **proportional to the periodicity**, providing a noise-robust, non-parametric measure of periodicity outperforming Fourier/autocorrelation for non-stationary signals.

---

### 4.2 Financial Crash Detection

**Gidea, M. & Katz, Y.** "Topological Data Analysis of Financial Time Series: Landscapes of Crashes." *Physica A*, 491:820–834, 2018.

**Method:** Sliding window embedding on log-returns of major indices. Track L2 norm of H1 persistence landscapes over time.

**Discovery:** H1 landscape norm showed a strong rising trend for **~250 trading days preceding** both the 2000 dot-com crash and the 2008 Lehman collapse. As a crash approaches, stock correlations change in a coordinated way that increases the loop structure in the return correlation point cloud. More specific than standard pairwise correlation signals.

**Follow-up (Rai et al., Chaos, Solitons & Fractals, 2024):** TDA features detected the 2008 financial crisis and COVID-19 crash across multiple global indices; the banking sector showed elevated topological complexity long after the primary crash, indicating persistent systemic stress.

---

### 4.3 Chaos and Dynamical Systems

**Method:** Delay embeddings of chaotic time series produce point clouds with specific topological signatures:
- **Periodic systems:** Strong H1 (circle topology)
- **Quasi-periodic (torus):** H1 and H2 (torus topology)
- **Chaotic attractors (Lorenz):** Complex H1 + H2 corresponding to the two lobes

**Applications:**
- **ECG arrhythmia classification:** Cardiac arrhythmias have distinct loop structures
- **EEG seizure detection:** Seizure transitions produce strong H1 signatures (Fernández et al., 2024)
- **Wheeze detection** (Emrani et al., IEEE Signal Processing Letters, 2014)

---

## 5. Computer Vision and Image Analysis

### 5.1 Shape Recognition — Persistent Homology Transform

**Turner, K., Mukherjee, S., Boyer, D.M.** "Persistent Homology Transform for Modeling Shapes and Surfaces." *Information and Inference*, 3(4):310–344, 2014.

**Persistent Homology Transform (PHT):** For a shape $M \subset \mathbb{R}^n$, compute the persistence diagram of the sublevel-set filtration in every direction $v \in S^{n-1}$. The map $M \mapsto \{\text{Dgm}(M, v)\}_{v}$ is **injective** — uniquely identifies piecewise-linear shapes.

**Euler Characteristic Transform (ECT):** Cheaper variant using Euler characteristic curves. Applied to primate molar shape analysis (paleontological databases), providing coordinate-free, alignment-free shape statistics.

**Reininghaus, J. et al.** "A Stable Multi-Scale Kernel for Topological Machine Learning." *CVPR* 2015.

Persistence scale-space kernel (stable SVM kernel for shape classification). Outperformed shape context and spin image on 3D shape datasets, especially for topological noise.

---

### 5.2 Image Segmentation with Topological Constraints

**Hu, X. et al.** "Topology-Preserving Deep Image Segmentation." *NeurIPS* 2019.

**Clough, J.R. et al.** "A Topological Loss Function for Deep-Learning Based Image Segmentation Using Persistent Homology." *IEEE TPAMI* 44(12), 2022.

Topological loss finds the most topologically incorrect critical simplices in the predicted segmentation and minimizes their persistence. Applied to cardiac MRI, road networks, cell segmentation — produces topologically valid segmentations even in low-contrast regions.

---

## 6. Network Analysis

### 6.1 Biological Networks

**Stolz, B. et al.** "Topological Data Analysis of Task-Based fMRI Data from Experiments on Schizophrenia." *Journal of Physics: Complexity*, 2:035006, 2021.

Vietoris-Rips filtrations on fMRI functional connectivity graphs. Schizophrenia patients showed significantly different Betti curve profiles from healthy controls, particularly H1 in the frontal-temporal axis — outperforming graph-theoretic features alone.

**TopoQA (Han et al., Bioinformatics, 2024):** PH integrated into GNN for protein complex quality assessment. H0/H1 from interface contact graphs encode triangular and ring interface motifs that pairwise features miss.

---

### 6.2 Social and Infrastructure Networks

**Carstens & Horadam** "Persistent Homology of Collaboration Networks." *Mathematical Problems in Engineering*, 2013.

Co-authorship networks analyzed as simplicial complexes. Large, long-lived H1 features corresponded to stable research communities with persistent intra-community collaboration cycles, capturing structure beyond graph modularity.

**Chordless Cycle Filtrations (Ferrà Marcús et al., 2025):** Filtration based on minimal chordless cycles detects effective topological dimension of networks. Power grids and road networks have dimension ~2 (planar); social networks have much higher effective dimension.

---

## 7. Summary Table of Landmark Papers

| Domain | Paper | Venue/Year | Key TDA Tool | Unique Contribution |
|--------|-------|------------|-------------|---------------------|
| Cancer genomics | Nicolau, Levine, Carlsson | PNAS 2011 | Mapper | c-MYB+ breast cancer subtype with 100% survival |
| Neuroscience | Giusti, Curto, Itskov | PNAS 2015 | Clique topology/Betti | Torus structure of hippocampal correlations |
| Protein structure | Cang & Wei | PLOS Comp Bio 2017 | Element-specific PH | State-of-art binding affinity prediction |
| scRNA-seq | Damrich, Berens, Kobak | NeurIPS ws 2023 | Spectral PH | Cell cycle loop detection |
| Medical imaging | Clough et al. | IEEE TPAMI 2022 | Topological loss | Topology-preserving anatomical segmentation |
| Amorphous materials | Nakamura, Hiraoka et al. | Nanotechnology 2015 | Alpha PH | Medium-range order in glass |
| Thermal conductivity | Minamitani et al. | JCP 2021 | H1 ring features | Design principles for thermal insulators |
| Phase transitions | Cole, Loges, Shiu | PRR 2021 | Persistence images | Topology-derived order parameters |
| Cosmology | Cole, Biagetti, Shiu | PRL 2021 | PH on matter fields | Primordial non-Gaussianity detection |
| Cosmic web | Wilding et al. | MNRAS 2021 | Alpha PH | Void topology / structure formation history |
| ML features | Adams et al. | JMLR 2017 | Persistence images | Stable vectorization for ML |
| Topological autoencoder | Moor, Horn, Rieck | ICML 2020 | Wasserstein PH loss | Topology-preserving latent representations |
| Topology layer | Brüel-Gabrielsson et al. | AISTATS 2020 | Differentiable PH | End-to-end topological regularization |
| Loss landscapes | Barannikov et al. | arXiv 2020 | Sublevel PH | Topological Obstructions Score |
| GNN + topology | Hofer, Graf, Rieck et al. | ICML 2020 | Learned filtrations | Topological graph classification |
| Time series | Perea & Harer | FoCM 2015 | Sliding window PH | Noise-robust periodicity score |
| Financial crashes | Gidea & Katz | Physica A 2018 | Persistence landscapes | 250-day early warning signal |
| Shape recognition | Turner, Mukherjee, Boyer | IMA J 2014 | PHT/ECT | Injective shape statistic |
| 3D shape matching | Reininghaus et al. | CVPR 2015 | Scale-space kernel | Stable SVM kernel for shapes |
| fMRI / schizophrenia | Stolz et al. | J Phys Complexity 2021 | VR filtration | Topological fingerprints of functional connectivity |

---

*Previous: [03_algorithms_and_software.md](03_algorithms_and_software.md) | Next: [05_research_frontiers.md](05_research_frontiers.md)*
