# Topological Data Analysis: Mathematical Foundations

## Overview

Topological Data Analysis (TDA) is a mathematical framework that uses tools from algebraic topology to extract shape-based features from data. The central premise is that the **topological and geometric structure** of data carries meaningful information about its underlying generating process — information that is often invisible to classical statistical methods.

This document covers the mathematical foundations required to understand TDA: metric spaces, simplicial complexes, homology theory, and Betti numbers.

---

## 1. Point Cloud Data and Metric Spaces

### 1.1 Metric Spaces

A **metric space** is a pair $(X, d)$ where $X$ is a set and $d: X \times X \to \mathbb{R}_{\geq 0}$ satisfies:
1. **Non-negativity:** $d(x,y) \geq 0$, with $d(x,y)=0 \iff x=y$
2. **Symmetry:** $d(x,y) = d(y,x)$
3. **Triangle inequality:** $d(x,z) \leq d(x,y) + d(y,z)$

**Point cloud data** is a finite set $P = \{p_1, \ldots, p_n\} \subset \mathbb{R}^d$ representing a discrete sample from some underlying geometric or topological object. The key challenge: can we recover the *shape* of the underlying object from only the finite sample?

### 1.2 Hausdorff Distance

For two compact subsets $A, B \subset (M, d)$:

$$d_H(A, B) = \max\left(\sup_{a \in A} \inf_{b \in B} d(a,b),\ \sup_{b \in B} \inf_{a \in A} d(a,b)\right)$$

This measures the worst-case deviation between two point sets and is fundamental to TDA stability arguments.

---

## 2. Simplicial Complexes

Simplicial complexes are the primary combinatorial objects used to build discrete approximations of topological spaces from point clouds.

### 2.1 Simplices

A **$k$-simplex** $\sigma$ is the convex hull of $k+1$ affinely independent points $\{v_0, v_1, \ldots, v_k\}$, written $\sigma = [v_0, v_1, \ldots, v_k]$. The **dimension** of $\sigma$ is $k$.

| Dimension | Name | Example |
|-----------|------|---------|
| 0 | Vertex | a point |
| 1 | Edge | a line segment |
| 2 | Triangle | a filled triangle |
| 3 | Tetrahedron | a solid tetrahedron |

A **face** of $\sigma$ is any simplex formed by a non-empty subset of its vertices.

### 2.2 Simplicial Complex

An **abstract simplicial complex** $K$ is a collection of simplices satisfying:
1. If $\sigma \in K$ and $\tau$ is a face of $\sigma$, then $\tau \in K$ (closure under faces)
2. For $\sigma, \tau \in K$, $\sigma \cap \tau$ is a face of both

The **geometric realization** of $K$ is denoted $|K|$.

### 2.3 Filtrations

A **filtration** on $K$ is a nested sequence of subcomplexes:

$$\emptyset = K_0 \subseteq K_1 \subseteq K_2 \subseteq \cdots \subseteq K_m = K$$

Equivalently, a filtration function $f: K \to \mathbb{R}$ where $f(\tau) \leq f(\sigma)$ whenever $\tau \subseteq \sigma$ (faces must enter before cofaces). Filtrations are the engine of persistent homology: by varying the threshold, we observe how topology changes across scales.

---

## 3. The Three Principal Complexes

### 3.1 Vietoris–Rips Complex

Given a finite metric space $(P, d)$ and threshold $r \geq 0$:

$$\text{VR}(P, r) = \{\sigma \subseteq P : \text{diam}(\sigma) \leq r\}$$

A simplex is included if and only if all pairwise distances among its vertices are $\leq r$. VR is a **flag complex**: fully determined by its 1-skeleton (edges).

**Key property:** VR is the most computationally tractable complex and is the default choice for most TDA pipelines. As $r$ grows, simplices are added and we track topological changes.

**Reference:** Vietoris, L. *Über den höheren Zusammenhang kompakter Räume.* Mathematische Annalen, 1927.

### 3.2 Čech Complex

Given $P \subset \mathbb{R}^d$ and $r \geq 0$:

$$\check{C}(P, r) = \{\sigma \subseteq P : \bigcap_{p \in \sigma} B(p, r) \neq \emptyset\}$$

A simplex is included if and only if the closed $r$-balls centered at its vertices have nonempty common intersection. Equivalently: the smallest enclosing ball of $\sigma$ has radius $\leq r$.

**Key theorem (Nerve Theorem):** $\check{C}(P, r) \simeq \bigcup_{p \in P} B(p, r)$ (homotopy equivalence), because the balls form a good cover (all intersections are convex, hence contractible).

### 3.3 Alpha Complex

Given $P \subset \mathbb{R}^d$, the alpha complex $\alpha(P, r)$ is a subcomplex of the **Delaunay triangulation** of $P$: a simplex $\sigma \in \alpha(P, r)$ iff its restricted circumradius (within the Voronoi cell) is $\leq r$.

**Key property:** $\alpha(P, r)$ is homotopy equivalent to the union of balls but is **much smaller** than VR or Čech (size $O(n^{\lceil d/2 \rceil})$ vs. exponential). Ideal for low-dimensional point clouds.

**Reference:** Edelsbrunner, H., Kirkpatrick, D., Seidel, R. *On the shape of a set of points in the plane.* IEEE Trans. Information Theory, 1983.

### 3.4 Comparison of Complexes

| Complex | Inclusion criterion | Size (worst case) | Homotopy type |
|---------|--------------------|--------------------|---------------|
| Vietoris-Rips $\text{VR}(P,r)$ | $\text{diam}(\sigma) \leq r$ | $O(2^n)$ | Approximates $\bigcup B(p,r)$ |
| Čech $\check{C}(P,r)$ | circumradius$(\sigma) \leq r$ | $O(2^n)$ | $\simeq \bigcup B(p,r)$ (exact) |
| Alpha $\alpha(P,r)$ | restricted circumradius $\leq r$ | $O(n^{\lceil d/2 \rceil})$ | $\simeq \bigcup B(p,r)$ (exact) |

**Interleaving inequality:**
$$\check{C}(P, r) \subseteq \text{VR}(P, 2r) \subseteq \check{C}(P, 2r)$$

The Vietoris-Rips complex $2r$-approximates the Čech complex, losing at most a factor of 2 in scale.

---

## 4. Homology Theory

Homology is the algebraic tool that quantifies the "holes" in a topological space at each dimension.

### 4.1 Chain Groups

Fix a coefficient field $\mathbb{F}$ (e.g., $\mathbb{Z}/2\mathbb{Z}$, $\mathbb{Q}$). The **$k$-th chain group** $C_k(K; \mathbb{F})$ is the $\mathbb{F}$-vector space with basis the set of oriented $k$-simplices of $K$. Elements are formal $\mathbb{F}$-linear combinations of $k$-simplices.

**Orientation convention:** $[v_0, \ldots, v_k] = \text{sgn}(\pi)\, [v_{\pi(0)}, \ldots, v_{\pi(k)}]$ for any permutation $\pi$. Over $\mathbb{Z}/2\mathbb{Z}$ orientation is irrelevant (most implementations use this field for speed).

### 4.2 Boundary Operator

The **boundary operator** $\partial_k: C_k(K) \to C_{k-1}(K)$ is defined on basis elements by:

$$\partial_k [v_0, v_1, \ldots, v_k] = \sum_{i=0}^k (-1)^i [v_0, \ldots, \hat{v}_i, \ldots, v_k]$$

where $\hat{v}_i$ denotes omission of vertex $v_i$.

**Examples:**
- $\partial_1 [v_0, v_1] = [v_1] - [v_0]$ (an edge maps to the difference of its endpoints)
- $\partial_2 [v_0, v_1, v_2] = [v_1,v_2] - [v_0,v_2] + [v_0,v_1]$ (a triangle maps to its boundary loop)

**Fundamental property:** The boundary of a boundary is zero:

$$\partial_k \circ \partial_{k+1} = 0$$

This gives the **chain complex**:
$$\cdots \xrightarrow{\partial_{k+1}} C_k \xrightarrow{\partial_k} C_{k-1} \xrightarrow{\partial_{k-1}} \cdots \xrightarrow{\partial_1} C_0 \to 0$$

### 4.3 Homology Groups

- **$k$-cycles:** $Z_k(K) = \ker(\partial_k)$ — chains with no boundary
- **$k$-boundaries:** $B_k(K) = \text{im}(\partial_{k+1})$ — chains that are boundaries of $(k+1)$-chains

Since $\partial^2 = 0$, we have $B_k \subseteq Z_k$.

**Definition:** The **$k$-th homology group** is:

$$H_k(K; \mathbb{F}) = Z_k(K) / B_k(K) = \ker(\partial_k) / \text{im}(\partial_{k+1})$$

Elements are **homology classes**: two cycles are homologous iff their difference is a boundary. Intuitively, homology classes are "independent holes" of dimension $k$.

**Geometric interpretation:**
- $H_0$: counts connected components
- $H_1$: counts independent 1-dimensional loops (holes that cannot be filled in)
- $H_2$: counts enclosed 2-dimensional voids (cavities)
- $H_k$: counts $k$-dimensional "holes"

### 4.4 Betti Numbers

The **$k$-th Betti number** is the rank of the $k$-th homology group:

$$\beta_k(K) = \dim_\mathbb{F} H_k(K; \mathbb{F})$$

**Examples of Betti numbers for common spaces:**

| Space | $\beta_0$ | $\beta_1$ | $\beta_2$ |
|-------|-----------|-----------|-----------|
| Point | 1 | 0 | 0 |
| Circle $S^1$ | 1 | 1 | 0 |
| Disk $D^2$ | 1 | 0 | 0 |
| Sphere $S^2$ | 1 | 0 | 1 |
| Torus $T^2$ | 1 | 2 | 1 |
| Klein bottle | 1 | 1 | 0 |
| Figure-eight | 1 | 2 | 0 |
| Genus-$g$ surface | 1 | $2g$ | 1 |

**Euler characteristic:** The alternating sum of Betti numbers:

$$\chi(K) = \sum_{k \geq 0} (-1)^k \beta_k = \sum_{k \geq 0} (-1)^k |K_k|$$

where $|K_k|$ is the number of $k$-simplices. This generalizes $V - E + F = 2$ for convex polyhedra.

---

## 5. The Nerve Theorem

The **Nerve Theorem** connects the topology of a space to the combinatorics of a cover:

**Definition:** Given a topological space $X$ and a cover $\mathcal{U} = \{U_\alpha\}$, the **nerve** $\mathcal{N}(\mathcal{U})$ is the simplicial complex with one vertex per $U_\alpha$ and a $k$-simplex $\{U_{\alpha_0}, \ldots, U_{\alpha_k}\}$ whenever $U_{\alpha_0} \cap \cdots \cap U_{\alpha_k} \neq \emptyset$.

**Nerve Theorem:** If every non-empty finite intersection $U_{\alpha_0} \cap \cdots \cap U_{\alpha_k}$ is contractible (a **good cover**), then:
$$X \simeq |\mathcal{N}(\mathcal{U})| \quad \text{(homotopy equivalence)}$$

**Applications:**
- **Čech complex = Nerve of balls:** $\check{C}(P, r)$ is the nerve of $\{B(p,r)\}_{p \in P}$, and since balls are convex (contractible), this equals the union of balls up to homotopy.
- **Mapper algorithm:** Applies this principle by approximating the nerve of a data cover via clustering.

---

## 6. Key Reference Texts

| Title | Authors | Year | Type |
|-------|---------|------|------|
| *Computational Topology: An Introduction* | Edelsbrunner, Harer | 2010 | Graduate textbook |
| *Algebraic Topology* | Hatcher | 2002 | Graduate textbook (free online) |
| *Elementary Applied Topology* | Ghrist | 2014 | Applied focus (free online) |
| *Topology and data* | Carlsson | 2009 | Survey article (Bull. AMS) |
| *Elements of Algebraic Topology* | Munkres | 1984 | Classic reference |

---

## Summary: Key Formulas

| Formula | Meaning |
|---------|---------|
| $\partial_k [v_0,\ldots,v_k] = \sum_{i=0}^k (-1)^i [v_0,\ldots,\hat{v}_i,\ldots,v_k]$ | Boundary operator |
| $\partial_k \circ \partial_{k+1} = 0$ | Boundary of boundary is zero |
| $H_k = \ker(\partial_k) / \text{im}(\partial_{k+1})$ | Homology group |
| $\beta_k = \dim H_k$ | Betti number |
| $\chi = \sum_k (-1)^k \beta_k$ | Euler characteristic |
| $\check{C}(P,r) \subseteq \text{VR}(P,2r) \subseteq \check{C}(P,2r)$ | Rips-Čech interleaving |

---

*Next: [02_persistent_homology.md](02_persistent_homology.md) — Persistent Homology, Barcodes, and Stability*
