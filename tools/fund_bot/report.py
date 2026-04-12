"""Report generation layer: produce a Markdown report from decision outputs.

The report is structured for human review and includes:
    - Header with date, fund name, and strategy type
    - Decision summary with confidence
    - Signal breakdown table
    - Key evidence and reasoning
    - Risk gates triggered
    - Redemption window and next review date
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from tools.fund_bot.models import (
    Decision,
    FundConfig,
    FundSnapshot,
    MarketRegime,
    SignalScore,
)


def generate_report(
    config: FundConfig,
    snapshot: FundSnapshot,
    signals: list[SignalScore],
    decision: Decision,
    regime: Optional[MarketRegime] = None,
) -> str:
    """Generate a complete Markdown report string.

    Args:
        config: Fund configuration.
        snapshot: Computed fund metrics.
        signals: Scored signals from the signal engine.
        decision: Final decision output.
        regime: Optional market regime context.

    Returns:
        A formatted Markdown string suitable for writing to a .md file.
    """
    lines: list[str] = []

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    report_date = datetime.now().strftime("%Y-%m-%d")
    lines.append(f"# {config.name} -- Decision Report")
    lines.append("")
    lines.append(f"**Report Date:** {report_date}")
    lines.append(f"**Strategy Type:** {config.strategy_type}")
    lines.append(f"**Redemption Cycle:** {config.redemption_cycle_days} days")
    lines.append("")

    # ------------------------------------------------------------------
    # Decision summary
    # ------------------------------------------------------------------
    lines.append("## Decision")
    lines.append("")
    action_emoji = _action_label(decision.action)
    lines.append(f"**Action: {decision.action}** {action_emoji}")
    lines.append(f"**Confidence:** {decision.confidence:.1%}")
    lines.append("")

    # ------------------------------------------------------------------
    # Fund metrics snapshot
    # ------------------------------------------------------------------
    lines.append("## Fund Metrics")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Total Return | {snapshot.total_return:.2%} |")
    lines.append(f"| Annualised Return (CAGR) | {snapshot.annualized_return:.2%} |")
    lines.append(f"| Max Drawdown | {snapshot.max_drawdown:.2%} |")
    lines.append(f"| Current Drawdown | {snapshot.current_drawdown:.2%} |")
    lines.append(f"| Days Since Peak | {snapshot.drawdown_recovery_days} |")
    lines.append(f"| Sharpe Ratio | {snapshot.sharpe_ratio:.2f} |")
    lines.append(f"| Recent 1M Return | {snapshot.recent_1m_return:.2%} |")
    lines.append(f"| Recent 3M Return | {snapshot.recent_3m_return:.2%} |")
    lines.append(f"| Annualised Volatility | {snapshot.volatility:.2%} |")
    lines.append(f"| NAV High-Water Mark | {snapshot.nav_high_watermark:.4f} |")
    lines.append(f"| Distance from High | {snapshot.distance_from_high:.2%} |")
    lines.append("")

    # ------------------------------------------------------------------
    # Market regime (if available)
    # ------------------------------------------------------------------
    if regime is not None:
        lines.append("## Market Regime")
        lines.append("")
        lines.append(f"| Dimension | State |")
        lines.append(f"|-----------|-------|")
        lines.append(f"| Growth Trend | {regime.growth_trend} |")
        lines.append(f"| Inflation Trend | {regime.inflation_trend} |")
        lines.append(f"| Policy Stance | {regime.policy_stance} |")
        lines.append(f"| Trend Strength | {regime.trend_strength:.2f} |")
        lines.append(f"| Volatility Regime | {regime.volatility_regime} |")
        lines.append("")

    # ------------------------------------------------------------------
    # Signal breakdown
    # ------------------------------------------------------------------
    lines.append("## Signal Breakdown")
    lines.append("")
    lines.append("| Signal | Score | Weight | Weighted |")
    lines.append("|--------|-------|--------|----------|")
    total_weighted = 0.0
    total_weight = 0.0
    for sig in signals:
        weighted = sig.score * sig.weight
        total_weighted += weighted
        total_weight += sig.weight
        lines.append(
            f"| {sig.signal_name} | {sig.score:.2f} | {sig.weight:.2f} "
            f"| {weighted:.3f} |"
        )
    if total_weight > 0:
        agg = total_weighted / total_weight
        lines.append(f"| **Aggregate** | **{agg:.2f}** | | |")
    lines.append("")

    # ------------------------------------------------------------------
    # Signal reasoning (key evidence)
    # ------------------------------------------------------------------
    lines.append("## Key Evidence")
    lines.append("")
    for sig in signals:
        lines.append(f"- **{sig.signal_name}:** {sig.reasoning}")
    lines.append("")

    # ------------------------------------------------------------------
    # Decision reasoning and risk gates
    # ------------------------------------------------------------------
    lines.append("## Decision Reasoning")
    lines.append("")
    for reason in decision.reasons:
        lines.append(f"- {reason}")
    lines.append("")

    if decision.invalidation_conditions:
        lines.append("## Risk Gates & Invalidation Conditions")
        lines.append("")
        for cond in decision.invalidation_conditions:
            lines.append(f"- {cond}")
        lines.append("")

    # ------------------------------------------------------------------
    # Next steps
    # ------------------------------------------------------------------
    lines.append("## Next Steps")
    lines.append("")
    lines.append(f"- **Next Redemption Window:** ~{config.redemption_cycle_days} days from last NAV date")
    lines.append(f"- **Next Review Date:** {decision.next_review_date}")
    lines.append("")

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------
    lines.append("---")
    lines.append(f"*Generated by fund_bot on {report_date}*")
    lines.append("")

    return "\n".join(lines)


def _action_label(action: str) -> str:
    """Return a short descriptive label for the action (no emoji)."""
    labels = {
        "BUY": "(strong conviction, add full position)",
        "SMALL_BUY": "(moderate conviction, add partial position)",
        "HOLD": "(maintain current position, monitor)",
        "WATCH_REDEEM": "(prepare for potential redemption, heightened monitoring)",
        "REDEEM": "(redeem at next available window)",
    }
    return labels.get(action, "")
