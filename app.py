"""AIValuation Lab v0.1 — editable scenario model using public data."""
from pathlib import Path
import pandas as pd
import streamlit as st
from models.data import validate_financials
from models.export import make_workbook
from models.valuation import Scenario, forecast_scenario, valuation_metrics

st.set_page_config(page_title="AIValuation Lab", page_icon="📊", layout="wide")
st.title("AIValuation Lab")
st.caption("v0.1 · Analyst-controlled financial scenarios · Not investment advice")
with st.expander("Instructions and limitations"):
    st.markdown("""Use the explicitly fictional sample or upload a verified public-financial-facts CSV.
Review revenue, operating income, periods and source URL. Enter enterprise value (not market cap),
edit scenario assumptions, and export an Excel workbook. No automatic SEC ingestion or PDF parsing.
Uploaded facts are **not** independently verified. Never upload confidential documents.""")

sample = Path(__file__).parent / "data" / "fictional_sample.csv"
upload = st.file_uploader("Upload verified public financial facts (CSV)", type="csv")
try:
    raw = pd.read_csv(upload if upload else sample)
except Exception as error:
    st.error(f"CSV could not be read: {error}")
    st.stop()

st.subheader("1. Review source facts")
st.caption("Demo figures are fictional; replace with verified public disclosures.")
edited = st.data_editor(raw, num_rows="fixed", use_container_width=True)
try:
    data = validate_financials(edited)
except (ValueError, TypeError) as error:
    st.error(str(error))
    st.stop()

selected = st.selectbox("Company / period", range(len(data)),
                        format_func=lambda i: f"{data.iloc[i]['company']} — {data.iloc[i]['period']}")
fact = data.iloc[selected]
revenue = float(fact["revenue_usd"])
income = float(fact["operating_income_usd"])
st.write("Evidence link (analyst-supplied):", fact["source_url"])

st.subheader("2. Enterprise value assumption")
ev = st.number_input("Illustrative enterprise value (USD)", min_value=0.0,
                     value=10_000_000_000.0, step=500_000_000.0,
                     help="EV is NOT market cap. Reconcile debt, cash and other EV adjustments.")
metrics = valuation_metrics(revenue, income, ev)
a, b, c = st.columns(3)
a.metric("Revenue", f"${revenue / 1e9:,.2f}B")
b.metric("Operating margin", f"{metrics['operating_margin']:.1%}")
c.metric("EV / revenue", f"{metrics['ev_to_revenue']:.2f}×")

st.subheader("3. One-year scenarios")
st.caption("All scenario assumptions are fictional defaults, not forecasts.")
defaults = [
    Scenario("Stress", .05, -.10, 4),
    Scenario("Base", .25, .10, 8),
    Scenario("Upside", .50, .25, 12),
]
editor_data = pd.DataFrame([{
    "Scenario": s.name, "Growth (%)": s.growth_rate * 100,
    "Operating margin (%)": s.operating_margin * 100,
    "EV / revenue (x)": s.revenue_multiple,
} for s in defaults])
chosen = st.data_editor(editor_data, num_rows="fixed", use_container_width=True)
try:
    scenarios = [Scenario(str(s["Scenario"]), float(s["Growth (%)"]) / 100,
                          float(s["Operating margin (%)"]) / 100,
                          float(s["EV / revenue (x)"])) for _, s in chosen.iterrows()]
    results = pd.DataFrame([forecast_scenario(revenue, s) for s in scenarios])
except (TypeError, ValueError) as error:
    st.error(f"Invalid scenario: {error}")
    st.stop()

st.dataframe(results, use_container_width=True)
st.bar_chart(results.set_index("scenario")[["illustrative_enterprise_value"]])

st.subheader("4. Export workbook")
book = make_workbook(str(fact["company"]), str(fact["period"]), revenue, income,
                     str(fact["source_url"]), ev, scenarios)
st.download_button("Download Excel model", book, "aivaluation_scenarios.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.caption("One-year multiple sensitivity only; not a DCF or investment recommendation.")
