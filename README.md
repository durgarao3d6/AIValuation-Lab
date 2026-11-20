# AIValuation Lab

**v0.1: public-data financial scenario modelling for indie-SaaS validation.** A Streamlit app with deterministic calculations, analyst-supplied evidence links, scenario comparisons, and formula-based Excel export.

> **Not investment advice.** The bundled company is **fictional**. The app does not yet automatically import SEC filings, parse PDFs, verify disclosures, or generate investment recommendations.

## Features
- Import manually verified public financial facts via CSV, or explore the fictional demo.
- Review and edit financial facts, reporting period, and citation URL.
- Calculate operating margin and enterprise value / revenue.
- Adjust one-year stress, base, and upside scenarios.
- Export a four-sheet Excel workbook: Source Facts, Assumptions, Scenarios, Methodology.
- Run automated tests locally and with GitHub Actions.

## Getting started

Python 3.11+:

```bash
git clone https://github.com/durgarao3d6/AIValuation-Lab.git
cd AIValuation-Lab
python -m venv .venv
source .venv/bin/activate # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
python -m pytest -q
```

## CSV schema

```csv
company,period,revenue_usd,operating_income_usd,source_url
Fictional AI Co (DEMO),FY2025,1000000000,-200000000,https://example.com/fictional-demo-not-a-filing
```

Enter **full USD units** (1000000000 for $1B, not 1). Revenue must be positive. Every row must include an HTTPS evidence URL. Values are **not automatically verified**; always check the underlying filings and reporting periods.

For real company facts, start with public [SEC EDGAR XBRL data](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) and verify against the issuer's original disclosures. Be aware that AI-related companies can have different segment mixes and financial definitions.

## Model methodology

- Operating margin = operating income / revenue.
- EV / revenue = analyst-entered enterprise value / reported revenue.
- Projected revenue = reported revenue × (1 + one-year growth assumption).
- Projected operating income = projected revenue × operating margin assumption.
- Illustrative EV = projected revenue × assumed EV / revenue multiple.

**EV is not equity market capitalization.** The analyst must reconcile debt, cash, and other required EV adjustments. The model is *one-year multiple sensitivity*, not a discounted cash flow or price target. Excel recalculates formulas on opening the exported workbook.

## Roadmap

1. **v0.1:** deterministic core, CSV evidence, editable scenario assumptions, workbook export and tests.
2. **v0.2:** public SEC XBRL ingestion with correct period, units and provenance.
3. **v0.3:** optional PDF import with page-level extraction review.
4. **Validation:** recruit 3–5 analysts, measure model preparation time and accuracy, test paid pilot willingness.

## Data and security

No authentication, database, hosted deployment, persistent user storage, or payments. Do not upload confidential or restricted financial documents to a public Streamlit deployment. Respect data access rights and licensing.

## License

MIT — see [LICENSE](LICENSE).
