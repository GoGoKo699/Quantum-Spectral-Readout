# Related work

The result concerns full classical reconstruction of the weighted energy law $`\mu_{H,\rho}`$ under explicitly charged Hamiltonian access. The [model](../science/model.md) separates physical source copies from reversible purified preparation. The [algorithm](../science/multilevel_algorithm.md) attains $`\widetilde O(\epsilon^{-2})`$ Hamiltonian cost with $`O(\epsilon^{-2})`$ physical copies; the [lower bounds](../science/lower_bounds.md) show that the Hamiltonian precision exponent is optimal when $`d=\Omega(\epsilon^{-1})`$, even with stronger coherent source access. A coherent-source upper with that Hamiltonian exponent already follows from prior work.

This comparison attributes the established ingredients and distinguishes the output metric, access assumptions, and charged resources. Bibliographic metadata and versioned manuscript URLs are provided in [references.bib](references.bib). The [resource chapter](../science/resources.md) derives the same-target protocol table.

## 1. Closest algorithmic comparisons

| Source | Established result or method | Relationship to the present theorem |
|---|---|---|
| [Li, Liao and Yang, arXiv:2608.22769v2](https://arxiv.org/pdf/2608.22769v2), Lemmas 35–37 | Coherent spectral sampling and classical $`W_1`$ distribution learning from a coherent experiment | Their components already imply the generic coherent-source $`\widetilde O(\epsilon^{-2})`$ Hamiltonian upper. The distinction here is obtaining that exponent from physical copies and proving the matching charged-Hamiltonian lower bound. |
| [Lin and Tong, PRX Quantum 3, 010318 (2022)](https://arxiv.org/pdf/2102.11340v2), Sections 2–3 | Mixed-source approximate CDF, one-ancilla Fourier measurements, and randomized estimation inspired by unbiased multilevel Monte Carlo | Their published variance and expected-time bounds directly specialize to full-$`W_1`$ cost $`\widetilde O(\epsilon^{-3})`$. Retaining one source across resolutions supplies a different coupling for the quadratic-cost consequence. |
| [Giles, Nagapetyan and Ritter, SIAM/ASA J. Uncertainty Quantification 3, 267–295 (2015)](https://people.maths.ox.ac.uk/gilesm/files/juq_15.pdf), Sections 2.1–2.3 | Multilevel approximation of entire distribution functions and densities | Whole-CDF telescopes and sample allocation are inherited. The integrated-indicator identity gives a short specialization to atomic spectral laws under $`W_1`$ loss. |
| [van Apeldoorn, TQC 2021](https://doi.org/10.4230/LIPIcs.TQC.2021.9), Definition 1 and Theorem 9 | Multidimensional amplitude estimation with a probability-preparation unitary, inverse, controls, and arbitrary garbage | This is the distribution-estimation primitive used in the coherent comparator. Its reversible-source assumptions must be retained; its query exponents do not require QRAM. |
| [Somma, New J. Phys. 21, 123025 (2019)](https://arxiv.org/pdf/1907.11748v2), Eqs. (2), (16)–(17) | Classical soft-bin energy estimates from source-copy time-series data; later evaluation of spectral functions | Reusable classical spectral output and subsequent function evaluation are established. Its soft-bin $`\ell_1`$ guarantee differs from $`W_1`$ and should be converted before comparing costs. |

### Coherent learning and graph implementation

Li–Liao–Yang's Lemma 37 applies to a general coherent experiment with a one-dimensional classical output. Its use after a precision-$`\epsilon`$ spectral sampler produces the generic $`\widetilde O(\epsilon^{-2})`$ Hamiltonian upper. Their advertised graph-local upper is $`\widetilde O(\epsilon^{-3})`$ because the sampler carries an additional graph implementation factor $`\sqrt\Delta`$, with $`\Delta=\Theta(\epsilon^{-2})`$. Their graph-local lower bound addresses that graph interface. The present normalization-one block-encoding and total-evolution statements do not close the graph-local gap.

### CDF estimation and the multilevel bridge

Lin–Tong already treats arbitrary mixed sources and explicitly discusses unbiased-multilevel inspiration. Their Section 3 gives pointwise variance $`\sigma^2`$ at expected evolution cost $`O(K\log K/\sigma^2)`$ for Fourier degree $`K`$. Choosing $`K=\widetilde O(\epsilon^{-1})`$ and $`\sigma=\Theta(\epsilon)`$ gives the direct full-law comparison in [resources](../science/resources.md). Their ground-energy Heisenberg guarantee has a different target and ground-overlap parameter.

Giles–Nagapetyan–Ritter analyzes whole-distribution multilevel approximations under assumptions including density smoothness and a supremum-norm target. The present proof uses

```math
\int\operatorname{Var}
\bigl(\mathbf1\{Y_\ell\leq x\}
-\mathbf1\{Y_{\ell-1}\leq x\}\bigr)\,dx
\leq\mathbb E|Y_\ell-Y_{\ell-1}|
```

to control integrated CDF error without requiring a density. The quantum-specific step identifies an exact common-eigenphase joint law for sequential readouts on one retained source, including mixed states with energy coherence. The multilevel estimator itself remains an application of established methodology.

Somma's soft-bin vector controls later averages through bounds involving the size of a function and its derivative. Its published time-series analysis charges approximately $`\epsilon^{-5}`$ preparations and $`\epsilon^{-6}`$ evolution for the stronger soft-bin $`\ell_1`$ target. Localizing each soft bin within $`O(\epsilon)`$ of its center and projecting to probabilities yields a sufficient $`O(\epsilon)`$ Wasserstein guarantee. Those sufficient costs are a weak competitive baseline; the elementary fine-QPE and Lin–Tong derivations provide sharper comparisons for the requested metric.

## 2. Spectral filters and energy-distribution diagnostics

[Roggero, Phys. Rev. A 102, 022409 (2020)](https://arxiv.org/pdf/2004.04889v2) constructs a Gaussian integral transform of the spectral density using qubitization and develops spectral-approximation error criteria. Its approximately inverse-resolution circuit length and its separate sample complexity, displayed in Table I, must both be charged. Filter circuit length alone is not the total cost of a classical approximation to an arbitrary full spectral law. Its kernel-based metric also requires an explicit conversion before comparing it to $`W_1`$.

[Fomichev et al., PRX Quantum 5, 040339 (2024)](https://arxiv.org/pdf/2310.18410v2) uses energy distributions to assess quantum-chemistry initial states. Section IV B.3 and Appendix G discuss coarse QPE, shifted grids, and kernel-density reconstruction. These establish the value of energy-distribution diagnostics and coarse readout. Those sections do not provide the retained coarse/fine coupling and arbitrary-atomic-$`W_1`$ complexity proved here. Initial-state preparation costs remain meaningful in both settings.

[Goh and Koczor, Phys. Rev. Research 8, 013250 (2026)](https://arxiv.org/pdf/2407.03414v2) estimates the density of states of fermionic systems, including chosen particle-number subspaces, by evolving simple random states and processing Fourier data. The method recovers the relevant trace in expectation and uses Gaussian broadening to accommodate finite evolution windows. Its normalization, random-state variance, measurement noise, and broadening resolution are explicit parts of that task. The analysis does not state the present uniform atomic-$`W_1`$ total-evolution law for an arbitrary supplied source. No quantitative advantage over its concrete physical examples is asserted here.

## 3. Other multilevel and structured spectral tasks

[Chen, Gao, Li, Wang and Wang, ICALP 2026](https://doi.org/10.4230/LIPIcs.ICALP.2026.58) introduces quantum multilevel estimation for scalar distribution functionals such as $`\sum_i f(p_i)`$. Its model and main constructions, Sections 1.1 and 3 and Theorems 12–13, use purified probability access, nondestructive singular-value discrimination, and adaptive estimation over dyadic probability scales. Thus multiscale spectral processing and nondestructive reuse are already established algorithmic tools. Its scalar-functional output and probability-preparation oracle differ from learning an entire energy law from physical source copies. The current result does not supply improved entropy-functional bounds for that access model.

[Chapman et al., arXiv:2610.02183v1](https://arxiv.org/pdf/2610.02183v1) introduce SPICES for single-particle spectral estimation. Definitions 1–2 and Theorem 3 concern a protected set of noninteracting modes hidden by a global unitary, with a separate spectator Hamiltonian. The method uses a supplied number observable, Gibbs-state access, and contour/signal assumptions to recover the single-particle energy distribution in Wasserstein distance. Its target is a quasiparticle energy comb, rather than the full weighted many-body measure of an arbitrary pair $`(H,\rho)`$. The additional physical structure can make this a useful and different task; no comparison of practical performance is implied by the generic oracle theorem.

## 4. Density-state spectrum lower bounds

[Wang, arXiv:2608.02600v4](https://arxiv.org/pdf/2608.02600v4), Theorem 5.15, establishes a nearly tight sample lower bound for learning a density operator's ordered eigenvalue vector in total variation. Section 1.2 specifies both physical-copy and purified-query access, and query consequences follow through sample-to-query lifting. This is a closely related spectrum-estimation lower bound and must not be dismissed merely because its metric is written as total variation.

Indeed, for density operators $`\tau,\sigma`$ define

```math
\nu_\tau=\frac1d\sum_i\delta_{d\lambda_i(\tau)-1}.
```

Ordering the eigenvalues gives the exact identity

```math
W_1(\nu_\tau,\nu_\sigma)
=\sum_i|\lambda_i(\tau)-\lambda_i(\sigma)|
=2\operatorname{TV}(\lambda(\tau),\lambda(\sigma)).
```

The obstruction to an immediate transfer is the input normalization. On a family promised to satisfy $`\|d\tau-I\|\leq M`$, set $`H_\tau=(d\tau-I)/M`$. Then

```math
e^{-itH_\tau}=e^{it/M}e^{-i\tau\,dt/M}.
```

A purifier supplies a block encoding of $`\tau`$ at constant query cost; it does not supply normalized evolution under $`H_\tau`$ at the same cost. The standard simulation conversion incurs the scale $`d/M`$. In the corresponding attempted lower-bound transfer, this factor cancels the leading dimension gain. A new conversion or a stronger reduction would need its own argument.

[Chen–Wang–Zhang, arXiv:2512.01971v1](https://arxiv.org/pdf/2512.01971v1), Definition 1.1 and Corollary 1.2, makes the relevant normalization explicit: its block-query lifting applies to a top block $`\tau/\alpha`$ with $`\alpha\geq1`$. The original [Wang–Zhang sample-to-query lifting theorem](https://doi.org/10.1137/24M1638616) likewise concerns a density-operator encoding. Neither grants a factor-$`d`$ amplification at unit cost. The detailed comparison, including conversion of arbitrary classical measure outputs to ordered spectrum estimates, is in [the lower-bound chapter](../science/lower_bounds.md). It is an analysis of these reductions, not a universal impossibility theorem for every conversion.

## 5. Established proof and implementation tools

The phase-estimation instrument uses the standard Fourier construction of [Cleve, Ekert, Macchiavello and Mosca](https://arxiv.org/pdf/quant-ph/9708016v1). The general-unitary block-encoding reduction is an instance of [Low and Chuang's qubitization](https://doi.org/10.22331/q-2019-07-12-163). The integrated-CDF identity is due to [Vallender](https://doi.org/10.1137/1118101), and the finite probability projection uses standard $`L^1`$ isotonic regression, for which [Rote](https://doi.org/10.4230/OASIcs.SOSA.2019.1) gives an efficient priority-queue implementation.

The lower bound reduces spectral reconstruction to approximate [oracle interrogation](https://arxiv.org/pdf/quant-ph/9805006v3) and uses standard [positive-weight adversary progress](https://doi.org/10.1006/jcss.2002.1826). The continuous-time progress calculation follows the Hamiltonian-oracle approach of [Yonge-Mallo](https://arxiv.org/pdf/1108.2479v1). Binary discrimination and hybrid arguments supply the separate source lower bounds. None of these general techniques is introduced here.

The specialized result is the resource consequence for this output task: a retained physical source supplies the needed resolution coupling, the resulting signed CDF can be returned as an explicit probability measure, and an ordered spectral family forces the stated charged-Hamiltonian cost even for stronger coherent strategies. Reusable output and simultaneous Lipschitz control are established benefits of Wasserstein reconstruction; their practical meaning and limitations are explained in [interpretation](../science/interpretation.md).
