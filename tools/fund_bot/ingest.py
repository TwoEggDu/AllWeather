"""Data ingestion layer: load fund configs and NAV series from disk.

Handles CSV and JSON parsing using only the standard library.
"""

from __future__ import annotations

import csv
import json
import os
from typing import Optional

from tools.fund_bot.models import FundConfig, HoldingSnapshot, NavPoint


def load_nav_series(csv_path: str) -> list[NavPoint]:
    """Read a NAV CSV file and return a chronologically-ordered list of NavPoints.

    Expected CSV columns: date, nav, cumulative_nav
    Handles optional BOM markers and strips whitespace from headers.

    Args:
        csv_path: Absolute or project-relative path to the CSV file.

    Returns:
        List of NavPoint sorted by date ascending.

    Raises:
        FileNotFoundError: If csv_path does not exist.
        ValueError: If required columns are missing.
    """
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"NAV file not found: {csv_path}")

    points: list[NavPoint] = []
    with open(csv_path, "r", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        # Normalise header names (strip whitespace, lowercase)
        if reader.fieldnames is None:
            raise ValueError(f"Empty or malformed CSV: {csv_path}")
        clean_fields = [f.strip().lower() for f in reader.fieldnames]
        for required in ("date", "nav", "cumulative_nav"):
            if required not in clean_fields:
                raise ValueError(
                    f"Missing required column '{required}' in {csv_path}. "
                    f"Found columns: {clean_fields}"
                )

        for row in reader:
            # Build a clean dict using normalised keys
            clean_row = {
                k.strip().lower(): v.strip() for k, v in row.items() if k
            }
            points.append(
                NavPoint(
                    date=clean_row["date"],
                    nav=float(clean_row["nav"]),
                    cumulative_nav=float(clean_row["cumulative_nav"]),
                )
            )

    # Sort by date ascending
    points.sort(key=lambda p: p.date)
    return points


def load_config(json_path: str) -> FundConfig:
    """Read a fund configuration JSON file.

    Args:
        json_path: Path to the JSON config file.

    Returns:
        A populated FundConfig instance.

    Raises:
        FileNotFoundError: If json_path does not exist.
        KeyError: If required fields are missing.
    """
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"Config file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as fh:
        data: dict = json.load(fh)

    required_keys = [
        "name", "strategy_type", "redemption_cycle_days",
        "nav_file", "holdings_dir", "reports_dir",
    ]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Missing required config field: '{key}'")

    return FundConfig(
        name=data["name"],
        strategy_type=data["strategy_type"],
        redemption_cycle_days=int(data["redemption_cycle_days"]),
        nav_file=data["nav_file"],
        holdings_dir=data["holdings_dir"],
        reports_dir=data["reports_dir"],
    )


def load_holdings(holdings_dir: str) -> Optional[HoldingSnapshot]:
    """Load the most recent holding snapshot from a directory of JSON files.

    Each JSON file in the directory should contain:
    {
        "date": "YYYY-MM-DD",
        "top_holdings": [{"name": "...", "weight": 0.1, "sector": "..."}],
        "sector_weights": {"sector_name": weight, ...},
        "total_concentration": 0.45,
        "style_label": "growth"
    }

    Args:
        holdings_dir: Directory containing holding JSON files.

    Returns:
        The most recent HoldingSnapshot, or None if directory is empty / missing.
    """
    if not os.path.isdir(holdings_dir):
        return None

    json_files = sorted(
        [f for f in os.listdir(holdings_dir) if f.endswith(".json")],
        reverse=True,  # most recent filename first (assumes YYYY-MM-DD prefix)
    )
    if not json_files:
        return None

    latest_path = os.path.join(holdings_dir, json_files[0])
    with open(latest_path, "r", encoding="utf-8") as fh:
        data: dict = json.load(fh)

    return HoldingSnapshot(
        date=data.get("date", ""),
        top_holdings=data.get("top_holdings", []),
        sector_weights=data.get("sector_weights", {}),
        total_concentration=float(data.get("total_concentration", 0.0)),
        style_label=data.get("style_label", ""),
    )
