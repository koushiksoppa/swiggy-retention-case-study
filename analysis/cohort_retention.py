"""
cohort_retention.py
-------------------
Tests the case study's core claim on REAL transaction data:

    "Retention is a habit problem: it is won or lost in a customer's first
     few orders, and how quickly the second order comes matters."

Dataset: UCI "Online Retail" (Chen, Sain & Guo, 2012) - every transaction of a
UK online retailer, 1 Dec 2010 to 9 Dec 2011, 541,909 invoice lines.
It is not food delivery, so this script tests the *pattern* (how repeat
behaviour builds order by order), not Swiggy's actual retention levels.
See data/README.md for how to download it.

Method choices (each one avoids a known trap):
  * An "order" is a distinct customer-day, so several invoices on one day
    do not count as repeat behaviour.
  * Cancellations (invoice starting "C"), returns, zero prices and rows with
    no customer ID are removed.
  * Customers first seen in Dec 2010 are excluded from acquisition analysis:
    the data starts that month, so they may be long-standing customers.
  * Repeat questions use a fixed 90-day window and only include customers
    whose relevant order is at least 90 days before the data ends, so
    recent customers are not counted as "not returning".
  * December 2011 is a partial month (9 days) and is excluded from the
    monthly cohort table.

Outputs:
  analysis/outputs/habit_ladder.csv
  analysis/outputs/second_order_speed.csv
  analysis/outputs/cohort_retention.csv
  analysis/outputs/summary.json
  charts/habit_ladder.png, charts/cohort_retention.png

Run:
  python analysis/cohort_retention.py
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
OUT = BASE / "analysis" / "outputs"
CHARTS = BASE / "charts"
OUT.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

DATA_END = pd.Timestamp("2011-12-09")
WINDOW_DAYS = 90
FAST_SECOND_ORDER_DAYS = 30
LADDER_MAX = 6

BLUE, INK, INK_SOFT, MUTED, GRID, SURFACE = "#2a78d6", "#0b0b0b", "#52514e", "#898781", "#e6e5e0", "#fcfcfb"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def load_raw() -> pd.DataFrame:
    """Read the dataset from either published format."""
    rda, xlsx = RAW / "onlineretail.rda", RAW / "Online Retail.xlsx"
    if rda.exists():
        import pyreadr
        df = pyreadr.read_r(str(rda))["onlineretail"]
    elif xlsx.exists():
        df = pd.read_excel(xlsx)
    else:
        raise FileNotFoundError("Dataset not found. See data/README.md for download steps.")
    logger.info("Loaded %s invoice lines", f"{len(df):,}")
    return df


def build_orders(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    raw_lines = len(df)
    df = df[df.CustomerID.notna()
            & ~df.InvoiceNo.astype(str).str.startswith("C")
            & (df.Quantity > 0) & (df.UnitPrice > 0)].copy()
    df["revenue"] = df.Quantity * df.UnitPrice
    df["day"] = pd.to_datetime(df.InvoiceDate).dt.normalize()
    orders = df.groupby(["CustomerID", "day"], as_index=False).revenue.sum().sort_values(["CustomerID", "day"])
    first = orders.groupby("CustomerID").day.transform("min")
    all_customers = orders.CustomerID.nunique()
    orders = orders[first >= "2011-01-01"].copy()
    orders["first_day"] = orders.groupby("CustomerID").day.transform("min")
    orders["order_n"] = orders.groupby("CustomerID").cumcount() + 1
    stats = {
        "raw_invoice_lines": raw_lines,
        "clean_invoice_lines": len(df),
        "customers_all": all_customers,
        "new_customers_2011": int(orders.CustomerID.nunique()),
        "orders_new_customers": len(orders),
    }
    return orders, stats


def habit_ladder(orders: pd.DataFrame) -> pd.DataFrame:
    """P(order n+1 within 90 days | customer placed order n)."""
    rows = []
    cutoff = DATA_END - pd.Timedelta(days=WINDOW_DAYS)
    for n in range(1, LADDER_MAX + 1):
        base = orders[(orders.order_n == n) & (orders.day <= cutoff)][["CustomerID", "day"]]
        nxt = orders[orders.order_n == n + 1][["CustomerID", "day"]].rename(columns={"day": "next_day"})
        m = base.merge(nxt, on="CustomerID", how="left")
        returned = ((m.next_day - m.day).dt.days <= WINDOW_DAYS).sum()
        rows.append({"after_order": n, "customers": len(m), "returned_within_90d": int(returned),
                     "return_rate_pct": round(returned / len(m) * 100, 1)})
    return pd.DataFrame(rows)


def second_order_speed(orders: pd.DataFrame) -> pd.DataFrame:
    """Do customers with a fast second order go on to a third more often?"""
    total = orders.groupby("CustomerID").order_n.max()
    firsts = orders[orders.order_n <= 2].pivot(index="CustomerID", columns="order_n", values="day")
    # Acquired at least 180 days before the data ends, so everyone had time to reach order 3.
    firsts = firsts[firsts[1] <= DATA_END - pd.Timedelta(days=180)].dropna()
    gap = (firsts[2] - firsts[1]).dt.days
    group = gap.le(FAST_SECOND_ORDER_DAYS).map({True: f"2nd order within {FAST_SECOND_ORDER_DAYS} days",
                                                False: f"2nd order after {FAST_SECOND_ORDER_DAYS} days"})
    d = pd.DataFrame({"group": group, "reached_3": total.reindex(gap.index) >= 3})
    out = d.groupby("group").agg(customers=("reached_3", "size"), reached_3rd_order=("reached_3", "sum"))
    out["reached_3rd_order_pct"] = (out.reached_3rd_order / out.customers * 100).round(1)
    return out.reset_index()


def cohort_table(orders: pd.DataFrame) -> pd.DataFrame:
    o = orders.copy()
    o["month"] = o.day.dt.to_period("M")
    o["cohort"] = o.first_day.dt.to_period("M")
    o = o[o.month <= pd.Period("2011-11", "M")]  # December 2011 is partial
    o["age"] = (o.month - o.cohort).apply(lambda x: x.n)
    counts = o.groupby(["cohort", "age"]).CustomerID.nunique().unstack()
    pct = counts.div(counts[0], axis=0) * 100
    pct.insert(0, "cohort_size", counts[0])
    pct.index = pct.index.astype(str)
    return pct.round(1)


def chart_ladder(ladder: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.15)
    x = [f"After order {n}" for n in ladder.after_order]
    ax.bar(x, ladder.return_rate_pct, color=BLUE, width=0.55)
    for i, (v, c) in enumerate(zip(ladder.return_rate_pct, ladder.customers)):
        ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=10, color=INK, fontweight="bold")
        ax.text(i, 3, f"n={c:,}", ha="center", fontsize=8, color="white")
    ax.set_ylim(0, 100)
    ax.set_ylabel("Ordered again within 90 days (%)", color=MUTED, fontsize=9)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.tick_params(axis="x", colors=INK)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    first, third = ladder.return_rate_pct.iloc[0], ladder.return_rate_pct.iloc[2]
    fig.text(0.02, 0.965, f"The habit ladder: {first:.0f}% return after a first order, {third:.0f}% after a third",
             fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.895, "Share of new customers placing their next order within 90 days. Real transactions, "
             "UCI Online Retail dataset (UK, 2011).", fontsize=9.5, color=INK_SOFT, va="top")
    path = CHARTS / "habit_ladder.png"
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def chart_cohorts(cohorts: pd.DataFrame) -> Path:
    grid = cohorts.drop(columns=["cohort_size", 0]).iloc[:, :6].dropna(how="all")
    sizes = cohorts.cohort_size.loc[grid.index]
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    fig.subplots_adjust(left=0.16, right=0.97, top=0.80, bottom=0.12)
    vmax = 35.0
    for r, (cohort, row) in enumerate(grid.iterrows()):
        for c, v in enumerate(row):
            if pd.isna(v):
                continue
            step = min(int(v / vmax * (len(BLUE_RAMP) - 1)), len(BLUE_RAMP) - 1)
            ax.add_patch(plt.Rectangle((c, r), 0.96, 0.92, color=BLUE_RAMP[step]))
            ax.text(c + 0.48, r + 0.46, f"{v:.0f}%", ha="center", va="center", fontsize=9,
                    color="white" if step >= 3 else INK)
    ax.set_xlim(0, grid.shape[1])
    ax.set_ylim(grid.shape[0], 0)
    ax.set_xticks([i + 0.48 for i in range(grid.shape[1])], [f"Month {i}" for i in grid.columns], color=INK, fontsize=9)
    ax.set_yticks([i + 0.46 for i in range(grid.shape[0])],
                  [f"{pd.Period(c).strftime('%b %Y')}  (n={int(n)})" for c, n in zip(grid.index, sizes)],
                  color=INK, fontsize=9)
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    fig.text(0.02, 0.965, "Monthly cohort retention: roughly 1 in 5 new customers is active in any later month",
             fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.02, 0.9, "Share of each month's new customers who ordered again N months later. Darker = higher. "
             "Dec 2011 excluded (partial month).", fontsize=9.5, color=INK_SOFT, va="top")
    path = CHARTS / "cohort_retention.png"
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def main() -> None:
    orders, stats = build_orders(load_raw())
    ladder = habit_ladder(orders)
    speed = second_order_speed(orders)
    cohorts = cohort_table(orders)

    mature = cohorts[cohorts.index <= "2011-08"]
    weighted_m1 = (mature[1] * mature.cohort_size).sum() / mature.cohort_size.sum()
    summary = {
        **stats,
        "habit_ladder_return_rate_pct": dict(zip(ladder.after_order.astype(str), ladder.return_rate_pct)),
        "no_second_order_within_90d_pct": round(100 - ladder.return_rate_pct.iloc[0], 1),
        "second_order_speed": speed.set_index("group").reached_3rd_order_pct.to_dict(),
        "month1_retention_weighted_pct_jan_aug_cohorts": round(float(weighted_m1), 1),
    }
    ladder.to_csv(OUT / "habit_ladder.csv", index=False)
    speed.to_csv(OUT / "second_order_speed.csv", index=False)
    cohorts.to_csv(OUT / "cohort_retention.csv")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")
    for p in (chart_ladder(ladder), chart_cohorts(cohorts)):
        logger.info("Chart written: %s", p.relative_to(BASE))
    logger.info("Summary: %s", json.dumps(summary, default=float))


if __name__ == "__main__":
    main()
