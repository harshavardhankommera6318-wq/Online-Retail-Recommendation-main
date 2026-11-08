import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "product_name",
    "category",
    "subcategory",
    "quantity",
    "unit_price",
    "total_amount",
    "purchase_month"
]


def clean_data(df):
    """Clean and validate retail transaction data."""

    df = df.copy()

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows with missing required values
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # Convert numerical columns
    numeric_columns = [
        "quantity", "unit_price", "total_amount"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df = df.dropna(subset=numeric_columns)

    # Remove invalid transactions
    df = df[
        (df["quantity"] > 0) &
        (df["unit_price"] > 0) &
        (df["total_amount"] > 0)
    ]

    return df.reset_index(drop=True)


def load_data(path="data/retail_transactions.csv"):
    """Load and clean the transaction dataset."""

    df = pd.read_csv(path)
    return clean_data(df)