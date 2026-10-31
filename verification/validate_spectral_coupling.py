#!/usr/bin/env python3
"""Finite, exact-matrix check of retained-state QPE coupling and CDF projection.

This validates selected finite identities, not the asymptotic theorem. All input
states and operators are synthetic and reproducible from the fixed RNG seed.
"""

import argparse
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.stats import wasserstein_distance

from exact_cdf_projection import project_uniform_cdf, cdf_to_probability_masses


SEED = 20261031
RNG = np.random.default_rng(SEED)


def phase_amplitudes(m, theta):
    j = np.arange(m)[:, None, None]
    t = np.arange(m)[None, :, None]
    return np.exp(1j * t * (theta[None, None, :] - 2 * np.pi * j / m)).mean(axis=1)


def median_three_kernel(m, theta):
    """Distribution of the numerical median, conditional on latent eigenphase."""
    amplitudes = phase_amplitudes(m, theta)
    raw_probabilities = np.abs(amplitudes) ** 2
    values = np.round(np.cos(2 * np.pi * np.arange(m) / m), 14)
    values, labels = np.unique(values, return_inverse=True)
    probabilities = np.zeros((len(values), len(theta)))
    np.add.at(probabilities, labels, raw_probabilities)
    cdf = np.cumsum(probabilities, axis=0)
    cdf = np.clip(cdf, 0, 1)
    median_cdf = 3 * cdf**2 - 2 * cdf**3
    median_probabilities = np.diff(median_cdf, axis=0, prepend=np.zeros((1, len(theta))))
    median_probabilities = np.maximum(median_probabilities, 0)
    median_probabilities /= median_probabilities.sum(axis=0, keepdims=True)
    return values, median_probabilities


def integrated_increment_variance(values_c, values_f, joint):
    marginal_c = joint.sum(axis=1)
    marginal_f = joint.sum(axis=0)
    second_moment_integral = float(np.sum(joint * np.abs(values_c[:, None] - values_f[None, :])))
    knots = np.unique(np.r_[[-1.0, 1.0], values_c, values_f])
    middle = (knots[:-1] + knots[1:]) / 2
    cdf_c = (values_c[:, None] <= middle[None, :]).T @ marginal_c
    cdf_f = (values_f[:, None] <= middle[None, :]).T @ marginal_f
    squared_mean_integral = float(np.dot(np.diff(knots), (cdf_f - cdf_c) ** 2))
    return {
        "expected_absolute_difference": second_moment_integral,
        "integrated_squared_mean": squared_mean_integral,
        "integrated_variance": second_moment_integral - squared_mean_integral,
    }


def sample_joint(joint, count):
    sampled = RNG.choice(joint.size, size=count, p=joint.ravel() / joint.sum())
    return np.unravel_index(sampled, joint.shape)


def main(output_path: Path):
    if not __debug__:
        raise RuntimeError("Run verification without -O or PYTHONOPTIMIZE; assertions are required.")
    dimension = 5
    random_matrix = RNG.normal(size=(dimension, dimension)) + 1j * RNG.normal(size=(dimension, dimension))
    eigenvectors, _ = np.linalg.qr(random_matrix)
    eigenvalues = np.array([-0.73, -0.16, 0.18, 0.62, 0.85])
    theta = np.arccos(eigenvalues)
    hamiltonian = (eigenvectors * eigenvalues) @ eigenvectors.conj().T
    walk = (eigenvectors * np.exp(1j * theta)) @ eigenvectors.conj().T
    psi = RNG.normal(size=dimension) + 1j * RNG.normal(size=dimension)
    psi /= np.linalg.norm(psi)
    pure = np.outer(psi, psi.conj())
    b = RNG.normal(size=(dimension, dimension)) + 1j * RNG.normal(size=(dimension, dimension))
    mixed_part = b @ b.conj().T
    mixed_part /= np.trace(mixed_part)
    mixed = 0.61 * pure + 0.39 * mixed_part
    states = {"coherent_pure": pure, "full_rank_mixed": mixed}

    amplitudes_c = phase_amplitudes(4, theta)
    amplitudes_f = phase_amplitudes(8, theta)
    kraus_c = np.array([(eigenvectors * row) @ eigenvectors.conj().T for row in amplitudes_c])
    kraus_f = np.array([(eigenvectors * row) @ eigenvectors.conj().T for row in amplitudes_f])
    checks = {}
    for name, rho in states.items():
        weights = np.real(np.diag(eigenvectors.conj().T @ rho @ eigenvectors))
        latent_joint = (np.abs(amplitudes_c) ** 2 * weights) @ (np.abs(amplitudes_f) ** 2).T
        exact_joint = np.empty((4, 8))
        maximum_imaginary_part = 0.0
        for a in range(4):
            for b in range(8):
                product = kraus_f[b] @ kraus_c[a]
                probability = np.trace(product @ rho @ product.conj().T)
                exact_joint[a, b] = probability.real
                maximum_imaginary_part = max(maximum_imaginary_part, abs(probability.imag))
        reset_joint = np.outer(exact_joint.sum(axis=1), exact_joint.sum(axis=0))
        # Selected six-step paths additionally check three coarse and three fine
        # measured QPE runs on one retained source, before classical medians.
        path_error = 0.0
        for _ in range(128):
            coarse = RNG.integers(4, size=3)
            fine = RNG.integers(8, size=3)
            product = np.eye(dimension, dtype=complex)
            eigen_amplitude = np.ones(dimension, dtype=complex)
            for a in coarse:
                product = kraus_c[a] @ product
                eigen_amplitude *= amplitudes_c[a]
            for b in fine:
                product = kraus_f[b] @ product
                eigen_amplitude *= amplitudes_f[b]
            exact = np.trace(product @ rho @ product.conj().T).real
            latent = float(weights @ np.abs(eigen_amplitude) ** 2)
            path_error = max(path_error, abs(exact - latent))
        checks[name] = {
            "source_H_commutator_frobenius": float(np.linalg.norm(hamiltonian @ rho - rho @ hamiltonian)),
            "source_min_eigenvalue": float(np.linalg.eigvalsh(rho).min()),
            "latent_weights": weights.tolist(),
            "joint_normalization_error": float(abs(exact_joint.sum() - 1)),
            "maximum_exact_vs_latent_error": float(np.max(np.abs(exact_joint - latent_joint))),
            "maximum_imaginary_residue": maximum_imaginary_part,
            "selected_six_step_path_maximum_error": path_error,
            "retained_vs_reset_total_variation": float(np.abs(exact_joint - reset_joint).sum() / 2),
        }

    weights = np.real(np.diag(eigenvectors.conj().T @ mixed @ eigenvectors))
    scaling = []
    for coarse_m in [4, 8, 16, 32, 64, 128, 256]:
        fine_m = 2 * coarse_m
        yc, pc = median_three_kernel(coarse_m, theta)
        yf, pf = median_three_kernel(fine_m, theta)
        joint = (pc * weights) @ pf.T
        reset = np.outer(pc @ weights, pf @ weights)
        coarse_first_error = float(np.sum(pc * weights * np.abs(yc[:, None] - eigenvalues)))
        fine_first_error = float(np.sum(pf * weights * np.abs(yf[:, None] - eigenvalues)))
        scaling.append({
            "coarse_qpe_clock_size": coarse_m,
            "fine_qpe_clock_size": fine_m,
            "coarse_mean_absolute_eigenvalue_error": coarse_first_error,
            "fine_mean_absolute_eigenvalue_error": fine_first_error,
            "retained": integrated_increment_variance(yc, yf, joint),
            "reset": integrated_increment_variance(yc, yf, reset),
        })

    # A deliberately small-sample signed telescoping CDF gives a nontrivial
    # positivity/monotonicity repair test, independent of asymptotic allocation.
    grid = np.linspace(-1, 1, 129)
    grid_step = float(grid[1] - grid[0])
    signed_mass = np.zeros(len(grid))
    exact_signed_mass = [Fraction(0) for _ in grid]

    def grid_index(values):
        return np.clip(np.rint((values + 1) / grid_step).astype(int), 0, len(grid) - 1)

    base_y, base_p = median_three_kernel(4, theta)
    base_n = 20
    draws = RNG.choice(len(base_y), size=base_n, p=base_p @ weights)
    np.add.at(signed_mass, grid_index(base_y[draws]), 1 / base_n)
    for index in grid_index(base_y[draws]):
        exact_signed_mass[index] += Fraction(1, base_n)
    counts = [12, 7, 4, 3, 2]
    for level, count in enumerate(counts, start=1):
        yc, pc = median_three_kernel(2 ** (level + 1), theta)
        yf, pf = median_three_kernel(2 ** (level + 2), theta)
        joint = (pc * weights) @ pf.T
        i, j = sample_joint(joint, count)
        np.add.at(signed_mass, grid_index(yf[j]), 1 / count)
        np.add.at(signed_mass, grid_index(yc[i]), -1 / count)
        for index in grid_index(yf[j]):
            exact_signed_mass[index] += Fraction(1, count)
        for index in grid_index(yc[i]):
            exact_signed_mass[index] -= Fraction(1, count)
    raw_cdf = np.cumsum(signed_mass)[:-1]
    true_grid_mass = np.zeros(len(grid))
    np.add.at(true_grid_mass, grid_index(eigenvalues), weights)
    true_grid_cdf = np.cumsum(true_grid_mass)[:-1]
    size = len(raw_cdf)
    # Variables [f,t]: min sum h_i t_i, subject to |f_i-G_i|<=t_i,
    # 0<=f_i<=1, f_i<=f_{i+1}. Endpoints are supplied by recovered masses.
    objective = np.r_[np.zeros(size), np.diff(grid)]
    monotone = np.zeros((size - 1, 2 * size))
    monotone[np.arange(size - 1), np.arange(size - 1)] = 1
    monotone[np.arange(size - 1), np.arange(1, size)] = -1
    identity = np.eye(size)
    constraints = np.vstack([np.c_[identity, -identity], np.c_[-identity, -identity], monotone])
    bounds = np.r_[raw_cdf, -raw_cdf, np.zeros(size - 1)]
    fit = linprog(objective, A_ub=constraints, b_ub=bounds,
                  bounds=[(0, 1)] * size + [(0, None)] * size, method="highs")
    if not fit.success:
        raise RuntimeError(fit.message)
    projected_cdf = fit.x[:size]
    projected_mass = np.diff(np.r_[0, projected_cdf, 1])
    projected_mass = np.maximum(projected_mass, 0)
    projected_mass /= projected_mass.sum()
    raw_grid_error = float(np.dot(np.diff(grid), np.abs(raw_cdf - true_grid_cdf)))
    projected_grid_error = float(np.dot(np.diff(grid), np.abs(projected_cdf - true_grid_cdf)))
    quantization_error = float(wasserstein_distance(grid, eigenvalues, true_grid_mass, weights))
    projected_true_error = float(wasserstein_distance(grid, eigenvalues, projected_mass, weights))
    exact_raw_cdf = []
    running_mass = Fraction(0)
    for mass in exact_signed_mass[:-1]:
        running_mass += mass
        exact_raw_cdf.append(running_mass)
    exact_projected_cdf = project_uniform_cdf(exact_raw_cdf)
    exact_projected_mass = cdf_to_probability_masses(exact_projected_cdf)
    exact_grid_step = Fraction(2, len(grid) - 1)
    exact_objective = exact_grid_step * sum(
        abs(fitted - raw) for fitted, raw in zip(exact_projected_cdf, exact_raw_cdf)
    )
    rational_cdf_float = np.array([float(value) for value in exact_projected_cdf])
    rational_mass_float = np.array([float(value) for value in exact_projected_mass])
    rational_grid_error = float(np.dot(np.diff(grid), np.abs(rational_cdf_float - true_grid_cdf)))
    rational_true_error = float(wasserstein_distance(grid, eigenvalues, rational_mass_float, weights))
    projection = {
        "grid_points": len(grid),
        "grid_mesh": grid_step,
        "source_copies_in_example": base_n + sum(counts),
        "negative_signed_mass_count": int(np.count_nonzero(signed_mass < -1e-12)),
        "raw_cdf_below_zero_count": int(np.count_nonzero(raw_cdf < -1e-12)),
        "raw_cdf_above_one_count": int(np.count_nonzero(raw_cdf > 1 + 1e-12)),
        "projection_solver_success": bool(fit.success),
        "projection_L1_objective": float(fit.fun),
        "raw_L1_error_to_quantized_target": raw_grid_error,
        "projected_W1_to_quantized_target": projected_grid_error,
        "twice_raw_error_bound": 2 * raw_grid_error,
        "target_quantization_W1": quantization_error,
        "projected_W1_to_original_target": projected_true_error,
        "full_bound_2raw_plus_quantization": 2 * raw_grid_error + quantization_error,
        "projected_mass_minimum": float(projected_mass.min()),
        "projected_mass_sum": float(projected_mass.sum()),
        "exact_rational_projector": {
            "algorithm": "Rote SOSA2019 Section9 unweighted L1 isotonic, exact Fraction arithmetic",
            "operation_bound": "O(K log K) heap operations for K CDF intervals",
            "signed_mass_sum_exact": str(sum(exact_signed_mass)),
            "objective_exact": str(exact_objective),
            "objective_float": float(exact_objective),
            "LP_objective_difference": abs(float(exact_objective) - float(fit.fun)),
            "raw_CDF_float_vs_rational_maximum_error": float(np.max(np.abs(
                raw_cdf - np.array([float(value) for value in exact_raw_cdf])
            ))),
            "probability_mass_sum_exact": str(sum(exact_projected_mass)),
            "minimum_probability_mass_exact": str(min(exact_projected_mass)),
            "positive_probability_masses": int(sum(mass > 0 for mass in exact_projected_mass)),
            "projected_W1_to_quantized_target": rational_grid_error,
            "projected_W1_to_original_target": rational_true_error,
        },
    }

    assert max(item["maximum_exact_vs_latent_error"] for item in checks.values()) < 1e-12
    assert max(item["selected_six_step_path_maximum_error"] for item in checks.values()) < 1e-12
    assert projection["negative_signed_mass_count"] > 0
    assert projected_grid_error <= 2 * raw_grid_error + 1e-10
    assert projected_true_error <= 2 * raw_grid_error + quantization_error + 1e-10
    assert sum(exact_signed_mass) == 1
    assert sum(exact_projected_mass) == 1 and min(exact_projected_mass) >= 0
    assert abs(float(exact_objective) - fit.fun) < 1e-10
    assert rational_grid_error <= 2 * raw_grid_error + 1e-10
    assert rational_true_error <= 2 * raw_grid_error + quantization_error + 1e-10
    report = {
        "scope": "Finite exact-matrix check; not a proof of general query complexity or novelty.",
        "seed": SEED,
        "dimension": dimension,
        "hamiltonian_eigenvalues": eigenvalues.tolist(),
        "walk_unitarity_error": float(np.linalg.norm(walk.conj().T @ walk - np.eye(dimension))),
        "H_cosine_walk_identity_error": float(np.linalg.norm(hamiltonian - (walk + walk.conj().T) / 2)),
        "exact_kraus_checks": checks,
        "median_three_resolution_checks": scaling,
        "signed_CDF_projection": projection,
        "all_assertions_passed": True,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "output": str(output_path),
        "maximum_joint_error": max(item["maximum_exact_vs_latent_error"] for item in checks.values()),
        "coarsest_retained_variance": scaling[0]["retained"]["integrated_variance"],
        "finest_retained_variance": scaling[-1]["retained"]["integrated_variance"],
        "finest_reset_variance": scaling[-1]["reset"]["integrated_variance"],
        "projection": projection,
        "passed": True,
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "results" / "spectral_coupling_validation.json",
        help="JSON report path; defaults to results/ next to this script.",
    )
    main(parser.parse_args().output.expanduser().resolve())
