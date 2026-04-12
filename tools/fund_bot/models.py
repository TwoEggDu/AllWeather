"""Data models for the fund tracking and decision support system.

All models use dataclasses for clarity and immutability where appropriate.
Strategy types: macro (macro hedge), cta, quant, long_only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class StrategyType(str, Enum):
    """Supported fund strategy types."""
    MACRO = "macro"
    CTA = "cta"
    QUANT = "quant"
    LONG_ONLY = "long_only"


class ActionType(str, Enum):
    """Possible decision actions, ordered from most bullish to most bearish."""
    BUY = "BUY"
    SMALL_BUY = "SMALL_BUY"
    HOLD = "HOLD"
    WATCH_REDEEM = "WATCH_REDEEM"
    REDEEM = "REDEEM"


# ---------------------------------------------------------------------------
# Layer 1: Raw data
# ---------------------------------------------------------------------------

@dataclass
class FundConfig:
    """Fund-level configuration loaded from a JSON file."""
    name: str
    strategy_type: str  # one of StrategyType values
    redemption_cycle_days: int
    nav_file: str       # path to NAV CSV
    holdings_dir: str   # directory containing periodic holding snapshots
    reports_dir: str    # output directory for generated reports


@dataclass
class NavPoint:
    """A single NAV observation."""
    date: str            # ISO date string YYYY-MM-DD
    nav: float           # unit net value
    cumulative_nav: float


# ---------------------------------------------------------------------------
# Layer 2: Standardized / computed metrics
# ---------------------------------------------------------------------------

@dataclass
class FundSnapshot:
    """Computed performance and risk metrics derived from the NAV series."""
    total_return: float           # cumulative return since inception
    annualized_return: float      # CAGR
    max_drawdown: float           # worst peak-to-trough decline (negative number)
    current_drawdown: float       # current decline from high-water mark
    drawdown_recovery_days: int   # days since last high-water mark (0 = at peak)
    sharpe_ratio: float           # annualized Sharpe (assumes rf=0 for simplicity)
    recent_1m_return: float       # most recent 1-month return
    recent_3m_return: float       # most recent 3-month return
    volatility: float             # annualized volatility of returns
    nav_high_watermark: float     # highest NAV observed
    distance_from_high: float     # pct distance from high-water mark (0 = at peak)


@dataclass
class HoldingSnapshot:
    """A point-in-time view of fund holdings and concentration."""
    date: str
    top_holdings: list[dict] = field(default_factory=list)
    # each dict: {"name": str, "weight": float, "sector": str}
    sector_weights: dict[str, float] = field(default_factory=dict)
    total_concentration: float = 0.0  # sum of top-N weights
    style_label: str = ""             # e.g. "growth", "value", "balanced"


# ---------------------------------------------------------------------------
# Layer 3: Market regime context
# ---------------------------------------------------------------------------

@dataclass
class MarketRegime:
    """Macro / market environment assessment."""
    date: str
    growth_trend: str       # "accelerating" | "stable" | "decelerating"
    inflation_trend: str    # "rising" | "stable" | "falling"
    policy_stance: str      # "easing" | "neutral" | "tightening"
    trend_strength: float   # 0-1, how clear is the macro trend
    volatility_regime: str  # "low" | "moderate" | "high"


# ---------------------------------------------------------------------------
# Layer 4: Signal scores
# ---------------------------------------------------------------------------

@dataclass
class SignalScore:
    """One scored signal from the signal engine."""
    signal_name: str
    score: float       # 0-1, higher = more favorable
    weight: float      # importance weight for aggregation
    reasoning: str     # human-readable explanation


# ---------------------------------------------------------------------------
# Layer 5: Decision output
# ---------------------------------------------------------------------------

@dataclass
class Decision:
    """Final buy / hold / redeem decision with supporting evidence."""
    action: str                    # one of ActionType values
    confidence: float              # 0-1
    reasons: list[str] = field(default_factory=list)
    invalidation_conditions: list[str] = field(default_factory=list)
    next_review_date: str = ""     # ISO date string
