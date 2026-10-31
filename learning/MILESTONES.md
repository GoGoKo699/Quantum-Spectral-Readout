# Thirty milestones for Quantum Spectral Readout

[Overview](../README.md) · [Childs bridge](CHILDS_BRIDGE.md) · [Scientific model](../science/model.md) · [Verification](../verification/README.md)

A source repeatedly supplies a quantum state, and controlled evolution under its Hamiltonian is available. The goal is to return a complete classical energy distribution while charging both source specimens and Hamiltonian interactions. The central mechanism joins measurements made at different resolutions on the same retained specimen. The lower bound asks how much interaction any successful reconstruction must use, even with stronger coherent access.

The single educational anchor is **Andrew M. Childs, *Lecture Notes on Quantum Algorithms*, 17 April 2025**: [author page](https://www.cs.umd.edu/~amchilds/qa/) and [author PDF][childs]. Section and page references below use that revision's printed pagination. The [Childs bridge](CHILDS_BRIDGE.md) translates the anchor's algorithms into this project's notation and supplies the additional mixed-state, probability, and reconstruction arguments. Research papers cited by the scientific chapters retain their role as sources for established methods.

This map has exactly **30 project-defined milestones** in two phases:

- **[M01–M12: background and preliminaries](#phase-i-foundations-and-local-tools).** Twelve milestones connect states, measurements, probability, access models, and distinguishability into the framework needed for the problem.
- **[M13–M30: narrative and innovation](#phase-ii-from-retained-measurements-to-a-complete-resource-law).** Eighteen milestones assemble the retained-source upper bound, the Hamiltonian and source lower bounds, and their scientific interpretation.

Within each phase the route moves from individual objects and mechanisms to their combined consequence. Dependencies name earlier milestones needed for that step; the canonical science links contain the full derivations. M13–M22 form the constructive route, M23–M28 form the lower-bound route, and M29–M30 integrate the comparisons and limits. The map covers the project's conceptual structure; technical details remain in the linked proofs.

## Phase I. Foundations and local tools

**Phase: background and preliminaries — M01–M12.** The first objects are states, energies, and measurement outcomes. Probability and query-complexity tools then make it possible to formulate one estimation task with both an algorithm and a lower bound.

### M01. States and mixtures

**Central question.** What information does a density operator describe when a source supplies repeated specimens?

**Understanding target.** Distinguish a pure state, a mixed state, and a purification. Recognize that fresh independent copies form a product input, while identical one-copy marginals alone do not guarantee independence. The source may also have coherence between different energy eigenspaces.

**Dependencies and story role.** None within this map. This establishes the physical input before introducing its energy statistics.

**Conceptual connection.** A physical specimen can be available even when the process that prepared it has no accessible inverse.

**Sources.** [Model §§1 and 3](../science/model.md#1-the-mathematical-input); [fresh-copy interface](../science/model.md#fresh-independent-copies). [Childs §§1.1–1.2, p. 1][childs] supplies the state-vector and circuit entry point; the mixed-state extension is developed in the [bridge §2](CHILDS_BRIDGE.md#2-notation-and-access-models).

### M02. Spectral projectors and weighted energy laws

**Central question.** How do a Hamiltonian and a source state together determine an energy distribution?

**Understanding target.** Read the spectral decomposition of a Hermitian operator and identify the mass of an energy eigenspace as $`\mathrm{Tr}(\rho P_\lambda)`$. Include degeneracies in its projector. Relate averages of functions of energy to $`\mathrm{Tr}[\rho f(H)]`$, and identify the normalized density of states as the special source $`I_d/d`$.

**Dependencies and story role.** [M01](#m01-states-and-mixtures). This turns the state description into the observable probability law that the project reconstructs.

**Conceptual connection.** The same Hamiltonian can produce different energy laws for different sources; learning the law does not require learning its eigenvectors.

**Sources.** [Model §§1–2](../science/model.md#1-the-mathematical-input); [observable interpretation](../science/interpretation.md#what-can-be-learned-from-the-returned-measure). [Childs §27.5, pp. 136–137][childs] connects Hermitian observables with dynamical measurement.

### M03. Controlled evolution and an energy reference

**Central question.** Why does absolute energy readout require an explicitly supplied controlled operation?

**Understanding target.** Distinguish an uncontrolled unitary channel from controlled evolution. A scalar energy shift disappears from the uncontrolled channel but becomes a measurable relative phase on a control. Interpret total interaction cost as the sum of absolute durations, including inverse and parallel calls.

**Dependencies and story role.** [M01](#m01-states-and-mixtures), [M02](#m02-spectral-projectors-and-weighted-energy-laws). This specifies which physical access makes the target identifiable and what that access costs.

**Conceptual connection.** The oracle assumption is part of the estimation problem, rather than an operation inferred from possession of an unknown unitary.

**Sources.** [Controlled-evolution model](../science/model.md#controlled-evolution); [lower-bound interaction convention](../science/lower_bounds.md#11-hamiltonian-interaction-time). [Childs §4.3, p. 19][childs] uses the controlled powers needed for phase estimation.

### M04. Measurement probabilities and state changes

**Central question.** What must be specified to reason about several measurements on one specimen?

**Understanding target.** Distinguish an outcome probability from the corresponding operation on the retained state. Interpret a Kraus operator as describing both pieces. Separate a state conditioned on a recorded outcome from the state obtained when that record is ignored.

**Dependencies and story role.** [M01](#m01-states-and-mixtures), [M03](#m03-controlled-evolution-and-an-energy-reference). This supplies the language needed to analyze reuse of a specimen without assuming that measurements leave its conditional state unchanged.

**Conceptual connection.** Repeated readout is governed by a measurement instrument; a one-shot probability formula does not by itself determine the joint outcome law.

**Sources.** [Upper bound §2.1](../science/multilevel_algorithm.md#21-the-phase-estimation-instrument) and [§3](../science/multilevel_algorithm.md#3-exact-coupling-from-retaining-the-same-system); [bridge §4](CHILDS_BRIDGE.md#4-why-retaining-one-copy-couples-two-resolutions). Childs's circuit measurement discussion in [§1.2, p. 1][childs] is an entry point; the general mixed-state instrument is supplied locally.

### M05. Fourier phase estimation

**Central question.** How do controlled powers turn an eigenphase into a finite clock outcome?

**Understanding target.** Connect the clock superposition, controlled powers, inverse Fourier transform, and measurement. Interpret the finite geometric sum that determines the output probabilities. Distinguish clock resolution from the charged sum of evolution durations or elementary walk queries.

**Dependencies and story role.** [M03](#m03-controlled-evolution-and-an-energy-reference), [M04](#m04-measurement-probabilities-and-state-changes). This supplies the quantum readout primitive used at every resolution.

**Conceptual connection.** Increasing the number of clock bits creates finer phase resolution through longer or more numerous oracle interactions.

**Sources.** [Upper bound §2.1](../science/multilevel_algorithm.md#21-the-phase-estimation-instrument); [Childs §4.3, p. 19, especially Eq. (4.17)][childs]. The [bridge §3](CHILDS_BRIDGE.md#3-from-an-eigenphase-to-a-weighted-spectral-law) connects this primitive to the energy law.

### M06. Tails, medians, and mean error

**Central question.** Why is a small typical readout error insufficient for the later transport estimate?

**Understanding target.** Relate a nonnegative error's expectation to its tail probabilities. Understand how the median of three conditionally independent readouts suppresses large errors, and why a uniform first-moment estimate is useful even when the true spectrum has atoms or tightly clustered energies.

**Dependencies and story role.** [M05](#m05-fourier-phase-estimation). This introduces the probabilistic guarantee needed to transport approximate outcomes back to their latent energies.

**Conceptual connection.** A constant number of readouts can change the decay of the error tail without changing the inverse-resolution cost exponent.

**Sources.** [Upper bound §2.3](../science/multilevel_algorithm.md#23-median-of-three), with the tail estimate in [§2.1](../science/multilevel_algorithm.md#21-the-phase-estimation-instrument). [Childs §4.3][childs] supplies phase-estimation background; the uniform median first-moment argument is proved in the project.

### M07. CDFs, quantiles, and Wasserstein distance

**Central question.** What does it mean to approximate a whole energy distribution when its atoms may move slightly?

**Understanding target.** Relate a probability measure to its cumulative distribution function and generalized quantile. Interpret Wasserstein distance as transported mass times distance, and use its integrated-CDF and quantile descriptions. Distinguish this loss from total variation and from relative accuracy for rare events.

**Dependencies and story role.** [M02](#m02-spectral-projectors-and-weighted-energy-laws), [M06](#m06-tails-medians-and-mean-error). This supplies the common error metric for the algorithm, output reconstruction, and lower-bound decoder.

**Conceptual connection.** Nearby atomic energies can be close in transport distance even when their point-mass distributions are maximally separated in total variation.

**Sources.** [Model §2](../science/model.md#2-a-completed-classical-output); [the transport proof in lower bounds §3](../science/lower_bounds.md#3-decoding-any-classical-probability-output); [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure). This transport material is an addition to the Childs route.

### M08. Independent samples and variance

**Central question.** How does averaging independent observations control a distribution estimate?

**Understanding target.** Interpret an empirical CDF as an average of threshold indicators. Connect independence with addition of variances, and distinguish expected estimation error from a constant-probability guarantee. Recognize the difference between independent source experiments and several measurements within one experiment.

**Dependencies and story role.** [M01](#m01-states-and-mixtures), [M07](#m07-cdfs-quantiles-and-wasserstein-distance). This explains the sampling cost against which multilevel allocation is compared.

**Conceptual connection.** The source-copy count and the cost of each measurement multiply in a naive fine-resolution protocol, so both resources need separate accounting.

**Sources.** [Independent fine-QPE baseline](../science/resources.md#2-independent-fine-qpe-baseline); [upper bound §5](../science/multilevel_algorithm.md#5-multilevel-cdf-estimator-and-variance-addition); [probability bridge](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure).

### M09. Coupling and multilevel telescoping

**Central question.** How can a carefully chosen joint law make a difference estimator cheaper?

**Understanding target.** Distinguish the marginal laws of two estimates from their coupling. Understand a telescope from a cheap coarse law to a fine law through successive corrections. The telescope requires matching marginals, while variance reduction requires the paired estimates to stay close.

**Dependencies and story role.** [M06](#m06-tails-medians-and-mean-error), [M07](#m07-cdfs-quantiles-and-wasserstein-distance), [M08](#m08-independent-samples-and-variance). This turns the probability tools into a strategy for distributing measurement effort across resolutions.

**Conceptual connection.** Whole-distribution multilevel estimation is established methodology; the quantum task is to realize the useful coupling with the available source access.

**Sources.** [Upper bound §5](../science/multilevel_algorithm.md#5-multilevel-cdf-estimator-and-variance-addition); [the multilevel attribution](../references/related_work.md#cdf-estimation-and-the-multilevel-bridge); [Giles, Nagapetyan and Ritter, §§2.1–2.3](https://people.maths.ox.ac.uk/gilesm/files/juq_15.pdf). The [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure) supplies the project-specific connection.

### M10. Block encodings and spectral walks

**Central question.** How can a Hermitian operator be accessed through a larger unitary?

**Understanding target.** Identify the signal block, encoding ancillas, normalization, and unspecified unitary completion. Understand how a product of reflections relates eigenvalues to walk phases. Distinguish queries to a supplied block encoding from the physical work required to construct it.

**Dependencies and story role.** [M02](#m02-spectral-projectors-and-weighted-energy-laws), [M03](#m03-controlled-evolution-and-an-energy-reference), [M05](#m05-fourier-phase-estimation). This introduces the alternative Hamiltonian interface used by both upper and lower bounds.

**Conceptual connection.** An eigenphase can encode energy through a cosine, so retaining the enlarged walk system becomes part of retaining the relevant information.

**Sources.** [Exact normalized block-encoding model](../science/model.md#exact-normalized-block-encoding); [Childs §29.1, pp. 143–144, and §29.3, pp. 146–147][childs]; [bridge §6](CHILDS_BRIDGE.md#6-from-block-encodings-to-retained-walk-measurements).

### M11. Distinguishability and error propagation

**Central question.** How can closeness of states or operations limit observable differences?

**Understanding target.** Connect pure-state overlap and binary discrimination, then distinguish state distance from an operation's worst-case channel error. Understand that processing cannot create distinguishability and that successive implementation errors admit a telescoping bound.

**Dependencies and story role.** [M01](#m01-states-and-mixtures), [M04](#m04-measurement-probabilities-and-state-changes), [M08](#m08-independent-samples-and-variance). This supplies the shared language for implementation robustness and impossibility results.

**Conceptual connection.** The same distinguishability principle can bound what noisy implementations change and what accurate estimators must distinguish.

**Sources.** [Upper bound §8.1](../science/multilevel_algorithm.md#81-implementation-error-is-measured-on-the-supplied-operations); [lower bounds §4.1](../science/lower_bounds.md#41-the-final-overlap-bound). [Childs §2.1, p. 7, and §23.1, Fact 23.1, p. 109][childs] cover unitary-error accumulation and pure-state discrimination; the [bridge §8](CHILDS_BRIDGE.md#8-implementation-errors-and-what-the-bridge-does-not-assume) specifies the additional channel-level accounting.

### M12. From local tools to an oracle problem

**Central question.** How do the input, output metric, and allowed operations determine a meaningful complexity claim?

**Understanding target.** Assemble the weighted law, fresh-copy source, controlled Hamiltonian interface, and completed classical output into one task. Distinguish an achieved cost from a lower bound for every allowed algorithm. Understand adversary progress as input-dependent distinguishability that known operations preserve and oracle interactions can change.

**Dependencies and story role.** [M03](#m03-controlled-evolution-and-an-energy-reference), [M07](#m07-cdfs-quantiles-and-wasserstein-distance), [M09](#m09-coupling-and-multilevel-telescoping), [M10](#m10-block-encodings-and-spectral-walks), [M11](#m11-distinguishability-and-error-propagation). This integrates the foundations into the framework for the constructive and lower-bound narratives.

**Conceptual connection.** Comparing algorithms requires the same output guarantee and charged interface; stronger algorithmic access can make a lower bound more informative.

**Sources.** [Model §§3–5](../science/model.md#3-source-access); [lower bounds §1](../science/lower_bounds.md#1-task-oracle-models-and-results). [Childs §§21.1–21.2, pp. 97–98, and §§23.1–23.2, starting pp. 109–110][childs] supplies the query and adversary foundations; see [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds).

## Phase II. From retained measurements to a complete resource law

**Phase: narrative and innovation — M13–M30.** The constructive route starts with one source specimen and ends with a finite probability measure and explicit costs. The lower-bound route starts with one hidden spectral displacement and assembles many of them into a dimension-sensitive obstruction. Established phase estimation, multilevel sampling, isotonic regression, and adversary methods retain their attribution throughout.

### M13. A physical source as an energy sampler

**Central question.** What random information does one specimen contribute to spectral readout?

**Understanding target.** Identify the source-weighted latent energy and the clock's noisy observation of it. A general source need not be pure or diagonal in energy. Track one copy request and the controlled evolution used to read it, while keeping the eventual finite classical measure as the required output.

**Dependencies and story role.** [M02](#m02-spectral-projectors-and-weighted-energy-laws), [M05](#m05-fourier-phase-estimation), [M12](#m12-from-local-tools-to-an-oracle-problem). This begins the project construction at the level of one physical experiment.

**Conceptual connection.** The sampled law depends jointly on the Hamiltonian and source, while the method needs no circuit that prepares or reverses that source.

**Sources.** [Upper theorem and access model](../science/multilevel_algorithm.md#1-statement-access-model-and-attribution); [bridge §3](CHILDS_BRIDGE.md#3-from-an-eigenphase-to-a-weighted-spectral-law); [Childs §§4.3 and 27.5][childs].

### M14. Retaining a specimen preserves a latent phase

**Central question.** Why do consecutive phase measurements on one mixed specimen have the needed joint law?

**Understanding target.** Follow the trace calculation for products of phase-estimation Kraus operators. The outcomes are independent conditional on one latent eigenphase, even when the input has coherence between eigenspaces. Conditional states may change; the calculation preserves the relevant marginals and common phase without preparing an eigenstate.

**Dependencies and story role.** [M04](#m04-measurement-probabilities-and-state-changes), [M05](#m05-fourier-phase-estimation), [M13](#m13-a-physical-source-as-an-energy-sampler). This establishes the mechanism that makes a coarse/fine pair useful.

**Conceptual connection.** Retaining the system realizes a coupling; replacing it with an independent source specimen changes that joint law.

**Sources.** [Upper bound §3, Lemma 2](../science/multilevel_algorithm.md#3-exact-coupling-from-retaining-the-same-system); [bridge §4](CHILDS_BRIDGE.md#4-why-retaining-one-copy-couples-two-resolutions). The instrument derivation extends the phase-estimation construction in [Childs §4.3][childs].

### M15. Uniform energy readout without a gap promise

**Central question.** How is phase error converted into a uniform mean energy error?

**Understanding target.** Understand the shifted evolution phase, clipped energy decoder, and treatment of phase wrap. Use the median of three readouts to obtain conditional mean error of order $`1/M`$ at clock size $`M`$, with interaction cost of order $`M`$. No minimum spectral gap, density, or atom weight is required.

**Dependencies and story role.** [M06](#m06-tails-medians-and-mean-error), [M14](#m14-retaining-a-specimen-preserves-a-latent-phase). This turns the exact coupling into a quantitative resolution guarantee.

**Conceptual connection.** Conditional tail control makes the readout guarantee uniform over arbitrary source-weighted spectral laws.

**Sources.** [Upper bound §§2.2–2.3](../science/multilevel_algorithm.md#22-an-energy-readout-without-phase-aliasing); [bridge §3](CHILDS_BRIDGE.md#3-from-an-eigenphase-to-a-weighted-spectral-law). [Childs §4.3][childs] supplies the underlying phase-estimation probabilities.

### M16. One output grid for every resolution

**Central question.** How can estimates from different clock sizes participate in one exact telescope?

**Understanding target.** Use a common terminal grid and the same deterministic decoder whenever a level reappears. Track finite rounding and cosine-evaluation errors in the first-moment bound. Recognize the known level-zero atom and the resulting terminal-law transport bias.

**Dependencies and story role.** [M07](#m07-cdfs-quantiles-and-wasserstein-distance), [M09](#m09-coupling-and-multilevel-telescoping), [M15](#m15-uniform-energy-readout-without-a-gap-promise). This creates compatible finite-valued marginals before they are subtracted.

**Conceptual connection.** A shared grid gives exact cancellation between levels and a finite classical representation without assuming a smooth spectrum.

**Sources.** [Upper bound §4](../science/multilevel_algorithm.md#4-one-fixed-output-grid-and-finite-energy-arithmetic); [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure). This discretization and telescope accounting is supplied by the project.

### M17. Integrated variance of a CDF correction

**Central question.** Why does the coarse/fine correction have small variance even for atomic spectra?

**Understanding target.** Relate the squared difference of two threshold indicators, integrated over the threshold, to the distance between their readouts. Combine this identity with the coupling bound to obtain integrated variance of order $`h_\ell`$. Add variances across independent batches before taking the final square root.

**Dependencies and story role.** [M08](#m08-independent-samples-and-variance), [M09](#m09-coupling-and-multilevel-telescoping), [M14](#m14-retaining-a-specimen-preserves-a-latent-phase), [M16](#m16-one-output-grid-for-every-resolution). This is the statistical bridge from one retained pair to the whole distribution estimator.

**Conceptual connection.** Integrated CDF loss makes proximity of paired energies useful without a density or pointwise smoothness assumption.

**Sources.** [Upper bound §5](../science/multilevel_algorithm.md#5-multilevel-cdf-estimator-and-variance-addition); [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure); [multilevel antecedents and specialization](../references/related_work.md#cdf-estimation-and-the-multilevel-bridge).

### M18. Allocating specimens across resolutions

**Central question.** How should sample counts balance shrinking correction variance against growing experiment cost?

**Understanding target.** Connect variance of order $`h_\ell`$ with per-pair cost of order $`h_\ell^{-1}`$. Understand the allocation yielding $`O(\epsilon^{-2})`$ copies and $`O(\epsilon^{-2}\log^3(1/\epsilon))`$ total interaction. Distinguish the alternative allocation's logarithmic tradeoff from a proved optimal joint frontier.

**Dependencies and story role.** [M15](#m15-uniform-energy-readout-without-a-gap-promise), [M17](#m17-integrated-variance-of-a-cdf-correction). This assembles the individual resolution costs into the first total-resource statement.

**Conceptual connection.** The longest retained experiment uses $`O(1/\epsilon)`$ interaction, but the sum across all experiments is the Hamiltonian resource being optimized.

**Sources.** [Upper bound §6](../science/multilevel_algorithm.md#6-parameter-allocation-and-interaction-resources); [resource table](../science/resources.md#1-common-task-and-resource-units); [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure).

### M19. Turning signed corrections into probabilities

**Central question.** How can a signed multilevel estimate become an actual probability measure?

**Understanding target.** Recognize that a telescope of empirical CDF differences may fail monotonicity or positivity. Understand why nearest monotone CDF projection in integrated absolute error loses only a constant factor. Recover nonnegative masses summing exactly to one, including possible atoms at both endpoints.

**Dependencies and story role.** [M07](#m07-cdfs-quantiles-and-wasserstein-distance), [M16](#m16-one-output-grid-for-every-resolution), [M17](#m17-integrated-variance-of-a-cdf-correction). This completes the required output type rather than stopping with a signed estimator.

**Conceptual connection.** Feasibility of the true terminal CDF links an optimization problem to the transport-error guarantee.

**Sources.** [Upper bound §7.1](../science/multilevel_algorithm.md#71-projection-and-the-probability-guarantee); [isotonic implementation and attribution in §7.2](../science/multilevel_algorithm.md#72-exact-arithmetic-and-a-finite-projection-algorithm); [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure).

### M20. Finite tolerance and classical arithmetic

**Central question.** What must be charged to make the returned distribution a finite computational object?

**Understanding target.** Reduce a binary rational tolerance to a comparable dyadic value before computing allocation integers. Separate its input length $`b`$ from precision-dependent work. Track rational CDF weights, exact projection, $`O(\epsilon^{-1}\log^2(1/\epsilon))`$ output bits, and total classical cost $`O(b)+\widetilde O(\epsilon^{-2})`$.

**Dependencies and story role.** [M16](#m16-one-output-grid-for-every-resolution), [M18](#m18-allocating-specimens-across-resolutions), [M19](#m19-turning-signed-corrections-into-probabilities). This closes the classical representation and processing part of the upper theorem.

**Conceptual connection.** Exact probability normalization can coexist with finite arithmetic; large intermediate denominators and input descriptions still have bit costs.

**Sources.** [Upper bound §7.2](../science/multilevel_algorithm.md#72-exact-arithmetic-and-a-finite-projection-algorithm); [exact rational projector](../verification/exact_cdf_projection.py) and [its documented scope](../verification/README.md#files-and-scope); [bridge §5](CHILDS_BRIDGE.md#5-from-coupled-readouts-to-a-classical-probability-measure).

### M21. General block encodings preserve the weighted law

**Central question.** Why does the same readout theorem hold for every exact normalized unitary completion?

**Understanding target.** Follow the flag-based Hermitianization, known signal reflection, and walk construction. Understand why pushing the walk's spectral measure through cosine gives the original source-weighted energy law. Retain the flag and encoding workspace through all readouts, and charge controlled forward and inverse block calls individually.

**Dependencies and story role.** [M10](#m10-block-encodings-and-spectral-walks), [M14](#m14-retaining-a-specimen-preserves-a-latent-phase), [M20](#m20-finite-tolerance-and-classical-arithmetic). This transfers the complete construction to the second access model with its ancillas and queries accounted for.

**Conceptual connection.** The common hidden variable is a walk eigenphase; opposite phases can correspond to the same energy, so conditioning only on energy is insufficient for the general raw-outcome argument.

**Sources.** [Upper bound §§9.1–9.3](../science/multilevel_algorithm.md#9-exact-controlled-block-encoding-formulation); [bridge §6](CHILDS_BRIDGE.md#6-from-block-encodings-to-retained-walk-measurements); [Childs §§29.1 and 29.3][childs].

### M22. Implementation error and fixed-source bias

**Central question.** Which finite inaccuracies preserve the stated success guarantee?

**Understanding target.** Combine the statistical success slack with a sum of operation-level half-diamond errors. Interpret Duhamel's duration-dependent bound and the fixed-source trace-norm bias bound. Distinguish these sufficient budgets from robustness under arbitrary top-block error, correlated source drift, or a general operator-Lipschitz assertion.

**Dependencies and story role.** [M11](#m11-distinguishability-and-error-propagation), [M20](#m20-finite-tolerance-and-classical-arithmetic), [M21](#m21-general-block-encodings-preserve-the-weighted-law). This completes the upper theorem with explicit implementation and source assumptions.

**Conceptual connection.** Comparing the actual measurement process to the ideal process controls the output event while keeping oracle implementation and source-preparation costs explicit.

**Sources.** [Upper bound §§8.1–8.3](../science/multilevel_algorithm.md#8-finite-accuracy-operations-and-source-perturbation); [implementation accounting](../science/model.md#6-what-a-physical-implementation-must-add); [Childs §2.1, p. 7][childs] and [bridge §8](CHILDS_BRIDGE.md#8-implementation-errors-and-what-the-bridge-does-not-assume).

### M23. Packing independent displacements into a spectrum

**Central question.** How can a norm-bounded Hamiltonian encode many independent unknown signs?

**Understanding target.** Build separated ordered spectral groups with hidden displacements of order $`\epsilon`$. Account for unequal multiplicities in an arbitrary dimension. Understand why the number of independently displaced groups is of order $`\min\{d,\epsilon^{-1}\}`$, with a known eigenbasis and freely preparable source.

**Dependencies and story role.** [M02](#m02-spectral-projectors-and-weighted-energy-laws), [M07](#m07-cdfs-quantiles-and-wasserstein-distance), [M12](#m12-from-local-tools-to-an-oracle-problem). This starts the lower-bound construction from individual spectral parameters.

**Conceptual connection.** The hard family isolates Hamiltonian information from eigenvector learning and source-preparation difficulty.

**Sources.** [Lower bounds §2](../science/lower_bounds.md#2-an-ordered-spectral-hypercube-in-every-dimension) and [§5.3](../science/lower_bounds.md#53-the-source-can-be-known-and-freely-reversible); [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds). The packing is supplied by the project within the query setting of [Childs §§21.1–21.2][childs].

### M24. Decoding an arbitrary classical output

**Central question.** Why must every accurate probability-measure output reveal many of the hidden signs?

**Understanding target.** Use quantile centroids on known mass intervals and compare each centroid with its group's midpoint. Convert Wasserstein error into a weighted Hamming-error bound without requiring the output to belong to the hard family. Distinguish pairwise distance between two hard inputs from the smaller charge per incorrectly decoded bit.

**Dependencies and story role.** [M07](#m07-cdfs-quantiles-and-wasserstein-distance), [M23](#m23-packing-independent-displacements-into-a-spectrum). This connects the actual output specification to an interrogation problem.

**Conceptual connection.** An unrestricted classical output cannot avoid the lower bound merely by choosing different support points or weights.

**Sources.** [Lower bounds §3](../science/lower_bounds.md#3-decoding-any-classical-probability-output) and [the midpoint factor-of-two distinction](../science/lower_bounds.md#exact-pairwise-distance-and-its-factor-of-two); [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds).

### M25. Required progress on the input hypercube

**Central question.** What global distinguishability change does successful sign recovery force?

**Understanding target.** Interpret adversary progress as an average overlap across neighboring hidden inputs. Understand how the decoder's average error bounds the final overlap through fidelity and concavity. The required progress change grows with the number of encoded signs, while known operations preserve progress.

**Dependencies and story role.** [M11](#m11-distinguishability-and-error-propagation), [M12](#m12-from-local-tools-to-an-oracle-problem), [M24](#m24-decoding-an-arbitrary-classical-output). This assembles individual output distinctions into one lower-bound quantity.

**Conceptual connection.** The input-label register is a mathematical proof device; it does not grant the estimator a register containing the unknown signs.

**Sources.** [Lower bounds §4](../science/lower_bounds.md#4-a-hypercube-adversary-lemma-with-explicit-output-constants); [Childs §§23.1–23.2, pp. 109 onward][childs]; [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds).

### M26. Charging every Hamiltonian interaction

**Central question.** How quickly can controlled evolution change the required adversary progress?

**Understanding target.** Relate the progress derivative to a commutator whose norm is controlled by one displacement scale. Orthogonal physical query sectors avoid an extra factor equal to the number of signs, giving $`T=\Omega(\min\{d,\epsilon^{-1}\}/\epsilon)`$. Include known driving controls, signed and parallel evolution, and adaptive durations under a branchwise hard cap.

**Dependencies and story role.** [M03](#m03-controlled-evolution-and-an-energy-reference), [M23](#m23-packing-independent-displacements-into-a-spectrum), [M25](#m25-required-progress-on-the-input-hypercube). This converts required progress into the dimension-sensitive total-time lower bound.

**Conceptual connection.** Arbitrary known controls do not reveal the hidden input; amplified unknown interaction strength is charged through its absolute rate.

**Sources.** [Lower bounds §§5.1–5.3](../science/lower_bounds.md#5-lower-bound-for-controlled-total-hamiltonian-evolution); [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds). [Childs §23.2][childs] supplies the adversary foundation; the continuous-time and adaptive accounting is developed in the project with its cited Hamiltonian-oracle source.

### M27. A weak exact block completion

**Central question.** How can the block-query lower bound control information outside the encoded Hamiltonian block?

**Understanding target.** Inspect the complete reflection oracle, including its square-root blocks. Understand why neighboring hidden inputs change the whole unitary only by the displacement scale. Apply the same progress argument to forward, inverse, controlled, and parallel queries to obtain the charged block-query bound.

**Dependencies and story role.** [M10](#m10-block-encodings-and-spectral-walks), [M25](#m25-required-progress-on-the-input-hypercube), [M26](#m26-charging-every-hamiltonian-interaction). This establishes the lower law in the second Hamiltonian interface.

**Conceptual connection.** An upper algorithm must tolerate every valid completion, while a lower bound can choose one valid completion that reveals no additional strong bits.

**Sources.** [Lower bounds §6](../science/lower_bounds.md#6-exact-weak-block-completion); [Childs §§29.1 and 23.2][childs]; [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds). Exact classical matrix-entry or graph-neighbor access is a different interface.

### M28. Separate source-copy and source-query obstructions

**Central question.** What changes when the unknown information is in the source weights instead of the Hamiltonian?

**Understanding target.** Use two nearby source mixtures on one known two-level Hamiltonian. Relate a successful distribution estimate to binary discrimination, giving an inverse-square copy requirement. Contrast this with the inverse-linear coherent-preparation-query obstruction proved using a complete weak purifier, with no additionally free unknown-source copies.

**Dependencies and story role.** [M08](#m08-independent-samples-and-variance), [M11](#m11-distinguishability-and-error-propagation), [M22](#m22-implementation-error-and-fixed-source-bias), [M27](#m27-a-weak-exact-block-completion). This completes the resource picture while keeping the different hard families separate.

**Conceptual connection.** Coordinatewise worst-case bounds do not establish one simultaneously hard input or a joint source/time frontier.

**Sources.** [Lower bounds §7](../science/lower_bounds.md#7-unknown-source-copies-an-elementary-sharp-exponent) and [§8](../science/lower_bounds.md#8-coherent-source-queries-an-explicit-weak-purifier); [Childs §23.1, Fact 23.1][childs] for the pure-state discrimination ingredient; [bridge §7](CHILDS_BRIDGE.md#7-from-adversary-progress-to-the-resource-lower-bounds).

### M29. Matched resource comparisons

**Central question.** Which apparent improvements survive matching the task, access model, and normalization?

**Understanding target.** Compare the retained-copy construction with fine-QPE sampling, the published approximate-CDF specialization, and the inherited coherent-source upper. Preserve preparation inverses, graph implementation costs, and density-operator normalization in each comparison. Translate physical energy tolerance and interaction time before interpreting a normalized resource formula.

**Dependencies and story role.** [M18](#m18-allocating-specimens-across-resolutions), [M21](#m21-general-block-encodings-preserve-the-weighted-law), [M26](#m26-charging-every-hamiltonian-interaction), [M28](#m28-separate-source-copy-and-source-query-obstructions). This places the proved consequences beside the closest results under comparable assumptions.

**Conceptual connection.** The fresh-copy realization changes a source-access requirement; the generic coherent Hamiltonian upper exponent and reusable spectral output already have precedents.

**Sources.** [Resources §§2–4](../science/resources.md#2-independent-fine-qpe-baseline); [closest algorithmic comparisons](../references/related_work.md#1-closest-algorithmic-comparisons); [normalization-sensitive lower-bound comparison](../science/lower_bounds.md#10-detailed-comparison-with-wangs-2026-spectrum-lower-bound); [physical energy units](../science/interpretation.md#physical-energy-units-and-normalization). [Childs §29.1][childs] supports the block-normalization language.

### M30. What the complete resource law establishes

**Central question.** What follows when the construction, converse, and access distinctions are combined?

**Understanding target.** Explain why independent source copies achieve the optimal Hamiltonian precision exponent up to logarithms in the worst case when $`d=\Omega(\epsilon^{-1})`$, while the lower law remains dimension sensitive. Interpret simultaneous Lipschitz-observable control and its classical evaluation cost. Preserve the separate-family qualification and the unresolved joint frontier, small-dimension upper, and universal depth questions.

**Dependencies and story role.** [M22](#m22-implementation-error-and-fixed-source-bias), [M28](#m28-separate-source-copy-and-source-query-obstructions), [M29](#m29-matched-resource-comparisons). This integrates both proof routes and their operational meaning into the complete project account.

**Conceptual connection.** Retention supplies the coupling, multilevel estimation and projection supply the classical output, and spectral packing with adversary progress supplies the obstruction. Finite verification checks identities and examples; the analytical proofs establish the universal scaling.

**Sources.** [Model §5](../science/model.md#5-resource-statements); [dimension-sensitive interpretation](../science/interpretation.md#why-the-lower-bound-has-a-dimension-threshold); [observable meaning](../science/interpretation.md#what-can-be-learned-from-the-returned-measure); [claim boundaries](../science/interpretation.md#boundaries-of-the-claim); [verification scope](../verification/README.md#files-and-scope). The [Childs bridge](CHILDS_BRIDGE.md) connects the selected anchor to the complete route.

[childs]: https://www.cs.umd.edu/~amchilds/qa/qa.pdf
