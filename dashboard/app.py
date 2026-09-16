import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# LOAD DATA
# =========================================================

from dashboard_data import (
    orders_dashboard,
    customer_summary,
    category_summary,
    seller_summary,
    orders,
    order_items,
    products,
    reviews
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# =========================================================
# PROFESSIONAL DASHBOARD STYLE
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #171923;
        border-right: 1px solid #2a2d38;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #f1f3f5;
    }

    /* KPI metric cards */
    div[data-testid="stMetric"] {
        background-color: #171923;
        border: 1px solid #2a2d38;
        border-radius: 12px;
        padding: 16px;
        min-height: 110px;
    }

    div[data-testid="stMetricLabel"] {
        color: #9ca3af;
        font-size: 0.85rem;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 700;
    }

    /* Headers */
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        font-weight: 600;
    }

    /* Horizontal line */
    hr {
        border-color: #2a2d38;
    }

    /* Info boxes */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #0e1117;
        border-color: #2a2d38;
    }

</style>
""",unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_number(value):

    if pd.isna(value):
        return "N/A"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_currency(value):

    if pd.isna(value):
        return "N/A"

    if abs(value) >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"R$ {value / 1_000:.1f}K"

    return f"R$ {value:,.0f}"


# =========================================================
# PREPARE ITEM + PRODUCT DATA
# =========================================================

item_data = order_items.merge(
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

item_data["product_category_name"] = (
    item_data["product_category_name"]
    .fillna("Unknown")
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛒 OLIST")
st.sidebar.caption("E-Commerce Analytics")
st.sidebar.markdown("---")

st.sidebar.caption(
    "Data: Brazilian E-Commerce Public Dataset by Olist"
)

st.sidebar.caption(
    "Built with Python • Pandas • Plotly • Streamlit"
)
page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Overview",
        "📈 Sales",
        "👥 Customers",
        "🛍️ Products",
        "🏪 Sellers",
        "🚚 Delivery & Reviews",
        "💡 Business Insights"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("🔎 Filters")


# =========================================================
# FILTER OPTIONS
# =========================================================

years = sorted(
    orders_dashboard["year"]
    .dropna()
    .unique()
)

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + list(years)
)


states = sorted(
    orders_dashboard["customer_state"]
    .dropna()
    .unique()
)

selected_state = st.sidebar.selectbox(
    "Customer State",
    ["All"] + list(states)
)


categories = sorted(
    item_data["product_category_name"]
    .dropna()
    .unique()
)

selected_category = st.sidebar.selectbox(
    "Product Category",
    ["All"] + list(categories)
)


# =========================================================
# BASE ORDER FILTER
# =========================================================

filtered_orders = orders_dashboard.copy()


if selected_year != "All":

    filtered_orders = filtered_orders[
        filtered_orders["year"] == selected_year
    ]


if selected_state != "All":

    filtered_orders = filtered_orders[
        filtered_orders["customer_state"] == selected_state
    ]


# =========================================================
# FILTER ITEMS USING FILTERED ORDERS
# =========================================================

filtered_items = item_data[
    item_data["order_id"].isin(
        filtered_orders["order_id"]
    )
].copy()


# =========================================================
# PRODUCT CATEGORY FILTER
# =========================================================

if selected_category != "All":

    filtered_items = filtered_items[
        filtered_items["product_category_name"]
        == selected_category
    ]


# =========================================================
# GET FINAL ORDER IDS
# =========================================================

if selected_category != "All":

    category_order_ids = filtered_items[
        "order_id"
    ].unique()

    filtered_orders = filtered_orders[
        filtered_orders["order_id"].isin(
            category_order_ids
        )
    ]

# =========================================================
# ACTIVE FILTER SUMMARY
# =========================================================

filter_parts = []

if selected_year != "All":
    filter_parts.append(f"Year: **{selected_year}**")

if selected_state != "All":
    filter_parts.append(f"State: **{selected_state}**")

if selected_category != "All":
    filter_parts.append(
        f"Category: **{selected_category}**"
    )

if filter_parts:

    st.info(
        "🔎 **Active Filters:** "
        + "  •  ".join(filter_parts)
    )

else:

    st.info(
        "🔎 **Showing:** All Years • All States • All Categories"
    )


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_orders = filtered_orders[
    "order_id"
].nunique()


# Sales value comes from filtered items
sales_value = filtered_items[
    "item_revenue"
].sum()


customers_count = filtered_orders[
    "customer_unique_id"
].nunique()


aov = (
    sales_value / total_orders
    if total_orders > 0
    else 0
)


avg_review = filtered_orders[
    "review_score"
].mean()


delivered = filtered_orders[
    filtered_orders[
        "order_delivered_customer_date"
    ].notna()
]


late_rate = (
    (
        delivered[
            "delivery_delay_days"
        ] > 0
    ).mean() * 100
    if len(delivered) > 0
    else 0
)


avg_delivery = (
    delivered[
        "delivery_days"
    ].mean()
    if len(delivered) > 0
    else 0
)


# =========================================================
# HEADER
# =========================================================

st.title("🛒 Olist E-Commerce Analytics")

st.markdown(
    """
    **Brazilian E-Commerce Marketplace Performance**

    Sales • Customers • Products • Sellers • Delivery • Satisfaction
    """
)

st.markdown("---")


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.metric(
        "Orders",
        format_number(total_orders)
    )


with col2:

    st.metric(
        "Sales Value",
        format_currency(sales_value)
    )


with col3:

    st.metric(
        "Unique Customers",
        format_number(customers_count)
    )


with col4:

    st.metric(
        "AOV",
        format_currency(aov)
    )


with col5:

    st.metric(
        "Avg Review Score",
        (
            f"{avg_review:.2f}"
            if not pd.isna(avg_review)
            else "N/A"
        )
    )


with col6:

    st.metric(
        "Late Delivery Rate",
        f"{late_rate:.1f}%"
    )


# =========================================================
# OVERVIEW
# =========================================================

if page == "📊 Overview":

    st.header("📊 Business Overview")

    # -----------------------------------------------------
    # MONTHLY SALES
    # -----------------------------------------------------

    monthly_filtered = (
        filtered_orders
        .groupby("year_month")
        .agg(
            orders=("order_id", "nunique")
        )
        .reset_index()
    )
   

    # Calculate monthly sales from filtered items
    monthly_sales = (
        filtered_items
        .groupby(
            filtered_items["order_id"]
            .map(
                filtered_orders.set_index(
                    "order_id"
                )["year_month"]
            )
        )
        .agg(
            sales_value=("item_revenue", "sum")
        )
        .reset_index()
        .rename(
            columns={
                "order_id": "year_month"
            }
        )
    )


    monthly_filtered = monthly_filtered.merge(
        monthly_sales,
        on="year_month",
        how="left"
    )

    monthly_filtered["sales_value"] = (
        monthly_filtered["sales_value"]
        .fillna(0)
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.line(
            monthly_filtered,
            x="year_month",
            y="sales_value",
            markers=True,
            title="Monthly Sales Value"
        )
        fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales Value (R$)",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.line(
            monthly_filtered,
            x="year_month",
            y="orders",
            markers=True,
            title="Monthly Orders"
        )
        fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Orders",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # =========================================================
    # REVENUE GROWTH
    # =========================================================

    monthly_sales["revenue_growth"] = (
        monthly_sales["sales_value"]
        .pct_change()
        * 100
    )
    fig = px.line(
    monthly_sales,
    x="year_month",
    y="revenue_growth",
    markers=True,
    title="Monthly Sales Growth"
    )

    fig.update_layout(
        template="plotly_dark",
        height=360,
        xaxis_title="Month",
        yaxis_title="Growth (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -----------------------------------------------------
    # CATEGORY + REVIEWS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    category_title = (
        f"Sales Value — {selected_category}"
        if selected_category != "All"
        else "Top 10 Categories by Sales Value"
    )
    with col1:

        category_chart = (
            filtered_items
            .groupby(
                "product_category_name"
            )
            .agg(
                sales_value=(
                    "item_revenue",
                    "sum"
                )
            )
            .reset_index()
            .sort_values(
                "sales_value",
                ascending=False
            )
            .head(10)
        )

        category_chart = (
            category_chart
            .sort_values("sales_value")
        )


        fig = px.bar(
            category_chart,
            x="sales_value",
            y="product_category_name",
            orientation="h",
            title=category_title
        )
        fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
        )

        fig.update_layout(
            xaxis_title="Sales Value (R$)",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        review_dist = (
            reviews[
                reviews["order_id"].isin(
                    filtered_orders["order_id"]
            )
        ]
        .groupby("review_score")
        .size()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
        .reset_index(name="reviews")
        )

        review_dist["review_score"] = (
            review_dist["review_score"].astype(int)
        )

        fig = px.bar(
            review_dist,
            x="review_score",
            y="reviews",
            text="reviews",
            title="Customer Review Distribution"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            template="plotly_dark",
            height=360,
            xaxis=dict(
                tickmode="linear",
                dtick=1,
                range=[0.5, 5.5],
                title="Review Score"
            ),
            yaxis_title="Number of Reviews",
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=40
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -----------------------------------------------------
    # DELIVERY
    # -----------------------------------------------------

    delivery_dist = (
        delivered
        .groupby("delivery_status")
        .size()
        .reindex(
            ["Early", "On Time", "Late"],
            fill_value=0
        )
        .reset_index(name="orders")
    )

    total_delivery_orders = delivery_dist["orders"].sum()

    delivery_dist["percentage"] = (
        delivery_dist["orders"]
        / total_delivery_orders
        * 100
    )

    fig = px.bar(
        delivery_dist,
        x="delivery_status",
        y="orders",
        text=delivery_dist["percentage"].map(
            lambda x: f"{x:.1f}%"
        ),
        title="Delivery Performance"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        height=330,
        xaxis_title="Delivery Status",
        yaxis_title="Orders",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# SALES
# =========================================================

elif page == "📈 Sales":

    st.header("📈 Sales Analysis")


    monthly_sales = (
        filtered_items
        .groupby(
            filtered_items["order_id"]
            .map(
                filtered_orders.set_index(
                    "order_id"
                )["year_month"]
            )
        )
        .agg(
            sales_value=(
                "item_revenue",
                "sum"
            )
        )
        .reset_index()
        .rename(
            columns={
                "order_id": "year_month"
            }
        )
    )


    monthly_orders = (
        filtered_orders
        .groupby("year_month")
        .agg(
            orders=("order_id", "nunique"),
            aov=("order_revenue", "mean")
        )
        .reset_index()
    )


    monthly_sales = monthly_sales.merge(
        monthly_orders[
            [
                "year_month",
                "orders"
            ]
        ],
        on="year_month",
        how="left"
    )


    monthly_sales["aov"] = (
        monthly_sales["sales_value"]
        / monthly_sales["orders"]
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.line(
            monthly_sales,
            x="year_month",
            y="sales_value",
            markers=True,
            title="Monthly Sales Value"
        )
        fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.line(
            monthly_sales,
            x="year_month",
            y="aov",
            markers=True,
            title="Monthly AOV"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    category_sales = (
        filtered_items
        .groupby("product_category_name")
        .agg(
            sales_value=(
                "item_revenue",
                "sum"
            ),
            quantity=(
                "order_id",
                "count"
            )
        )
        .reset_index()
        .sort_values(
            "sales_value",
            ascending=False
        )
        .head(15)
    )


    fig = px.bar(
        category_sales.sort_values(
            "sales_value"
        ),
        x="sales_value",
        y="product_category_name",
        orientation="h",
        title="Top 15 Categories by Sales Value"
    )
    fig.update_layout(
    template="plotly_dark",
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=40
    )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CUSTOMERS
# =========================================================

elif page == "👥 Customers":

    st.header("👥 Customer Analysis")


    filtered_customer_ids = (
        filtered_orders[
            "customer_unique_id"
        ].unique()
    )


    filtered_customers = customer_summary[
        customer_summary[
            "customer_unique_id"
        ].isin(
            filtered_customer_ids
        )
    ]


    repeat_customers = (
        filtered_customers[
            "customer_type"
        ]
        == "Repeat Customer"
    ).sum()


    one_time_customers = (
        filtered_customers[
            "customer_type"
        ]
        == "One-Time Customer"
    ).sum()


    avg_customer_value = (
        filtered_customers[
            "revenue"
        ].mean()
    )


    col1, col2, col3 = st.columns(3)


    with col1:
        st.metric(
            "Repeat Customers",
            format_number(
                repeat_customers
            )
        )


    with col2:
        st.metric(
            "One-Time Customers",
            format_number(
                one_time_customers
            )
        )


    with col3:
        st.metric(
            "Avg Customer Value",
            format_currency(
                avg_customer_value
            )
        )


    customer_type = (
        filtered_customers[
            "customer_type"
        ]
        .value_counts()
        .reset_index()
    )


    customer_type.columns = [
        "customer_type",
        "customers"
    ]


    fig = px.pie(
        customer_type,
        names="customer_type",
        values="customers",
        hole=0.45,
        title="Customer Type Distribution"
    )
    fig.update_layout(
    template="plotly_dark",
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=40
    )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# CUSTOMER RETENTION
# =========================================================

    customer_type = (
        filtered_customers["customer_type"]
        .value_counts()
        .reset_index()
    )

    customer_type.columns = [
        "customer_type",
        "customers"
    ]

    customer_type["percentage"] = (
        customer_type["customers"]
        / customer_type["customers"].sum()
        * 100
    )


    customer_revenue_type = (
        filtered_customers
        .groupby("customer_type")
        .agg(
            customers=("customer_unique_id", "nunique"),
            revenue=("revenue", "sum"),
            avg_customer_revenue=("revenue", "mean")
        )
        .reset_index()
    )

    customer_revenue_type

    fig = px.bar(
        customer_revenue_type,
        x="customer_type",
        y="revenue",
        title="Sales Value by Customer Type",
        text="revenue"
    )

    fig.update_layout(
        template="plotly_dark",
        height=360,
        yaxis_title="Sales Value (R$)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )





# =========================================================
# PRODUCTS
# =========================================================

elif page == "🛍️ Products":

    st.header("🛍️ Product Analysis")


    product_summary = (
        filtered_items
        .groupby(
            "product_category_name"
        )
        .agg(
            sales_value=(
                "item_revenue",
                "sum"
            ),
            quantity=(
                "order_id",
                "count"
            ),
            avg_price=(
                "price",
                "mean"
            ),
            avg_freight=(
                "freight_value",
                "mean"
            )
        )
        .reset_index()
    )


    col1, col2 = st.columns(2)


    with col1:

        top_products = (
            product_summary
            .sort_values(
                "sales_value",
                ascending=False
            )
            .head(10)
        )


        fig = px.bar(
            top_products.sort_values(
                "sales_value"
            ),
            x="sales_value",
            y="product_category_name",
            orientation="h",
            title="Top Categories by Sales"
        )
        fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.scatter(
            product_summary,
            x="avg_price",
            y="quantity",
            size="sales_value",
            hover_name="product_category_name",
            title="Category Price vs Quantity"
        )
        fig.update_layout(
        template="plotly_dark",
        height=360,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40
        )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================================
# PRODUCT PERFORMANCE MATRIX
# =========================================================

    product_summary["freight_ratio"] = np.where(
        product_summary["avg_price"] > 0,
        (
            product_summary["avg_freight"]
            / product_summary["avg_price"]
        ) * 100,
        np.nan
    )

    fig = px.scatter(
        product_summary,
        x="quantity",
        y="sales_value",
        size="sales_value",
        hover_name="product_category_name",
        title="Category Volume vs Sales Value"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Quantity Sold",
        yaxis_title="Sales Value (R$)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    freight_top = (
    product_summary
    .dropna(subset=["freight_ratio"])
    .sort_values(
        "freight_ratio",
        ascending=False
    )
    .head(10)
    )
    fig = px.bar(
    freight_top.sort_values("freight_ratio"),
    x="freight_ratio",
    y="product_category_name",
    orientation="h",
    title="Categories with Highest Freight-to-Price Ratio"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        xaxis_title="Freight / Price (%)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# SELLERS
# =========================================================

elif page == "🏪 Sellers":

    st.header("🏪 Seller Analysis")


    seller_filtered = seller_summary.copy()


    top_sellers = (
        seller_filtered
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(15)
    )


    fig = px.bar(
        top_sellers.sort_values(
            "revenue"
        ),
        x="revenue",
        y="seller_id",
        orientation="h",
        title="Top 15 Sellers by Sales Value"
    )
    fig.update_layout(
    template="plotly_dark",
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=40
    )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    fig = px.scatter(
        seller_filtered[
            seller_filtered["orders"] >= 20
        ],
        x="orders",
        y="revenue",
        size="quantity",
        hover_name="seller_id",
        title="Seller Order Volume vs Sales Value"
    )
    fig.update_layout(
    template="plotly_dark",
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=40
    )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# SELLER ADVANCED PERFORMANCE
# =========================================================

    seller_reviews = (
        filtered_orders
        .merge(
            item_data[
                [
                    "order_id",
                    "seller_id"
                ]
            ].drop_duplicates(),
            on="order_id",
            how="inner"
        )
        .groupby("seller_id")
        .agg(
            avg_review_score=(
                "review_score",
                "mean"
            ),
            orders=(
                "order_id",
                "nunique"
            )
        )
        .reset_index()
    )

    seller_delivery = (
    filtered_orders[
        filtered_orders[
            "order_delivered_customer_date"
        ].notna()
    ]
    .merge(
        item_data[
            [
                "order_id",
                "seller_id"
            ]
        ].drop_duplicates(),
        on="order_id",
        how="inner"
    )
    .groupby("seller_id")
    .agg(
        avg_delivery_days=(
            "delivery_days",
            "mean"
        ),
        late_rate=(
            "delivery_delay_days",
            lambda x: (x > 0).mean() * 100
        )
    )
    .reset_index()
    )

    seller_advanced = (
    seller_filtered
    .merge(
        seller_reviews,
        on="seller_id",
        how="left",
        suffixes=("", "_review")
    )
    .merge(
        seller_delivery,
        on="seller_id",
        how="left"
    )
    )
    seller_chart = seller_advanced[
    seller_advanced["orders"] >= 20
    ].copy()

    fig = px.scatter(
    seller_chart,
    x="revenue",
    y="avg_review_score",
    size="orders",
    hover_name="seller_id",
    title="Seller Sales Value vs Customer Satisfaction"
)

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Sales Value (R$)",
        yaxis_title="Average Review Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    fig = px.scatter(
    seller_chart.dropna(
        subset=[
            "orders",
            "late_rate"
        ]
    ),
    x="orders",
    y="late_rate",
    size="revenue",
    hover_name="seller_id",
    title="Seller Order Volume vs Late Delivery Rate"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Orders",
        yaxis_title="Late Delivery Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# DELIVERY & REVIEWS
# =========================================================

elif page == "🚚 Delivery & Reviews":

    st.header(
        "🚚 Delivery & Customer Satisfaction"
    )


    delivery_dist = (
        delivered
        .groupby("delivery_status")
        .size()
        .reset_index(
            name="orders"
        )
    )


    fig = px.bar(
        delivery_dist,
        x="delivery_status",
        y="orders",
        title="Delivery Status"
    )
    fig.update_layout(
    template="plotly_dark",
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=40
    )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )
    early_count = (
    delivered["delivery_status"]
    .eq("Early")
    .sum()
    )

    late_count = (
        delivered["delivery_status"]
        .eq("Late")
        .sum()
    )

    not_delivered_count = (
        filtered_orders["delivery_status"]
        .eq("Not Delivered")
        .sum()
    )

    early_rate = (
        early_count / len(delivered) * 100
        if len(delivered) > 0
        else 0
    )

    late_rate_value = (
        late_count / len(delivered) * 100
        if len(delivered) > 0
        else 0
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Early Delivery",
            f"{early_rate:.1f}%"
        )

    with col2:
        st.metric(
            "Late Delivery",
            f"{late_rate_value:.1f}%"
        )

    with col3:
        st.metric(
            "Not Delivered",
            format_number(not_delivered_count)
        )


    review_delivery = (
        filtered_orders
        .dropna(
            subset=[
                "review_score",
                "delivery_days"
            ]
        )
        .groupby("review_score")
        .agg(
            avg_delivery_days=(
                "delivery_days",
                "mean"
            ),
            orders=(
                "order_id",
                "nunique"
            )
        )
        .reset_index()
    )


    fig = px.bar(
        review_delivery,
        x="review_score",
        y="avg_delivery_days",
        title="Average Delivery Time vs Review Score"
    )


    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=1,
            range=[0.5, 5.5]
        ),
        yaxis_title="Average Delivery Days"
    )
    fig.update_layout(
    template="plotly_dark",
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=40
    )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# STATE DELIVERY PERFORMANCE
# =========================================================

    state_delivery = (
        filtered_orders[
            filtered_orders[
                "order_delivered_customer_date"
            ].notna()
        ]
        .groupby("customer_state")
        .agg(
            orders=("order_id", "nunique"),
            avg_delivery_days=(
                "delivery_days",
                "mean"
            ),
            late_rate=(
                "delivery_delay_days",
                lambda x: (x > 0).mean() * 100
            )
        )
        .reset_index()
    )
    state_delivery = state_delivery[
    state_delivery["orders"] >= 100
    ]
    state_delivery_chart = (
    state_delivery
    .sort_values(
        "late_rate",
        ascending=False
    )
    .head(15)
    )

    fig = px.bar(
        state_delivery_chart.sort_values(
            "late_rate"
        ),
        x="late_rate",
        y="customer_state",
        orientation="h",
        title="States with Highest Late Delivery Rate"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Late Delivery Rate (%)",
        yaxis_title="State"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    delivery_review = (
        filtered_orders
        .dropna(
            subset=[
                "review_score",
                "delivery_delay_days"
            ]
        )
        .groupby("review_score")
        .agg(
            avg_delay_days=(
                "delivery_delay_days",
                "mean"
            ),
            avg_delivery_days=(
                "delivery_days",
                "mean"
            ),
            orders=(
                "order_id",
                "nunique"
            )
        )
        .reset_index()
    )
    fig = px.bar(
    delivery_review,
    x="review_score",
    y="avg_delay_days",
    title="Average Delivery Delay by Review Score"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis=dict(
            tickmode="linear",
            dtick=1,
            range=[0.5, 5.5]
        ),
        xaxis_title="Review Score",
        yaxis_title="Average Delay (Days)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# BUSINESS INSIGHTS
# =========================================================

elif page == "💡 Business Insights":

# =========================================================
# DYNAMIC BUSINESS INSIGHTS
# =========================================================

    st.header("💡 Business Insights")

    st.markdown(
        "Automatically generated observations from the "
        "current dashboard selection."
    )

    st.markdown("---")


    st.subheader("📊 Current Filtered Performance")


    col1, col2 = st.columns(2)


    with col1:

        st.info(
            f"**{format_number(total_orders)} orders** "
            f"are included in the current selection."
        )


        st.info(
            f"Sales value is "
            f"**{format_currency(sales_value)}**."
        )


    with col2:

        st.info(
            f"Average customer review is "
            f"**{avg_review:.2f}/5**."
        )


        st.info(
            f"Late delivery rate is "
            f"**{late_rate:.1f}%**."
        )


    st.markdown("---")


    if len(delivered) > 0:

        st.subheader(
            "🚚 Delivery Observation"
        )

        st.info(
            f"Average delivery time for the "
            f"current selection is approximately "
            f"**{avg_delivery:.1f} days**."
        )

    st.subheader("📈 Sales")

    st.info(
        f"The current selection contains "
        f"**{format_number(total_orders)} orders** "
        f"with a sales value of "
        f"**{format_currency(sales_value)}**."
    )
    filtered_customer_ids = filtered_orders["customer_unique_id"].dropna().unique()

    filtered_customers = customer_summary[
        customer_summary["customer_unique_id"].isin(filtered_customer_ids)
    ]

    repeat_percentage = (
        filtered_customers["customer_type"]
        .eq("Repeat Customer")
        .mean() * 100
        if not filtered_customers.empty
        else 0
    )


    st.subheader("👥 Customer Behavior")

    st.info(
        f"Repeat customers represent approximately "
        f"**{repeat_percentage:.1f}%** of customers "
        f"in the current selection."
    )

    st.subheader("🚚 Delivery")

    st.info(
        f"Among delivered orders, approximately "
        f"**{late_rate:.1f}%** were delivered "
        f"after the estimated delivery date."
    )
    st.subheader("⭐ Customer Satisfaction")

    st.info(
        f"The average review score in the current "
        f"selection is **{avg_review:.2f}/5**."
    )
    
    state_delivery = (
    filtered_orders[
        filtered_orders["order_delivered_customer_date"].notna()
    ]
    .groupby("customer_state")
    .agg(
        orders=("order_id", "nunique"),
        late_rate=(
            "delivery_delay_days",
            lambda values: (values > 0).mean() * 100
        )
    )
    .reset_index()
    )

    if not state_delivery.empty:
        priority_state = (
            state_delivery
            .sort_values(
                ["orders", "late_rate"],
                ascending=[False, False]
            )
            .iloc[0]
        )

        st.subheader("🎯 Operational Focus")

        st.warning(
            f"**{priority_state['customer_state']}** "
            f"has **{int(priority_state['orders']):,} orders** "
            f"with a late-delivery rate of "
            f"**{priority_state['late_rate']:.1f}%**."
        )

    st.markdown("---")

    st.subheader("📌 Dashboard Summary")

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Average Delivery Time",
            f"{avg_delivery:.1f} days"
            if not pd.isna(avg_delivery)
            else "N/A"
        )

    with summary_col2:

        st.metric(
            "Delivered Orders",
            format_number(len(delivered))
        )

    with summary_col3:

        st.metric(
            "Items Sold",
            format_number(len(filtered_items))
        )
# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Olist E-Commerce Analytics | "
    "Python • Pandas • Plotly • Streamlit"
)