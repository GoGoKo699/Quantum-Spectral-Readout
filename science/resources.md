# Resource comparison

Full spectral readout has two independent inputs: a source state and access to its Hamiltonian. Their costs should be compared separately. The [model](model.md) specifies physical source copies, purified preparation queries, controlled evolution, and exact normalized block encodings. The [multilevel algorithm](multilevel_algorithm.md) achieves the optimal worst-case Hamiltonian precision exponent from physical copies, up to logarithms; a coherent-source upper with that exponent is already available from prior work.

## 1. Common task and resource units

Every upper bound below returns a finite classical probability measure approximating

```math
\mu_{H,\rho}(B)=\operatorname{Tr}[\rho E_H(B)],
\qquad \|H\|\leq1,
```

in $`W_1`$ distance at most $`\epsilon`$, with constant success probability. The source may be mixed and need not commute with $`H`$. A physical-copy protocol receives independent copies of the same state. A coherent-source protocol instead receives a unitary $`P_\rho`$ preparing a purification, its inverse, and controlled versions; calls in both directions are counted.

Hamiltonian cost means total absolute evolution time $`\sum_r|t_r|`$ or queries to an exact normalization-one block encoding, as appropriate. A long controlled evolution is not a unit-cost sample. Source preparation, matrix loading, and construction of the supplied Hamiltonian interface have no implicit zero-cost implementation.

Write $`L=\Theta(\log(1/\epsilon))`$. A tilde suppresses logarithms in inverse precision. Upper bounds are guarantees for the named protocols, not impossibility statements about their whole access classes.

| Protocol | Source resource | Total Hamiltonian resource | Maximum evolution or queries within one retained-source experiment |
|---|---:|---:|---:|
| Independent finest-resolution robust QPE, followed by an empirical measure | $`O(\epsilon^{-2})`$ physical copies | $`O(\epsilon^{-3})`$ | $`O(\epsilon^{-1})`$ |
| Direct full-$`W_1`$ specialization of Lin–Tong's approximate-CDF estimator | $`\widetilde O(\epsilon^{-2})`$ physical copies | Expected evolution $`\widetilde O(\epsilon^{-3})`$ | Evolution $`\widetilde O(\epsilon^{-1})`$ |
| Coherent spectral sampler followed by Li–Liao–Yang distribution learning | $`\widetilde O(\epsilon^{-1})`$ controlled preparation/inverse calls | $`\widetilde O(\epsilon^{-2})`$ | No maximum-run bound asserted here |
| Retained-copy multilevel algorithm, copy-efficient allocation | $`O(\epsilon^{-2})`$ physical copies | $`O(\epsilon^{-2}L^3)`$ | $`O(\epsilon^{-1})`$ |
| Retained-copy multilevel algorithm, alternative allocation | $`O(\epsilon^{-2}L)`$ physical copies | $`O(\epsilon^{-2}L^2)`$ | $`O(\epsilon^{-1})`$ |

The Lin–Tong row is derived from their published variance and expected-time guarantees below. It does not establish cubic optimality for all possible uses of their data. The coherent row follows from [Li–Liao–Yang, Lemmas 35–37](https://arxiv.org/pdf/2608.22769v2) with generic Hamiltonian access separated from graph implementation cost. The final two rows are proved in [the algorithm chapter](multilevel_algorithm.md).

The [lower-bound chapter](lower_bounds.md) proves the following separate minimax statements:

| Resource | Lower bound | Qualification |
|---|---:|---|
| Charged Hamiltonian evolution or generic block-encoding queries | $`\Omega(\min\{d,\epsilon^{-1}\}/\epsilon)`$ | Holds even with a known freely preparable source and stronger coherent control; gives $`\Omega(\epsilon^{-2})`$ when $`d=\Omega(\epsilon^{-1})`$ |
| Physical copies of an unknown source | $`\Omega(\epsilon^{-2})`$ | A fixed known two-level Hamiltonian suffices |
| Controlled coherent preparation/inverse queries | $`\Omega(\epsilon^{-1})`$ | An explicit weak purifier is supplied; unknown-source copies are not additionally free |

These lower bounds use separate hard families. They do not characterize a joint resource frontier for every input. The Hamiltonian lower bound applies to the specified evolution/amplitude oracle, not automatically to exact classical matrix-entry or graph-neighbor access. A matching general upper bound for the small-dimension expression is not claimed.

## 2. Independent fine-QPE baseline

Let $`Y`$ be a robust energy readout with a uniform conditional mean error $`\mathbb E[|Y-\lambda|\mid\lambda]=O(\epsilon)`$. The [phase-estimation construction](multilevel_algorithm.md) implements it at cost $`O(\epsilon^{-1})`$. Its output law $`\nu`$ obeys $`W_1(\nu,\mu)=O(\epsilon)`$ by coupling the readout to its latent energy.

For $`N`$ independent outcomes, let $`F_N`$ be the empirical CDF. Since every indicator has variance at most one quarter,

```math
\begin{aligned}
\mathbb E\|F_N-F_\nu\|_1
&\leq \int_{-1}^{1}
\sqrt{\frac{F_\nu(x)(1-F_\nu(x))}{N}}\,dx\\
&\leq N^{-1/2}.
\end{aligned}
```

Taking $`N=O(\epsilon^{-2})`$, with sufficiently small bias and statistical-error constants, gives the requested constant-success guarantee. Rounding the empirical measure to an $`O(\epsilon)`$ grid changes its Wasserstein distance by at most the rounding distance. The total Hamiltonian cost is therefore

```math
N\cdot O(\epsilon^{-1})=O(\epsilon^{-3}).
```

This baseline directly uses the requested Wasserstein metric. A stronger total-variation guarantee for a growing histogram would introduce unnecessary costs and would not be the appropriate comparison.

## 3. Lin–Tong's approximate CDF under the same target

[Lin and Tong](https://arxiv.org/pdf/2102.11340v2) provide a one-ancilla, fresh-copy approximate-CDF estimator for arbitrary mixed sources. Their Section 3, especially Eqs. (14)–(17), supplies a reusable random trigonometric estimator of degree $`K`$. After a constant Hamiltonian normalization, pointwise variance at most $`\sigma^2`$ requires

```math
N_s=O\!\left(\frac{\log^2 K}{\sigma^2}\right),
\qquad
\mathbb E T=O\!\left(\frac{K\log K}{\sigma^2}\right).
```

The real and imaginary measurements change the number of source copies only by a constant factor. Their approximate-CDF guarantee brackets the true CDF by shifts of size $`\delta`$ and a filter error $`\eta`$:

```math
F(x-\delta)-\eta\leq\widetilde F(x)
\leq F(x+\delta)+\eta.
```

On a bounded interval this implies integrated bias $`O(\delta+\eta)`$. In particular,

```math
\int_{\mathbb R}[F(x+\delta)-F(x-\delta)]\,dx=2\delta,
```

so no smooth-density assumption is needed. Integrating the pointwise standard-deviation bound contributes $`O(\sigma)`$. Their filter construction, Lemma 6, uses

```math
K=O\!\left(\delta^{-1}\log(\delta^{-1}\eta^{-1})\right).
```

Choose $`\delta,\eta,\sigma=\Theta(\epsilon)`$ with suitable constants. Evaluate the real part of the classical estimator on a grid of mesh $`O(\epsilon)`$ and apply the CDF projection described in [the algorithm chapter](multilevel_algorithm.md). The variance bound applies to the grid values. Monotonicity of the true CDF bounds the remaining discretization error by a constant times the mesh. This yields

```math
N_s=\widetilde O(\epsilon^{-2}),
\qquad
\mathbb E T=\widetilde O(\epsilon^{-3}).
```

This is a direct specialization of the published guarantee to full-law Wasserstein reconstruction. It is not a lower bound against other reorganizations of the estimator. Their Heisenberg scaling for ground-energy estimation concerns a different output task and a separate lower bound on ground-state overlap.

## 4. The inherited coherent-source upper

### 4.1 Source access is part of the comparison

Let a controlled unitary $`P_\rho`$ prepare a purification of $`\rho`$, and supply its controlled inverse. Coherent phase estimation gives a sampler $`S_\eta`$ whose measured energy law has Wasserstein bias at most $`\eta`$. One call uses one preparation and $`\widetilde O(\eta^{-1})`$ Hamiltonian resource; its inverse uses one inverse preparation and the corresponding inverse dynamics. The environment and unmeasured work registers can be retained as garbage.

[Li–Liao–Yang, Lemma 37](https://arxiv.org/pdf/2608.22769v2) learns the one-dimensional output law of such a coherent experiment to Wasserstein error $`\epsilon`$ with $`\widetilde O(\epsilon^{-1})`$ controlled forward/inverse experiment calls. Taking $`\eta=\Theta(\epsilon)`$ gives

```math
Q_\rho=\widetilde O(\epsilon^{-1}),
\qquad
Q_H\text{ or }T=\widetilde O(\epsilon^{-2}).
```

The measure is classical and has $`O(\epsilon^{-1})`$ support points. This generic coherent-source upper is inherited from their sampler and distribution-learning proof. The retained-copy theorem reaches the same Hamiltonian exponent without a reversible preparation circuit.

### 4.2 Ordinary gates and QRAM

The distribution learner invokes [van Apeldoorn's multidimensional amplitude estimation](https://doi.org/10.4230/LIPIcs.TQC.2021.9). Definition 1 permits arbitrary normalized garbage and explicitly assumes controlled forward/inverse probability-oracle calls. With total probability mass one and constant failure probability, Theorem 9 gives approximately inverse-linear oracle cost and $`\widetilde O(q/\alpha^2)`$ additional two-qubit gates for coordinate accuracy $`\alpha`$, where $`q`$ is the oracle register size.

In the dyadic Wasserstein construction, $`\alpha=\epsilon/\operatorname{polylog}(1/\epsilon)`$. Thus an ordinary implementation can use $`\widetilde O(q\epsilon^{-2})`$ additional gates. QRAM is not necessary for the table's query exponents. This gate count is separate from the cost of executing each source or Hamiltonian oracle call.

If source preparation is expensive, its coherent-query advantage may matter, but its inverse and coherent controls must actually be available. If only physical source specimens are supplied, the coherent row is not an admissible replacement. The [model](model.md) states these interfaces independently rather than treating a source copy as a reversible circuit.

### 4.3 Graph access has another normalization cost

Li–Liao–Yang's graph-local algorithm has cost $`\widetilde O(\epsilon^{-3})`$. Their Lemma 35 charges an additional factor $`\sqrt\Delta`$ per spectral-sampler implementation, and the graph truncation uses $`\Delta=\Theta(\epsilon^{-2})`$. The coherent distribution-learning step is already present. A generic normalization-one block query does not remove that graph implementation cost, and no graph-local query improvement follows from the present theorem.

## 5. Classical processing and interpretation

The multilevel protocol uses a common finite grid, accumulates a signed histogram, and projects its CDF to a probability CDF. The full error proof, exact rational representation, and classical costs are in [the algorithm chapter](multilevel_algorithm.md). A standard [isotonic regression algorithm](https://doi.org/10.4230/OASIcs.SOSA.2019.1) gives the projection in $`O(K\log K)`$ arithmetic operations for $`K=O(\epsilon^{-1})`$ grid intervals. Overall classical work is $`\widetilde O(\epsilon^{-2})`$ and the output uses $`O(\epsilon^{-1}\log^2(1/\epsilon))`$ bits, apart from the requested tolerance's description.

The [exact projector](../verification/exact_cdf_projection.py) and [coupling/projection validation](../verification/validate_spectral_coupling.py) check positivity, normalization, and agreement with an independent linear-program solution on a finite nonmonotone example. The analytic proof establishes the general guarantee.

A successful classical Wasserstein output controls all later 1-Lipschitz spectral averages on the same event. This is an established consequence of the output metric, not another speedup claim. The [interpretation chapter](interpretation.md) explains subsequent function-evaluation costs and the limitations for sharp thresholds, individual energy levels, and relative thermodynamic errors. Further source-specific comparisons appear in [related work](../references/related_work.md).
