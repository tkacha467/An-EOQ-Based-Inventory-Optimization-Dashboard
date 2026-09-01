import math
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
            raise ValueError(f"Column '{col}' must contain only numeric values.")
        if (values <= 0).any():
            raise ValueError(f"Column '{col}' must contain only positive values.")


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
    result["Daily_Demand"] = d / 365
    result["Reorder_Point"] = result["Daily_Demand"] * lead

    return result


def calculate_cost_tradeoff(product_row: pd.Series, points: int = 60) -> pd.DataFrame:
    """Return ordering, holding and total cost over quantities around the EOQ."""
    d = float(product_row["Annual_Demand"])
    s = float(product_row["Ordering_Cost"])
    h = float(product_row["Holding_Cost"])
    eoq = math.sqrt((2 * d * s) / h)

    low = max(1, int(eoq * 0.25))
    high = max(low + 1, int(eoq * 2.0))
    quantities = pd.Series(range(low, high + 1, max(1, (high - low) // points)))
    quantities = quantities.drop_duplicates().astype(float)

    tradeoff = pd.DataFrame({"Order_Quantity": quantities})
    tradeoff["Ordering_Cost"] = (d / tradeoff["Order_Quantity"]) * s
    tradeoff["Holding_Cost"] = (tradeoff["Order_Quantity"] / 2) * h
    tradeoff["Total_Cost"] = tradeoff["Ordering_Cost"] + tradeoff["Holding_Cost"]
    tradeoff["Is_EOQ"] = tradeoff["Order_Quantity"].eq(round(eoq))

    # Ensure the exact EOQ is represented even though the chart uses integer quantities.
    eoq_row = pd.DataFrame({
        "Order_Quantity": [eoq],
        "Ordering_Cost": [(d / eoq) * s],
        "Holding_Cost": [(eoq / 2) * h],
        "Total_Cost": [(d / eoq) * s + (eoq / 2) * h],
        "Is_EOQ": [True],
    })
    return pd.concat([tradeoff, eoq_row], ignore_index=True).sort_values("Order_Quantity").reset_index(drop=True)
