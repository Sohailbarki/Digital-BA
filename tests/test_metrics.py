import pytest

from digital_ba.metrics import (
    FunnelStep,
    MetricComputationError,
    conversion_rate,
    customer_acquisition_cost,
    engagement_rate,
    funnel_drop_off,
    return_on_ad_spend,
    weighted_average,
)


def test_conversion_rate_basic():
    assert conversion_rate(25, 100) == pytest.approx(0.25)


def test_conversion_rate_invalid_inputs():
    with pytest.raises(MetricComputationError):
        conversion_rate(-1, 100)
    with pytest.raises(MetricComputationError):
        conversion_rate(10, 0)
    with pytest.raises(MetricComputationError):
        conversion_rate(101, 100)


def test_customer_acquisition_cost():
    assert customer_acquisition_cost(1000, 50) == pytest.approx(20)

    with pytest.raises(MetricComputationError):
        customer_acquisition_cost(100, 0)


def test_return_on_ad_spend():
    assert return_on_ad_spend(5000, 1000) == pytest.approx(5)
    with pytest.raises(MetricComputationError):
        return_on_ad_spend(0, -1)


def test_engagement_rate():
    assert engagement_rate(200, 1000) == pytest.approx(0.2)
    with pytest.raises(MetricComputationError):
        engagement_rate(100, 0)


def test_funnel_drop_off():
    funnel = [
        FunnelStep("Landing Page", 1000),
        FunnelStep("Signup", 400),
        FunnelStep("Onboarding", 200),
    ]

    drops = funnel_drop_off(funnel)
    assert drops == [
        ("Landing Page", pytest.approx(0.0)),
        ("Signup", pytest.approx(0.6)),
        ("Onboarding", pytest.approx(0.5)),
    ]


def test_funnel_drop_off_error_cases():
    with pytest.raises(MetricComputationError):
        funnel_drop_off([])

    funnel = [FunnelStep("Step 1", 100), FunnelStep("Step 2", 120)]
    with pytest.raises(MetricComputationError):
        funnel_drop_off(funnel)


def test_weighted_average():
    values = [70, 80, 90]
    weights = [1, 2, 3]
    assert weighted_average(values, weights) == pytest.approx(83.3333, rel=1e-4)


def test_weighted_average_errors():
    with pytest.raises(MetricComputationError):
        weighted_average([], [])
    with pytest.raises(MetricComputationError):
        weighted_average([1, 2], [1])
    with pytest.raises(MetricComputationError):
        weighted_average([1, 2], [1, 0])

    with pytest.raises(MetricComputationError):
        weighted_average([1, 2], [0.5, 0.5 - 0.5])
