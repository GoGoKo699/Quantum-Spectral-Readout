# Lower bounds for classical spectral readout

[Overview](../README.md) · [Model](model.md) · [Upper bound](multilevel_algorithm.md) · [Resources](resources.md)

This chapter gives self-contained proofs for the resource lower bounds of classical spectral readout. It distinguishes Hamiltonian interaction time, block-encoding queries, physical source copies, and reversible source-preparation queries. The lower-bound methods are standard adversary and binary-discrimination methods; the task-specific ingredient is the reduction from an arbitrary classical Wasserstein output to approximate interrogation of separated eigenvalue displacements.

## 1. Task, oracle models, and results

Let $`H=H^\dagger`$ act on a $`d`$-dimensional system, with known bound $`\|H\|\le 1`$. For a density operator $`\rho`$, define its weighted spectral measure by

```math
\mu_{H,\rho}(B)=\mathrm{Tr}[\rho E_H(B)],
```

where $`E_H`$ is the spectral projection-valued measure of $`H`$. The normalized density of states is the special case

```math
\mu_H=\mu_{H,I_d/d}=\frac1d\sum_{k=1}^d\delta_{\lambda_k(H)}.
```

The estimator must return a classical probability measure $`\widehat\mu`$ satisfying

**(1)**

```math
\Pr\!\left[W_1(\widehat\mu,\mu_{H,\rho})\le\epsilon\right]\ge\frac23
```

on every allowed input. The output may have arbitrary support, weights, and representation. Its meaning and subsequent classical processing cannot depend on further uncharged calls to the input oracles. An instruction to sample from the still-unknown Hamiltonian is not a classical approximation already returned by the algorithm.

All resource bounds below are worst-case hard caps. Arbitrary finite-dimensional ancillas, input-independent operations, intermediate measurements, randomness, classical adaptivity, and final collective measurements are permitted. An algorithm can retain every source specimen and ancillary register. No limitation on classical computation is used.

### 1.1 Hamiltonian interaction time

The evolution interface supplies controlled $`\exp(-itH)`$, for real $`t`$. A call is charged $`|t|`$; the cost is total summed interaction duration,

```math
T=\sum_k |t_k|.
```

The bound includes reverse evolution and arbitrary controls between calls. Parallel interactions are charged by the sum of their durations, not just their elapsed wall-clock time. A stronger continuous-control formulation, and the treatment of adaptive durations, are specified in Section 5.

Controlled access is part of the model. With only the uncontrolled channel $`X\mapsto e^{-itH}Xe^{itH}`$, the shift $`H\mapsto H+cI`$ is unobservable, although it translates the desired measure. Absolute spectral readout would then be unidentifiable without an additional energy reference.

### 1.2 Generic exact block encodings

An exact normalized block encoding is a unitary $`U_H`$ satisfying

```math
(\langle 0^a|\otimes I)U_H(|0^a\rangle\otimes I)=H.
```

Controlled $`U_H`$, $`U_H^\dagger`$, and controlled $`U_H^\dagger`$ are permitted and individually counted. A generic-interface algorithm must work for every valid completion of the specified block. We exhibit a particular exact completion whose unused blocks do not reveal strong classical eigenvalue bits.

### 1.3 Two distinct source interfaces

In the copy model, all dependence on the unknown source enters through at most $`N_\rho`$ copies of the product state $`\rho^{\otimes N_\rho}`$. No preparation unitary or inverse is available.

In the coherent source model, the source is supplied by a unitary $`U_\rho`$ with

```math
U_\rho|0\rangle=|\Psi_\rho\rangle,\qquad
\mathrm{Tr}_{E}|\Psi_\rho\rangle\langle\Psi_\rho|=\rho.
```

Calls to $`U_\rho,U_\rho^\dagger`$, and their controlled versions are counted in $`Q_\rho`$. This model does not additionally provide free copies of the unknown $`\rho`$. Without that restriction, a lower bound on $`Q_\rho`$ alone would be false: an algorithm could use only the free copies.

### 1.4 The lower bounds

For universal positive constants and $`0\lt \epsilon\le 1/256`$:

| Charged resource | Lower bound | Hard input and additional power allowed |
|---|---:|---|
| Total Hamiltonian interaction time $`T`$ | $`\Omega(\min\{d,\epsilon^{-1}\}/\epsilon)`$ | Source $`I_d/d`$ is known and freely preparable; all source coherences, ancillas, controls, and reverse evolution are allowed. |
| Generic exact block-encoding queries $`Q_H`$ | $`\Omega(\min\{d,\epsilon^{-1}\}/\epsilon)`$ | Same known free source; an explicit one-ancilla Hermitian unitary completion is supplied. |
| Unknown source copies $`N_\rho`$, $`d\ge2`$ | $`\Omega(\epsilon^{-2})`$ | $`H`$ is a fixed, classically known two-level Hamiltonian. |
| Coherent source-preparation queries $`Q_\rho`$, $`d\ge2`$ | $`\Omega(\epsilon^{-1})`$ | Same known $`H`$; an explicit weak purifier and its inverse are supplied. |

The first two bounds imply $`\Omega(\epsilon^{-2})`$ when $`d\ge c/\epsilon`$. At fixed $`d`$, the stated Hamiltonian lower bound is only $`\Omega(d/\epsilon)`$. It does not assert a violation of fixed-parameter Heisenberg scaling.

The four entries are separate coordinatewise minimax statements. They do not establish one input family on which all bounds must be saturated simultaneously, nor a joint resource tradeoff. No universal coherence-depth lower bound is claimed.

## 2. An ordered spectral hypercube in every dimension

Fix $`d\ge1`$ and $`0\lt \epsilon\le1/256`$. Set

**(2)**

```math
\delta=32\epsilon,\qquad
m=\min\!\left\{d,\left\lfloor\frac1{256\epsilon}\right\rfloor\right\}.
```

Thus $`m\ge1`$, $`m\delta\le1/8`$, and

**(3)**

```math
m\ge\frac1{512}\min\{d,\epsilon^{-1}\}.
```

For the last inequality, use $`\lfloor x\rfloor\ge x/2`$ when $`x\ge1`$, followed by $`\min\{d,a/256\}\ge\min\{d,a\}/256`$.

Partition the known computational basis into $`m`$ groups of sizes

```math
r_j\in\{\lfloor d/m\rfloor,\lceil d/m\rceil\},\qquad
\sum_{j=1}^m r_j=d.
```

Let $`P_j`$ denote the corresponding orthogonal projectors and $`w_j=r_j/d`$. Then

**(4)**

```math
\sum_j P_j=I_d,\qquad \sum_jw_j=1,\qquad
w_j\ge\frac1{2m}.
```

Indeed, $`d/m\ge1`$ and $`\lfloor d/m\rfloor\ge d/(2m)`$.

For $`z=(z_1,\ldots,z_m)\in\{-1,+1\}^m`$, define

**(5)**

```math
b_j=4\delta\left(j-\frac{m+1}{2}\right),\qquad
\lambda_j(z)=b_j+\delta z_j,\qquad
H_z=\sum_{j=1}^m\lambda_j(z)P_j.
```

These Hamiltonians obey stronger bounds than the task requires:

**(6)**

```math
\|H_z\|\le (2m-1)\delta\le\frac14,
\qquad
\lambda_{j+1}(z)-\lambda_j(z)\ge2\delta\gt 0.
```

In particular, the spectral order is the same for every $`z`$. Their normalized spectral measures are

**(7)**

```math
\mu_z=\mu_{H_z}=\sum_{j=1}^m w_j\delta_{\lambda_j(z)}.
```

All $`P_j,w_j,b_j,\delta`$, and the family itself may be disclosed to the algorithm. Only $`z`$ is hidden. Disclosure can only strengthen the algorithm, and demonstrates that the hardness does not rely on learning an unknown eigenbasis.

### Exact pairwise distance and its factor of two

Because the atoms have fixed order and fixed masses, quantile coupling gives

**(8)**

```math
W_1(\mu_z,\mu_{z'})
=\sum_jw_j|\lambda_j(z)-\lambda_j(z')|
=2\delta\sum_jw_j\mathbf1\{z_j\ne z'_j\}.
```

For equal masses this is $`2\delta\,d_{\mathrm H}(z,z')/m`$.

Equation (8) concerns two members of the hard family. The arbitrary-output decoder below has only a $`\delta`$ charge per wrong bit. These constants must not be interchanged. For example, with $`m=1`$, the output $`\delta_{b_1}`$ has distance $`\delta`$ from either hard measure; a fixed tie rule decodes the wrong bit on one of them. A putative $`2\delta`$-per-decoding-error inequality is therefore false.

## 3. Decoding any classical probability output

The following argument puts no restriction on the number of output atoms.

First push the output through the clipping map $`c(x)=\max\{-1,\min\{1,x\}\}`$. Since $`c`$ is 1-Lipschitz and fixes every true spectral point,

```math
W_1(c_\#\widehat\mu,\mu_z)\le W_1(\widehat\mu,\mu_z).
```

We may therefore assume all outputs are supported on $`[-1,1]`$. This also ensures finite quantile integrals on failure outcomes. Any invalid failure output can be replaced by $`\delta_0`$.

For a probability measure $`\nu`$ on the line, let $`q_\nu(u)=F_\nu^{-1}(u)`$, $`0\lt u\lt 1`$, be its generalized quantile. The standard one-dimensional transport identities are

**(9)**

```math
W_1(\nu,\mu)
=\int_0^1|q_\nu(u)-q_\mu(u)|\,du
=\int_{\mathbb R}|F_\nu(t)-F_\mu(t)|\,dt.
```

For completeness, $`|x-y|=\int|\mathbf1\{x\le t\}-\mathbf1\{y\le t\}|dt`$. Every coupling consequently has expected cost at least the CDF integral. In the coupling $`X=q_\nu(U),Y=q_\mu(U)`$ with common uniform $`U`$, the two threshold events are nested at every $`t`$, so equality holds. This proves both formulas. The underlying identity is classical; see Vallender [R1].

Write $`s_j=\sum_{k\le j}w_k`$, $`s_0=0`$. Define the output quantile centroids

**(10)**

```math
\widehat q_j=\frac1{w_j}\int_{s_{j-1}}^{s_j}q_{\widehat\mu}(u)\,du,
\qquad
\widehat z_j=
\begin{cases}
+1,&\widehat q_j\ge b_j,\\
-1,&\widehat q_j\lt b_j.
\end{cases}
```

This is a mathematical postprocessing of the returned classical measure. It need not be computationally efficient, because the lower bound grants unrestricted classical processing. The plus sign at equality fixes an otherwise arbitrary tie rule.

On the interval $`(s_{j-1},s_j)`$, the true quantile is the constant $`\lambda_j(z)`$. Jensen's inequality and the midpoint threshold imply

**(11)**

```math
\begin{aligned}
W_1(\widehat\mu,\mu_z)
&=\sum_j\int_{s_{j-1}}^{s_j}
 |q_{\widehat\mu}(u)-\lambda_j(z)|\,du\\
&\ge\sum_jw_j|\widehat q_j-\lambda_j(z)|\\
&\ge\delta\sum_jw_j\mathbf1\{\widehat z_j\ne z_j\}\\
&\ge\frac{\delta}{2m}\,d_{\mathrm H}(\widehat z,z).
\end{aligned}
```

The middle inequality holds because a centroid on the wrong side of the midpoint $`b_j`$ is at least $`\delta`$ away from the true atom $`b_j+\delta z_j`$. It remains valid at a tie.

Thus every successful output in (1) satisfies

**(12)**

```math
d_{\mathrm H}(\widehat z,z)
\le\frac{2m\epsilon}{\delta}
=\frac m{16}.
```

The error count is always at most $`m`$. Since the success probability is at least $`2/3`$ on every input,

**(13)**

```math
\mathbb E[d_{\mathrm H}(\widehat z,z)\mid z]
\le\frac23\frac m{16}+\frac13m
=\frac{3m}{8}.
```

This converts spectral estimation to approximate oracle interrogation, a standard query-complexity task [R2]. Crucially, it does not assume that the algorithm outputs a member of the hard family.

## 4. A hypercube adversary lemma with explicit output constants

Purify the initial randomness and every intermediate measurement, retaining discarded environments. Write $`|\psi_z\rangle`$ for the resulting final pure state. The final classical decoder acts on this state by a measurement and classical postprocessing.

Let

```math
e_{zj}=\Pr[\widehat z_j\ne z_j\mid z],\qquad
\bar e=\frac1{m2^m}\sum_z\sum_{j=1}^m e_{zj}.
```

Equation (13) gives $`\bar e\le3/8`$.

Introduce an auxiliary input-label register with computational basis $`|z\rangle`$, and let $`X_j`$ flip its $`j`$th bit. This register is only a proof device. Define

**(14)**

```math
\Gamma=\sum_{j=1}^mX_j,\qquad
|\Omega\rangle=2^{-m/2}\sum_z|z\rangle|\psi_z\rangle,\qquad
W=\langle\Omega|(\Gamma\otimes I)|\Omega\rangle.
```

Equivalently,

**(15)**

```math
W=2^{-m}\sum_z\sum_j
\mathrm{Re}\langle\psi_z|\psi_{z^{(j)}}\rangle,
```

where $`z^{(j)}`$ flips bit $`j`$. Both orientations of each hypercube edge appear in (15); this convention gives $`W_{\rm init}=m`$, not $`m/2`$. The initial state is independent of $`z`$, and every input-independent operation preserves $`W`$.

### 4.1 The final overlap bound

Consider an edge $`z,z^{(j)}`$, and set $`a=e_{zj}`$, $`b=e_{z^{(j)},j}`$. Applying the final binary bit-decoder measurement to the two states gives

**(16)**

```math
|\langle\psi_z|\psi_{z^{(j)}}\rangle|
\le \sqrt{a(1-b)}+\sqrt{b(1-a)}.
```

This is the elementary fidelity data-processing bound. It can also be proved directly: split the inner product using the two POVM elements $`E,I-E`$, apply the triangle inequality, and then Cauchy–Schwarz separately to the vectors obtained by applying $`\sqrt E`$ and $`\sqrt{I-E}`$.

Put $`s=(a+b)/2`$. A second Cauchy–Schwarz inequality gives

**(17)**

```math
\sqrt{a(1-b)}+\sqrt{b(1-a)}
\le \sqrt{(a+b)(2-a-b)}
=g(s),\qquad
g(s)=2\sqrt{s(1-s)}.
```

The function $`g`$ is concave on all of $`[0,1]`$. Averaging over oriented edges gives mean $`s=\bar e`$, since the bit-flip map permutes the inputs. Hence

**(18)**

```math
W_{\rm final}
\le m\,g(\bar e)
\le m\,g(3/8)
=\frac{\sqrt{15}}4m.
```

Jensen's inequality is valid even if some individual edges have $`s\gt 1/2`$. Monotonicity of $`g`$ is used only after averaging, at $`\bar e\le3/8\lt 1/2`$.

Define

**(19)**

```math
\kappa=1-\frac{\sqrt{15}}4\gt 0.
```

Every successful spectral estimator must decrease progress by at least $`\kappa m`$.

This is a standard positive-weight adversary argument [R3]. The continuous-time use of progress derivatives is also standard [R4]; the explicit calculation below is included to fix the resource model.

## 5. Lower bound for controlled total Hamiltonian evolution

For the hard family, the input-labelled Hamiltonian is

**(20)**

```math
\mathcal G
=\sum_z|z\rangle\langle z|\otimes H_z
=I\otimes\sum_j b_jP_j+\delta\sum_jZ_j\otimes P_j,
```

where $`Z_j|z\rangle=z_j|z\rangle`$.

The known baseline term commutes with $`\Gamma`$. In each orthogonal physical block $`P_j`$, only $`X_j`$ fails to commute with the unknown term. Therefore

**(21)**

```math
[\Gamma\otimes I,\mathcal G]
=\delta\sum_j[X_j,Z_j]\otimes P_j,
\qquad
\|[\Gamma\otimes I,\mathcal G]\|=2\delta.
```

Tensoring unused ancillas does not change this norm.

### 5.1 Arbitrary controls and signed evolution

Consider a continuous computation whose physical Hamiltonian is an arbitrary input-independent driver plus oracle interactions. An allowed oracle term has the form

**(22)**

```math
a_\ell(s)V_\ell(s)^\dagger
\bigl(C_\ell(s)\otimes H_z^{(\ell)}\bigr)V_\ell(s),
```

where $`a_\ell(s)`$ is real, $`C_\ell(s)`$ is a known Hermitian control contraction on registers separate from the queried system, and $`V_\ell(s)`$ is input independent. The query may be routed to any system register. Its rate is charged $`|a_\ell(s)|`$; $`C_\ell`$ may be absorbed into the normalization so that $`\|C_\ell\|\le1`$.

This model allows turning queries off, controlled evolution, sign reversal, arbitrary known conjugations, and simultaneous interactions. Input-independent drivers and pulses commute with $`\Gamma`$ on the label register. Equation (21), invariance under known conjugations, and the triangle inequality imply

**(23)**

```math
\left|\frac{dW}{ds}\right|
\le2\delta\sum_\ell|a_\ell(s)|.
```

Integrating and charging

```math
T=\int\sum_\ell|a_\ell(s)|\,ds
```

gives

**(24)**

```math
W_{\rm init}-W_{\rm final}\le2\delta T.
```

Consequently,

**(25)**

```math
T\ge\frac{\kappa m}{2\delta}
=\Omega\!\left(\frac{\min\{d,\epsilon^{-1}\}}{\epsilon}\right).
```

No restriction on the strength of the input-independent driver was used. The unknown interaction strength, including any externally amplified coefficient, must be charged through its absolute rate.

For a single discrete evolution call, the same bound can be seen without differentiation: along an edge $`z,z^{(j)}`$, the affected physical block changes by

**(26)**

```math
|e^{-it(b_j+\delta)}-e^{-it(b_j-\delta)}|
=2|\sin(\delta t)|
\le2\delta|t|.
```

The commutator again has only that one active bit in each physical block. Long evolution, inverse evolution, and controls cannot evade the bound.

### 5.2 Adaptive durations with a branchwise hard cap

A finite adaptive protocol may choose its next duration $`t_h`$ from the classical measurement history $`h`$, subject to

```math
\sum_{\text{queries along }h}|t_h|\le T
```

on every complete history. Simply summing the longest duration at every query depth can overcharge such a protocol, so that argument is not used.

Instead purify the measurements while retaining an orthogonal history register, and use a common clock $`s\in[0,T]`$ that measures accumulated interaction duration. For each decision-tree node $`h`$, let $`\tau(h)`$ be its accumulated preceding cost. During the interval

```math
[\tau(h),\,\tau(h)+|t_h|]
```

the history-$`h`$ branch evolves under $`\mathrm{sign}(t_h)H_z`$, with its prescribed query control and register routing. At the endpoint, apply the known unitary dilation of that branch's intervening processing and measurement, controlled on its history. Finished branches are inactive for the remaining clock interval.

The union of these branch endpoints is a known finite schedule determined by the protocol, independent of $`z`$. At each clock value, the active generator is a direct sum over orthogonal history sectors. Each active sector has commutator norm at most $`2\delta`$, so the complete generator also has norm bound $`2\delta`$. All history updates commute with $`\Gamma`$. Thus the same integration over the common interval $`[0,T]`$ proves (25).

This construction preserves the adaptive protocol's classical output law because the history is retained, exactly as in its standard measurement dilation. It does not assume a distribution of stopping times. Limits of finite protocols with the same hard cap whose output distributions converge in total variation inherit the bound by continuity.

For a coherently time-controlled query, a declared duration is charged by the maximum absolute duration on its coherent branches. It is already covered by the contraction-controlled model above. No alternative notion of an unobserved branch's quantum “expected duration” is assumed.

### 5.3 The source can be known and freely reversible

The source for the proof is $`I_d/d`$, independently of $`z`$. It can be granted for free, together with any known purification, its preparation unitary and inverse, and unlimited additional copies. All such operations are input independent and preserve $`W`$.

For the general weighted-measure task, a fixed known pure source also suffices: choose one unit vector $`|j\rangle`$ in each $`P_j`$ and use

```math
|\phi\rangle=\sum_j\sqrt{w_j}\,|j\rangle.
```

Its weighted spectral measure is exactly (7). Granting this known source and its coherent preparation for free yields the same lower bound.

The theorem therefore does not attribute the Hamiltonian-time obstruction to a difficulty preparing or reversing the source. It also does not claim the bound for every fixed source: a known state supported on one known eigenvector can have a much easier spectral measure.

## 6. Exact weak block completion

Define the real two-by-two matrix

**(27)**

```math
R(h)=
\begin{pmatrix}
h&\sqrt{1-h^2}\\
\sqrt{1-h^2}&-h
\end{pmatrix},
\qquad |h|\lt 1.
```

It satisfies $`R(h)^\dagger=R(h)`$ and $`R(h)^2=I_2`$. Give the algorithm the unitary

**(28)**

```math
U_z=\sum_{j=1}^m R(\lambda_j(z))\otimes P_j.
```

The first register is a single block-encoding ancilla. Its upper-left block is $`H_z`$, so this is an exact normalized block encoding. Moreover, $`U_z^\dagger=U_z`$.

The derivative is

**(29)**

```math
R'(h)=
\begin{pmatrix}
1&-h/\sqrt{1-h^2}\\
-h/\sqrt{1-h^2}&-1
\end{pmatrix},
\qquad
R'(h)^2=\frac1{1-h^2}I_2.
```

Hence

```math
\|R'(h)\|=\frac1{\sqrt{1-h^2}}\le\frac2{\sqrt3}
\quad\text{for }|h|\le\frac12.
```

All interpolation points between $`b_j-\delta`$ and $`b_j+\delta`$ lie in this interval. Integration gives

**(30)**

```math
\|R(b_j+\delta)-R(b_j-\delta)\|
\le\frac{4\delta}{\sqrt3}.
```

The unused square-root block changes only by the same weak amount. There is no uncharged strong bit in the oracle completion.

Let $`\mathcal U=\sum_z|z\rangle\langle z|\otimes U_z`$. In physical block $`P_j`$, the oracle depends only on $`z_j`$. Therefore

**(31)**

```math
\|[\Gamma\otimes I,\mathcal U]\|
=\max_j\|R(b_j+\delta)-R(b_j-\delta)\|
\le\frac{4\delta}{\sqrt3}.
```

One query changes progress by at most this norm:

**(32)**

```math
\begin{aligned}
|W_{\rm after}-W_{\rm before}|
&=\left|\langle\Omega|
\mathcal U^\dagger(\Gamma\otimes I)\mathcal U
-(\Gamma\otimes I)|\Omega\rangle\right|\\
&\le\|[\Gamma\otimes I,\mathcal U]\|.
\end{aligned}
```

Controlled calls add an identity block and do not increase the norm. Inverse calls are the same oracle on this family. Query choices based on measured history can be coherently controlled on the retained history register. A hard cap of $`Q_H`$ queries can be padded with inactive controlled calls.

The required progress gap now gives

**(33)**

```math
Q_H\ge\frac{\kappa\sqrt3\,m}{4\delta}
=\Omega\!\left(\frac{\min\{d,\epsilon^{-1}\}}{\epsilon}\right).
```

If multiple queries occur in parallel, each is charged and the same bound follows by telescoping over them. The result concerns a generic block-encoding interface. A different input promise that exposes extra strong information in another oracle block is a different access model and is not covered by declaring its cost to be one generic block query.

## 7. Unknown source copies: an elementary sharp exponent

For $`d\ge2`$, fix the known Hamiltonian

```math
H_*=-|0\rangle\langle0|+|1\rangle\langle1|
```

with zero action on the remaining subspace, which is never populated. Let

**(34)**

```math
\rho_\pm=
\left(\frac12\pm\epsilon\right)|0\rangle\langle0|
+\left(\frac12\mp\epsilon\right)|1\rangle\langle1|.
```

The two spectral measures have distance

**(35)**

```math
W_1(\mu_{H_*,\rho_+},\mu_{H_*,\rho_-})=4\epsilon,
```

because a mass $`2\epsilon`$ moves across distance $`2`$. Their means are respectively $`-2\epsilon`$ and $`+2\epsilon`$.

A successful $`W_1`$-estimate has mean within $`\epsilon`$ of the true mean, since $`x\mapsto x`$ is 1-Lipschitz. The sign of its mean therefore distinguishes $`\rho_+`$ and $`\rho_-`$ with probability at least $`2/3`$. The radius-$`\epsilon`$ success sets are disjoint; the pairwise distance here is $`4\epsilon`$, not $`2\epsilon`$.

The states commute, so any experiment on $`N`$ copies is a channel applied to the classical product distributions

```math
P_\pm^{\otimes N},\qquad P_\pm=(1/2\pm\epsilon,\,1/2\mp\epsilon).
```

The single-copy root fidelity, also called the Bhattacharyya coefficient, is

```math
B(P_+,P_-)=\sqrt{1-4\epsilon^2}.
```

For arbitrary classical distributions, Cauchy–Schwarz applied to
$`(\sqrt p-\sqrt q)(\sqrt p+\sqrt q)`$ gives
$`\mathrm{TV}(P,Q)\le\sqrt{1-B(P,Q)^2}`$. Multiplicativity and Bernoulli's inequality consequently give

**(36)**

```math
\begin{aligned}
\mathrm{TV}(P_+^{\otimes N},P_-^{\otimes N})
&\le\sqrt{1-(1-4\epsilon^2)^N}\\
&\le 2\epsilon\sqrt N.
\end{aligned}
```

Equal-prior binary success probability is at most $`(1+\mathrm{TV})/2`$. Success at least $`2/3`$ requires TV at least $`1/3`$, and hence

**(37)**

```math
N_\rho\ge\frac1{36\epsilon^2}.
```

Arbitrary joint measurements, source retention, and unlimited operations involving the known $`H_*`$ cannot increase this input distinguishability. Adaptive protocols with a hard copy cap are covered by padding with unused copies. This is the standard two-point sampling obstruction, not a new quantum copy lower-bound technique.

## 8. Coherent source queries: an explicit weak purifier

Use the same two source states. Define

```math
\theta_\pm=\frac\pi4\mp\frac12\arcsin(2\epsilon),\qquad
A(\theta)=
\begin{pmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{pmatrix}.
```

On the two-dimensional active source subspace and one environment qubit, let

**(38)**

```math
U_\pm=\mathrm{CNOT}\,(A(\theta_\pm)\otimes I).
```

Extend these unitaries by the identity outside the active source subspace when $`d\gt 2`$. Then

```math
U_\pm|00\rangle
=\sqrt{1/2\pm\epsilon}\,|00\rangle
+\sqrt{1/2\mp\epsilon}\,|11\rangle,
```

which is a purification of $`\rho_\pm`$. This specifies the whole unitary, not just its action on the initial state.

Let $`\Delta_\theta=\arcsin(2\epsilon)`$. The oracle difference is exactly

**(39)**

```math
\|U_+-U_-\|=2\sin(\Delta_\theta/2).
```

For $`0\lt \epsilon\le1/4`$,

**(40)**

```math
2\sin(\Delta_\theta/2)
\le\Delta_\theta
\le\frac{2\epsilon}{\sqrt{1-4\epsilon^2}}
\le\frac{4\epsilon}{\sqrt3}.
```

The same difference norm holds for inverse calls, and does not increase for controlled calls. One may even grant a direct selector between forward, inverse, and inactive queries at the same cost: its difference norm is the maximum of these three blocks.

A standard hybrid argument shows that after $`Q_\rho`$ queries, the Euclidean distance between purifications of the two final algorithm states is at most

**(41)**

```math
Q_\rho\|U_+-U_-\|.
```

Indeed, replace the calls one at a time; each replacement changes the final state vector by at most the oracle difference norm, while all surrounding unitaries preserve norm. Purified adaptivity and unused-query padding are allowed.

The trace distance of two pure states is no larger than their Euclidean vector distance. Therefore the output distributions can have TV at most the right-hand side of (41). The same binary-decision reduction used above requires TV at least $`1/3`$, giving

**(42)**

```math
Q_\rho
\ge\frac1{6\sin(\tfrac12\arcsin(2\epsilon))}
\ge\frac{\sqrt3}{12\epsilon}.
```

The source is the only input that varies in this proof; $`H_*`$ is fully known. Every use of an unknown source copy must enter through a counted preparation call. The result is the usual coherent amplitude-estimation lower exponent, provided here with a complete weak oracle so that uncontrolled parts of a purification unitary cannot supply extra information. General sample-to-query lifting also supplies this exponent [R6].

## 9. What the finite-dimensional result does and does not say

The hard family has $`m=\Theta(\min\{d,\epsilon^{-1}\})`$ ordered, independently shifted spectral groups. A displacement is of order $`\epsilon`$; a nontrivial fraction of these displacements must be learned. The cost $`\Omega(m/\epsilon)`$ is a direct-sum cost for many parameters.

When $`d`$ is fixed and $`\epsilon\to0`$, this construction yields $`\Omega(d/\epsilon)`$. When $`d`$ grows enough to support $`m=\Theta(1/\epsilon)`$ resolvable groups in a bounded interval, it yields $`\Omega(\epsilon^{-2})`$. The Hamiltonians in the proof are diagonal in a disclosed basis. No random eigenbasis, matrix-element loading, QRAM, graph-access assumption, or state-preparation cost is hidden in the time bound.

The dimension-independent upper $`\widetilde O(\epsilon^{-2})`$, if combined with these theorems, is optimal in the high-dimensional worst case. These lower bounds alone do not give a matching small-$`d`$ upper for arbitrary weighted measures. In particular, unknown weights and the cost of the source must be accounted for separately in any finite-dimensional refinement.

A single energy expectation with reversible source preparation admits the standard amplitude-estimation exponent $`1/\epsilon`$. The present task returns one classical measure approximating all 1-Lipschitz spectral expectations simultaneously. The stronger output requirement can incur an additional inverse-precision factor in the high-dimensional worst case. This is an output-size/parameter-count obstruction in the oracle model, rather than a claim that every individual spectral observable is hard.

The proof does not establish a universal depth lower bound, a benefit or impossibility of inter-shot entanglement under every resource budget, an expected-stopping-time theorem, or a joint Pareto frontier. It also does not close the graph-local query gap in Li–Liao–Yang [R8]: graph ports and generic unitary block encodings have different implementation costs.

## 10. Detailed comparison with Wang's 2026 spectrum lower bound

### 10.1 The close mathematical relationship

Wang's revised *A Unified Complexity Framework for Quantum Property Testing*, arXiv:2608.02600v4, is an essential related result [R5]. Theorem 5.15 gives a sample lower bound for learning the ordered eigenvalue vector of a density operator $`\tau`$ in total variation error $`\eta`$:

**(43)**

```math
S_W(d,\eta)
=\Omega\!\left(
\frac{d^2}{
\eta^2\log^2d\,\max\{1,\eta^2\log^2d\}}
\right).
```

The spectrum bound follows there by reduction from estimating trace distance to $`I_d/d`$. The paper's Section 1.2 defines coherent query access as a unitary preparing a purification of $`\tau`$. Combining its hard binary distinction with purified sample-to-query lifting yields

**(44)**

```math
Q_W(d,\eta)
=\Omega\!\left(
\frac{d}{
\eta\log d\,\sqrt{\max\{1,\eta^2\log^2d\}}}
\right).
```

For $`\eta\log d\le1`$, this is $`\Omega(d/(\eta\log d))`$.

The output metrics are related by an exact identity. For density operators $`\tau,\sigma`$, define

```math
\nu_\tau=\frac1d\sum_i\delta_{d\lambda_i(\tau)-1}.
```

Ordering both spectra gives

**(45)**

```math
W_1(\nu_\tau,\nu_\sigma)
=\sum_i|\lambda_i(\tau)-\lambda_i(\sigma)|
=2\,\mathrm{TV}(\lambda(\tau),\lambda(\sigma)).
```

For a positive normalization $`M`$, consider a promised family satisfying
$`\|d\tau-I\|\le M`$, and set

**(46)**

```math
H_\tau=\frac{d\tau-I}{M}.
```

Then

**(47)**

```math
W_1(\mu_{H_\tau},\mu_{H_\sigma})
=\frac1M\|\lambda(\tau)-\lambda(\sigma)\|_1
=\frac2M\mathrm{TV}(\lambda(\tau),\lambda(\sigma)).
```

Thus an output-metric mismatch does not explain the difference between the results.

Even an arbitrary probability-measure output can be converted to a density-spectrum estimate. Take its $`d`$ equal-mass quantile centroids $`\widehat h_i`$, form
$`\widetilde\lambda_i=(1+M\widehat h_i)/d`$, and use (11)'s first Jensen step:

```math
\sum_i|\widetilde\lambda_i-\lambda_i(\tau)|
\le M W_1(\widehat\mu,\mu_{H_\tau}).
```

The raw vector may fail positivity or normalization. Its nearest $`\ell_1`$ projection onto the ordered probability simplex is within another $`M W_1`$, because the true vector is feasible. Consequently one obtains a valid sorted probability vector with TV error at most $`M W_1`$. This loses only a constant relative to the exact pairwise identity (47).

### 10.2 The access normalization does not transfer for free

The relevant purified access in [R5,R6] supplies $`U_\tau|0\rangle=|\Psi_\tau\rangle`$, with forward, inverse, and controlled queries counted. A constant number of such queries constructs a block encoding of $`\tau`$. It does not directly provide a normalized block encoding of $`(d\tau-I)/M`$.

In the evolution picture the required rescaling is explicit:

**(48)**

```math
e^{-itH_\tau}
=e^{it/M}\,e^{-i\tau\,dt/M}.
```

The scalar phase is known and can be implemented on the control. The unknown density-operator interaction has duration $`d|t|/M`$. A standard block-encoding simulation therefore incurs the factor $`d/M`$ in its time-dependent query cost, in addition to its precision/call overhead.

The same issue appears before simulation: combining a block encoding of $`\tau`$ with the known identity gives a block encoding of

```math
\frac{d\tau-I}{d+1}
=\frac{M}{d+1}H_\tau.
```

Its normalization is $`(d+1)/M`$ relative to the desired $`H_\tau`$. Amplifying this block is a charged operation.

The lifting corollary itself states its domain precisely. Corollary 1.2 of Chen–Wang–Zhang [R6] lower-bounds queries to an oracle whose top block is $`\tau/\alpha`$, for $`\alpha\ge1`$. The earlier Wang–Zhang theorem [R7] used the same kind of density-operator normalization. Neither statement allows $`\alpha`$ of order $`1/d`$ at unit cost.

For the strongest possible test of a direct transfer, grant that the relevant Wang hard distinction also has the promise in (46). Even granting ideal simulation with query cost proportional to $`dT/M`$, substitution into (44) gives only

**(49)**

```math
T=\Omega\!\left(
\frac{M}{
\eta\log d\,\sqrt{\max\{1,\eta^2\log^2d\}}}
\right).
```

With $`\eta=\Theta(M\epsilon_H)`$, the leading ratio $`M/\eta`$ becomes $`\Theta(1/\epsilon_H)`$. The factor $`d`$ has cancelled. Actual simulation overhead cannot strengthen this simple inference.

Equation (49) is an analysis of that specific reduction, not a theorem that every conceivable conversion must cost exactly $`d/M`$. A new, stronger conversion or a new argument using the prior hard family would require its own proof. The inspected lifting theorem and the usual normalization conversion do not immediately yield (25) or (33).

### 10.3 The tempting reverse reduction has the wrong direction

If $`H`$ is trace zero and $`\|H\|\le1/2`$, then $`\tau=(I+H)/d`$ is a density operator. For the known maximally entangled state $`|\Phi_d\rangle`$, the vector $`(\sqrt{I+H}\otimes I)|\Phi_d\rangle`$ is normalized and has reduced state $`\tau`$. Any construction that realizes this state-preparation map from the normalized-$`H`$ interface, whether efficient or even free, has the following direction.

This observation runs from the stronger normalized-$`H`$ interface to the purifier. It does not implement normalized $`H`$ from the purifier. A lower bound for the weaker purifier interface cannot be transferred to the stronger interface in that direction.

Accordingly, Wang's results are closely related, current spectrum-estimation lower bounds, but their inspected statements do not subsume the present charged Hamiltonian-time bound by a free change of variables. Any assertion that spectrum estimation had no sharp lower bounds before this work would be false.

## 11. Attribution and remaining research boundaries

The ingredients inherited from established work are:

1. One-dimensional quantile/CDF transport identities [R1].
2. Oracle interrogation and positive-weight adversary progress [R2,R3].
3. Continuous-time adversary differentiation with arbitrary known driving controls [R4].
4. Fidelity/trace-distance data processing, binary discrimination, and hybrid bounds; these were reconstructed directly in the proofs above.
5. Sample-to-query lifting and coherent Bernoulli/amplitude-estimation lower exponents [R6,R7].

The specialized content proved here is the ordered spectral packing with an arbitrary-output quantile decoder, its weak exact block completion, and the resulting finite-dimensional resource law under explicitly charged controls and evolution. These arguments are not proposed as new general adversary machinery.

The generic coherent upper exponent $`\widetilde O(\epsilon^{-2})`$ is already implied by Li–Liao–Yang's spectral-sampling and coherent distribution-estimation components [R8]. Combining that upper with the lower proved here identifies the optimal Hamiltonian-query exponent in the high-dimensional regime. A source-copy implementation attaining the same exponent has a separate operational consequence: the optimal Hamiltonian scaling does not require reversible source access. Prior multilevel and independent-shot methods must be credited in establishing that algorithmic comparison.

The mathematical questions left open are a matching finite-$`d`$ upper for all source models, expected-cost formulations, a universal coherence-depth theorem, and a joint time/source tradeoff. None is needed for the high-dimensional worst-case lower bounds proved here. The comparison of the fresh-copy upper with the closest spectral-estimation algorithms is logically separate from these lower-bound proofs.

## References

- **[R1]** S. S. Vallender, *Calculation of the Wasserstein Distance Between Probability Distributions on the Line*, Theory of Probability & Its Applications 18, 784–786 (1974). [Primary publication](https://doi.org/10.1137/1118101). The transport identity is also proved in Section 3 above.
- **[R2]** Wim van Dam, *Quantum Oracle Interrogation: Getting all information for almost half the price*, FOCS 1998. [Author's arXiv manuscript](https://arxiv.org/abs/quant-ph/9805006), [publication](https://doi.org/10.1109/SFCS.1998.743486). Cited for the interrogation task and its established query-complexity context, not as the source of the spectral packing.
- **[R3]** Andris Ambainis, *Quantum Lower Bounds by Quantum Arguments*, J. Comput. Syst. Sci. 64 (2002). [Author's arXiv manuscript](https://arxiv.org/abs/quant-ph/0002066), [publication](https://doi.org/10.1006/jcss.2002.1826). The particular progress and output calculations are proved above.
- **[R4]** David Yonge-Mallo, *Adversary lower bounds in the Hamiltonian oracle model*, arXiv:1108.2479 (2011; original manuscript written in 2007). [Primary PDF](https://arxiv.org/pdf/1108.2479). Sections 2–3 cover signed oracle strength, input-independent drivers, orthogonal physical query sectors, and spectral adversary progress.
- **[R5]** Qisheng Wang, *A Unified Complexity Framework for Quantum Property Testing*, arXiv:2608.02600v4, 29 October 2026. [Referenced revision](https://arxiv.org/pdf/2608.02600v4). See Sections 1.2, 1.2.2, 5.3, and 5.4, particularly Theorem 5.15 and the purified-query convention.
- **[R6]** Kean Chen, Qisheng Wang, Zhicheng Zhang, *A List of Complexity Bounds for Property Testing by Quantum Sample-to-Query Lifting*, arXiv:2512.01971v1 (2025). [Primary full text](https://arxiv.org/html/2512.01971v1). Definition 1.1, Theorem 1.1, and Corollary 1.2 specify purified access and the normalization $`\alpha\ge1`$.
- **[R7]** Qisheng Wang and Zhicheng Zhang, *Quantum Lower Bounds by Sample-to-Query Lifting*, SIAM J. Comput. 54, 1294–1334 (2025). [Final arXiv version](https://arxiv.org/abs/2308.01794), [publication](https://doi.org/10.1137/24M1638616). Cited for the original block-encoded lifting framework; the sharpened normalization statement used in Section 10 is quoted from [R6].
- **[R8]** Rong-Hua Li, Meihao Liao, Yichun Yang, *Classical and quantum spectral density estimation under local graph access*, arXiv:2608.22769v2 (2026). [Primary manuscript](https://arxiv.org/abs/2608.22769). The generic coherent ingredients of Lemmas 35 and 37 already give the $`\widetilde O(\epsilon^{-2})`$ block-query upper; the graph-local implementation has additional costs.

## Finite verification artifact

The companion script [validate_spectral_lower.py](../verification/validate_spectral_lower.py) checks small hypercube commutator matrices, the edge-overlap inequality on a finite grid, unequal-multiplicity quantile transport, the midpoint counterexample to an erroneous factor of two, and the explicit purifier difference. These checks can catch algebra or convention mistakes; the proofs above, rather than finite experiments, establish the asymptotic statements.
