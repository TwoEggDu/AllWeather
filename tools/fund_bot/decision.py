"""Decision engine: convert signal scores into an actionable buy/hold/redeem decision.

The engine performs two passes:
    1. Weighted score aggregation (soft scoring).
    2. Hard gate overrides (binary conditions that force specific actions).

Thresholds and gate definitions are configurable constants at the top of this module.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from tools.fund_bot.models import (
    ActionType,
    Decision,
    FundConfig,
    FundSnapshot,
    HoldingSnapshot,
    SignalScore,
)


# ---------------------------------------------------------------------------
# Configurable thresholds for weighted score -> action mapping
# ---------------------------------------------------------------------------

THRESHOLD_BUY: float = 0.70          # score > 0.70 -> BUY
THRESHOLD_SMALL_BUY: float = 0.55    # 0.55 < score <= 0.70 -> SMALL_BUY
THRESHOLD_HOLD: float = 0.40         # 0.40 < score <= 0.55 -> HOLD
THRESHOLD_WATCH_REDEEM: float = 0.25 # 0.25 < score <= 0.40 -> WATCH_REDEEM
# score <= 0.25 -> REDEEM

# ---------------------------------------------------------------------------
# Hard gate definitions
# ---------------------------------------------------------------------------

# If max drawdown exceeds this (absolute), flag concern
HARD_GATE_MAX_DD: float = 0.25       # -25%

# If current drawdown exceeds this AND recovery > N days, escalate to WATCH_REDEEM
HARD_GATE_CURRENT_DD: float = 0.15   # -15%
HARD_GATE_STALE_RECOVERY_DAYS: int = 90

# If distance from high exceeds this, never upgrade to BUY
HARD_GATE_DISTANCE_FROM_HIGH: float = 0.10  # 10% below peak

# Concentration threshold: if top-N concentration > this, add risk warning
HARD_GATE_CONCENTRATION: float = 0.65


# ---------------------------------------------------------------------------
# Core decision function
# ---------------------------------------------------------------------------

def make_decision(
    signals: list[SignalScore],
    fund_config: FundConfig,
    snapshot: Optional[FundSnapshot] = None,
    holding: Optional[HoldingSnapshot] = None,
) -> Decision:
    """Convert a list of signal scores into a final decision.

    Two-pass process:
        Pass 1 -- Weighted aggregation: sum(score_i * weight_i) / sum(weight_i)
        Pass 2 -- Hard gate overrides: check binary conditions that may
                   upgrade or downgrade the action.

    Args:
        signals: List of scored signals from a signal engine.
        fund_config: Fund configuration (used for redemption cycle, etc.).
        snapshot: Optional fund snapshot for hard-gate checks.
        holding: Optional holding snapshot for concentration gates.

    Returns:
        A Decision with action, confidence, reasons, and invalidation conditions.
    """
    # ----- Pass 1: Weighted score -----
    total_weight = sum(s.weight for s in signals)
    if total_weight == 0:
        weighted_score = 0.5
    else:
        weighted_score = sum(s.score * s.weight for s in signals) / total_weight

    action = _score_to_action(weighted_score)
    reasons: list[str] = [
        f"Weighted signal score: {weighted_score:.3f}",
    ]
    # Add top contributing signals
    sorted_signals = sorted(signals, key=lambda s: s.score * s.weight, reverse=True)
    for sig in sorted_signals[:3]:
        reasons.append(f"  {sig.signal_name}: {sig.score:.2f} (w={sig.weight:.2f}) -- {sig.reasoning}")

    invalidation: list[str] = []
    gates_triggered: list[str] = []

    # ----- Pass 2: Hard gates -----
    if snapshot is not None:
        action, gates_triggered, invalidation = _apply_hard_gates(
            action=action,
            weighted_score=weighted_score,
            snapshot=snapshot,
            holding=holding,
            fund_config=fund_config,
        )
        if gates_triggered:
            reasons.append("Hard gates triggered:")
            reasons.extend(f"  - {g}" for g in gates_triggered)

    # Confidence: the weighted score itself, adjusted slightly by gate triggers
    confidence = weighted_score
    if gates_triggered:
        # Gate overrides reduce confidence to reflect uncertainty
        confidence = max(0.0, confidence - 0.05 * len(gates_triggered))

    # Next review date: roughly one redemption cycle from now
    next_review = (
        datetime.now() + timedelta(days=fund_config.redemption_cycle_days)
    ).strftime("%Y-%m-%d")

    return Decision(
        action=action,
        confidence=round(confidence, 3),
        reasons=reasons,
        invalidation_conditions=invalidation,
        next_review_date=next_review,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _score_to_action(score: float) -> str:
    """Map a weighted score to an action string using configurable thresholds."""
    if score > THRESHOLD_BUY:
        return ActionType.BUY.value
    elif score > THRESHOLD_SMALL_BUY:
        return ActionType.SMALL_BUY.value
    elif score > THRESHOLD_HOLD:
        return ActionType.HOLD.value
    elif score > THRESHOLD_WATCH_REDEEM:
        return ActionType.WATCH_REDEEM.value
    else:
        return ActionType.REDEEM.value


def _apply_hard_gates(
    action: str,
    weighted_score: float,
    snapshot: FundSnapshot,
    holding: Optional[HoldingSnapshot],
    fund_config: FundConfig,
) -> tuple[str, list[str], list[str]]:
    """Check hard gate conditions and potentially override the action.

    Returns:
        (possibly_modified_action, list_of_gate_descriptions, invalidation_conditions)
    """
    gates: list[str] = []
    invalidation: list[str] = []

    # Gate 1: Severe drawdown + stalled recovery -> at least WATCH_REDEEM
    if (
        abs(snapshot.current_drawdown) >= HARD_GATE_CURRENT_DD
        and snapshot.drawdown_recovery_days >= HARD_GATE_STALE_RECOVERY_DAYS
    ):
        gates.append(
            f"Current DD {snapshot.current_drawdown:.1%} with "
            f"{snapshot.drawdown_recovery_days}d stalled recovery "
            f"(thresholds: {-HARD_GATE_CURRENT_DD:.0%} / {HARD_GATE_STALE_RECOVERY_DAYS}d)"
        )
        if action in (ActionType.BUY.value, ActionType.SMALL_BUY.value, ActionType.HOLD.value):
            action = ActionType.WATCH_REDEEM.value
        invalidation.append(
            "Upgrade if NAV recovers above "
            f"{snapshot.nav_high_watermark * (1 - HARD_GATE_CURRENT_DD / 2):.4f} "
            "and recovery trend resumes."
        )

    # Gate 2: Distance from high -> never BUY (only SMALL_BUY at best)
    if snapshot.distance_from_high >= HARD_GATE_DISTANCE_FROM_HIGH:
        if action == ActionType.BUY.value:
            gates.append(
                f"Distance from high {snapshot.distance_from_high:.1%} "
                f">= {HARD_GATE_DISTANCE_FROM_HIGH:.0%}; "
                "capping action at SMALL_BUY."
            )
            action = ActionType.SMALL_BUY.value
            invalidation.append(
                "Upgrade to BUY once NAV recovers to within "
                f"{HARD_GATE_DISTANCE_FROM_HIGH:.0%} of high-water mark."
            )

    # Gate 3: Max drawdown severity -> add warning but don't override
    if abs(snapshot.max_drawdown) >= HARD_GATE_MAX_DD:
        gates.append(
            f"Historical max DD {snapshot.max_drawdown:.1%} breaches "
            f"{-HARD_GATE_MAX_DD:.0%} threshold; elevated tail risk."
        )
        invalidation.append(
            "Monitor closely: fund has demonstrated capacity for "
            f"{snapshot.max_drawdown:.1%} drawdowns."
        )

    # Gate 4: Extreme concentration risk
    if holding is not None and holding.total_concentration >= HARD_GATE_CONCENTRATION:
        gates.append(
            f"Top holdings concentration {holding.total_concentration:.0%} "
            f">= {HARD_GATE_CONCENTRATION:.0%}; idiosyncratic risk elevated."
        )
        if action == ActionType.BUY.value:
            action = ActionType.SMALL_BUY.value
        invalidation.append(
            "Re-evaluate if concentration drops below "
            f"{HARD_GATE_CONCENTRATION:.0%}."
        )

    return action, gates, invalidation
