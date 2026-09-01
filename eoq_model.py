import math
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "Product",
    "Annual_Demand",
    "Ordering_Cost",
    "Holding_Cost",
    "Lead_Time_Days",
]

NUMERIC_COLUMNS = [
    "Annual_Demand",
    "Ordering_Cost",
    "Holding_Cost",
    "Lead_Time_Days",
]


def validate_input_dataframe(df: pd.DataFrame) -> None:
    """Validate the input dataframe required by the EOQ model."""
    if df is None or df.empty:
        raise ValueError("The dataset is empty.")

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    for col in NUMERIC_COLUMNS:
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any():
            raise ValueError(f"Column '{col}' contains non-numeric or missing (NaN) values.")
        if (values <= 0).any():
            raise ValueError(f"Column '{col}' contains zero or negative values. All values must be positive (> 0).")


def calculate_eoq(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate EOQ and related inventory metrics for every product."""
    validate_input_dataframe(df)
    result = df.copy()

    d = pd.to_numeric(result["Annual_Demand"], errors="raise")
    s = pd.to_numeric(result["Ordering_Cost"], errors="raise")
    h = pd.to_numeric(result["Holding_Cost"], errors="raise")
    lead = pd.to_numeric(result["Lead_Time_Days"], errors="raise")

    result["EOQ"] = (2 * d * s / h).pow(0.5)
    result["Number_of_Orders_Per_Year"] = d / result["EOQ"]
    result["Annual_Ordering_Cost"] = (d / result["EOQ"]) * s
    result["Annual_Holding_Cost"] = (result["EOQ"] / 2) * h
    result["Total_Annual_Inventory_Cost"] = (
        result["Annual_Ordering_Cost"] + result["Annual_Holding_Cost"]
    )
    result["Daily_Demand"] = d / 365.0
    result["Reorder_Point"] = result["Daily_Demand"] * lead

    return result


def calculate_cost_tradeoff(
    annual_demand=None,
    ordering_cost=None,
    holding_cost=None,
    product_row=None,
    points: int = 60,
    num_points: int = None
) -> pd.DataFrame:
    """Return ordering, holding and total cost over quantities around the EOQ."""
    if num_points is not None:
        points = num_points

    target = product_row if product_row is not None else annual_demand

    if isinstance(target, (pd.Series, dict)):
        d = float(target["Annual_Demand"])
        s = float(target["Ordering_Cost"])
        h = float(target["Holding_Cost"])
    else:
        d = float(annual_demand)
        s = float(ordering_cost)
        h = float(holding_cost)

    if d <= 0 or s <= 0 or h <= 0:
        raise ValueError("Annual_Demand, Ordering_Cost, and Holding_Cost must be positive (> 0).")

    eoq = math.sqrt((2 * d * s) / h)

    low = max(1.0, eoq * 0.25)
    high = max(low + 1.0, eoq * 2.0)
    
    quantities = np.linspace(low, high, points)

    tradeoff = pd.DataFrame({"Order_Quantity": quantities})
    tradeoff["Annual_Ordering_Cost"] = (d / tradeoff["Order_Quantity"]) * s
    tradeoff["Annual_Holding_Cost"] = (tradeoff["Order_Quantity"] / 2.0) * h
    tradeoff["Total_Annual_Inventory_Cost"] = tradeoff["Annual_Ordering_Cost"] + tradeoff["Annual_Holding_Cost"]
    
    # Also support alias column names for compatibility
    tradeoff["Ordering_Cost"] = tradeoff["Annual_Ordering_Cost"]
    tradeoff["Holding_Cost"] = tradeoff["Annual_Holding_Cost"]
    tradeoff["Total_Cost"] = tradeoff["Total_Annual_Inventory_Cost"]
    tradeoff["Is_EOQ"] = np.isclose(tradeoff["Order_Quantity"], eoq, rtol=1e-2)

    return tradeoff
