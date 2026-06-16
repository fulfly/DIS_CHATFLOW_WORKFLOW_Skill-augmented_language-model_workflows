#!/usr/bin/env python
"""Run all manuscript figure scripts with their default input paths."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    scripts = [
        ROOT / "scripts/fig3_model_performance.py",
        ROOT / "scripts/fig4_viscosity_timecourse.py",
        ROOT / "scripts/fig5_optimized_formulation_validation.py",
    ]
    for script in scripts:
        subprocess.run([sys.executable, str(script)], check=True)


if __name__ == "__main__":
    main()

