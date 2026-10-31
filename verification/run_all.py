#!/usr/bin/env python3
"""Run both finite verification scripts and record reports with source hashes.

The numerical assertions check selected finite identities, not the general
theorems. All paths are resolved relative to this file, independent of cwd.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


BASE = Path(__file__).resolve().parent
RESULTS = BASE / "results"
CHECKS = (
    (
        "spectral_coupling",
        "validate_spectral_coupling.py",
        "spectral_coupling_validation.json",
        "all_assertions_passed",
    ),
    (
        "spectral_lower",
        "validate_spectral_lower.py",
        "spectral_lower_validation.json",
        "all_checks_passed",
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not __debug__:
        parser.error("Run without -O or PYTHONOPTIMIZE; verification requires assertions.")
    try:
        dependencies = {name: version(name) for name in ("numpy", "scipy")}
    except PackageNotFoundError as exc:
        parser.error(f"{exc}. Install verification/requirements.txt first.")

    RESULTS.mkdir(parents=True, exist_ok=True)
    manifest_path = RESULTS / "run_manifest.json"
    manifest = {
        "scope": "Finite consistency checks; not formal theorem verification or a hardware benchmark.",
        "started_at_utc": utc_now(),
        "python": platform.python_version(),
        "dependencies": dependencies,
        "source_sha256": {
            name: sha256(BASE / name)
            for name in (
                "run_all.py",
                "validate_spectral_coupling.py",
                "validate_spectral_lower.py",
                "exact_cdf_projection.py",
                "requirements.txt",
            )
        },
        "expected_snapshot_sha256": {
            report_name: sha256(BASE / "expected" / report_name)
            for _, _, report_name, _ in CHECKS
        },
        "status": "running",
        "checks": [],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    all_passed = True
    for name, script_name, report_name, pass_key in CHECKS:
        report_path = RESULTS / report_name
        report_path.unlink(missing_ok=True)
        print(f"Running {script_name}", flush=True)
        started = time.monotonic()
        completed = subprocess.run(
            [sys.executable, "-B", str(BASE / script_name), "--output", str(report_path)],
            cwd=BASE,
            check=False,
        )
        check = {
            "name": name,
            "script": script_name,
            "return_code": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "report": report_name,
            "passed": False,
        }
        if report_path.is_file():
            check["report_sha256"] = sha256(report_path)
            try:
                report = json.loads(report_path.read_text())
                check["passed"] = completed.returncode == 0 and report.get(pass_key) is True
                if not check["passed"]:
                    check["failure"] = "Nonzero return code or missing positive assertion summary."
            except (OSError, json.JSONDecodeError) as exc:
                check["failure"] = f"Could not read report: {exc}"
        else:
            check["failure"] = "The check did not produce its JSON report."
        all_passed = all_passed and check["passed"]
        manifest["checks"].append(check)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    manifest["finished_at_utc"] = utc_now()
    manifest["status"] = "passed" if all_passed else "failed"
    manifest["all_checks_passed"] = all_passed
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "all_checks_passed": all_passed,
        "manifest": str(manifest_path),
        "results_directory": str(RESULTS),
    }, indent=2))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
