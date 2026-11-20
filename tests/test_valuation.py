import math
import pytest
from models.valuation import Scenario, forecast_scenario, valuation_metrics

def test_ratios():
    actual = valuation_metrics(1000, -200, 10000)
    assert actual["operating_margin"] == pytest.approx(-.2)
    assert actual["ev_to_revenue"] == pytest.approx(10)

def test_scenario():
    result = forecast_scenario(1000, Scenario("Base", .25, .10, 8))
    assert result["projected_revenue"] == 1250
    assert result["projected_operating_income"] == 125
    assert result["illustrative_enterprise_value"] == 10000

@pytest.mark.parametrize("revenue,income,ev", [(0,0,1),(-1,0,1),(100,0,-1),(math.nan,0,1)])
def test_invalid_values(revenue, income, ev):
    with pytest.raises(ValueError):
        valuation_metrics(revenue, income, ev)

def test_declining_revenue():
    result = forecast_scenario(100, Scenario("Stress", -.5, -.2, 3))
    assert result["projected_revenue"] == 50

def test_excess_decline_rejected():
    with pytest.raises(ValueError):
        forecast_scenario(100, Scenario("Impossible", -1.01, .1, 2))
