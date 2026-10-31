# Full spectral readout from fresh source copies: upper bound

[Overview](../README.md) · [Model](model.md) · [Lower bounds](lower_bounds.md) · [Resources](resources.md)

## 1. Statement, access model, and attribution

Let $`H`$ be a Hermitian operator on a finite-dimensional Hilbert space $`\mathcal H`$, with $`\|H\|\leq 1`$. Let $`\rho`$ be an arbitrary density operator on $`\mathcal H`$. The source supplies independent copies of this same state. We do not assume a classical description, a preparation unitary, access to a purification, an inverse preparation, or a reflection about the source. In particular, $`[H,\rho]`$ need not vanish. The target is the probability measure

```math
 \mu(B)=\operatorname{Tr}(\rho E_H(B)),\qquad B\subseteq[-1,1],
```

where $`E_H`$ denotes the spectral measure of $`H`$.

In the evolution formulation, the supplied operation is

```math
 C_H(t)=|0\rangle\langle0|\otimes I+
        |1\rangle\langle1|\otimes e^{-itH}.
```

Controlled evolution is an explicit access assumption. It is not inferred from an uncontrolled black-box evolution. The charged interaction resource is the sum of $`|t|`$ over all calls, including calls in different experiments. The construction below uses nonnegative times only. It keeps one source copy during a short sequence of phase-estimation measurements, then discards that copy. Independent source experiments are never coherently joined.

For probability measures on the real line, write $`F_\nu(x)=\nu((-\infty,x])`$. We use the standard identity

```math
 W_1(\nu,\nu')=\int_{\mathbb R}|F_\nu(x)-F_{\nu'}(x)|\,dx.
```

This is the one-dimensional Wasserstein/CDF identity; see Vallender [V74]. All measures constructed below are supported on $`[-1,1]`$, so the integral is restricted to that interval.

**Theorem 1 (fresh-copy spectral readout).** For every rational $`0<\epsilon\leq 1/4`$, there is a protocol in the model above that outputs a finite classical probability measure $`\widehat\mu`$, supported on $`O(1/\epsilon)`$ explicitly specified rational grid points, such that

```math
 \Pr\{W_1(\widehat\mu,\mu)\leq\epsilon\}\geq 2/3.
```

It uses

```math
 N=O(\epsilon^{-2})\quad\text{source copies},\qquad
 T=O\!\left(\epsilon^{-2}\log^3(1/\epsilon)\right)
       \quad\text{total absolute evolution time}.
```

The total evolution while retaining any one source system is $`O(1/\epsilon)`$. This is an achieved resource bound, not a lower bound on circuit depth. It does not include a claim about hardware wall-clock time, error-correction overhead, or the difficulty of supplying the evolution interface.

With exact quantum operations and exact classical projection, the explicit parameters below give success probability at least $`11/12`$. This slack permits finite-accuracy implementations as specified in Section 8. The output can be represented with $`O(\epsilon^{-1}\log^2(1/\epsilon))`$ bits, in addition to a description of the requested tolerance. Beyond reading the tolerance input, classical processing is polynomial and can be implemented with $`\widetilde O(\epsilon^{-2})`$ bit operations using the standard fixed-precision arithmetic conventions detailed in Section 7.

The same copy bound and an $`O(\epsilon^{-2}\log^3(1/\epsilon))`$ query bound hold if an exact normalized block encoding of $`H`$, its inverse, and their controlled versions are supplied. Section 9 gives the reduction for a general, not necessarily Hermitian, block-encoding unitary, including the additional flag and retained workspace.

The proof combines established phase estimation, nondemolition spectral measurements, multilevel Monte Carlo, and isotonic regression. Whole-distribution multilevel estimators predate this application [GNR15], and the coherent-source Hamiltonian-query upper with the same precision exponent is already implied by Li, Liao and Yang [LLY26, Lemmas 35–37]. The claim proved here is the fresh-copy realization with separate source and evolution accounting. The existence of a reusable classical distribution is not itself a new feature of spectral estimation.

## 2. A phase estimator with a uniform first-moment bound

### 2.1 The phase-estimation instrument

Let $`W`$ be a unitary with spectral resolution

```math
 W=\sum_{\theta}e^{2\pi i\theta}P_\theta,
 \qquad \theta\in[0,1).
```

For a power of two $`M`$, ordinary Fourier phase estimation prepares a uniform clock of size $`M`$, applies controlled powers of $`W`$, applies the inverse discrete Fourier transform to the clock, and measures its value $`y\in\{0,\ldots,M-1\}`$. Its Kraus operator on the retained system is

```math
 K_{M,y}(W)=\frac1M\sum_{r=0}^{M-1}
                  e^{-2\pi i r y/M}W^r.
```

This is the standard phase-estimation construction; [CEMM98, Section 5, Eqs. (5.1)–(5.2)] gives the corresponding Fourier amplitudes. We retain the operator form because it specifies the measurement back-action that the multilevel coupling needs.

On an eigenphase $`\theta`$, the output law is

```math
 p_M(y\mid\theta)
 =\left|\frac1M\sum_{r=0}^{M-1}
       e^{2\pi i r(\theta-y/M)}\right|^2.
```

The usual limiting interpretation applies when the phase difference is an integer. In particular, the expression is then one at the matching grid point. The completeness relation
$`\sum_yK_{M,y}^\dagger K_{M,y}=I`$ follows directly from Fourier orthogonality.

Let $`d_{\mathbb T}`$ denote circular distance on $`\mathbb R/\mathbb Z`$. The geometric-series formula and
$`|\sin(\pi u)|\geq 2d_{\mathbb T}(u,0)`$ give

```math
 p_M(y\mid\theta)
 \leq \min\!\left\{1,\frac{1}
       {4M^2d_{\mathbb T}(\theta,y/M)^2}\right\}.
```

For $`s>0`$, a convenient uniform tail bound is

```math
 \Pr_\theta\{d_{\mathbb T}(\theta,y/M)\geq s\}
 \leq \min\{1,2/(Ms)\}.
```

Here is an elementary verification of the constant. Each distance annulus
$`[k/M,(k+1)/M)`$ contains at most two clock points. If $`Ms\geq2`$ and $`r=\lfloor Ms\rfloor`$, summing the pointwise probability bound gives at most
$`\frac12\sum_{k=r}^{\infty}k^{-2}\leq[2(r-1)]^{-1}`$.
Since $`r-1\geq Ms/3`$ in this range, the result is at most $`2/(Ms)`$. If $`Ms<2`$, the bound by one suffices. Values $`s>1/2`$ have zero tail.

### 2.2 An energy readout without phase aliasing

For the evolution interface, use

```math
 V=-e^{-i\pi H/2}.
```

An energy $`\lambda\in[-1,1]`$ corresponds to
$`\theta_\lambda=1/2-\lambda/4\in[1/4,3/4]`$. The known minus sign in the definition of $`V`$ is implemented as a phase on the control; it is not an additional Hamiltonian assumption. Decode a clock outcome by

```math
 g(q)=\operatorname{clip}_{[-1,1]}(2-4q),
 \qquad q=y/M.
```

For every $`q\in[0,1)`$ and every $`\theta=\theta_\lambda`$,

```math
 |g(q)-\lambda|\leq8d_{\mathbb T}(q,\theta).
```

Indeed, when the shorter circular arc is the ordinary interval between $`q`$ and $`\theta`$, clipping cannot increase the error and the factor four suffices. Otherwise $`|q-\theta|>1/2`$; because $`\theta\in[1/4,3/4]`$, the circular distance is at least $`1/4`$, whereas the energy error is at most two. This proves the decoder bound also across the phase wrap.

Combining the circular-phase tail with the decoder bound, one ordinary readout $`X_M`$ satisfies

```math
 \Pr_\lambda\{|X_M-\lambda|\geq r\}
 \leq\min\{1,16/(Mr)\}.
```

Its first moment has an avoidable logarithmic tail loss. We remove that loss with a constant number of retained-system measurements.

### 2.3 Median of three

Perform three ordinary readouts of clock size $`M`$ on the same retained system, with fresh clock ancillas. Section 3 proves that these three outputs are independent conditional on a common latent eigenphase. Let $`Y_M`$ be their ordinary real median.

If the median differs from $`\lambda`$ by at least $`r`$, at least two readouts have absolute error at least $`r`$. Conditional independence and a union bound over the three pairs imply

```math
 \Pr_\lambda\{|Y_M-\lambda|\geq r\}
 \leq\min\{1,768/(M^2r^2)\}.
```

Integrating this tail over $`0\leq r\leq2`$, or over the larger interval $`0\leq r<\infty`$, yields

```math
 \mathbb E_\lambda|Y_M-\lambda|
 \leq \frac{32\sqrt3}{M}
 \leq\frac{64}{M}.
```

This is uniform in the energy and the dimension, with no spectral-gap, density, or minimum-weight assumption. The use of a real energy median rather than a naive circular phase median avoids a boundary convention for the latter.

An ordinary size-$`M`$ readout applies controlled $`V^{2^k}`$ for $`k=0,\ldots,\log_2M-1`$. In the evolution model, these powers require total evolution
$`\frac{\pi}{2}(M-1)`$. Thus a median readout has total evolution
$`\frac{3\pi}{2}(M-1)`$. Its known circuit work includes the clock Fourier transforms and control phases.

## 3. Exact coupling from retaining the same system

The following statement formalizes both the median repetition and the coarse/fine coupling.

**Lemma 2 (retained-system spectral coupling).** Fix a unitary $`W`$, a state $`\sigma`$, and clock sizes $`M_1,\ldots,M_r`$. Apply the phase-estimation instruments from Section 2.1 sequentially to one copy of $`\sigma`$, retaining the full system on which $`W`$ acts between instruments. Then

```math
 \Pr(y_1,\ldots,y_r)
 =\sum_\theta \operatorname{Tr}(\sigma P_\theta)
                 \prod_{i=1}^{r}p_{M_i}(y_i\mid\theta).
```

Consequently, the joint output law can be represented by drawing one latent phase from the spectral measure of $`W`$ in $`\sigma`$, then drawing the clock outcomes independently conditional on that phase. This latent variable is a proof device; the protocol does not prepare or identify an eigenstate.

**Proof.** All $`K_{M_i,y_i}(W)`$ are functions of the same normal operator. They therefore commute with each other and with their adjoints. The sequential probability is

```math
 \begin{aligned}
 &\operatorname{Tr}\!\left(
 K_r\cdots K_1\,\sigma\,K_1^\dagger\cdots K_r^\dagger
 \right)\\
 &\qquad=\operatorname{Tr}\!\left(
 \sigma\prod_{i=1}^{r}K_i^\dagger K_i\right)
 =\sum_\theta \operatorname{Tr}(\sigma P_\theta)
                 \prod_{i=1}^{r}|k_i(\theta)|^2,
 \end{aligned}
```

where $`k_i(\theta)`$ is the eigenvalue of $`K_i`$ at phase $`\theta`$. The definition of the single-readout distribution identifies its squared modulus with $`p_{M_i}`$. This argument uses neither purity nor commutation of $`\sigma`$ with $`W`$. Degenerate eigenspaces are handled by their full projectors. $`\square`$

After an earlier outcome is observed, the conditional source state generally changes. The lemma does not claim otherwise. It says exactly which joint classical statistics the changed state produces. In particular, every later readout has the same unconditional marginal as a standalone readout on the original source. The nonselective instrument preserves all spectral weights.

At level $`\ell\geq1`$, run three readouts of size $`M_{\ell-1}`$, followed by three of size $`M_\ell`$, on one fresh source copy. Take the two medians. The resulting pair has the correct coarse and fine marginal laws and a common latent energy. Distinct pairs, and pairs belonging to distinct levels, use independent source copies and fresh ancillary states.

Retaining the source is material. If it is independently replaced between the coarse and fine readouts, the two latent energies are independent. For a fixed two-atom source law, their expected separation then approaches a nonzero constant as the resolution improves, so the variance estimate in Section 5 no longer follows.

## 4. One fixed output grid and finite energy arithmetic

Choose $`L`$ below and put

```math
 M_\ell=2^\ell,\quad h_\ell=2^{-\ell},\quad
 h=h_L,\quad
 \Gamma=\{-1+jh:0\leq j\leq J\},\quad J=2M_L.
```

The same final grid is used at every level. There is no changing-grid identification hidden in the telescope.

In the direct-evolution construction, each decoded value is rational and can be computed exactly from $`y`$ and $`M_\ell`$. It is already on $`\Gamma`$ for the parameter range used below. More generally, including the cosine decoder in Section 9, compute each decoded energy to absolute error at most $`h/4`$, clip to $`[-1,1]`$, and round to a nearest point of $`\Gamma`$. This is a fixed, deterministic finite computation for each clock value. The resulting change in a decoded energy is at most $`3h/4`$. There is no need to decide an exact transcendental rounding tie.

The real median is 1-Lipschitz under the maximum perturbation of its three arguments. Therefore the grid-valued median, denoted $`Z_\ell`$, satisfies under its latent energy

```math
 \mathbb E_\lambda|Z_\ell-\lambda|
 \leq64h_\ell+\tfrac34h
 \leq K h_\ell,\qquad K=65.
```

For every coarse/fine pair produced on one copy, the exact latent-phase coupling, the moment bound, and the triangle inequality give

```math
 \mathbb E|Z_\ell^{+}-Z_{\ell-1}^{-}|
 \leq K(h_\ell+h_{\ell-1})=3K h_\ell.
```

The superscripts distinguish the two outcomes of that pair. They do not denote different marginal samplers. Whenever level $`\ell-1`$ appears elsewhere, it uses exactly the same clock, decoder, numerical tolerance, and final-grid map.

Let $`\nu_\ell`$ be the law of $`Z_\ell`$, with CDF $`F_\ell`$. Coupling $`Z_\ell`$ to its latent energy gives

```math
 W_1(\nu_\ell,\mu)\leq K h_\ell.
```

At $`M_0=1`$, the phase-estimation output is deterministically zero and both decoders used here return energy $`+1`$. Thus $`\nu_0=\delta_1`$ is known and its CDF need not be sampled. Keeping an optional empirical level-zero batch changes none of the stated bounds, but it is unnecessary.

## 5. Multilevel CDF estimator and variance addition

For $`\ell\geq1`$, define the random function

```math
 D_\ell(x)=\mathbf1\{Z_\ell^{+}\leq x\}
                  -\mathbf1\{Z_{\ell-1}^{-}\leq x\}.
```

For any two real numbers $`u,v`$,

```math
 \int_{\mathbb R}
  |\mathbf1\{u\leq x\}-\mathbf1\{v\leq x\}|^2\,dx
 =|u-v|.
```

The integrand is the indicator of the interval between $`u`$ and $`v`$, apart from irrelevant endpoints. Consequently,

```math
 v_\ell:=\int_{-1}^{1}\operatorname{Var}(D_\ell(x))\,dx
 \leq \mathbb E|Z_\ell^{+}-Z_{\ell-1}^{-}|
 \leq C_vh_\ell,\qquad C_v=3K=195.
```

No pointwise density bound is involved. This is the specific reason that atoms and arbitrarily clustered energies are harmless under the integrated-CDF loss.

Take $`n_\ell`$ independent pairs at each level and define

```math
 G(x)=F_0(x)+
       \sum_{\ell=1}^{L}\frac1{n_\ell}
                    \sum_{r=1}^{n_\ell}D_{\ell,r}(x).
```

The exact marginals established in Section 3 imply
$`\mathbb E D_\ell=F_\ell-F_{\ell-1}`$, so
$`\mathbb EG=F_L`$. The independent batches give the pointwise variance identity

```math
 \operatorname{Var}(G(x))
 =\sum_{\ell=1}^{L}
                  \frac{\operatorname{Var}(D_\ell(x))}{n_\ell}.
```

Jensen's inequality, Tonelli's theorem for the nonnegative integrands, and Cauchy–Schwarz on an interval of length two now yield

```math
 \begin{aligned}
 \mathbb E\|G-F_L\|_{L^1}
 &\leq\int_{-1}^{1}
                \sqrt{\operatorname{Var}(G(x))}\,dx\\
 &\leq\left(2\sum_{\ell=1}^{L}\frac{v_\ell}{n_\ell}\right)^{1/2}.
 \end{aligned}
```

Adding variances before taking the square root is essential. Applying a triangle inequality separately to the expected errors of all levels would incur an unnecessary logarithmic loss.

The telescope and allocation principle are standard multilevel Monte Carlo. Giles, Nagapetyan and Ritter [GNR15, Sections 2.1–2.3] construct whole-CDF multilevel estimators under smooth-density and supremum-error hypotheses and discuss the earlier Banach-valued framework. Our use of the elementary integrated-indicator identity changes the error calculation to the atomic $`W_1`$ setting; it does not create a new general multilevel framework.

## 6. Parameter allocation and interaction resources

Choose

```math
 L=\left\lceil\log_2(24K/\epsilon)\right\rceil,\qquad
 A=96^2C_v,\qquad
 n_\ell=\left\lceil
       A\epsilon^{-2}(\ell+1)^2\,2^{-\ell}\right\rceil
       \quad(1\leq\ell\leq L).
```

The constants are deliberately conservative and are not practical resource estimates. Since $`\sum_{\ell\geq0}(\ell+1)^{-2}<2`$, the variance bound and the variance-addition estimate imply

```math
 \mathbb E\|G-F_L\|_1
 \leq2\sqrt{C_v/A}\,\epsilon=\epsilon/48.
```

The terminal bias satisfies $`W_1(\nu_L,\mu)\leq Kh_L\leq\epsilon/24`$.

The source count is bounded by

```math
 N=\sum_{\ell=1}^{L}n_\ell
 \leq A\epsilon^{-2}
       \sum_{\ell=0}^{\infty}(\ell+1)^2\,2^{-\ell}+L
 =12A\epsilon^{-2}+L
 =O(\epsilon^{-2}).
```

One level-$`\ell`$ pair contains three size-$`M_\ell`$ and three size-$`M_{\ell-1}`$ readouts. Its evolution time is at most

```math
 \tau_\ell
 =\frac{3\pi}{2}
       \big((M_\ell-1)+(M_{\ell-1}-1)\big)
 \leq\frac{9\pi}{4}2^\ell.
```

It follows that

```math
 \begin{aligned}
 T&=\sum_{\ell=1}^{L}n_\ell\tau_\ell\\
 &\leq\frac{9\pi}{4}
       \left(A\epsilon^{-2}\sum_{\ell=1}^{L}(\ell+1)^2+
             \sum_{\ell=1}^{L}2^\ell\right)\\
 &=O(\epsilon^{-2}L^3+\epsilon^{-1})
  =O(\epsilon^{-2}\log^3(1/\epsilon)).
 \end{aligned}
```

The last equality uses $`2^L<48K/\epsilon`$. The pair-cost bound also gives the claimed $`O(1/\epsilon)`$ retained-experiment evolution bound.

There are $`3\ell+3(\ell-1)`$ variable-time controlled-evolution calls in a level-$`\ell`$ pair. Summing against the allocation above shows that their count is
$`O(\epsilon^{-2}+L^2)`$; the interaction time, rather than merely the number of variable-duration calls, is charged in the total-time bound. The known Fourier-transform gates and controls must also be implemented. With a standard circuit they require $`O(\ell^2)`$ elementary gates per pair before compiling rotation accuracy. Their total is $`O(\epsilon^{-2}+L^3)`$, up to the chosen finite-gate-set synthesis overhead. The cost of realizing each supplied controlled evolution is separate from this known-gate accounting.

An alternative allocation $`n_\ell=\lceil A'\epsilon^{-2}(L+1)2^{-\ell}\rceil`$ gives $`O(\epsilon^{-2}L^2)`$ total evolution and $`O(\epsilon^{-2}L)`$ copies. We use the quadratic-in-level allocation in Theorem 1 because it removes the logarithmic overhead in the copy count. These are two achieved resource allocations, not a characterization of the joint optimal frontier.

## 7. A genuine finite probability measure and its classical cost

### 7.1 Projection and the probability guarantee

The function $`G`$ is the CDF of a signed grid measure of total mass one. It can be negative or nonmonotone, so it is not an acceptable final probability measure.

Let $`x_j=-1+jh`$ and let $`G_j`$ be the constant value of $`G`$ on
$`[x_j,x_{j+1})`$, for $`0\leq j<J`$. Solve

```math
 \min_{0\leq c_0\leq c_1\leq\cdots\leq c_{J-1}\leq1}
       h\sum_{j=0}^{J-1}|c_j-G_j|.
```

If an additive objective tolerance $`\zeta`$ is used, the returned value must be within $`\zeta`$ of the minimum. Set

```math
 \widehat p_0=c_0,\quad
 \widehat p_j=c_j-c_{j-1}\ (1\leq j<J),\quad
 \widehat p_J=1-c_{J-1},
 \qquad
 \widehat\mu=\sum_{j=0}^{J}\widehat p_j\delta_{x_j}.
```

Every mass is nonnegative and their sum is exactly one. In particular, endpoint mass is included; imposing $`c_0=0`$ or $`c_{J-1}=1`$ would incorrectly prohibit atoms at the endpoints.

The grid CDF of $`\nu_L`$ is feasible in this minimization. Optimality, the triangle inequality, and the Wasserstein/CDF identity imply

```math
 \begin{aligned}
 W_1(\widehat\mu,\nu_L)
 &=\|\widehat F-F_L\|_1\\
 &\leq\|\widehat F-G\|_1+\|G-F_L\|_1\\
 &\leq2\|G-F_L\|_1+\zeta.
 \end{aligned}
```

Combining the terminal bias, the statistical estimate, and the projection inequality,

```math
 \mathbb E W_1(\widehat\mu,\mu)
 \leq\epsilon/12+\zeta.
```

With exact projection, Markov's inequality gives failure probability at most $`1/12`$ at threshold $`\epsilon`$. Allowing $`\zeta\leq\epsilon/12`$ gives failure probability at most $`1/6`$. This leaves a further failure allowance of $`1/6`$ for the quantum implementation error in Section 8.

### 7.2 Exact arithmetic and a finite projection algorithm

The signed histogram can be accumulated by adding $`+1/n_\ell`$ and $`-1/n_\ell`$ at the two grid locations of each pair, together with the known base atom at $`+1`$. It is unnecessary to store the individual measurement records.

For a simple exact representation, let $`D=\prod_{\ell=1}^{L}n_\ell`$. This need not be the least common denominator. Store the signed histogram and its CDF as integer numerators over $`D`$. Its bit length satisfies

```math
 \log_2D
 \leq\sum_{\ell=1}^{L}\log_2 n_\ell
 =O(L^2).
```

The extra bits needed for signed intermediate values are $`O(\log L)`$, since each empirical correction CDF lies in $`[-1,1]`$. Histogram accumulation therefore takes $`O(N)`$ additions of $`O(L^2)`$-bit integers after the constants $`D/n_\ell`$ are computed. Grid indices have $`O(L)`$ bits.

The projection problem is ordinary isotonic $`L^1`$ regression. First replace each $`G_j`$ by $`a_j=\operatorname{clip}_{[0,1]}G_j`$. For every feasible $`c_j`$,

```math
 |c_j-G_j|=|c_j-a_j|+|a_j-G_j|,
```

so clipping changes the objective only by a constant. Rote's exact priority-queue algorithm [R19, Section 7, Algorithm 3; Section 8, Theorem 2, p. 1:6; Section 9 for uniform weights] computes a minimizer in $`O(J\log J)`$ comparisons/arithmetic operations and $`O(J)`$ storage. Its output values are selected from the clipped input values, so an optimal solution lies in $`[0,1]`$ and retains the same rational denominator. The common grid weight $`h`$ is irrelevant to the minimizer. Thus the output probabilities have $`O(L^2)`$-bit numerators and denominator.

For a completely elementary fallback, sort
$`\mathcal S=\{0,1\}\cup\{G_j:0<G_j<1\}`$.
There is an optimal CDF projection taking all its values in $`\mathcal S`$. To see this, partition any optimum into maximal constant blocks. If an unanchored block value lies strictly between every data value and its neighboring block values, its objective is locally linear. A nonzero slope contradicts optimality, while a zero slope allows the block to move until it reaches a data value, a boundary, or a preceding anchored block. Repeating from left to right anchors every block without increasing cost.

Writing the sorted candidates as $`s_1<\cdots<s_q`$, use

```math
 B_{0,k}=h|s_k-G_0|,\qquad
 B_{j,k}=h|s_k-G_j|+\min_{r\leq k}B_{j-1,r}.
```

Prefix minima evaluate each row in $`O(q)`$ operations; backtracking returns the optimum. This takes $`O(J^2)`$ operations and polynomial storage, since $`q\leq J+2`$. All objective values have denominator $`DM_L`$ and $`O(L^2)`$ numerator bits. Even this slower fallback has $`\widetilde O(\epsilon^{-2})`$ bit cost and does not require an optimization oracle.

Using the standard priority-queue method, working storage for the signed histogram, CDF, and fit is $`O(JL^2)`$ bits, in addition to polynomial-in-$`L`$ setup data and the current quantum source. The output has $`J+1=O(1/\epsilon)`$ possible support points, each a dyadic rational, and $`O(L^2)`$-bit rational probabilities. Trigonometric values in the block-encoding formulation need only $`O(L)`$ bits of absolute precision and can be computed in polynomial time in $`L`$; the direct-evolution decoder uses exact dyadic arithmetic. Thus the output and classical work are finite and explicitly charged.

## 8. Finite-accuracy operations and source perturbation

### 8.1 Implementation error is measured on the supplied operations

The preceding proof first defines an ideal measurement protocol. Let its quantum operations be channels $`\mathcal E_1,\ldots,\mathcal E_R`$, including all controlled evolutions, clock gates, and any resets or measurements whose accuracy is not idealized. Suppose the implemented channels satisfy

```math
 \eta_r=\tfrac12\|\widetilde{\mathcal E}_r-\mathcal E_r\|_\diamond,
 \qquad \sum_{r=1}^{R}\eta_r\leq1/6.
```

A telescoping hybrid of composed channels, contractivity under the remaining channels, and data processing under the final classical measurement imply that the total variation distance between the ideal and implemented complete classical transcripts is at most $`\sum_r\eta_r`$. The same is true after deterministic postprocessing. Therefore any success event loses probability at most $`1/6`$.

Together with the expected-error bound, taking an objective tolerance $`\zeta\leq\epsilon/12`$ proves the stated success probability $`2/3`$. This argument remains valid if measurements are deferred or if a chosen implementation uses classical feed-forward: the channel comparison includes the classical records and conditional controls.

For unitary implementations it suffices that

```math
 \|\widetilde U_r-U_r\|\leq\eta_r,
```

because the half-diamond distance between the associated unitary channels is at most this operator-norm difference. An elementary uniform choice is $`\eta_r\leq1/(6R)`$, or separate budgets summing to $`1/6`$ for dynamics and known gates. All ideal operation counts and requested evolution times are fixed by $`\epsilon`$, so the budget can be chosen before data collection. Only $`O(\log R)`$ accuracy bits are needed when operations can be approximated to error $`\eta`$ at cost polynomial in $`\log(1/\eta)`$. For the fixed direct-evolution interface, the displayed operation counts give $`\log R=O(\log(1/\epsilon))`$. If every known gate of a block-encoding implementation is counted separately, $`R`$ also depends polynomially on the stated encoding and control-register sizes, and those terms remain in $`\log R`$. An efficient precision-synthesis guarantee is a property of the chosen compiler or Hamiltonian implementation; it is not assumed for an otherwise unspecified physical interface.

If an evolution implementation has a cost function $`C_{\rm impl}(t,\eta)`$, its end-to-end implementation cost is the actual sum
$`\sum_r C_{\rm impl}(t_r,\eta_r)`$, with the chosen budgets. The interaction-time bound specifies $`\sum_r|t_r|`$; it does not substitute for that implementation cost. Similarly, a source preparation cost $`C_\rho`$, when one is meaningful, contributes $`NC_\rho`$. No data-loading or state-preparation cost is set to zero by the theorem.

### 8.2 A sufficient bound for dynamics generated by a nearby Hamiltonian

If every requested controlled evolution is implemented using one fixed Hermitian $`H'`$ with $`\|H'-H\|\leq\xi`$, Duhamel's formula gives

```math
 \|e^{-itH'}-e^{-itH}\|\leq |t|\xi.
```

Thus its contribution to the hybrid budget is at most $`T\xi`$. For example, $`\xi\leq1/(12T)`$ reserves half of the channel-error budget for this error and half for other operations. This is a conservative sufficient implementation condition, not an optimal stability theorem.

We do not assert
$`W_1(\mu_{H,\rho},\mu_{H',\rho})\leq\|H-H'\|`$
for arbitrary noncommuting $`H,H'`$. Scalar Lipschitz functions are not uniformly operator Lipschitz. The Duhamel bound and the explicit instrument comparison avoid that unsupported step.

In the block-encoding model, the channel-error budget can likewise be enforced through operator-norm approximations to the actual supplied controlled $`U`$, controlled $`U^\dagger`$, and known gates. A bound only on the error of the top-left encoded block is not silently promoted to an operator-norm bound for the whole unitary. Robustness to such a weaker encoding guarantee would require a separate argument.

### 8.3 Fixed source bias

If the actual independent source copies are all copies of a fixed state $`\sigma`$, the protocol estimates $`\mu_{H,\sigma}`$. Measurement data processing and the diameter of $`[-1,1]`$ imply

```math
 W_1(\mu_{H,\sigma},\mu_{H,\rho})
 \leq 2\,\operatorname{TV}(\mu_{H,\sigma},\mu_{H,\rho})
 \leq\|\sigma-\rho\|_1.
```

Equivalently, in the dual formulation one subtracts $`f(0)`$ from a 1-Lipschitz test function, so $`\|f(H)-f(0)I\|\leq1`$, and then applies the trace-norm inequality. To estimate the intended law to tolerance $`\epsilon`$, one may run the theorem at $`\epsilon/2`$ and require $`\|\sigma-\rho\|_1\leq\epsilon/2`$. The asymptotic resources are unchanged.

Identical independent source copies are part of the theorem. Merely bounding the individual marginals of a correlated sequence does not justify the independence used in the variance addition. No drift or correlated-source theorem is claimed here.

## 9. Exact controlled-block-encoding formulation

### 9.1 Hermitianization of a general unitary completion

Suppose $`U`$ acts on an encoding register $`A`$ of $`a`$ qubits and the source system, and

```math
 (\langle0^a|\otimes I)\,U\,(|0^a\rangle\otimes I)=H.
```

This is an exact, normalization-one block encoding. The full unitary $`U`$ is not assumed Hermitian. Controlled $`U`$ and controlled $`U^\dagger`$ are explicitly supplied and each use is charged.

Add one flag qubit and define

```math
 S=|0\rangle\langle1|\otimes U+
   |1\rangle\langle0|\otimes U^\dagger,\qquad
 J|\psi\rangle=|+\rangle|0^a\rangle|\psi\rangle.
```

Then $`S=S^\dagger`$, $`S^2=I`$, and

```math
 J^\dagger S J
 =\tfrac12\big((\langle0^a|\otimes I)U(|0^a\rangle\otimes I)
             +(\langle0^a|\otimes I)U^\dagger(|0^a\rangle\otimes I)\big)
 =H.
```

Let $`\Pi=JJ^\dagger`$, $`R=2\Pi-I`$, and

```math
 W=RS.
```

The reflection $`R`$ is about a known flag/encoding-ancilla state, tensored with the identity on the source. It is not a reflection about $`\rho`$. This construction is a direct instance of standard qubitization [LC19, Theorem 2; Section 4, Corollary 9 and Lemma 10].

For completeness, if $`H|\lambda\rangle=\lambda|\lambda\rangle`$, set
$`u_\lambda=J|\lambda\rangle`$. For $`|\lambda|<1`$, put

```math
 s_\lambda=\sqrt{1-\lambda^2},\qquad
 v_\lambda=(Su_\lambda-\lambda u_\lambda)/s_\lambda.
```

The two vectors are orthonormal, $`v_\lambda`$ lies in $`\Pi^\perp`$, and on their span

```math
 S=\begin{pmatrix}\lambda&s_\lambda\\s_\lambda&-\lambda\end{pmatrix},
 \quad
 R=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
 \quad
 W=\begin{pmatrix}\lambda&s_\lambda\\-s_\lambda&\lambda\end{pmatrix}.
```

Thus the walk phases are $`\pm\arccos\lambda`$. If $`\lambda=\pm1`$, the plane collapses to the one-dimensional invariant vector $`u_\lambda`$, with walk eigenvalue $`\lambda`$; no division by zero is used.

### 9.2 The weighted measure is preserved exactly

Prepare the known ancillary state and the given source copy, producing
$`\sigma=J\rho J^\dagger`$. The spectral measure of $`W`$ in $`\sigma`$, pushed forward by
$`e^{2\pi i\theta}\mapsto\cos(2\pi\theta)`$, is exactly $`\mu_{H,\rho}`$.

A short proof that also covers coherent mixed sources is to define
$`C=(W+W^\dagger)/2`$. Since $`RJ=J`$,

```math
 CJ=\tfrac12(RS+SR)J
    =\tfrac12(R+I)SJ
    =\Pi SJ=JH.
```

Therefore $`f(C)J=Jf(H)`$ for every function on the finite spectrum. It follows that
$`\operatorname{Tr}[\sigma f(C)]=\operatorname{Tr}[\rho f(H)]`$.
But $`C`$ is the function $`\cos(2\pi\theta)`$ of $`W`$, proving the claimed pushforward identity.

Use ordinary QPE on $`W`$ and decode by

```math
 g_{\rm walk}(q)=\cos(2\pi q).
```

This function is $`2\pi`$-Lipschitz in circular distance, hence obeys the same conservative factor-eight bound from Section 2.2. The tail and median calculations of Section 2 apply with the same constants. Section 4 handles finite cosine arithmetic and the common output grid.

Apply Lemma 2 to the same enlarged retained state $`J\rho J^\dagger`$ and the same walk $`W`$. The coarse and fine medians then share a latent walk phase, whose cosine is their common latent energy. The flag, encoding register, and any oracle workspace that is part of the unitary $`U`$ must remain available through all six readouts. They must not be measured, reinitialized, or postselected onto the signal subspace between readouts. Only the phase-estimation clock ancillas are reset. Resetting the encoding register generally destroys the exact coupling.

### 9.3 Query and ancillary accounting

One can implement $`S`$ by first applying
$`|0\rangle\langle0|\otimes U^\dagger+
 |1\rangle\langle1|\otimes U`$,
then applying $`X`$ to the flag. This uses one flag-controlled $`U`$ and one flag-controlled $`U^\dagger`$. An outer control for phase estimation is implemented with known conjunction controls and a clean auxiliary bit, if necessary. Consequently each controlled $`W`$ uses at most two supplied controlled block-encoding queries, plus known gates and the reflection $`R`$.

QPE of clock size $`M`$ uses $`M-1`$ controlled $`W`$ applications when powers are expanded into individual walk queries. A paired level sample uses at most
$`3(M_\ell-1)+3(M_{\ell-1}-1)\leq(9/2)M_\ell`$
walk queries and at most $`9M_\ell`$ supplied block-encoding queries. The resource calculation of Section 6 therefore gives

```math
 Q_U=O(\epsilon^{-2}L^3)
```

with the same $`O(\epsilon^{-2})`$ source copies and $`O(1/\epsilon)`$ maximum queries within one retained sample.

The retained source uses $`\lceil\log_2\dim\mathcal H\rceil`$ qubits in a qubit implementation, the supplied encoding workspace has $`a`$ qubits, Hermitianization adds one flag, and ordinary QPE adds at most $`L`$ clock qubits. Known multiple controls and reflections have their own conventional workspace/gate costs. For example, linear-size clean-ancilla conjunction circuits give $`O(a)`$ known gates and $`O(a)`$ reusable scratch for each reflection; other standard decompositions trade these resources. The theorem does not call the total ancillary overhead constant or omit the supplied oracle workspace. It needs no second copy of $`\rho`$ inside a sample.

There is no approximation to $`H`$ or Hamiltonian simulation inside this exact block-encoding reduction. If the supplied normalization exceeds one, or if constructing its oracle has a nonunit cost, that normalization/access cost has to be included separately. This query bound concerns exactly the normalized interface above.

## 10. Scope of the completed upper theorem

The derivation establishes the claimed fresh-copy upper for all finite-dimensional Hermitian contractions and all fixed independent source states. Its two potentially delicate steps are explicit: the full retained-system instrument has the joint law of Lemma 2, and the signed estimator is converted to an actual finite probability measure by the isotonic projection and Wasserstein bound in Section 7. No spectral smoothness, minimum gap, source inverse, source purification, postselection success probability, or free data-loading oracle is used.

The proof does not establish a tight joint copy/evolution frontier, an optimal logarithmic factor, a universal depth separation, a graph-local query improvement, or a practical advantage for a concrete Hamiltonian family. Generic finite-operation error budgets are sufficient conditions, not a fault-tolerance or noise threshold theorem. Approximate block encodings specified only through their encoded block, correlated source sequences, and stability with respect to noncommuting Hamiltonian perturbations beyond the instrument budget are outside the statement.

## References and exact source locations

- **[V74]** S. S. Vallender, “Calculation of the Wasserstein Distance Between Probability Distributions on the Line,” Theory of Probability and Its Applications 18(4), 784–786 (1974), DOI [10.1137/1118101](https://doi.org/10.1137/1118101). The paper's principal result is the equality of $`W_1`$ and the integrated absolute difference of CDFs. [Primary journal archive entry](https://www.mathnet.ru/eng/tvp4387).
- **[CEMM98]** R. Cleve, A. Ekert, C. Macchiavello and M. Mosca, “Quantum algorithms revisited,” Proc. R. Soc. A 454, 339–354 (1998), DOI [10.1098/rspa.1998.0164](https://doi.org/10.1098/rspa.1998.0164). The inspected [arXiv:quant-ph/9708016v1](https://arxiv.org/abs/quant-ph/9708016) has phase estimation in Section 5, Eqs. (5.1)–(5.2), and probability amplification in Appendix C. The uniform median first-moment calculation used above is supplied explicitly rather than attributed as a theorem of that source.
- **[LC19]** G. H. Low and I. L. Chuang, “Hamiltonian Simulation by Qubitization,” Quantum 3, 163 (2019), DOI [10.22331/q-2019-07-12-163](https://doi.org/10.22331/q-2019-07-12-163). [Final primary PDF](https://quantum-journal.org/papers/q-2019-07-12-163/pdf/), Theorem 2 on p. 6 and Section 4, especially Corollary 9 and Lemma 10 on pp. 10–11, provide qubitization of reflections and the one-extra-flag construction for general signal unitaries. The explicit compression identity in Section 9.2 fixes the source-weighted measure needed here.
- **[GNR15]** M. B. Giles, T. Nagapetyan and K. Ritter, “Multilevel Monte Carlo Approximation of Distribution Functions and Densities,” SIAM/ASA Journal on Uncertainty Quantification 3, 267–295 (2015), DOI [10.1137/140960086](https://doi.org/10.1137/140960086). [Author's primary PDF](https://people.maths.ox.ac.uk/gilesm/files/juq_15.pdf), Sections 2.1–2.3: smooth-density assumption A1, coupled approximations A2, and the multilevel distribution-function estimator. The introduction discusses Banach-valued multilevel antecedents.
- **[R19]** G. Rote, “Isotonic Regression by Dynamic Programming,” SOSA 2019, OASIcs 69, 1:1–1:18, DOI [10.4230/OASIcs.SOSA.2019.1](https://doi.org/10.4230/OASIcs.SOSA.2019.1). [Final primary PDF](https://drops.dagstuhl.de/storage/01oasics/oasics-vol069-sosa2019/OASIcs.SOSA.2019.1/OASIcs.SOSA.2019.1.pdf), Section 7, Algorithms 2–3; Section 8, Theorem 2 on p. 1:6; Section 9 for the uniform-weight simplification.
- **[LLY26]** Li, Liao and Yang, “Classical and quantum spectral density estimation under local graph access,” [arXiv:2608.22769v2](https://arxiv.org/abs/2608.22769), Section 4.3, Lemma 35 and Section 4.4, Lemmas 36–37. Their coherent spectral sampler and coherent $`W_1`$ distribution estimator imply the generic coherent-source upper with the same Hamiltonian precision exponent after the graph-specific walk implementation cost is separated. Their local-graph access cost and lower bound are different resources from the controlled-evolution and normalized-block-encoding interfaces used here.
