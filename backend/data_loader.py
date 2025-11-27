import pandas as pd
from pathlib import Path
from functools import lru_cache
import logging
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "Walmart_Sales.csv"

@lru_cache(maxsize=1)
def load_raw_data_cached() -> pd.DataFrame:
    logger.info(f"Loading CSV from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    # FIX: Correct datetime parsing
    df["Date"] = pd.to_datetime(df["Date"], format="mixed")

    return df

def load_raw_data(copy: bool = False) -> pd.DataFrame:
    """
    Load raw data from CSV.
    
    Args:
        copy: If True, return a copy. If False, return a view (default).
              Only use copy=True when you need to modify the DataFrame.
    
    Returns:
        DataFrame with the raw data
    """
    if copy:
        return load_raw_data_cached().copy()
    return load_raw_data_cached()

def get_time_series(store_id: int | None = None) -> pd.DataFrame:
    # Need copy since we're modifying (renaming, sorting)
    df = load_raw_data(copy=True)

    if store_id is not None:
        df = df[df["Store"] == store_id]
    else:
        df = df.groupby("Date", as_index=False)["Weekly_Sales"].sum()

    df = df.rename(columns={"Date": "timestamp", "Weekly_Sales": "value"})
    df = df.sort_values("timestamp")

    return df[["timestamp", "value"]]
