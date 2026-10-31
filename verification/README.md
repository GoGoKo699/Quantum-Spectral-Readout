# Finite verification

These scripts check selected algebraic identities, couplings, and reconstruction steps used in the spectral-readout analysis. They use small synthetic matrices and fixed random seeds. The checks support the stated finite examples; the mathematical proofs establish the asymptotic resource bounds.

## Run

Use Python 3.11 or later. The recorded environment used Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0; requirements.txt pins the two observed dependency versions.

Install the requirements in your chosen Python environment, then run the entry point. Both commands accept an absolute repository path and can be issued from any working directory:

```sh
python -m pip install -r /path/to/repository/verification/requirements.txt
python /path/to/repository/verification/run_all.py
```

The entry point runs both checks using the same Python interpreter. It writes fresh JSON reports and run_manifest.json under verification/results/, which is ignored by Git. The manifest records dependency versions, source-file hashes, report hashes, and each check's status. A failed assertion or missing report produces a nonzero exit code. Run without Python's -O option or PYTHONOPTIMIZE: assertions are required and the scripts reject optimized execution.

Each check can also be run separately. Its default output location is the same results/ directory, independently of the current working directory. An optional --output argument selects another report path.

```sh
python /path/to/repository/verification/validate_spectral_coupling.py
python /path/to/repository/verification/validate_spectral_lower.py
```

## Files and scope

| File | What it checks or supplies |
|---|---|
| validate_spectral_coupling.py | Sequential phase-estimation Kraus probabilities on a retained pure or mixed source; selected six-measurement paths; retained versus reset coupling examples; median-of-three resolution examples; and probability reconstruction from a signed empirical CDF. |
| exact_cdf_projection.py | An exact rational implementation of unweighted L1 isotonic regression for a uniform grid, followed by conversion to nonnegative normalized masses. The coupling check compares its objective with a SciPy linear program. |
| validate_spectral_lower.py | Small hypercube adversary commutators, unequal multiplicities, arbitrary-output quantile decoding examples, the edge-fidelity inequality on a finite grid, weak source-purifier completions, and a counterexample to an incorrect factor of two in the decoder bound. |
| expected/ | Two actual reports from the recorded verification runs, retained as reproducibility snapshots. |
| run_all.py | Runs the checks, verifies their assertion-summary fields, and records a fresh manifest. |

The coupling example uses a five-dimensional synthetic unitary with a prescribed spectral cosine relation. It checks the retained-source measurement identities; it does not compile a generic block encoding or simulate a quantum device. Its deliberately small-sample CDF example tests projection and positivity, not the theorem's asymptotic sample allocation.

The lower-bound examples include dimensions 1, 5, and 7, 1,800 generated probability-measure outputs, and 1,002,001 edge-fidelity grid pairs. These finite examples cannot prove the universal adversary inequality or its asymptotic scaling. The midpoint counterexample does establish the failure of the specified doubled decoder charge.

The matrices and optimization diagnostics use floating-point arithmetic. Only the rational CDF projector and its exact mass/objective calculations use fractions. Its O(K log K) operation count is the comparison/heap-operation count, not a claim that arbitrary-size integer arithmetic has constant cost. The implementation applies to equal-width CDF intervals; it does not implement the general weighted-grid algorithm.

The projector follows the unweighted specialization in Section 9 of Günter Rote, *Isotonic Regression by Dynamic Programming*, SOSA 2019, [doi:10.4230/OASIcs.SOSA.2019.1](https://doi.org/10.4230/OASIcs.SOSA.2019.1).

## Interpreting the recorded reports

The expected/ files are preserved observations, not exact golden outputs for every platform. Floating-point residues can vary with numerical libraries and BLAS implementations. A linear program can also choose a different minimizer when the optimum is nonunique. The scripts assert structural identities and inequalities with stated tolerances and verify the exact rational projection objective against the LP objective; run_all.py relies on those assertions rather than requiring byte-for-byte equality with a recorded report.

The suite does not establish novelty, provide experimental hardware evidence, validate a noise model, or prove a joint source/time tradeoff. It also does not certify the claimed theorems through a formal proof assistant.
