"""Exact L1 projection of a signed CDF on a uniform one-dimensional grid.

The priority-queue algorithm is the unweighted specialization in Section 9 of
Gunter Rote, "Isotonic Regression by Dynamic Programming", SOSA 2019,
DOI:10.4230/OASIcs.SOSA.2019.1.  Theorem 2 establishes O(K log K) operations
and O(K) storage for the weighted algorithm.  This implementation uses exact
rational arithmetic; the stated operation count does not treat arbitrary-size
integer arithmetic as constant-cost.

The input CDF contains one value on each of K equal-width grid intervals.
Outside the grid support its values are understood to be zero and one.
"""

from fractions import Fraction
import heapq
from numbers import Rational


def _fractions(values):
    result = []
    for value in values:
        if not isinstance(value, Rational):
            raise TypeError("Use integer or rational input, not floating point.")
        result.append(Fraction(value))
    return result


def project_uniform_cdf(raw_cdf):
    """Minimize sum_j |cdf_j - raw_cdf_j| under 0 <= cdf_1 <= ... <= 1.

    For a uniform grid the common interval width does not change the minimizer.
    Clipping the input to [0,1] changes the constrained objective only by a
    constant.  Each heap key is an exact rational input value.  Two insertions
    and one maximum deletion implement the unweighted form of Rote's algorithm;
    a backward pass recovers an optimum from the recorded prefix minima.
    """
    raw = _fractions(raw_cdf)
    zero, one = Fraction(0), Fraction(1)
    heap = []
    prefix_minima = []
    for value in raw:
        clipped = min(one, max(zero, value))
        heapq.heappush(heap, -clipped)
        heapq.heappush(heap, -clipped)
        heapq.heappop(heap)
        prefix_minima.append(-heap[0])

    fitted = prefix_minima[:]
    for j in range(len(fitted) - 2, -1, -1):
        fitted[j] = min(fitted[j], fitted[j + 1])
    return fitted


def cdf_to_probability_masses(cdf):
    """Recover exact nonnegative masses at the K+1 grid nodes."""
    cdf = _fractions(cdf)
    augmented = [Fraction(0), *cdf, Fraction(1)]
    masses = [right - left for left, right in zip(augmented, augmented[1:])]
    if any(mass < 0 for mass in masses):
        raise ValueError("CDF must be nondecreasing and lie in [0,1].")
    return masses


def project_signed_uniform_masses(signed_masses):
    """Project a normalized signed grid measure to a probability measure."""
    signed_masses = _fractions(signed_masses)
    if not signed_masses or sum(signed_masses) != 1:
        raise ValueError("Signed grid masses must have exact total mass one.")
    cumulative = Fraction(0)
    raw_cdf = []
    for mass in signed_masses[:-1]:
        cumulative += mass
        raw_cdf.append(cumulative)
    return cdf_to_probability_masses(project_uniform_cdf(raw_cdf))
