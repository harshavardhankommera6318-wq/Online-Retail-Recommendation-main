import os
import numpy as np
import pandas as pd

np.random.seed(42)

products = {
    "Electronics": ["Headphones", "Laptop", "Mouse", "Keyboard",
                    "Smartphone", "Smartwatch"],
    "Fashion": ["T-Shirt", "Jeans", "Shoes", "Jacket", "Watch"],
    "Home": ["Table", "Chair", "Lamp", "Bedsheet", "Pillow"],
    "Books": ["Python Programming", "AI Basics", "Data Science",
              "Machine Learning", "Web Development"],
    "Beauty": ["Face Wash", "Shampoo", "Perfume", "Moisturizer"]
}

prices = {
    product: np.random.randint(100, 5000)
    for category in products.values()
    for product in category
}

rows = []

for transaction in range(1, 1801):
    customer = f"CUST{np.random.randint(1, 251):03d}"
    category = np.random.choice(list(products.keys()))
    product = np.random.choice(products[category])
    quantity = np.random.randint(1, 5)
    price = prices[product]

    rows.append({
        "transaction_id": f"TRX{transaction:04d}",
        "customer_id": customer,
        "product_name": product,
        "category": category,
        "subcategory": category,
        "quantity": quantity,
        "unit_price": price,
        "total_amount": quantity * price,
        "purchase_month": np.random.choice([
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ])
    })

df = pd.DataFrame(rows)

os.makedirs("data", exist_ok=True)
df.to_csv("data/retail_transactions.csv", index=False)

print("Dataset generated successfully!")
print("Total transactions:", len(df))
print(df.head())