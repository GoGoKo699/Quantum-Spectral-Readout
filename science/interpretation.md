# Interpretation and boundaries

[Overview](../README.md) · [Model](model.md) · [Resources](resources.md) · [Proof](multilevel_algorithm.md)

## Why source access matters

A laboratory source can supply a new state while offering no way to reverse its preparation. The mathematical copy interface captures that distinction. It permits a mixed state and does not require a preparation circuit or access to the environment that purifies it.

The algorithm still needs to retain each system during several phase-estimation measurements. Those measurements are diagonal in the same spectral decomposition. Their outcomes have the law of conditionally independent observations of one common latent eigenphase, which determines an energy. In the block-encoding construction this is a phase of the enlarged walk. The coarse and fine estimates therefore concern the same latent energy, even if the incoming state has coherence between energies. Resetting the source between the two estimates replaces this coupling by independent energies and can leave a variance of order one.

This mechanism is proved at the level of the complete measurement instrument in [Upper bound, Section 3](multilevel_algorithm.md#3-exact-coupling-from-retaining-the-same-system). It gives a useful access-model result: reversible source preparation is unnecessary for the optimal worst-case Hamiltonian precision exponent. It does not establish a practical advantage for a particular apparatus or a universal lower bound on coherent evolution depth.

## Why multiple resolutions help

A straightforward strategy estimates every sampled energy to the final resolution. In the normalized model, one fine energy measurement costs order $`\epsilon^{-1}`$ evolution, up to precision logarithms. Estimating a general one-dimensional probability law from independent exact samples takes order $`\epsilon^{-2}`$ samples for constant-probability Wasserstein accuracy. Combining those choices gives a direct baseline of order $`\epsilon^{-3}`$ total evolution.

The multilevel construction spends most copies on cheap coarse information and progressively fewer on expensive corrections. At resolution $`h_\ell=2^{-\ell}`$, a coupled pair of CDF indicators differs only between its two readout values. Exactly,

```math
\int_{-1}^{1}
\left|\mathbf1\{x\ge Z_\ell\}
-\mathbf1\{x\ge Z_{\ell-1}\}\right|^2dx
=|Z_\ell-Z_{\ell-1}|.
```

The expected right-hand side is $`O(h_\ell)`$, while experiment cost is $`O(h_\ell^{-1})`$. This is the critical multilevel balance that removes one inverse-precision factor from the direct baseline. Multilevel distribution estimation itself is established methodology; the [related-work comparison](../references/related_work.md) identifies the antecedents and the exact specialization made here.

The signed corrections need not form a probability distribution. That is why valid reconstruction is part of the theorem. Isotonic CDF projection enforces nonnegative masses and unit total mass, with only a constant-factor increase in Wasserstein error. The [exact rational implementation](../verification/exact_cdf_projection.py) and an independent linear program test this step on a deliberately nonmonotone example.

## What can be learned from the returned measure

Once $`W_1(\widehat\mu,\mu)\le\epsilon`$, all Lipschitz spectral observables obey their corresponding deterministic error bound on that same event. There is no new union bound for each later query.

| Spectral question | Consequence on $`[-1,1]`$ |
|---|---|
| Mean energy, $`f(x)=x`$ | Absolute error at most $`\epsilon`$ |
| Moment $`f(x)=x^k`$, integer $`k\ge1`$ | Absolute error at most $`k\epsilon`$ |
| A smoothed interval indicator with slope at most $`1/w`$ | Absolute error at most $`\epsilon/w`$ for the smoothed quantity |
| A clipped energy penalty with slope at most $`L`$ | Absolute error at most $`L\epsilon`$ |
| $`f(x)=e^{-\beta x}`$, $`\beta\ge0`$ | Absolute error at most $`\beta e^\beta\epsilon`$ |

These bounds follow directly from the Lipschitz constants, not from additional quantum measurements. A smoothed projector differs from a sharp projector in its transition region; without a promise on spectral mass there, the table does not control that additional bias. For large $`\beta`$, the exponential Lipschitz constant can make the final bound weak. A relative partition-function or rare-event guarantee requires information beyond fixed absolute Wasserstein accuracy.

For an output supported on $`J+1`$ grid points, one later expectation is the weighted sum of $`J+1`$ function evaluations. Thus reuse requires classical work, including the requested precision and cost of evaluating $`f`$; it requires no further quantum queries. Function-approximation error adds to the displayed Wasserstein bound.

The output is source weighted. For $`\rho=I_d/d`$, the exponential integral equals the partition function divided by $`d`$. For a general source, it is $`\mathrm{Tr}[\rho e^{-\beta H}]`$. Those are different physical quantities. Reusable spectral information is an inherited motivation for classical spectral estimation, including Somma's 2019 formulation; it is not an additional novelty claim here.

## Why the lower bound has a dimension threshold

The hard Hamiltonians contain $`m=\Theta(\min\{d,\epsilon^{-1}\})`$ ordered spectral groups. Each group has an independently hidden displacement of order $`\epsilon`$. A good classical probability output reveals enough of those displacements to solve approximate oracle interrogation.

The resulting resource law is

```math
\Omega(m/\epsilon)
=\Omega\!\left(\frac{\min\{d,\epsilon^{-1}\}}{\epsilon}\right).
```

When dimension grows with inverse precision, many distinguishable spectral locations must be learned. At fixed dimension, this construction gives only the linear inverse-precision law multiplied by $`d`$. It does not contradict single-parameter Heisenberg scaling. The eigenbasis is known in this hard family, so eigenvector learning does not cause the obstruction.

The source-copy lower bound uses a separate family: two nearby unknown weights on a fixed known two-level Hamiltonian. Its $`\Omega(\epsilon^{-2})`$ scaling is the ordinary sampling obstruction. Combining the two arguments establishes coordinatewise minimax optimality, not a joint resource frontier for one input.

## Physical energy units and normalization

Suppose a physical Hamiltonian $`A`$ has known bound $`\|A\|\le B`$ with $`B\gt 0`$, and the desired Wasserstein error in energy units is $`\Delta`$. Set $`H=A/B`$ and $`\epsilon=\Delta/B`$, in the theorem's regime $`0\lt \Delta/B\le1/4`$. Pushing the returned measure forward by multiplication by $`B`$ gives physical error at most $`\Delta`$.

For evolution access, a normalized call $`e^{-itH}`$ is a physical call $`e^{-i(t/B)A}`$. In units with $`\hbar=1`$, the achieved scalings become

```math
N_\rho=O((B/\Delta)^2),\qquad
T_{\rm physical}
=O\!\left(\frac{B}{\Delta^2}\log^3(B/\Delta)\right),
```

with $`O(\Delta^{-1})`$ maximum interaction time per retained specimen. This is a unit conversion, not a free physical amplification of the Hamiltonian. An implementation may have overhead that depends on duration, requested accuracy, system size, or control strength.

For a supplied block encoding of $`A/\alpha`$, the query bound instead uses $`\epsilon=\Delta/\alpha`$ in the regime $`0\lt \Delta/\alpha\le1/4`$ and becomes $`O((\alpha/\Delta)^2\log^3(\alpha/\Delta))`$. Query cost and physical interaction time are distinct. The comparison with density-operator spectrum lower bounds depends critically on this normalization; [Lower bounds, Section 10](lower_bounds.md#10-detailed-comparison-with-wangs-2026-spectrum-lower-bound) works through it explicitly.

## Boundaries of the claim

The proved theorem covers arbitrary finite-dimensional Hermitian contractions, arbitrary fixed independent sources, supplied controlled evolution or exact normalized block encodings, and a classical Wasserstein output. It supplies explicit finite-operation error budgets and an exact probability reconstruction.

The following remain outside the result:

- A tight joint frontier between source calls, Hamiltonian resources, and coherent duration.
- A matching small-dimension upper for every source model, or a theorem for expected stopping costs.
- Guaranteed accuracy for sharp thresholds, rare-event relative errors, or general low-temperature relative quantities.
- Correlated source sequences, approximate block encodings specified only by top-block error, or unrestricted stability under noncommuting Hamiltonian perturbations.
- A graph-local query improvement, a QRAM advantage, or a practical hardware speedup.

The generic coherent-source Hamiltonian upper exponent is inherited from the prior spectral-sampling and distribution-estimation components discussed in [Related work](../references/related_work.md). The current note's consequence is the fresh-copy realization and the matched normalized-interface lower exponent, with those distinctions preserved.
