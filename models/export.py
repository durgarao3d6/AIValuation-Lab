"""Excel model export with source inputs, assumptions, and formulas."""
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

def make_workbook(company, period, revenue, operating_income, source_url, enterprise_value, scenarios):
    wb = Workbook()
    facts = wb.active
    facts.title = "Source Facts"
    facts.append(["Field", "Value", "Evidence / classification"])
    for item in [
        ("Company", company, "Analyst supplied"),
        ("Period", period, "Analyst supplied; match reporting periods"),
        ("Revenue (USD)", revenue, source_url),
        ("Operating income (USD)", operating_income, source_url),
        ("Enterprise value (USD)", enterprise_value, "Analyst assumption, NOT market cap"),
        ("Operating margin", '=IFERROR(B5/B4,"")', "Operating income / revenue"),
        ("EV / revenue", '=IFERROR(B6/B4,"")', "EV / revenue"),
    ]:
        facts.append(item)
    assumptions = wb.create_sheet("Assumptions")
    assumptions.append(["Scenario", "Growth rate", "Operating margin", "EV / revenue multiple"])
    for s in scenarios:
        assumptions.append([s.name, s.growth_rate, s.operating_margin, s.revenue_multiple])
    output = wb.create_sheet("Scenarios")
    output.append(["Scenario", "Projected revenue (USD)", "Projected operating income (USD)", "Illustrative EV (USD)"])
    for row in range(2, len(scenarios) + 2):
        output.append([
            f"=Assumptions!A{row}",
            f"='Source Facts'!$B$4*(1+Assumptions!B{row})",
            f"=B{row}*Assumptions!C{row}",
            f"=B{row}*Assumptions!D{row}",
        ])
    notes = wb.create_sheet("Methodology")
    for line in [
        "AIValuation Lab v0.1 — illustrative one-year scenarios",
        "Source facts are analyst supplied, not automatically verified.",
        "Enterprise value is NOT interchangeable with equity market cap.",
        "Projected EV = projected revenue * scenario EV/revenue multiple.",
        "No DCF, financial advice, guaranteed forecasts or automatic extraction.",
        "Excel or compatible software recalculates formulas when opened.",
    ]:
        notes.append([line])
    for sheet in wb:
        sheet.freeze_panes = "A2"
        for cell in sheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="173A53")
        for col in sheet.columns:
            width = min(90, max(len(str(cell.value or "")) for cell in col) + 3)
            sheet.column_dimensions[get_column_letter(col[0].column)].width = max(18, width)
    facts["B7"].number_format = "0.0%"
    facts["B8"].number_format = '0.00"x"'
    for row in range(2, len(scenarios) + 2):
        assumptions.cell(row, 2).number_format = "0.0%"
        assumptions.cell(row, 3).number_format = "0.0%"
    output_file = BytesIO()
    wb.save(output_file)
    return output_file.getvalue()
