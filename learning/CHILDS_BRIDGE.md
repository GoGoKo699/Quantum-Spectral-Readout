# From Childs's quantum algorithms notes to spectral readout

[Overview](../README.md) · [Thirty milestones](MILESTONES.md) · [Model](../science/model.md) · [Upper proof](../science/multilevel_algorithm.md) · [Lower proof](../science/lower_bounds.md)

An energy measurement produces one outcome. This project asks how much quantum access is needed to return a classical approximation to the entire energy distribution of a supplied source. The useful connection to quantum algorithms is that phase estimation both reads spectral information and controls how the measured system changes. Retaining that system lets two measurement resolutions refer to the same underlying energy.

This bridge uses **Andrew M. Childs, *Lecture Notes on Quantum Algorithms*** as its single educational anchor. It connects the relevant parts of those notes to the project's definitions and proofs. The [milestone map](MILESTONES.md) organizes the complete conceptual route; the scientific chapters remain authoritative for exact statements, constants, assumptions, and research attribution.

## 1. The selected source

Use the [author's PDF](https://www.cs.umd.edu/~amchilds/qa/qa.pdf), dated **17 April 2025**, linked from the [author's course-notes page](https://www.cs.umd.edu/~amchilds/qa/). The following locators refer to its **printed page numbers**. PDF-viewer page numbers are eight larger in this version; the links below use viewer pages. The document has 191 PDF pages.

| Entry point in Childs | Printed page | Connection developed here |
|---|---:|---|
| §§1.1–1.2 | [1](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=9) | State vectors, registers, circuits, and measurement |
| §4.3, especially Eq. (4.17) | [19](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=27) | Fourier phase-estimation probabilities |
| §27.5 | [136–137](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=144) | Turning dynamics into an operator measurement |
| §29.1 | [143–144](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=151) | Block encodings and their normalization |
| §29.3 | [146–147](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=154) | Two-dimensional subspaces behind qubitization |
| §§21.1–21.2 | [97–98](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=105) | Specifying and charging a quantum oracle |
| §§23.1–23.2; Fact 23.1 | [109–112](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=117) | State overlap and adversary progress |
| §2.1, Lemma 2.2 | [7](https://www.cs.umd.edu/~amchilds/qa/qa.pdf#page=15) | Accumulation of unitary implementation error |

These are entry points, not a requirement to read the notes in full. Sections 3–8 below supply the project-specific connections. In particular, the mixed-state measurement instrument, Wasserstein/CDF argument, multilevel allocation, and positive-measure reconstruction are developed in this repository; they are not attributed to Childs. The classical methods and quantum ingredients retain their primary research citations in the [upper proof](../science/multilevel_algorithm.md#references-and-exact-source-locations) and [related-work account](../references/related_work.md).

## 2. Notation and access models

Three objects have different roles. A **state** describes the system being measured; an **operator** specifies its energy; a **unitary interface** supplies the allowed interaction. The table translates the notation needed to move between the anchor and this project.

| Object | Translation used in this repository |
|---|---|
| A unitary eigenvalue written as $`e^{i\varphi}`$ | Write it as $`e^{2\pi i\theta}`$, with $`\theta=\varphi/(2\pi)`$ modulo one. |
| An $`n`$-qubit phase register | Its clock size is $`M=2^n`$; level $`\ell`$ uses $`M_\ell=2^\ell`$. |
| A supplied eigenvector | Replace it by a general density operator $`\rho`$; the measurement then samples a source-weighted spectral law. |
| A matrix in the encoded block | The theorem uses a Hermitian $`H`$ with $`\|H\|\le1`$ and an exact encoding of $`H`$ itself. |
| The encoding unitary $`U`$ | This is Hamiltonian access. It is distinct from a source-preparation unitary $`U_\rho`$. |
| Oracle cost | Count normalized block queries, or charge an evolution by its absolute duration. A large controlled power is not free. |

A density operator is a positive semidefinite matrix with trace one. A pure state has the form $`\rho=|\psi\rangle\langle\psi|`$; mixtures and reduced states also fit this description. An independent source request supplies one specimen in state $`\rho`$. It supplies no inverse preparation circuit or access to an environment that purifies the state. Those are stronger, separately specified interfaces.

The evolution model supplies controlled $`e^{-itH}`$, including its known control structure, and charges

```math
T=\sum_r |t_r|.
```

This counts all interactions across all specimens. It differs from the number of variable-duration calls and from hardware elapsed time. Controlled access also supplies an energy reference: shifting $`H`$ by a scalar changes a controlled relative phase, whereas an uncontrolled unitary channel cannot reveal that shift. The [model chapter](../science/model.md#4-two-alternative-hamiltonian-interfaces) states these distinctions precisely.

Two symbols are reused in different scientific chapters. The upper proof's $`\Gamma`$ is an output grid; the lower proof's $`\Gamma`$ is an adversary matrix. The walk unitary is $`W`$, while the lower proof also calls its real-valued progress function $`W`$. Section 7 below calls the latter $`\mathcal P`$ to keep their roles separate.

## 3. From an eigenphase to a weighted spectral law

For the finite-dimensional spectral decomposition

```math
H=\sum_\lambda \lambda P_\lambda,
\qquad
\mu_{H,\rho}
=\sum_\lambda \mathrm{Tr}(\rho P_\lambda)\,\delta_\lambda,
```

$`P_\lambda`$ projects onto the entire eigenspace of energy $`\lambda`$, including any degeneracy. The notation $`\delta_\lambda`$ means unit probability mass at that energy. Thus $`\mathrm{Tr}(\rho P_\lambda)`$ is the probability that an ideal energy measurement finds $`\lambda`$. For $`\rho=I_d/d`$, these weights are eigenspace dimensions divided by $`d`$.

The target depends on these weights, even when the input state has coherence between different energies. For example, take

```math
H=-\tfrac12|0\rangle\langle0|
  +\tfrac12|1\rangle\langle1|,
\qquad
|+\rangle=(|0\rangle+|1\rangle)/\sqrt2.
```

Both $`|+\rangle\langle+|`$ and $`I_2/2`$ have the energy law
$`\tfrac12\delta_{-1/2}+\tfrac12\delta_{1/2}`$. Their quantum states are different, and the first does not commute with $`H`$. Spectral readout is therefore less information than state tomography.

The project turns the energy into a phase using

```math
V=-e^{-i\pi H/2},
\qquad
\theta_\lambda=\tfrac12-\tfrac{\lambda}{4}.
```

The spectrum of $`H`$ lies in $`[-1,1]`$, so these phases lie in $`[1/4,3/4]`$. The known minus sign is a control phase. A Fourier readout $`y`$ of a clock of size $`M`$ is decoded by clipping $`2-4y/M`$ to $`[-1,1]`$. This phase window and decoder fix the aliasing convention; phases are periodic, energies in the target interval are not.

In the two-level example, the phases are $`5/8`$ and $`3/8`$. A clock of size eight represents both exactly. Its ordinary phase measurement returns $`y=5`$ or $`y=3`$, each with probability one half, and the decoder returns the corresponding energy. The controlled evolution times are $`\pi/2`$, $`\pi`$, and $`2\pi`$, totaling $`7\pi/2`$ for this one readout. The example makes both the output and its interaction charge explicit. General spectra require an approximation analysis.

The conceptual route is Childs §4.3 followed by §27.5. The [upper proof, Section 2](../science/multilevel_algorithm.md#2-a-phase-estimator-with-a-uniform-first-moment-bound), supplies this particular energy normalization, decoder, uniform error bound, and cost calculation.

## 4. Why retaining one copy couples two resolutions

A measurement description must specify both the outcome probabilities and what happens to the retained system. For Fourier phase estimation of a unitary $`W`$, the operator associated with clock outcome $`y`$ is

```math
K_{M,y}(W)=\frac1M\sum_{r=0}^{M-1}
e^{-2\pi i r y/M}W^r.
```

On a state $`\sigma`$, the unnormalized state after that outcome is
$`K_{M,y}\sigma K_{M,y}^\dagger`$; its trace is the outcome probability. Summing those probabilities gives one. This operator-valued description is the measurement **instrument** needed here.

Every such operator is a function of the same $`W`$. If its phase projectors are $`P_\theta`$, sequential readouts on one retained system consequently obey

```math
\Pr(y_1,\ldots,y_r)
=\sum_\theta \mathrm{Tr}(\sigma P_\theta)
 \prod_{i=1}^{r}p_{M_i}(y_i\mid\theta).
```

To obtain this identity, write the sequential Born probability, cycle $`\sigma`$ to the front of the trace, and commute the factors $`K_i^\dagger K_i`$. Their spectral decomposition gives the displayed product. No step requires $`\sigma`$ to be pure or to commute with $`W`$.

The resulting classical law has a useful description: draw one latent phase, then draw the outcomes independently conditional on that phase. This is a representation of the joint probability law. It does not say the unknown source was physically prepared as a known eigenstate. The state conditioned on an observed outcome generally changes; the factorization already accounts for that change.

For direct evolution, the latent phase determines one energy. A coarse and a fine readout on the same specimen therefore estimate that same energy. Replacing the specimen between them instead draws independent energies. In the two-atom example above, two independent exact energies differ by one with probability one half, so their expected separation is one half. Two exact readouts of the same latent energy agree. With finite-resolution readouts, the retained-system separation shrinks with the resolution.

The construction also repeats each resolution three times and takes a real median. This step addresses a subtlety in going from phase-estimation success probability to mean absolute error. One ordinary readout has a tail bounded by a constant times $`1/(Mr)`$ at error threshold $`r`$. If the median is wrong by at least $`r`$, two of the three readouts must be wrong by that much. Conditional independence squares the tail, so integration gives

```math
\mathbb E_\lambda |Y_M-\lambda|\le 64/M.
```

The bound is uniform in energy, dimension, and spectral gaps. Its constant is conservative. This first-moment argument and the exact sequential instrument identity are supplied in [upper Sections 2–3](../science/multilevel_algorithm.md#3-exact-coupling-from-retaining-the-same-system). They are the extra steps required before the familiar phase-estimation circuit can support the distribution estimator.

## 5. From coupled readouts to a classical probability measure

### The loss matches spectral displacement

Let $`F_\nu(x)=\nu((-\infty,x])`$ be the cumulative distribution function, or CDF. For probability measures on the line,

```math
W_1(\nu,\mu)
=\int_{\mathbb R}|F_\nu(x)-F_\mu(x)|\,dx.
```

This metric charges moved probability mass times distance. For example,
$`W_1(\delta_0,\delta_h)=|h|`$, although the total variation distance between distinct point masses is one. Small energy displacements are therefore small errors under the requested metric. The [model](../science/model.md#2-a-completed-classical-output) and [lower proof, Section 3](../science/lower_bounds.md#3-decoding-any-classical-probability-output), give the transport identities and their scope.

### A fine correction has small integrated variance

Put $`h_\ell=2^{-\ell}`$. Round every readout to the same final rational grid. A level-$`\ell`$ experiment produces a coupled fine/coarse pair, written $`Z_\ell^+`$ and $`Z_{\ell-1}^-`$, using one specimen and fresh clocks. Its correction to a CDF is

```math
D_\ell(x)
=\mathbf1\{Z_\ell^+\le x\}
-\mathbf1\{Z_{\ell-1}^-\le x\}.
```

For fixed values $`u,v`$, the squared difference of their two indicators is one exactly between them, apart from endpoints. Thus

```math
\int_{\mathbb R}
|\mathbf1\{u\le x\}-\mathbf1\{v\le x\}|^2\,dx
=|u-v|.
```

The retained-system coupling and first-moment estimates make the expected separation $`O(h_\ell)`$. Therefore the integrated variance of $`D_\ell`$ is also $`O(h_\ell)`$, while the interaction cost of one pair is $`O(h_\ell^{-1})`$. This argument accommodates atoms and clustered energies; it needs no smooth spectral density.

Let $`F_\ell`$ be the marginal CDF at level $`\ell`$. Averaging $`n_\ell`$ independent corrections at each level gives

```math
G(x)=F_0(x)+
\sum_{\ell=1}^{L}\frac1{n_\ell}
 \sum_{r=1}^{n_\ell}D_{\ell,r}(x),
\qquad
\mathbb E G=F_L.
```

Here $`F_0`$ is the known base CDF. The expected corrections telescope because each pair has the correct standalone marginals. Independent source experiments allow variances to add. On the interval of length two,

```math
\mathbb E\|G-F_L\|_1
\le
\left(2\sum_{\ell=1}^{L}
 \frac{v_\ell}{n_\ell}\right)^{1/2},
\qquad v_\ell=O(h_\ell).
```

Taking $`L=\Theta(\log(1/\epsilon))`$ and
$`n_\ell`$ proportional to $`\epsilon^{-2}(\ell+1)^2 2^{-\ell}`$, with integer rounding and the constants in the proof, yields

```math
N_\rho=O(\epsilon^{-2}),
\qquad
T=O(\epsilon^{-2}\log^3(1/\epsilon)).
```

Most copies are spent on cheap coarse measurements; fewer are spent on expensive fine corrections. The [resource comparison](../science/resources.md#2-independent-fine-qpe-baseline) derives the direct $`O(\epsilon^{-3})`$ baseline that resolves every independent sample finely. The multilevel construction improves that baseline's Hamiltonian exponent. A coherent-source upper with exponent two already follows from prior work; the present comparison concerns which source interface suffices.

### Signed corrections must be made into a valid output

A correction adds mass at one grid point and subtracts it at another. Hence $`G`$ can decrease or leave the interval $`[0,1]`$. Returning it directly would fail the requirement of a classical probability measure.

On the common grid $`x_j=-1+jh`$, let $`G_j`$ be its value between consecutive points. Fit a nondecreasing sequence by

```math
\min_{0\le c_0\le\cdots\le c_{J-1}\le1}
h\sum_{j=0}^{J-1}|c_j-G_j|.
```

This is an isotonic $`L^1`$ fit. Its consecutive increments, together with the endpoint masses, define a probability measure:

```math
\begin{aligned}
\widehat p_0&=c_0,\\
\widehat p_j&=c_j-c_{j-1}\quad(1\le j\lt J),\\
\widehat p_J&=1-c_{J-1}.
\end{aligned}
```

All weights are nonnegative and sum to one. The true grid CDF $`F_L`$ is feasible, so optimality and the triangle inequality give

```math
W_1(\widehat\mu,\nu_L)\le2\|G-F_L\|_1
```

for an exact fit. An additive fitting tolerance adds to the right-hand side. Adding terminal bias completes the error argument. [Upper Sections 5–7](../science/multilevel_algorithm.md#5-multilevel-cdf-estimator-and-variance-addition) give the allocations, success probability, exact rational reconstruction, and classical bit cost.

Transport, multilevel Monte Carlo, and isotonic regression are established methods. This section explains their particular combination in the repository; it does not make them additional educational-anchor assignments or attribute them to the Childs notes.

## 6. From block encodings to retained walk measurements

The block-encoding route begins at Childs §§29.1 and 29.3. The supplied full unitary $`U`$ need not itself be Hermitian, even though its encoded block $`H`$ is. The repository handles that distinction explicitly.

Add a flag and define

```math
S=|0\rangle\langle1|\otimes U
 +|1\rangle\langle0|\otimes U^\dagger,
\qquad
J|\psi\rangle=|+\rangle|0^a\rangle|\psi\rangle.
```

Then $`S`$ is a Hermitian involution and $`J^\dagger S J=H`$. With
$`\Pi=JJ^\dagger`$, construct $`W=(2\Pi-I)S`$. Each interior energy $`\lambda`$ determines a two-dimensional invariant plane with walk phases $`\pm\arccos\lambda`$. The endpoint energies have one-dimensional invariant states. A measured fractional phase $`q`$ is decoded as $`\cos(2\pi q)`$.

It is also necessary to preserve the **weights** of the energy law. Let
$`\sigma=J\rho J^\dagger`$ and $`C=(W+W^\dagger)/2`$. The compression identity $`CJ=JH`$ gives

```math
\mathrm{Tr}[\sigma f(C)]
=\mathrm{Tr}[\rho f(H)].
```

Thus the walk's phase distribution, mapped through the cosine, is precisely the desired source-weighted energy distribution, including for coherent mixed inputs.

The complete walk system must survive the paired measurements: source, flag, encoding register, and any workspace belonging to $`U`$. Reset only the clock ancillas between readouts. Reinitializing or postselecting the encoding register can destroy the common-phase coupling. The reflection about $`\Pi`$ concerns known ancillary states and acts as the identity on the source; it requires no reflection about an unknown $`\rho`$.

Each controlled walk application costs at most two supplied controlled block queries. A clock of size $`M`$ uses $`M-1`$ walk applications. This transfers the multilevel calculation to the block-query model. [Upper Section 9](../science/multilevel_algorithm.md#9-exact-controlled-block-encoding-formulation) supplies the full construction and workspace accounting.

Normalization remains part of access. An oracle encoding $`A/\alpha`$ provides that scaled operator; physical error $`\Delta`$ means normalized tolerance $`\epsilon=\Delta/\alpha`$. Constructing the oracle, loading its data, and amplifying its block have their own costs.

## 7. From adversary progress to the resource lower bounds

Childs's query and adversary chapters provide the starting language. The present lower bound must additionally connect an arbitrary probability-measure output to information about weak spectral displacements.

For $`0\lt\epsilon\le1/256`$, the proof uses $`m=\Theta(\min\{d,\epsilon^{-1}\})`$ ordered spectral groups, with known projectors and almost equal weights. Each group hides one sign in

```math
H_z=\sum_{j=1}^{m}(b_j+\delta z_j)P_j,
\qquad
z_j\in\{-1,1\},
\qquad
\delta=32\epsilon.
```

The known centers are separated enough to keep the spectral order fixed. A quantile decoder divides any returned probability law into intervals of the prescribed masses and compares each interval's mean location with its center. A wrong sign costs at least $`\delta`$ times that group's weight in Wasserstein error. Consequently, a successful estimate must recover most signs. This reduction does not require the estimator to return a member of the hard family.

The factor is important: two opposite hard atoms are separated by $`2\delta`$, but an arbitrary returned atom at their midpoint can be only $`\delta`$ from either. The [quantile-decoding proof](../science/lower_bounds.md#3-decoding-any-classical-probability-output) keeps these two charges separate.

Use the hypercube adjacency $`\Gamma=\sum_jX_j`$ on an auxiliary register labeling the hidden signs. If $`|\psi_z\rangle`$ is the algorithm's state on input $`z`$, define

```math
|\Omega\rangle=2^{-m/2}\sum_z|z\rangle|\psi_z\rangle,
\qquad
\mathcal P=\langle\Omega|(\Gamma\otimes I)|\Omega\rangle.
```

This input-label register is a proof device, inaccessible to the algorithm. The progress starts at $`m`$. The required decoding accuracy and an overlap bound force it down by a constant fraction of $`m`$. This is the adversary pattern; the [lower proof, Section 4](../science/lower_bounds.md#4-a-hypercube-adversary-lemma-with-explicit-output-constants), establishes the constants for approximate sign recovery.

The decisive resource calculation is how slowly a weak oracle can change this progress. Neighboring hidden inputs differ by order $`\delta`$ in energy. The labeled commutator has norm $`2\delta`$, so the progress change is bounded by $`2\delta`$ times total charged interaction duration, including reverse and controlled interactions. The block-query proof supplies a complete unitary whose unused blocks also change only by order $`\delta`$. Otherwise an unused block might reveal a hidden sign at no additional cost.

The result is

```math
T,\ Q_H
=\Omega\!\left(
\frac{\min\{d,\epsilon^{-1}\}}{\epsilon}
\right).
```

The [evolution proof](../science/lower_bounds.md#5-lower-bound-for-controlled-total-hamiltonian-evolution) handles arbitrary controls and adaptive durations under a hard cap. The [weak block completion](../science/lower_bounds.md#6-exact-weak-block-completion) handles the generic block interface. These are not immediate substitutions into a unit-strength bit-oracle bound.

For fixed dimension, the displayed bound is only $`\Omega(d/\epsilon)`$. The quadratic inverse-precision regime needs dimension large enough to contain order $`1/\epsilon`$ resolvable groups. The hard family has a known eigenbasis and can use a known freely reversible source; the obstruction concerns the amount of spectral information returned.

The source bounds use a different family in dimension at least two: nearby unknown weights on two known energy levels. They give $`\Omega(\epsilon^{-2})`$ physical copies, or $`\Omega(\epsilon^{-1})`$ queries to an explicit weak purification oracle when every generated unknown-source copy is charged. [Lower Sections 7–8](../science/lower_bounds.md#7-unknown-source-copies-an-elementary-sharp-exponent) derive them. These separate worst-case statements do not establish a simultaneous hard instance or a joint source/time frontier.

## 8. Implementation errors and what the bridge does not assume

Childs §2.1 gives the unitary-error starting point. The repository uses a more general channel comparison because a complete experiment includes measurements, resets, and classical records. If the ideal and implemented operations have half-diamond distances $`\eta_r`$, their composed classical transcripts differ in total variation by at most $`\sum_r\eta_r`$. The diamond norm allows an arbitrary reference system in this comparison.

The [finite-accuracy theorem](../science/multilevel_algorithm.md#8-finite-accuracy-operations-and-source-perturbation) budgets $`\sum_r\eta_r\le1/6`$ and includes classical fitting tolerance, leaving success probability at least two thirds. This is an operation-by-operation sufficient condition. It neither supplies a physical compiler nor proves a hardware noise threshold.

The completed route connects four different requirements:

- **Input:** independent specimens and explicitly supplied controlled dynamics or exact normalized block access.
- **Mechanism:** repeated measurements on one retained system, producing a common latent spectral variable.
- **Output:** an explicitly stored, nonnegative, normalized classical measure, with finite reconstruction cost.
- **Limits:** a dimension-dependent Hamiltonian lower bound and separately charged source bounds.

On the successful output event, every later 1-Lipschitz spectral average has absolute error at most $`\epsilon`$. Evaluating that average still requires classical work on the returned measure. Sharp spectral thresholds and relative errors for rare events require further assumptions; see [Interpretation and boundaries](../science/interpretation.md).

The [thirty milestones](MILESTONES.md) join these requirements into a conceptual route. The [verification guide](../verification/README.md) documents finite checks of the coupling, reconstruction, and lower-bound calculations. Those checks support implementation and algebra review; the canonical proofs establish the asymptotic statements.
