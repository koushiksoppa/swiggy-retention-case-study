"""
ab_test_sample_size.py
----------------------
Sample size and run time for the A/B test in docs/AB_TEST_DESIGN.md
(the "Your usual?" one-tap re-order widget for customers before their 3rd order).

Standard two-proportion test, two-sided:
    n per arm = (z_{1-alpha/2} * sqrt(2 p_bar (1-p_bar)) + z_{1-beta} * sqrt(p1(1-p1) + p2(1-p2)))^2 / (p2 - p1)^2

The baseline 30-day re-order rate is an ASSUMPTION (Swiggy does not publish it);
the grid shows how the answer moves with it.

Run:
    python analysis/ab_test_sample_size.py
"""

from __future__ import annotations

import math
from pathlib import Path
from statistics import NormalDist

import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

ALPHA, POWER = 0.05, 0.80


def n_per_arm(p1: float, p2: float, alpha: float = ALPHA, power: float = POWER) -> int:
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(power)
    p_bar = (p1 + p2) / 2
    num = (z_a * math.sqrt(2 * p_bar * (1 - p_bar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (p2 - p1) ** 2)


def main() -> None:
    rows = []
    for base in (0.25, 0.30, 0.35, 0.40):
        for lift_pts in (0.01, 0.02, 0.03):
            rows.append({"baseline_d30_reorder": base, "absolute_lift_pts": lift_pts * 100,
                         "relative_lift_pct": round(lift_pts / base * 100, 1),
                         "users_per_arm": n_per_arm(base, base + lift_pts)})
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / "ab_test_sample_size.csv", index=False)
    print(grid.to_string(index=False))
    print(f"\nBase case (30% -> 32%): {n_per_arm(0.30, 0.32):,} users per arm, alpha={ALPHA}, power={POWER}")


if __name__ == "__main__":
    main()
