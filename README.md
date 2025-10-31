# Digital-BA

Utilities for working with common digital business analytics metrics. The
package ships with functions to compute conversion rates, return on ad spend,
customer acquisition cost, engagement rate, and more.

## Getting Started

Install dependencies and run the tests with:

```bash
python -m pip install -e .[test]
pytest
```

Alternatively, since the project uses a ``src`` layout you can execute the
modules directly via ``python -m`` once the repository is on your ``PYTHONPATH``.

## Available Metrics

* ``conversion_rate`` – conversions divided by the number of visitors.
* ``customer_acquisition_cost`` – average spend required per acquired customer.
* ``return_on_ad_spend`` – revenue generated per dollar spent on advertising.
* ``engagement_rate`` – engagement per audience size.
* ``funnel_drop_off`` – percentage drop between steps in a funnel.
* ``weighted_average`` – helper for weighted scoring models.

All metric functions perform input validation and raise
``MetricComputationError`` with descriptive messages when the supplied data is
invalid. See ``tests/test_metrics.py`` for usage examples.
