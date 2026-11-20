from io import BytesIO
import pandas as pd
import pytest
from openpyxl import load_workbook
from models.data import validate_financials
from models.export import make_workbook
from models.valuation import Scenario

def test_valid_csv():
    frame = pd.DataFrame([{"company":"Demo","period":"FY2025","revenue_usd":1000,
        "operating_income_usd":-100,"source_url":"https://example.com/filing"}])
    assert validate_financials(frame).iloc[0]["revenue_usd"] == 1000

def test_invalid_source_url():
    frame = pd.DataFrame([{"company":"Demo","period":"FY2025","revenue_usd":1000,
        "operating_income_usd":-100,"source_url":"not-a-url"}])
    with pytest.raises(ValueError):
        validate_financials(frame)

def test_export_formulas_and_evidence():
    xlsx = make_workbook("Demo","FY2025",1000,-100,"https://example.com/filing",10000,
                         [Scenario("Base",.25,.1,8)])
    wb = load_workbook(BytesIO(xlsx))
    assert wb.sheetnames == ["Source Facts","Assumptions","Scenarios","Methodology"]
    assert wb["Source Facts"]["C4"].value == "https://example.com/filing"
    assert wb["Source Facts"]["B7"].value == '=IFERROR(B5/B4,"")'
    assert wb["Scenarios"]["B2"].value.startswith("=")
