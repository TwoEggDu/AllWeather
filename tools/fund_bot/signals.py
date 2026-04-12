"""Signal computation layer -- the core of the decision support system.

Each strategy type has its own signal engine that produces 5 scored signals.
All scores are in [0, 1] where higher = more favourable for holding / buying.
Every signal includes a human-readable reasoning string.

Strategy-specific engines:
    MacroHedgeSignals  -- macro hedge funds
    CTASignals         -- CTA / managed futures
    QuantSignals       -- quant / market-neutral / stat-arb
    LongOnlySignals    -- long-only equity

Factory:
    get_signal_engine(strategy_type) -> BaseSignalEngine
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from tools.fund_bot.models import (
    FundSnapshot,
    HoldingSnapshot,
    MarketRegime,
    SignalScore,
)


# =========================================================================
# Base class
# =========================================================================

class BaseSignalEngine(ABC):
    """Abstract base for strategy-specific signal computation."""

    @abstractmethod
    def compute_signals(
        self,
        snapshot: FundSnapshot,
        holding: Optional[HoldingSnapshot],
        regime: Optional[MarketRegime],
    ) -> list[SignalScore]:
        """Return a list of scored signals for this strategy type.

        Args:
            snapshot: Computed fund performance metrics.
            holding: Latest holding / concentration data (may be None).
            regime: Current macro / market regime (may be None).

        Returns:
            A list of exactly 5 SignalScore objects.
        """
        ...


# =========================================================================
# Shared signal helpers
# =========================================================================

def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp a value to [lo, hi]."""
    return max(lo, min(hi, value))


def _fund_quality_score(snapshot: FundSnapshot) -> SignalScore:
    """Evaluate intrinsic fund quality from performance metrics.

    Scoring logic:
        - Base score from Sharpe ratio: sharpe >= 1.5 -> 1.0, sharpe <= 0 -> 0.0
        - Penalty for deep max drawdown: dd worse than -20% starts penalising
        - Bonus for positive recent momentum (3m return > 0)

    This signal is shared across all strategy types.
    """
    # Sharpe component (60% weight within this signal)
    sharpe_score = _clamp(snapshot.sharpe_ratio / 1.5)

    # Drawdown component (25% weight)
    # max_drawdown is negative; -0.05 is excellent, -0.30 is terrible
    dd_abs = abs(snapshot.max_drawdown)
    dd_score = _clamp(1.0 - dd_abs / 0.30)

    # Momentum component (15% weight)
    momentum_score = _clamp(0.5 + snapshot.recent_3m_return * 5)

    score = 0.60 * sharpe_score + 0.25 * dd_score + 0.15 * momentum_score
    score = _clamp(score)

    parts: list[str] = []
    parts.append(f"Sharpe {snapshot.sharpe_ratio:.2f}")
    parts.append(f"MaxDD {snapshot.max_drawdown:.1%}")
    parts.append(f"3M return {snapshot.recent_3m_return:.1%}")
    reasoning = f"Fund quality score {score:.2f}: {', '.join(parts)}"

    return SignalScore(
        signal_name="fund_quality",
        score=score,
        weight=0.25,
        reasoning=reasoning,
    )


def _redemption_timing_score(
    snapshot: FundSnapshot,
    redemption_cycle_days: int = 30,
) -> SignalScore:
    """Evaluate whether now is a tactically good time relative to redemption windows.

    Scoring logic:
        - If the fund is near its high-water mark (distance < 2%), score high
          (good time to lock in gains if considering redemption).
        - If deep in drawdown AND recovery is stalling, the next window matters more.
        - For buying: if in drawdown, the timing may be favourable (contrarian entry).
        - Neutral score (0.5) when there is no strong timing signal.

    The score is intentionally symmetric: high = favourable for current positioning.
    """
    dist = snapshot.distance_from_high  # 0 = at peak, positive = below peak
    recovery = snapshot.drawdown_recovery_days

    if dist < 0.02:
        # Near peak -- good position, no urgency
        score = 0.7
        reasoning = (
            f"NAV within {dist:.1%} of high-water mark; "
            "comfortable position regardless of redemption window."
        )
    elif dist < 0.05 and recovery < redemption_cycle_days:
        # Mild drawdown, recovering -- wait it out
        score = 0.6
        reasoning = (
            f"Mild drawdown ({dist:.1%} from high), "
            f"recovering for {recovery}d; patience warranted."
        )
    elif dist >= 0.10 and recovery > 2 * redemption_cycle_days:
        # Deep drawdown, stalled recovery -- timing matters
        score = 0.3
        reasoning = (
            f"Significant drawdown ({dist:.1%} from high) "
            f"with {recovery}d since peak; redemption window approaching."
        )
    else:
        score = 0.5
        reasoning = (
            f"Distance from high {dist:.1%}, "
            f"recovery days {recovery}; no strong timing signal."
        )

    return SignalScore(
        signal_name="redemption_timing",
        score=_clamp(score),
        weight=0.10,
        reasoning=reasoning,
    )


# =========================================================================
# Macro Hedge signal engine
# =========================================================================

class MacroHedgeSignals(BaseSignalEngine):
    """Signal engine for macro hedge fund strategies.

    Signals (5):
        1. fund_quality       (w=0.25) -- intrinsic performance & risk metrics
        2. style_tailwind     (w=0.25) -- macro regime clarity + fund alignment
        3. holding_structure   (w=0.20) -- portfolio concentration & style
        4. position_rhythm     (w=0.20) -- NAV position relative to high
        5. redemption_timing   (w=0.10) -- tactical redemption window awareness
    """

    def compute_signals(
        self,
        snapshot: FundSnapshot,
        holding: Optional[HoldingSnapshot],
        regime: Optional[MarketRegime],
    ) -> list[SignalScore]:
        signals: list[SignalScore] = []

        # 1. Fund quality (shared)
        signals.append(_fund_quality_score(snapshot))

        # 2. Style tailwind -- macro regime clarity + fund alignment
        signals.append(self._style_tailwind(snapshot, regime))

        # 3. Holding structure
        signals.append(self._holding_structure(holding))

        # 4. Position rhythm
        signals.append(self._position_rhythm(snapshot))

        # 5. Redemption timing (shared)
        signals.append(_redemption_timing_score(snapshot))

        return signals

    @staticmethod
    def _style_tailwind(
        snapshot: FundSnapshot,
        regime: Optional[MarketRegime],
    ) -> SignalScore:
        """Macro regime clarity and fund alignment.

        High score when:
            - The macro regime is clear (high trend_strength).
            - Growth is not decelerating sharply (macro hedge funds
              generally benefit from directional trends).
            - The fund's recent performance suggests it is capturing
              the prevailing trend.

        Without regime data, falls back to a neutral score based
        solely on the fund's recent returns as a proxy.
        """
        if regime is None:
            # Fallback: use recent returns as a rough proxy for trend capture
            proxy = _clamp(0.5 + snapshot.recent_3m_return * 4)
            return SignalScore(
                signal_name="style_tailwind",
                score=proxy,
                weight=0.25,
                reasoning=(
                    f"No regime data; using 3M return ({snapshot.recent_3m_return:.1%}) "
                    "as proxy for macro trend capture."
                ),
            )

        # Regime clarity component
        clarity = regime.trend_strength  # 0-1

        # Direction component: macro hedge benefits from clear, non-stagnant regimes
        direction_map = {
            "accelerating": 0.8,
            "stable": 0.5,
            "decelerating": 0.3,
        }
        direction = direction_map.get(regime.growth_trend, 0.5)

        # Policy alignment: easing is generally supportive for risk assets
        policy_map = {"easing": 0.7, "neutral": 0.5, "tightening": 0.3}
        policy = policy_map.get(regime.policy_stance, 0.5)

        score = _clamp(0.4 * clarity + 0.35 * direction + 0.25 * policy)

        reasoning = (
            f"Regime clarity {clarity:.2f}, growth {regime.growth_trend}, "
            f"policy {regime.policy_stance} -> tailwind score {score:.2f}"
        )
        return SignalScore(
            signal_name="style_tailwind",
            score=score,
            weight=0.25,
            reasoning=reasoning,
        )

    @staticmethod
    def _holding_structure(holding: Optional[HoldingSnapshot]) -> SignalScore:
        """Evaluate portfolio concentration and style consistency.

        High score when:
            - Concentration is moderate (not too concentrated, not too diluted).
            - Style label is present and consistent.
        Low score when:
            - Extreme concentration (> 60%) or no data.
        """
        if holding is None:
            return SignalScore(
                signal_name="holding_structure",
                score=0.5,
                weight=0.20,
                reasoning="No holding data available; defaulting to neutral.",
            )

        conc = holding.total_concentration
        # Ideal concentration band: 20-50%
        if 0.20 <= conc <= 0.50:
            conc_score = 0.8
        elif conc < 0.20:
            conc_score = 0.5  # too diversified for a macro fund
        elif conc <= 0.60:
            conc_score = 0.6
        else:
            conc_score = 0.3  # overly concentrated

        style_bonus = 0.1 if holding.style_label else 0.0
        score = _clamp(conc_score + style_bonus)

        reasoning = (
            f"Concentration {conc:.0%}, style '{holding.style_label}'; "
            f"holding structure score {score:.2f}"
        )
        return SignalScore(
            signal_name="holding_structure",
            score=score,
            weight=0.20,
            reasoning=reasoning,
        )

    @staticmethod
    def _position_rhythm(snapshot: FundSnapshot) -> SignalScore:
        """NAV position relative to high-water mark.

        Evaluates whether the fund is in a healthy rhythm of making new highs
        versus being stuck in a drawdown.

        High score: near or at highs, short recovery periods.
        Low score: deep drawdown, long recovery.
        """
        dist = snapshot.distance_from_high
        recovery = snapshot.drawdown_recovery_days

        # Distance component: closer to high = better
        dist_score = _clamp(1.0 - dist / 0.15)

        # Recovery speed component: faster recovery = better
        recovery_score = _clamp(1.0 - recovery / 180)

        score = _clamp(0.6 * dist_score + 0.4 * recovery_score)

        reasoning = (
            f"Distance from high {dist:.1%}, recovery days {recovery}; "
            f"rhythm score {score:.2f}"
        )
        return SignalScore(
            signal_name="position_rhythm",
            score=score,
            weight=0.20,
            reasoning=reasoning,
        )


# =========================================================================
# CTA signal engine
# =========================================================================

class CTASignals(BaseSignalEngine):
    """Signal engine for CTA / managed futures strategies.

    Signals (5):
        1. fund_quality       (w=0.25) -- intrinsic performance & risk metrics
        2. trend_strength     (w=0.25) -- cross-asset trend environment
        3. volatility_regime  (w=0.20) -- vol environment suitability
        4. drawdown_pattern   (w=0.20) -- drawdown depth & recovery behaviour
        5. redemption_timing  (w=0.10) -- tactical redemption window awareness
    """

    def compute_signals(
        self,
        snapshot: FundSnapshot,
        holding: Optional[HoldingSnapshot],
        regime: Optional[MarketRegime],
    ) -> list[SignalScore]:
        signals: list[SignalScore] = []

        signals.append(_fund_quality_score(snapshot))
        signals.append(self._trend_strength(snapshot, regime))
        signals.append(self._volatility_regime(snapshot, regime))
        signals.append(self._drawdown_pattern(snapshot))
        signals.append(_redemption_timing_score(snapshot))

        return signals

    @staticmethod
    def _trend_strength(
        snapshot: FundSnapshot,
        regime: Optional[MarketRegime],
    ) -> SignalScore:
        """Cross-asset trend environment favourability for CTAs.

        CTAs profit from persistent trends. High score when:
            - Macro trend strength is high.
            - Growth trend is clearly directional (accelerating or decelerating).
            - The fund itself shows positive recent momentum.
        """
        if regime is None:
            proxy = _clamp(0.5 + snapshot.recent_3m_return * 3)
            return SignalScore(
                signal_name="trend_strength",
                score=proxy,
                weight=0.25,
                reasoning=(
                    f"No regime data; using 3M return ({snapshot.recent_3m_return:.1%}) "
                    "as proxy for trend environment."
                ),
            )

        # CTAs benefit from clear trends in either direction
        directional_bonus = {
            "accelerating": 0.8,
            "decelerating": 0.7,  # also good for CTAs (short positioning)
            "stable": 0.3,        # range-bound is worst for trend followers
        }
        dir_score = directional_bonus.get(regime.growth_trend, 0.5)
        clarity = regime.trend_strength

        score = _clamp(0.5 * clarity + 0.5 * dir_score)

        reasoning = (
            f"Trend clarity {clarity:.2f}, growth direction {regime.growth_trend}; "
            f"CTA trend environment score {score:.2f}"
        )
        return SignalScore(
            signal_name="trend_strength",
            score=score,
            weight=0.25,
            reasoning=reasoning,
        )

    @staticmethod
    def _volatility_regime(
        snapshot: FundSnapshot,
        regime: Optional[MarketRegime],
    ) -> SignalScore:
        """Volatility environment suitability for CTAs.

        Moderate-to-high volatility is generally favourable for trend-following.
        Very low vol often means markets are range-bound, reducing CTA opportunity.
        Extremely high vol can cause whipsaws and drawdowns.
        """
        if regime is None:
            # Fallback: use the fund's own volatility as a proxy
            vol = snapshot.volatility
            if 0.08 <= vol <= 0.25:
                score = 0.7
                reasoning = f"Fund vol {vol:.1%} in moderate range; likely ok for CTA."
            elif vol < 0.08:
                score = 0.4
                reasoning = f"Fund vol {vol:.1%} is low; may indicate suppressed trends."
            else:
                score = 0.5
                reasoning = f"Fund vol {vol:.1%} is elevated; whipsaw risk."
            return SignalScore(
                signal_name="volatility_regime",
                score=_clamp(score),
                weight=0.20,
                reasoning=reasoning,
            )

        vol_map = {"low": 0.3, "moderate": 0.8, "high": 0.5}
        score = vol_map.get(regime.volatility_regime, 0.5)
        reasoning = (
            f"Market vol regime: {regime.volatility_regime}; "
            f"CTA vol suitability score {score:.2f}"
        )
        return SignalScore(
            signal_name="volatility_regime",
            score=_clamp(score),
            weight=0.20,
            reasoning=reasoning,
        )

    @staticmethod
    def _drawdown_pattern(snapshot: FundSnapshot) -> SignalScore:
        """Evaluate drawdown depth and recovery behaviour.

        CTAs can have sharp but short drawdowns. The key question:
        is the current drawdown within the fund's historical pattern,
        and is recovery progressing?

        High score: shallow drawdown or recovering quickly.
        Low score: drawdown is deep and stalling.
        """
        dd = abs(snapshot.current_drawdown)
        max_dd = abs(snapshot.max_drawdown)
        recovery = snapshot.drawdown_recovery_days

        # Is current DD within historical norms?
        if max_dd > 0:
            dd_ratio = dd / max_dd  # how much of max DD is being used
        else:
            dd_ratio = 0.0

        dd_score = _clamp(1.0 - dd_ratio)
        recovery_score = _clamp(1.0 - recovery / 120)

        score = _clamp(0.6 * dd_score + 0.4 * recovery_score)

        reasoning = (
            f"Current DD {snapshot.current_drawdown:.1%} vs max DD "
            f"{snapshot.max_drawdown:.1%} (ratio {dd_ratio:.0%}), "
            f"recovery {recovery}d; pattern score {score:.2f}"
        )
        return SignalScore(
            signal_name="drawdown_pattern",
            score=score,
            weight=0.20,
            reasoning=reasoning,
        )


# =========================================================================
# Quant signal engine
# =========================================================================

class QuantSignals(BaseSignalEngine):
    """Signal engine for quant / market-neutral / stat-arb strategies.

    Signals (5):
        1. fund_quality       (w=0.25) -- intrinsic performance & risk metrics
        2. alpha_decay        (w=0.25) -- excess return trend (is alpha fading?)
        3. market_breadth     (w=0.20) -- market breadth favourability
        4. factor_environment (w=0.20) -- factor regime suitability
        5. redemption_timing  (w=0.10) -- tactical redemption window awareness
    """

    def compute_signals(
        self,
        snapshot: FundSnapshot,
        holding: Optional[HoldingSnapshot],
        regime: Optional[MarketRegime],
    ) -> list[SignalScore]:
        signals: list[SignalScore] = []

        signals.append(_fund_quality_score(snapshot))
        signals.append(self._alpha_decay(snapshot))
        signals.append(self._market_breadth(regime))
        signals.append(self._factor_environment(snapshot, regime))
        signals.append(_redemption_timing_score(snapshot))

        return signals

    @staticmethod
    def _alpha_decay(snapshot: FundSnapshot) -> SignalScore:
        """Assess whether the fund's excess returns are decaying over time.

        Compares recent 1M and 3M returns against the annualised return.
        If recent returns are significantly below the historical average,
        alpha may be decaying.

        High score: recent returns in line with or above historical average.
        Low score: recent returns sharply below historical pace.
        """
        ann = snapshot.annualized_return
        recent_1m_ann = snapshot.recent_1m_return * 12  # rough annualisation
        recent_3m_ann = snapshot.recent_3m_return * 4

        if ann == 0:
            ratio = 1.0
        else:
            # Average of the two annualised recent returns vs historical
            recent_avg = (recent_1m_ann + recent_3m_ann) / 2
            ratio = recent_avg / ann if ann != 0 else 1.0

        # ratio > 1 means recent is beating historical -> good
        # ratio < 0.5 means serious decay
        score = _clamp(0.3 + 0.7 * min(ratio, 1.5) / 1.5)

        reasoning = (
            f"Annualised return {ann:.1%}, recent 1M ann. {recent_1m_ann:.1%}, "
            f"recent 3M ann. {recent_3m_ann:.1%}; "
            f"alpha decay score {score:.2f}"
        )
        return SignalScore(
            signal_name="alpha_decay",
            score=score,
            weight=0.25,
            reasoning=reasoning,
        )

    @staticmethod
    def _market_breadth(regime: Optional[MarketRegime]) -> SignalScore:
        """Market breadth favourability for quant strategies.

        Quant strategies (especially stat-arb) tend to perform well when
        market breadth is wide and cross-sectional dispersion is high.
        They struggle when a few names drive the entire market.

        Without regime data, defaults to neutral.
        """
        if regime is None:
            return SignalScore(
                signal_name="market_breadth",
                score=0.5,
                weight=0.20,
                reasoning="No regime data; defaulting to neutral market breadth.",
            )

        # Use volatility regime as a rough proxy for cross-sectional dispersion
        # Higher vol -> more dispersion -> better for quant
        vol_map = {"low": 0.4, "moderate": 0.7, "high": 0.6}
        base_score = vol_map.get(regime.volatility_regime, 0.5)

        # Stable growth is worst for dispersion; extremes create opportunities
        growth_map = {
            "accelerating": 0.6,
            "stable": 0.4,
            "decelerating": 0.7,
        }
        growth_adj = growth_map.get(regime.growth_trend, 0.5)

        score = _clamp(0.5 * base_score + 0.5 * growth_adj)

        reasoning = (
            f"Vol regime {regime.volatility_regime}, growth {regime.growth_trend}; "
            f"breadth score {score:.2f}"
        )
        return SignalScore(
            signal_name="market_breadth",
            score=score,
            weight=0.20,
            reasoning=reasoning,
        )

    @staticmethod
    def _factor_environment(
        snapshot: FundSnapshot,
        regime: Optional[MarketRegime],
    ) -> SignalScore:
        """Factor regime suitability for quant strategies.

        Evaluates whether the current macro environment supports common
        systematic factors (value, momentum, quality).

        In absence of regime data, uses the fund's own return pattern
        as a proxy for factor environment health.
        """
        if regime is None:
            # Positive recent returns + low volatility = likely healthy factor env
            vol_ok = 1.0 if snapshot.volatility < 0.20 else 0.5
            ret_ok = _clamp(0.5 + snapshot.recent_3m_return * 4)
            score = _clamp(0.5 * vol_ok + 0.5 * ret_ok)
            return SignalScore(
                signal_name="factor_environment",
                score=score,
                weight=0.20,
                reasoning=(
                    f"No regime data; proxy from vol {snapshot.volatility:.1%} "
                    f"and 3M ret {snapshot.recent_3m_return:.1%}; score {score:.2f}"
                ),
            )

        # Factor-friendly environment: moderate vol, easing or neutral policy
        policy_map = {"easing": 0.7, "neutral": 0.6, "tightening": 0.4}
        policy_score = policy_map.get(regime.policy_stance, 0.5)

        vol_map = {"low": 0.5, "moderate": 0.8, "high": 0.4}
        vol_score = vol_map.get(regime.volatility_regime, 0.5)

        score = _clamp(0.5 * vol_score + 0.5 * policy_score)

        reasoning = (
            f"Policy {regime.policy_stance}, vol {regime.volatility_regime}; "
            f"factor environment score {score:.2f}"
        )
        return SignalScore(
            signal_name="factor_environment",
            score=score,
            weight=0.20,
            reasoning=reasoning,
        )


# =========================================================================
# Long-Only Equity signal engine
# =========================================================================

class LongOnlySignals(BaseSignalEngine):
    """Signal engine for long-only equity strategies.

    Signals (5):
        1. fund_quality       (w=0.25) -- intrinsic performance & risk metrics
        2. market_valuation   (w=0.25) -- market valuation environment
        3. style_alignment    (w=0.20) -- fund style vs current regime
        4. concentration_risk (w=0.20) -- portfolio concentration assessment
        5. redemption_timing  (w=0.10) -- tactical redemption window awareness
    """

    def compute_signals(
        self,
        snapshot: FundSnapshot,
        holding: Optional[HoldingSnapshot],
        regime: Optional[MarketRegime],
    ) -> list[SignalScore]:
        signals: list[SignalScore] = []

        signals.append(_fund_quality_score(snapshot))
        signals.append(self._market_valuation(snapshot, regime))
        signals.append(self._style_alignment(snapshot, holding, regime))
        signals.append(self._concentration_risk(holding))
        signals.append(_redemption_timing_score(snapshot))

        return signals

    @staticmethod
    def _market_valuation(
        snapshot: FundSnapshot,
        regime: Optional[MarketRegime],
    ) -> SignalScore:
        """Assess the overall market valuation environment.

        For long-only equity, stretched valuations + tightening policy = danger.
        Reasonable valuations + easing policy = opportunity.

        Without regime data, uses the fund's own drawdown / momentum as proxy.
        """
        if regime is None:
            # Proxy: if the fund is near highs with good momentum, market is OK
            dist = snapshot.distance_from_high
            mom = snapshot.recent_3m_return
            score = _clamp(0.5 * (1.0 - dist / 0.10) + 0.5 * (0.5 + mom * 4))
            return SignalScore(
                signal_name="market_valuation",
                score=score,
                weight=0.25,
                reasoning=(
                    f"No regime data; proxy from distance-from-high {dist:.1%} "
                    f"and 3M momentum {mom:.1%}; score {score:.2f}"
                ),
            )

        # Policy direction matters most for equity valuation
        policy_map = {"easing": 0.8, "neutral": 0.5, "tightening": 0.2}
        policy = policy_map.get(regime.policy_stance, 0.5)

        # Growth trend affects earnings outlook
        growth_map = {"accelerating": 0.8, "stable": 0.6, "decelerating": 0.3}
        growth = growth_map.get(regime.growth_trend, 0.5)

        # High inflation is a headwind for equity valuations
        infl_map = {"falling": 0.7, "stable": 0.5, "rising": 0.3}
        inflation = infl_map.get(regime.inflation_trend, 0.5)

        score = _clamp(0.4 * policy + 0.35 * growth + 0.25 * inflation)

        reasoning = (
            f"Policy {regime.policy_stance}, growth {regime.growth_trend}, "
            f"inflation {regime.inflation_trend}; valuation score {score:.2f}"
        )
        return SignalScore(
            signal_name="market_valuation",
            score=score,
            weight=0.25,
            reasoning=reasoning,
        )

    @staticmethod
    def _style_alignment(
        snapshot: FundSnapshot,
        holding: Optional[HoldingSnapshot],
        regime: Optional[MarketRegime],
    ) -> SignalScore:
        """Assess whether the fund's investment style aligns with the regime.

        Growth style + accelerating economy = aligned.
        Value style + decelerating economy with easing policy = aligned.
        Mismatch lowers the score.
        """
        if holding is None or regime is None:
            # Without data, use recent performance as a proxy for alignment
            score = _clamp(0.5 + snapshot.recent_1m_return * 6)
            return SignalScore(
                signal_name="style_alignment",
                score=score,
                weight=0.20,
                reasoning=(
                    "Insufficient data for style-regime alignment; "
                    f"using 1M return ({snapshot.recent_1m_return:.1%}) as proxy; "
                    f"score {score:.2f}"
                ),
            )

        style = holding.style_label.lower()

        # Define alignment matrix
        alignment: float = 0.5  # default neutral
        if style in ("growth", "aggressive_growth"):
            if regime.growth_trend == "accelerating":
                alignment = 0.9
            elif regime.growth_trend == "stable":
                alignment = 0.6
            else:
                alignment = 0.3
        elif style in ("value", "deep_value"):
            if regime.growth_trend == "decelerating" and regime.policy_stance == "easing":
                alignment = 0.8
            elif regime.growth_trend == "stable":
                alignment = 0.6
            else:
                alignment = 0.4
        elif style == "balanced":
            alignment = 0.6  # balanced style is moderate in all regimes

        score = _clamp(alignment)
        reasoning = (
            f"Style '{style}' vs growth={regime.growth_trend}, "
            f"policy={regime.policy_stance}; alignment score {score:.2f}"
        )
        return SignalScore(
            signal_name="style_alignment",
            score=score,
            weight=0.20,
            reasoning=reasoning,
        )

    @staticmethod
    def _concentration_risk(holding: Optional[HoldingSnapshot]) -> SignalScore:
        """Portfolio concentration assessment for long-only equity.

        Long-only funds with extreme concentration carry higher idiosyncratic
        risk. Moderate concentration (25-45%) is ideal for conviction-driven
        managers. Over 60% is a red flag.
        """
        if holding is None:
            return SignalScore(
                signal_name="concentration_risk",
                score=0.5,
                weight=0.20,
                reasoning="No holding data; defaulting to neutral concentration risk.",
            )

        conc = holding.total_concentration
        if 0.25 <= conc <= 0.45:
            score = 0.8
            label = "healthy range"
        elif conc < 0.25:
            score = 0.6
            label = "low conviction / closet indexing risk"
        elif conc <= 0.60:
            score = 0.5
            label = "moderately concentrated"
        else:
            score = 0.25
            label = "highly concentrated, elevated idiosyncratic risk"

        n_holdings = len(holding.top_holdings)
        reasoning = (
            f"Top-{n_holdings} concentration {conc:.0%} ({label}); "
            f"score {score:.2f}"
        )
        return SignalScore(
            signal_name="concentration_risk",
            score=_clamp(score),
            weight=0.20,
            reasoning=reasoning,
        )


# =========================================================================
# Factory
# =========================================================================

_ENGINE_MAP: dict[str, type[BaseSignalEngine]] = {
    "macro": MacroHedgeSignals,
    "cta": CTASignals,
    "quant": QuantSignals,
    "long_only": LongOnlySignals,
}


def get_signal_engine(strategy_type: str) -> BaseSignalEngine:
    """Return the appropriate signal engine for the given strategy type.

    Args:
        strategy_type: One of 'macro', 'cta', 'quant', 'long_only'.

    Returns:
        An instance of the matching signal engine.

    Raises:
        ValueError: If strategy_type is not recognised.
    """
    engine_cls = _ENGINE_MAP.get(strategy_type)
    if engine_cls is None:
        valid = ", ".join(sorted(_ENGINE_MAP.keys()))
        raise ValueError(
            f"Unknown strategy type '{strategy_type}'. Valid types: {valid}"
        )
    return engine_cls()
