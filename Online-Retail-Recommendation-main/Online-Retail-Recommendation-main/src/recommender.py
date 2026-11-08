import pandas as pd


def popular_products(df, top_n=5):
    """Recommend products based on total units purchased."""

    popular = (
        df.groupby("product_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    popular.columns = ["product_name", "units_sold"]

    return popular


def customer_recommendations(df, customer_id, top_n=5):
    """
    Recommend products using item co-occurrence.

    Products frequently purchased by customers who bought
    the selected customer's products are recommended.
    """

    customer_data = df[df["customer_id"] == customer_id]

    if customer_data.empty:
        return popular_products(df, top_n)

    purchased = set(customer_data["product_name"].unique())

    # Build customer-product purchase matrix
    basket = pd.crosstab(
        df["customer_id"],
        df["product_name"]
    )

    # Calculate product co-occurrence
    co_occurrence = basket.T.dot(basket)

    scores = {}

    for product in purchased:
        if product in co_occurrence.columns:
            related = co_occurrence[product]

            for recommended_product, score in related.items():
                if recommended_product not in purchased:
                    scores[recommended_product] = (
                        scores.get(recommended_product, 0) + score
                    )

    if not scores:
        return popular_products(df, top_n)

    result = pd.DataFrame(
        scores.items(),
        columns=["product_name", "recommendation_score"]
    )

    result = result.sort_values(
        "recommendation_score",
        ascending=False
    ).head(top_n)

    return result.reset_index(drop=True)


def category_products(df, category):
    """Return product performance within a category."""

    filtered = df[df["category"] == category]

    return (
        filtered.groupby("product_name")
        .agg(
            units_sold=("quantity", "sum"),
            revenue=("total_amount", "sum")
        )
        .sort_values("revenue", ascending=False)
        .reset_index()
    )