import pandas as pd
import numpy as np

# LOAD DATA

from pathlib import Path
import kagglehub

# Download/cache Olist dataset
DATA_DIR = Path(
    kagglehub.dataset_download("olistbr/brazilian-ecommerce")
)

customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")
sellers = pd.read_csv(DATA_DIR / "olist_sellers_dataset.csv")


# DATE CONVERSION


data_column = [ "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"]
for columns in data_column:
    orders[columns] = pd.to_datetime(orders[columns],errors="coerce" )


# DELIVERY METRICS


orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400


orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# delivery matrics 

orders["delivery_status"] = np.where(
    orders["order_delivered_customer_date"].isna(),
    "Not Delivered",
    np.where(
        orders["delivery_delay_days"] > 0,
        "Late",
        np.where(
            orders["delivery_delay_days"] < 0,
            "Early",
            "On Time"
        )
    )
)


# ITEM REVENUE


order_items["item_revenue"] = (
    order_items["price"]
    + order_items["freight_value"]
)

# ORDER REVENUE

order_revenue = (
    order_items
    .groupby("order_id")
    .agg(
        order_revenue=("item_revenue", "sum"),
        items=("order_id", "count")
    )
    .reset_index()
)

# print(order_revenue.shape)
# print(order_revenue["order_id"].nunique())


# ORDER + CUSTOMER


orders_dashboard = orders.merge(
    customers[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left",
    validate="one_to_one"
)

print(orders_dashboard.shape)
print(orders_dashboard["order_id"].nunique())

orders_dashboard = orders_dashboard.merge(
    order_revenue,
    on="order_id",
    how="left",
    validate="one_to_one"
)



# REVIEW SUMMARY


review_summary = (
    reviews
    .groupby("order_id")
    .agg(
        review_count=("review_id", "count"),
        review_score=("review_score", "mean")
    )
    .reset_index()
)

orders_dashboard = orders_dashboard.merge(
    review_summary,
    on="order_id",
    how="left",
    validate="one_to_one"
)


# TIME FEATURES


orders_dashboard["year"] = (
    orders_dashboard["order_purchase_timestamp"]
    .dt.year
)

orders_dashboard["month"] = (
    orders_dashboard["order_purchase_timestamp"]
    .dt.month
)

orders_dashboard["year_month"] = (
    orders_dashboard["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)


# CUSTOMER SUMMARY


customer_summary = (
    orders_dashboard
    .groupby("customer_unique_id")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("order_revenue", "sum")
    )
    .reset_index()
)

customer_summary["customer_type"] = np.where(
    customer_summary["orders"] > 1,
    "Repeat Customer",
    "One-Time Customer"
)


# PRODUCT CATEGORY SUMMARY


item_product = order_items.merge(
    products[
        [
            "product_id",
            "product_category_name"
        ]
    ],
    on="product_id",
    how="left",
    validate="many_to_one"
)

category_summary = (
    item_product
    .groupby("product_category_name")
    .agg(
        revenue=("item_revenue", "sum"),
        quantity=("order_id", "count"),
        avg_price=("price", "mean"),
        avg_freight=("freight_value", "mean")
    )
    .reset_index()
)


# SELLER SUMMARY


seller_summary = (
    order_items
    .groupby("seller_id")
    .agg(
        revenue=("item_revenue", "sum"),
        quantity=("order_id", "count"),
        orders=("order_id", "nunique"),
        avg_price=("price", "mean")
    )
    .reset_index()
)

seller_summary = seller_summary.merge(
    sellers[
        [
            "seller_id",
            "seller_city",
            "seller_state"
        ]
    ],
    on="seller_id",
    how="left",
    validate="one_to_one"
)


# MONTHLY SUMMARY


monthly_summary = (
    orders_dashboard
    .groupby("year_month")
    .agg(
        orders=("order_id", "nunique"),
        revenue=("order_revenue", "sum"),
        avg_order_value=("order_revenue", "mean")
    )
    .reset_index()
)


# DATA QUALITY CHECKS


print("Orders:", orders_dashboard.shape)
print("Customers:", customer_summary.shape)
print("Categories:", category_summary.shape)
print("Sellers:", seller_summary.shape)
print("Monthly:", monthly_summary.shape)

print("\nDashboard data pipeline loaded successfully.")
