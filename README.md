# Quantum Spectral Readout

**A classical energy distribution from independent quantum source copies, with separately charged source and Hamiltonian resources.**

Given a Hermitian operator $`H`$ with $`\|H\|\le1`$ and a source state $`\rho`$, the target is the complete source-weighted energy law

```math
\mu_{H,\rho}(B)=\mathrm{Tr}[\rho E_H(B)].
```

The source may be mixed and may have coherence between different energies. The algorithm receives fresh independent copies; it needs no source-preparation unitary, inverse, purification, or reflection. It returns a finite classical probability measure $`\widehat\mu`$ whose Wasserstein distance from the true law is at most $`\epsilon`$, with probability at least $`2/3`$.

## Main result

The protocol uses repeated phase measurements on each retained specimen to couple coarse and fine energy estimates. A multilevel estimator combines those pairs, and an exact isotonic projection converts its signed intermediate output into normalized, nonnegative probabilities.

For rational $`0<\epsilon\le1/4`$, the proved upper bounds are:

| Resource | Achieved bound |
|---|---:|
| Independent copies of $`\rho`$ | $`O(\epsilon^{-2})`$ |
| Total controlled-Hamiltonian interaction time | $`O(\epsilon^{-2}\log^3(1/\epsilon))`$ |
| Exact normalized block-encoding queries, as an alternative interface | $`O(\epsilon^{-2}\log^3(1/\epsilon))`$ |
| Evolution time or block queries while retaining one specimen | $`O(\epsilon^{-1})`$ |
| Classical output size | $`O(\epsilon^{-1}\log^2(1/\epsilon))`$ bits |
| Classical processing | $`\widetilde O(\epsilon^{-2})`$ bit operations |

Controlled evolution is explicitly supplied, and time means the sum of absolute interaction durations across all experiments. Block-encoding queries are a different access model, not an identification of physical time with gate count. State preparation, oracle construction, known gates, workspace, and finite-accuracy implementation have separate accounting in the [model](science/model.md) and [upper-bound proof](science/multilevel_algorithm.md).

The classical processing bound is beyond reading the encoded tolerance; the tolerance may have an arbitrarily long input representation.

A complementary lower bound holds even when the source is known and freely reversible:

```math
T,\ Q_H=\Omega\!\left(\frac{\min\{d,\epsilon^{-1}\}}{\epsilon}\right).
```

Thus the Hamiltonian precision exponent is optimal, up to logarithmic factors, in the worst case when $`d=\Omega(\epsilon^{-1})`$. A separate two-level family proves $`\Omega(\epsilon^{-2})`$ source copies are necessary. These are coordinatewise worst-case statements from different hard families; they do not establish a joint tradeoff for every input. The [lower-bound chapter](science/lower_bounds.md) treats arbitrary classical probability outputs, inverse queries, adaptive controls, and summed parallel interaction costs.

## What the distribution answers

On the same success event, every 1-Lipschitz function $`f`$ obeys

```math
\left|\int f\,d\widehat\mu-\mathrm{Tr}[\rho f(H)]\right|\le\epsilon.
```

The classical output can therefore answer later smooth energy questions without further quantum queries. This interpretation and the reusable-output feature are established ideas in spectral estimation. Wasserstein accuracy does **not** by itself guarantee accurate sharp spectral projectors, rare-event relative errors, or low-temperature relative partition functions. The [interpretation](science/interpretation.md) explains both the useful observables and these limitations.

## Contribution and relationship to prior work

The upper proof specializes established phase estimation, nondemolition measurements, distribution-valued multilevel Monte Carlo, and isotonic regression to the fresh-copy interface. The generic coherent-source Hamiltonian-query upper exponent is already implied by Li–Liao–Yang's 2026 spectral-sampling and distribution-estimation components. The result here supplies an explicit fresh-copy realization with source and evolution accounting, together with a normalized-interface lower bound against stronger coherent algorithms.

The lower-bound machinery is standard. Its task-specific part is an ordered spectral packing, a decoder for arbitrary Wasserstein outputs, and a weak block-encoding completion that fixes the access normalization. The [source-by-source comparison](references/related_work.md) credits inherited results and treats the closest 2026 spectrum-estimation and multilevel-estimation work. No exhaustive priority certification or practical hardware advantage is claimed.

## Read the research

| Page | What it establishes |
|---|---|
| [Task and access models](science/model.md) | Exact input, output, success, normalization, and resource conventions |
| [Fresh-copy multilevel algorithm](science/multilevel_algorithm.md) | Instrument coupling, uniform error, valid probability reconstruction, finite precision, and general block encodings |
| [Lower bounds](science/lower_bounds.md) | Dimension-sensitive Hamiltonian obstruction and separate source-access obstructions |
| [Resource comparison](science/resources.md) | Achieved costs and comparisons under matched metrics and interfaces |
| [Interpretation and boundaries](science/interpretation.md) | Physical meaning, observable queries, energy units, and unsupported extensions |
| [Related work](references/related_work.md) | Primary sources, exact locations, inherited ingredients, and remaining distinctions |
| [Reproducible verification](verification/README.md) | Finite instrument, transport, projection, and oracle checks |

The repository is a mathematical research note with executable finite checks. The checks test identities and conventions; the analytical proofs establish the asymptotic statements. They do not certify novelty or simulate a fault-tolerant implementation.

## Run the checks

```bash
python -m pip install -r verification/requirements.txt
python verification/run_all.py
```

The standard-library exact CDF projector can also be used independently. See the [verification guide](verification/README.md) for outputs, expected results, and what each check covers.

## Purpose and contact

This repository serves as a record of the work and a guide for the author's self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).

Code and text are distributed under the [MIT license](LICENSE).
