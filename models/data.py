"""Validate analyst-supplied financial facts."""
from urllib.parse import urlparse
import pandas as pd

REQUIRED_COLUMNS = ("company", "period", "revenue_usd", "operating_income_usd", "source_url")

def validate_financials(frame: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED_COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("At least one row is required")
    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Required fields cannot be blank")
    clean = frame.copy()
    for col in ("revenue_usd", "operating_income_usd"):
        clean[col] = pd.to_numeric(clean[col], errors="raise")
        if not clean[col].map(lambda x: pd.notna(x) and abs(x) != float("inf")).all():
            raise ValueError(f"{col} must be finite")
    if (clean["revenue_usd"] <= 0).any():
        raise ValueError("Revenue must be positive")
    for col in ("company", "period", "source_url"):
        if not clean[col].map(lambda x: isinstance(x, str) and bool(x.strip())).all():
            raise ValueError(f"{col} must be non-empty text")
    for url in clean["source_url"]:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("source_url must be HTTPS")
    return clean
