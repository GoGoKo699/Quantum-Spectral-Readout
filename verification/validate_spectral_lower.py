#!/usr/bin/env python3
"""Finite checks for the spectral-readout lower-bound derivation.

These are convention/algebra checks, not proofs of an asymptotic lower bound.
They use no sampled quantum algorithm and make no performance claim.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np


TOL = 2e-11


def spectral_norm(a: np.ndarray) -> float:
    return float(np.linalg.norm(a, ord=2))


def block_diagonal(blocks: list[np.ndarray]) -> np.ndarray:
    size = sum(block.shape[0] for block in blocks)
    out = np.zeros((size, size), dtype=np.result_type(*blocks))
    offset = 0
    for block in blocks:
        n = block.shape[0]
        out[offset : offset + n, offset : offset + n] = block
        offset += n
    return out


def atom_w1(x: np.ndarray, p: np.ndarray, y: np.ndarray, q: np.ndarray) -> float:
    """Exact monotone coupling of two finite atomic probability measures."""
    ix, iy = np.argsort(x), np.argsort(y)
    x, p, y, q = x[ix], p[ix].copy(), y[iy], q[iy].copy()
    i = j = 0
    result = 0.0
    while i < len(x) and j < len(y):
        amount = min(p[i], q[j])
        result += amount * abs(x[i] - y[j])
        p[i] -= amount
        q[j] -= amount
        if p[i] < 1e-14:
            i += 1
        if q[j] < 1e-14:
            j += 1
    return float(result)


def quantile_centroids(
    atoms: np.ndarray, masses: np.ndarray, target_masses: np.ndarray
) -> np.ndarray:
    order = np.argsort(atoms)
    atoms, masses = atoms[order], masses[order]
    out = np.zeros(len(target_masses))
    output_knots = np.r_[0.0, np.cumsum(masses)]
    target_knots = np.r_[0.0, np.cumsum(target_masses)]
    for j, w in enumerate(target_masses):
        for k, x in enumerate(atoms):
            overlap = max(
                0.0,
                min(target_knots[j + 1], output_knots[k + 1])
                - max(target_knots[j], output_knots[k]),
            )
            out[j] += overlap * x / w
    return out


def family(d: int, eps: float) -> dict:
    delta = 32.0 * eps
    m = min(d, math.floor(1.0 / (256.0 * eps)))
    assert 1 <= m <= d
    ranks = np.full(m, d // m, dtype=int)
    ranks[: d % m] += 1
    masses = ranks / d
    bases = 4.0 * delta * (np.arange(1, m + 1) - (m + 1) / 2.0)
    signs = np.array(list(itertools.product((-1, 1), repeat=m)), dtype=int)
    group_eigenvalues = bases[None, :] + delta * signs
    diagonals = np.repeat(group_eigenvalues, ranks, axis=1)
    assert np.max(np.abs(diagonals)) <= 0.25 + TOL
    assert np.min(masses) >= 1.0 / (2.0 * m) - TOL
    assert m >= min(d, 1.0 / eps) / 512.0 - TOL
    if m > 1:
        assert np.min(np.diff(group_eigenvalues, axis=1)) >= 2.0 * delta - TOL
    return {
        "d": d,
        "eps": eps,
        "delta": delta,
        "m": m,
        "ranks": ranks,
        "masses": masses,
        "bases": bases,
        "signs": signs,
        "group_eigenvalues": group_eigenvalues,
        "diagonals": diagonals,
    }


def check_adversary(data: dict) -> dict:
    d, m, delta = data["d"], data["m"], data["delta"]
    signs = data["signs"]
    n = len(signs)
    index = {tuple(z): i for i, z in enumerate(signs)}
    gamma = np.zeros((n, n))
    for i, z in enumerate(signs):
        for j in range(m):
            flipped = z.copy()
            flipped[j] *= -1
            gamma[i, index[tuple(flipped)]] = 1.0
    uniform = np.ones(n) / math.sqrt(n)
    assert abs(float(uniform @ gamma @ uniform) - m) < TOL

    g = np.diag(data["diagonals"].reshape(-1))
    gamma_h = np.kron(gamma, np.eye(d))
    comm_h = spectral_norm(gamma_h @ g - g @ gamma_h)
    assert abs(comm_h - 2.0 * delta) < TOL

    blocks = []
    for diagonal in data["diagonals"]:
        h = np.diag(diagonal)
        s = np.diag(np.sqrt(1.0 - diagonal**2))
        u = np.block([[h, s], [s, -h]])
        assert spectral_norm(u.T - u) < TOL
        assert spectral_norm(u @ u - np.eye(2 * d)) < TOL
        assert spectral_norm(u[:d, :d] - h) < TOL
        blocks.append(u)
    oracle = block_diagonal(blocks)
    gamma_u = np.kron(gamma, np.eye(2 * d))
    comm_u = spectral_norm(gamma_u @ oracle - oracle @ gamma_u)
    max_edge = 0.0
    for i, z in enumerate(signs):
        for j in range(m):
            flipped = z.copy()
            flipped[j] *= -1
            other = index[tuple(flipped)]
            max_edge = max(max_edge, spectral_norm(blocks[i] - blocks[other]))
    assert abs(comm_u - max_edge) < TOL
    assert comm_u <= 4.0 * delta / math.sqrt(3.0) + TOL

    evolution_checks = []
    for t in [0.0, 0.25, 1.0, 7.5, math.pi / (2.0 * delta)]:
        evolution = np.diag(np.exp(-1j * t * np.diag(g)))
        comm = spectral_norm(gamma_h @ evolution - evolution @ gamma_h)
        expected = 2.0 * abs(math.sin(delta * t))
        assert abs(comm - expected) < TOL
        assert comm <= 2.0 * delta * abs(t) + TOL
        evolution_checks.append({"t": t, "commutator_norm": comm})

    return {
        "d": d,
        "m": m,
        "eps": data["eps"],
        "delta": delta,
        "ranks": data["ranks"].tolist(),
        "hamiltonian_commutator_norm": comm_h,
        "block_oracle_commutator_norm": comm_u,
        "largest_oracle_edge_norm": max_edge,
        "evolution_checks": evolution_checks,
    }


def check_transport(data: dict, rng: np.random.Generator) -> dict:
    signs, eigenvalues = data["signs"], data["group_eigenvalues"]
    masses, bases, delta = data["masses"], data["bases"], data["delta"]
    maximum_pairwise_residual = 0.0
    for z, x in zip(signs, eigenvalues):
        for zz, y in zip(signs, eigenvalues):
            actual = atom_w1(x, masses, y, masses)
            expected = 2.0 * delta * float(masses @ (z != zz))
            maximum_pairwise_residual = max(
                maximum_pairwise_residual, abs(actual - expected)
            )
    assert maximum_pairwise_residual < TOL

    minimum_decoder_slack = math.inf
    minimum_jensen_slack = math.inf
    for _ in range(600):
        i = int(rng.integers(len(signs)))
        k = int(rng.integers(1, 12))
        atoms = rng.uniform(-1.0, 1.0, size=k)
        weights = rng.dirichlet(np.ones(k))
        centroids = quantile_centroids(atoms, weights, masses)
        decoded = np.where(centroids >= bases, 1, -1)
        w1 = atom_w1(atoms, weights, eigenvalues[i], masses)
        centroid_cost = float(masses @ np.abs(centroids - eigenvalues[i]))
        decoder_cost = delta * float(masses @ (decoded != signs[i]))
        minimum_decoder_slack = min(minimum_decoder_slack, w1 - decoder_cost)
        minimum_jensen_slack = min(minimum_jensen_slack, w1 - centroid_cost)
        assert w1 + TOL >= centroid_cost
        assert centroid_cost + TOL >= decoder_cost
    return {
        "d": data["d"],
        "m": data["m"],
        "maximum_pairwise_formula_residual": maximum_pairwise_residual,
        "arbitrary_output_cases": 600,
        "minimum_decoder_slack": minimum_decoder_slack,
        "minimum_jensen_slack": minimum_jensen_slack,
    }


def check_fidelity() -> dict:
    grid = np.linspace(0.0, 1.0, 1001)
    a, b = grid[:, None], grid[None, :]
    s = (a + b) / 2.0
    lhs = np.sqrt(a * (1.0 - b)) + np.sqrt(b * (1.0 - a))
    rhs = 2.0 * np.sqrt(s * (1.0 - s))
    maximum_violation = float(np.max(lhs - rhs))
    assert maximum_violation < TOL
    mean_error = (2.0 / 3.0) * (1.0 / 16.0) + 1.0 / 3.0
    final_progress_factor = 2.0 * math.sqrt(mean_error * (1.0 - mean_error))
    assert abs(mean_error - 3.0 / 8.0) < TOL
    assert abs(final_progress_factor - math.sqrt(15.0) / 4.0) < TOL
    return {
        "grid_pairs": int(lhs.size),
        "maximum_edge_inequality_violation": maximum_violation,
        "mean_error": mean_error,
        "final_progress_factor": final_progress_factor,
        "kappa": 1.0 - final_progress_factor,
    }


def rotation(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta), -math.sin(theta)],
         [math.sin(theta), math.cos(theta)]]
    )


def check_purifiers() -> list[dict]:
    cnot = np.array(
        [[1.0, 0.0, 0.0, 0.0],
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 0.0, 1.0],
         [0.0, 0.0, 1.0, 0.0]]
    )
    results = []
    for eps in [1e-4, 1e-3, 0.01, 0.1, 0.25]:
        angle = math.asin(2.0 * eps)
        up = cnot @ np.kron(rotation(math.pi / 4.0 - angle / 2.0), np.eye(2))
        um = cnot @ np.kron(rotation(math.pi / 4.0 + angle / 2.0), np.eye(2))
        for sign, u in [(1.0, up), (-1.0, um)]:
            psi = u[:, 0].reshape(2, 2)
            reduced = psi @ psi.conj().T
            expected = np.diag([0.5 + sign * eps, 0.5 - sign * eps])
            assert spectral_norm(reduced - expected) < TOL
        norm_difference = spectral_norm(up - um)
        expected_difference = 2.0 * math.sin(angle / 2.0)
        assert abs(norm_difference - expected_difference) < TOL
        assert abs(spectral_norm(up.T - um.T) - norm_difference) < TOL
        assert norm_difference <= 4.0 * eps / math.sqrt(3.0) + TOL
        query_constant = 1.0 / (3.0 * norm_difference)
        assert query_constant + TOL >= math.sqrt(3.0) / (12.0 * eps)
        results.append(
            {"eps": eps, "norm_difference": norm_difference,
             "hybrid_query_lower_bound": query_constant}
        )
    return results


def main(output_path: Path) -> None:
    if not __debug__:
        raise RuntimeError("Run verification without -O or PYTHONOPTIMIZE; assertions are required.")
    rng = np.random.default_rng(20261031)
    instances = [family(1, 1.0 / 512.0),
                 family(5, 1.0 / 1000.0),
                 family(7, 1.0 / 1024.0)]
    delta = 0.1
    midpoint_distance = atom_w1(
        np.array([0.0]), np.array([1.0]),
        np.array([-delta]), np.array([1.0])
    )
    assert abs(midpoint_distance - delta) < TOL
    assert midpoint_distance < 2.0 * delta
    result = {
        "purpose": "Finite convention and algebra checks; not an asymptotic proof.",
        "adversary": [check_adversary(data) for data in instances],
        "transport": [check_transport(data, rng) for data in instances],
        "edge_fidelity": check_fidelity(),
        "purifiers": check_purifiers(),
        "midpoint_counterexample": {
            "m": 1, "baseline": 0.0, "true_bit": -1, "decoded_tie_bit": 1,
            "displacement": delta, "w1": midpoint_distance,
            "invalid_twice_displacement_decoder_bound": 2.0 * delta,
            "rejects_invalid_factor_two": True,
        },
        "all_checks_passed": True,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True, "report": str(output_path),
                      "families": len(instances),
                      "arbitrary_output_transport_cases": 600 * len(instances),
                      "edge_fidelity_grid_pairs": 1001**2}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "results" / "spectral_lower_validation.json",
        help="JSON report path; defaults to results/ next to this script.",
    )
    main(parser.parse_args().output.expanduser().resolve())
