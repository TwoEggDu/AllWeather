"""Analytics layer: compute fund performance and risk metrics from NAV series.

Uses only the standard library (math module). No numpy / pandas dependency.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from typing import Sequence

from tools.fund_bot.models import FundSnapshot, NavPoint

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRADING_DAYS_PER_YEAR: int = 252
RISK_FREE_RATE: float = 0.0  # assume rf = 0 for Sharpe calculation (MVP)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _parse_date(d: str) -> date:
    """Parse an ISO date string to a date object."""
    return datetime.strptime(d, "%Y-%m-%d").date()


def _period_returns(nav_series: Sequence[NavPoint]) -> list[float]:
    """Compute period-over-period simple returns from an ordered NAV series.

    Returns a list of length len(nav_series) - 1.
    """
    returns: list[float] = []
    for i in range(1, len(nav_series)):
        prev = nav_series[i - 1].nav
        curr = nav_series[i].nav
        if prev == 0:
            returns.append(0.0)
        else:
            returns.append(curr / prev - 1.0)
    return returns


# ---------------------------------------------------------------------------
# Public metric functions
# ---------------------------------------------------------------------------

def total_return(nav_series: Sequence[NavPoint]) -> float:
    """Cumulative return from first to last NAV observation.

    Formula: (last_nav / first_nav) - 1
    """
    if len(nav_series) < 2:
        return 0.0
    return nav_series[-1].nav / nav_series[0].nav - 1.0


def annualized_return(nav_series: Sequence[NavPoint]) -> float:
    """Compound annual growth rate (CAGR).

    Uses calendar days between first and last observation.
    """
    if len(nav_series) < 2:
        return 0.0
    start_date = _parse_date(nav_series[0].date)
    end_date = _parse_date(nav_series[-1].date)
    days = (end_date - start_date).days
    if days <= 0:
        return 0.0
    cum = nav_series[-1].nav / nav_series[0].nav
    years = days / 365.25
    if cum <= 0:
        return -1.0
    return cum ** (1.0 / years) - 1.0


def max_drawdown(nav_series: Sequence[NavPoint]) -> float:
    """Maximum peak-to-trough drawdown (returned as a negative number).

    Walks the NAV series tracking the running peak and worst decline.
    """
    if len(nav_series) < 2:
        return 0.0
    peak = nav_series[0].nav
    worst = 0.0
    for point in nav_series:
        if point.nav > peak:
            peak = point.nav
        dd = (point.nav - peak) / peak if peak > 0 else 0.0
        if dd < worst:
            worst = dd
    return worst


def current_drawdown(nav_series: Sequence[NavPoint]) -> float:
    """Current drawdown from the high-water mark (negative number or zero)."""
    if not nav_series:
        return 0.0
    hwm = max(p.nav for p in nav_series)
    last = nav_series[-1].nav
    if hwm == 0:
        return 0.0
    return (last - hwm) / hwm


def drawdown_recovery_days(nav_series: Sequence[NavPoint]) -> int:
    """Number of calendar days since the last NAV high-water mark.

    Returns 0 if the latest observation IS the high-water mark.
    """
    if not nav_series:
        return 0
    hwm_nav = max(p.nav for p in nav_series)
    # Find the date of the most recent occurrence of the high-water mark
    hwm_date_str = ""
    for p in nav_series:
        if p.nav >= hwm_nav:
            hwm_date_str = p.date
    last_date = _parse_date(nav_series[-1].date)
    hwm_date = _parse_date(hwm_date_str)
    return (last_date - hwm_date).days


def volatility(nav_series: Sequence[NavPoint]) -> float:
    """Annualized volatility of period returns.

    Annualises by sqrt(trading_days_per_year) assuming roughly monthly data.
    Adapts the scaling factor based on average inter-observation days.
    """
    rets = _period_returns(nav_series)
    if len(rets) < 2:
        return 0.0

    # Estimate average days between observations for annualisation
    start = _parse_date(nav_series[0].date)
    end = _parse_date(nav_series[-1].date)
    total_days = (end - start).days
    avg_period_days = total_days / len(rets) if len(rets) > 0 else 30
    periods_per_year = 365.25 / avg_period_days if avg_period_days > 0 else 12

    mean = sum(rets) / len(rets)
    variance = sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)
    return math.sqrt(variance * periods_per_year)


def sharpe_ratio(nav_series: Sequence[NavPoint]) -> float:
    """Annualized Sharpe ratio (excess return / volatility).

    Assumes risk-free rate = RISK_FREE_RATE (default 0).
    """
    ann_ret = annualized_return(nav_series)
    vol = volatility(nav_series)
    if vol == 0:
        return 0.0
    return (ann_ret - RISK_FREE_RATE) / vol


def recent_return(nav_series: Sequence[NavPoint], months: int) -> float:
    """Return over approximately the last N months.

    Finds the observation closest to N months before the last date.
    """
    if len(nav_series) < 2:
        return 0.0
    last_date = _parse_date(nav_series[-1].date)
    target_days = months * 30  # rough approximation
    best_idx = 0
    best_diff = float("inf")
    for i, p in enumerate(nav_series):
        diff = abs((last_date - _parse_date(p.date)).days - target_days)
        if diff < best_diff:
            best_diff = diff
            best_idx = i
    start_nav = nav_series[best_idx].nav
    if start_nav == 0:
        return 0.0
    return nav_series[-1].nav / start_nav - 1.0


def nav_high_watermark(nav_series: Sequence[NavPoint]) -> float:
    """Highest NAV ever observed."""
    if not nav_series:
        return 0.0
    return max(p.nav for p in nav_series)


def distance_from_high(nav_series: Sequence[NavPoint]) -> float:
    """Percentage distance of latest NAV below the high-water mark.

    Returns 0.0 when at the peak; a positive fraction otherwise.
    Example: 0.05 means the current NAV is 5% below the all-time high.
    """
    if not nav_series:
        return 0.0
    hwm = nav_high_watermark(nav_series)
    if hwm == 0:
        return 0.0
    return (hwm - nav_series[-1].nav) / hwm


# ---------------------------------------------------------------------------
# Composite snapshot builder
# ---------------------------------------------------------------------------

def compute_snapshot(nav_series: list[NavPoint]) -> FundSnapshot:
    """Build a FundSnapshot by computing all metrics from the NAV series.

    This is the main entry point for the analytics layer.
    """
    return FundSnapshot(
        total_return=total_return(nav_series),
        annualized_return=annualized_return(nav_series),
        max_drawdown=max_drawdown(nav_series),
        current_drawdown=current_drawdown(nav_series),
        drawdown_recovery_days=drawdown_recovery_days(nav_series),
        sharpe_ratio=sharpe_ratio(nav_series),
        recent_1m_return=recent_return(nav_series, months=1),
        recent_3m_return=recent_return(nav_series, months=3),
        volatility=volatility(nav_series),
        nav_high_watermark=nav_high_watermark(nav_series),
        distance_from_high=distance_from_high(nav_series),
    )
