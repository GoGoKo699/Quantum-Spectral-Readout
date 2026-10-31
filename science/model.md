# Task, access models, and theorem map

[Repository overview](../README.md) · [Upper bound](multilevel_algorithm.md) · [Lower bounds](lower_bounds.md) · [Resource comparison](resources.md)

## 1. The mathematical input

Let $`\mathcal H`$ have finite dimension $`d`$. The unknown Hermitian operator $`H`$ satisfies a known normalization $`\|H\|\le1`$. The source is one fixed density operator $`\rho`$ on $`\mathcal H`$. It can be mixed, and $`[H,\rho]=0`$ is not assumed.

For the spectral projection-valued measure $`E_H`$, define

```math
\mu_{H,\rho}(B)=\operatorname{Tr}[\rho E_H(B)].
```

Equivalently, if $`H=\sum_\lambda\lambda P_\lambda`$ with distinct energies, then

```math
\mu_{H,\rho}=\sum_\lambda\operatorname{Tr}(\rho P_\lambda)\,\delta_\lambda.
```

Degeneracies are included in $`P_\lambda`$. The task estimates the energy law weighted by the given source. It does not reconstruct the eigenvectors or the state. For $`\rho=I_d/d`$, it becomes the normalized density of states, including multiplicities.

## 2. A completed classical output

For an encoded rational tolerance $`0<\epsilon\le1/4`$, return a finite classical probability measure $`\widehat\mu`$ satisfying

```math
\Pr[W_1(\widehat\mu,\mu_{H,\rho})\le\epsilon]\ge\frac23.
```

The measure has nonnegative weights summing exactly to one. It is available for classical computation after quantum access ends. A promise to keep sampling from the original unknown Hamiltonian is not the required output. The upper algorithm uses $`O(\epsilon^{-1})`$ rational grid points and $`O(\epsilon^{-1}\log^2(1/\epsilon))`$ total output bits.

For probability measures on the line, Wasserstein distance admits the CDF and quantile identities

```math
W_1(\nu,\mu)
=\int_{\mathbb R}|F_\nu(x)-F_\mu(x)|\,dx
=\int_0^1|F_\nu^{-1}(u)-F_\mu^{-1}(u)|\,du.
```

The first identity is classical [Vallender, 1974](https://doi.org/10.1137/1118101); [Lower bounds, Section 3](lower_bounds.md#3-decoding-any-classical-probability-output) proves both directly. On $`[-1,1]`$, this metric measures how much probability mass must move, multiplied by how far it moves. It can tolerate a small displacement of an atom even though total variation between the displaced point masses is one.

The dual description gives one simultaneous event for all Lipschitz tests:

```math
W_1(\widehat\mu,\mu_{H,\rho})\le\epsilon
\quad\Longrightarrow\quad
\left|\int f\,d\widehat\mu-\operatorname{Tr}[\rho f(H)]\right|
\le L_f\epsilon
```

when $`f`$ has Lipschitz constant $`L_f`$. The function may be chosen after the classical measure is obtained. An indicator of an exact spectral interval is discontinuous and is not covered by this inequality without extra spectral assumptions.

## 3. Source access

### Fresh independent copies

Each request supplies a new copy of the same $`\rho`$. The source input is a product state across requests. The algorithm may retain and measure a specimen repeatedly. The construction uses one specimen for a pair of three-readout medians and then discards it.

No classical description of $`\rho`$, reversible preparation, purification, inverse preparation, or reflection about the source is supplied. Retaining a specimen does require coherent access to its system during the paired experiment. It does not imply coherent access to the process that created it.

Independence is an assumption, not a conclusion from identical one-copy marginals. Correlated or drifting sources need separate analysis. If each independent input is a fixed state $`\sigma`$, the method estimates its law; the source-bias bound

```math
W_1(\mu_{H,\sigma},\mu_{H,\rho})\le\|\sigma-\rho\|_1
```

is proved in [Upper bound, Section 8.3](multilevel_algorithm.md#83-fixed-source-bias).

### Coherent source access for comparisons and lower bounds

A stronger interface supplies a full unitary $`U_\rho`$ preparing a purification of $`\rho`$, with forward, inverse, and controlled calls available. Count every such call in $`Q_\rho`$. This interface does not additionally give free copies of an unknown $`\rho`$ when a lower bound on $`Q_\rho`$ is asserted.

Hamiltonian lower bounds use a known source independent of the hidden Hamiltonian, so its copies, purification, and reversible preparation may all be free. This deliberately removes source difficulty from those lower bounds.

## 4. Two alternative Hamiltonian interfaces

### Controlled evolution

For any requested real time $`t`$, the oracle supplies

```math
C_H(t)=|0\rangle\langle0|\otimes I
+|1\rangle\langle1|\otimes e^{-itH}.
```

The charged resource is

```math
T=\sum_k|t_k|.
```

The sum includes every call on every source specimen. Negative times are charged by their absolute duration. Simultaneous interactions are charged by summed durations. Hardware elapsed time and the number of variable-duration calls are separate quantities.

Controlled access is supplied explicitly. An uncontrolled unitary channel is unchanged by $`H\mapsto H+cI`$ and cannot identify an absolute energy shift. The theorem does not infer a controlled unknown evolution from that weaker interface.

### Exact normalized block encoding

A full unitary $`U`$ with an encoding register of $`a`$ qubits satisfies

```math
(\langle0^a|\otimes I)U(|0^a\rangle\otimes I)=H.
```

Controlled $`U`$ and $`U^\dagger`$ are supplied, and every use counts as one oracle query. The completion away from this block can be arbitrary. The upper proof works for every such completion by adding a flag and qubitizing a Hermitian involution. The lower proof supplies one explicit weak completion, as a generic-interface algorithm must also succeed on it.

The walk's flag and encoding workspace are retained throughout each coarse/fine experiment. Resetting that workspace between readouts generally destroys the coupling. Known ancilla preparation and reflections are not reflections about the unknown source. Their register and gate costs are detailed in [Upper bound, Section 9](multilevel_algorithm.md#9-exact-controlled-block-encoding-formulation).

For a supplied encoding of $`A/\alpha`$, use $`H=A/\alpha`$ and normalized tolerance $`\epsilon=\Delta/\alpha`$ to request physical error $`\Delta`$. The factor $`\alpha`$ cannot be dropped or amplified away for free. An approximation guarantee only on the encoded block is weaker than a norm guarantee on the full unitary; robustness to the former is outside the exact-encoding theorem.

## 5. Resource statements

### Upper theorem

The fresh-copy construction has

```math
N_\rho=O(\epsilon^{-2}),\qquad
T=O(\epsilon^{-2}\log^3(1/\epsilon))
```

or the same asymptotic query bound $`Q_H`$ in the normalized block interface. The longest retained-specimen sequence uses $`O(\epsilon^{-1})`$ interaction time or oracle queries. Classical reconstruction costs $`\widetilde O(\epsilon^{-2})`$ bit operations beyond reading the encoded tolerance. A different sample allocation gives $`O(\epsilon^{-2}\log(1/\epsilon))`$ copies and $`O(\epsilon^{-2}\log^2(1/\epsilon))`$ interaction cost.

Here logarithmic notation concerns precision dependence; it does not hide the implementation cost of the supplied interface or an unstated state-preparation circuit. The exact theorem and conservative constants are in [the upper proof](multilevel_algorithm.md). No practical constant-factor estimate is made.

### Separate minimax lower bounds

For $`0<\epsilon\le1/256`$ and all integers $`d\ge1`$,

```math
T,\ Q_H=\Omega\!\left(\frac{\min\{d,\epsilon^{-1}\}}{\epsilon}\right).
```

This allows arbitrary ancillas, known driving controls, intermediate measurements, inverse access, and adaptive query choices under a worst-case hard cap. It holds with a known, freely reversible source. A disclosed eigenbasis suffices for the hard family.

For $`d\ge2`$, distinct hard families with a fixed known Hamiltonian give

```math
N_\rho\ge\frac1{36\epsilon^2},\qquad
Q_\rho\ge\frac{\sqrt3}{12\epsilon}.
```

Each inequality is a separate worst-case statement. Their combination identifies optimal precision exponents in the large-dimension regime, but does not determine a joint source/time frontier or a simultaneous hard instance. At fixed $`d`$, the stated Hamiltonian lower bound is only $`\Omega(d/\epsilon)`$. No universal coherence-depth lower bound follows.

## 6. What a physical implementation must add

If preparing a copy costs $`C_\rho`$, preparation contributes $`N_\rho C_\rho`$. If a controlled evolution of duration $`t`$ and allowed error $`\eta`$ costs $`C_{\rm impl}(t,\eta)`$, its actual implementation contributes the sum of those costs. Oracle-query optimality alone says nothing about which implementation is practically best.

The finite-accuracy theorem bounds the sum of channel errors over the complete protocol. An error budget of half-diamond distances summing to at most $`1/6`$ leaves overall success at least $`2/3`$ after classical projection tolerance is included. This is a sufficient finite-operation budget, not a noise threshold or a fault-tolerance theorem. Duhamel's bound supplies one conservative condition for evolution under a nearby fixed Hamiltonian; an arbitrary operator-Lipschitz stability claim for noncommuting Hamiltonians is not assumed.

See [Interpretation and boundaries](interpretation.md) for physical units and observable examples, and [Related work](../references/related_work.md) for the inherited mechanisms and precise comparator models.
