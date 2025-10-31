"""Utility functions for common digital business analytics metrics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


class MetricComputationError(ValueError):
    """Raised when a metric cannot be computed due to invalid inputs."""


@dataclass(frozen=True)
class FunnelStep:
    """Represents a step in a conversion funnel.

    Attributes
    ----------
    name:
        Human readable name for the step.
    visitors:
        The number of visitors or events recorded for this step.
    """

    name: str
    visitors: int

    def __post_init__(self) -> None:
        if self.visitors < 0:
            raise MetricComputationError("Visitors in a funnel step cannot be negative.")


def _ensure_positive(value: float, *, allow_zero: bool = False) -> None:
    if value < 0 or (not allow_zero and value == 0):
        raise MetricComputationError("Expected a positive numeric value.")


def conversion_rate(conversions: float, visitors: float) -> float:
    """Return the conversion rate as a floating point ratio.

    Parameters
    ----------
    conversions:
        Total number of successful conversions.
    visitors:
        Total number of visitors or sessions.
    """

    _ensure_positive(conversions, allow_zero=True)
    _ensure_positive(visitors)

    if conversions > visitors:
        raise MetricComputationError(
            "Conversions cannot exceed visitors when computing a conversion rate."
        )
    return conversions / visitors


def customer_acquisition_cost(marketing_spend: float, new_customers: float) -> float:
    """Return the average cost to acquire a single customer."""

    _ensure_positive(marketing_spend, allow_zero=True)
    _ensure_positive(new_customers)
    return marketing_spend / new_customers


def return_on_ad_spend(revenue: float, ad_spend: float) -> float:
    """Compute Return On Ad Spend (ROAS)."""

    _ensure_positive(revenue, allow_zero=True)
    _ensure_positive(ad_spend)
    return revenue / ad_spend


def engagement_rate(interactions: float, audience_size: float) -> float:
    """Compute engagement rate for a social media post or campaign."""

    _ensure_positive(interactions, allow_zero=True)
    _ensure_positive(audience_size)
    return interactions / audience_size


def funnel_drop_off(funnel: Sequence[FunnelStep]) -> list[tuple[str, float]]:
    """Return percentage drop-off between consecutive funnel steps.

    The returned list contains tuples of ``(step_name, drop_off)`` representing
    the drop from the previous step to the current one. The first step always
    reports a drop-off of ``0.0``.
    """

    if not funnel:
        raise MetricComputationError("Funnel must contain at least one step.")

    drops: list[tuple[str, float]] = []
    previous_visitors: float | None = None

    for step in funnel:
        if previous_visitors is None:
            drops.append((step.name, 0.0))
            previous_visitors = step.visitors
            continue

        if previous_visitors == 0:
            raise MetricComputationError("Encountered zero visitors in previous funnel step.")

        drop_off = 1 - (step.visitors / previous_visitors)
        if drop_off < 0:
            raise MetricComputationError(
                "Visitors increased between funnel steps; check the input ordering."
            )
        drops.append((step.name, drop_off))
        previous_visitors = step.visitors

    return drops


def weighted_average(values: Iterable[float], weights: Iterable[float]) -> float:
    """Compute a weighted average with explicit error checking."""

    values_list = list(values)
    weights_list = list(weights)

    if not values_list or not weights_list:
        raise MetricComputationError("Values and weights must not be empty.")
    if len(values_list) != len(weights_list):
        raise MetricComputationError("Values and weights must be the same length.")

    for weight in weights_list:
        _ensure_positive(weight)

    total_weight = sum(weights_list)
    if total_weight == 0:
        raise MetricComputationError("Total weight cannot be zero.")

    weighted_sum = sum(value * weight for value, weight in zip(values_list, weights_list))
    return weighted_sum / total_weight
