"""Deterministic, transparent valuation formulas."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Scenario:
    name: str
    growth_rate: float
    operating_margin: float
    revenue_multiple: float

def finite(value, label):
    if isinstance(value, bool):
        raise ValueError(f"{label} must be finite")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be finite") from exc
    if not isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result

def valuation_metrics(revenue, operating_income, enterprise_value):
    revenue = finite(revenue, "Revenue")
    income = finite(operating_income, "Operating income")
    ev = finite(enterprise_value, "Enterprise value")
    if revenue <= 0 or ev < 0:
        raise ValueError("Revenue must be positive and EV nonnegative")
    return {"operating_margin": income / revenue, "ev_to_revenue": ev / revenue}

def forecast_scenario(revenue, scenario: Scenario):
    revenue = finite(revenue, "Revenue")
    growth = finite(scenario.growth_rate, "Growth rate")
    margin = finite(scenario.operating_margin, "Operating margin")
    multiple = finite(scenario.revenue_multiple, "Revenue multiple")
    if revenue <= 0 or growth < -1 or multiple < 0:
        raise ValueError("Revenue must be positive, growth >= -100%, and multiple >= 0")
    projected = revenue * (1 + growth)
    return {
        "scenario": scenario.name,
        "growth_rate": growth,
        "operating_margin": margin,
        "revenue_multiple": multiple,
        "projected_revenue": projected,
        "projected_operating_income": projected * margin,
        "illustrative_enterprise_value": projected * multiple,
    }
