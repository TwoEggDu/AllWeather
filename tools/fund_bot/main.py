"""Entry point for the fund decision support system.

Usage:
    python -m tools.fund_bot.main --config tools/fund_bot/funds/example/config.json

The pipeline:
    1. Load fund config from JSON
    2. Load NAV series from CSV
    3. Compute performance / risk snapshot (analytics layer)
    4. Load holdings if available
    5. Construct market regime (placeholder -- TODO: integrate real data)
    6. Run strategy-specific signal engine
    7. Make buy / hold / redeem decision
    8. Generate Markdown report and write to disk
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime

from tools.fund_bot.analytics import compute_snapshot
from tools.fund_bot.decision import make_decision
from tools.fund_bot.ingest import load_config, load_holdings, load_nav_series
from tools.fund_bot.models import MarketRegime
from tools.fund_bot.report import generate_report
from tools.fund_bot.signals import get_signal_engine


def _default_regime() -> MarketRegime:
    """Return a placeholder market regime for MVP testing.

    In production this would be sourced from the macro dashboard or
    an external data feed. The placeholder represents a mild
    late-cycle environment.
    """
    return MarketRegime(
        date=datetime.now().strftime("%Y-%m-%d"),
        growth_trend="stable",
        inflation_trend="falling",
        policy_stance="easing",
        trend_strength=0.6,
        volatility_regime="moderate",
    )


def run(config_path: str) -> str:
    """Execute the full pipeline for a single fund.

    Args:
        config_path: Path to the fund config JSON file.

    Returns:
        The generated Markdown report string.
    """
    # 1. Load config
    print(f"[fund_bot] Loading config: {config_path}")
    config = load_config(config_path)
    print(f"[fund_bot] Fund: {config.name} ({config.strategy_type})")

    # 2. Load NAV series
    # Resolve nav_file relative to the config file's directory if not absolute
    if os.path.isabs(config.nav_file):
        nav_path = config.nav_file
    else:
        # Try relative to project root first, then relative to config dir
        if os.path.isfile(config.nav_file):
            nav_path = config.nav_file
        else:
            config_dir = os.path.dirname(os.path.abspath(config_path))
            nav_path = os.path.join(config_dir, os.path.basename(config.nav_file))

    print(f"[fund_bot] Loading NAV series: {nav_path}")
    nav_series = load_nav_series(nav_path)
    print(f"[fund_bot] Loaded {len(nav_series)} NAV observations "
          f"({nav_series[0].date} to {nav_series[-1].date})")

    # 3. Compute snapshot
    snapshot = compute_snapshot(nav_series)
    print(f"[fund_bot] Snapshot: return={snapshot.total_return:.2%}, "
          f"sharpe={snapshot.sharpe_ratio:.2f}, "
          f"maxDD={snapshot.max_drawdown:.2%}")

    # 4. Load holdings (optional)
    holdings_dir = config.holdings_dir
    if not os.path.isabs(holdings_dir):
        if not os.path.isdir(holdings_dir):
            config_dir = os.path.dirname(os.path.abspath(config_path))
            holdings_dir = os.path.join(config_dir, os.path.basename(holdings_dir))
    holding = load_holdings(holdings_dir)
    if holding:
        print(f"[fund_bot] Loaded holdings snapshot from {holding.date}")
    else:
        print("[fund_bot] No holdings data available (will use defaults)")

    # 5. Market regime (placeholder)
    regime = _default_regime()
    print(f"[fund_bot] Regime: growth={regime.growth_trend}, "
          f"policy={regime.policy_stance}, vol={regime.volatility_regime}")

    # 6. Signal computation
    engine = get_signal_engine(config.strategy_type)
    signals = engine.compute_signals(snapshot, holding, regime)
    print(f"[fund_bot] Computed {len(signals)} signals:")
    for sig in signals:
        print(f"  {sig.signal_name}: {sig.score:.2f} (w={sig.weight})")

    # 7. Decision
    decision = make_decision(signals, config, snapshot=snapshot, holding=holding)
    print(f"[fund_bot] Decision: {decision.action} "
          f"(confidence={decision.confidence:.1%})")

    # 8. Generate report
    report = generate_report(config, snapshot, signals, decision, regime)

    # Write report to disk
    reports_dir = config.reports_dir
    if not os.path.isabs(reports_dir):
        if not os.path.isdir(reports_dir):
            config_dir = os.path.dirname(os.path.abspath(config_path))
            reports_dir_candidate = os.path.join(
                config_dir, os.path.basename(reports_dir)
            )
            if os.path.isdir(reports_dir_candidate):
                reports_dir = reports_dir_candidate

    os.makedirs(reports_dir, exist_ok=True)
    report_date = datetime.now().strftime("%Y-%m-%d")
    report_filename = f"{report_date}_{config.strategy_type}_report.md"
    report_path = os.path.join(reports_dir, report_filename)
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"[fund_bot] Report written to: {report_path}")

    return report


def main() -> None:
    """CLI entry point with argparse."""
    parser = argparse.ArgumentParser(
        prog="fund_bot",
        description=(
            "Private fund decision support system. "
            "Evaluates buy/hold/redeem decisions for funds across "
            "macro hedge, CTA, quant, and long-only equity strategies."
        ),
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to fund config JSON file.",
    )
    args = parser.parse_args()

    try:
        report = run(args.config)
        print("\n" + "=" * 60)
        print(report)
    except Exception as exc:
        print(f"[fund_bot] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
