#  Olist E-Commerce Analytics Dashboard

An end-to-end **Brazilian e-commerce data analysis and business intelligence project** built using Python, Pandas, Plotly, and Streamlit.

This project analyzes the Brazilian E-Commerce Public Dataset by Olist to understand sales performance, customer behavior, product categories, seller performance, delivery efficiency, and customer satisfaction.

The analysis is transformed into an interactive dashboard that allows users to explore the business data using dynamic filters and visualizations.

---
##  Live Dashboard

**[Open Live Dashboard](https://olist-ecommerce-analytics.onrender.com)**

The dashboard is deployed using Render and built with Streamlit.

##  Project Overview

E-commerce platforms generate large amounts of transactional data across customers, orders, products, sellers, payments, reviews, and delivery.

The goal of this project is to transform raw e-commerce data into meaningful business insights through:

- Data understanding and validation
- Exploratory Data Analysis (EDA)
- Relationship analysis between multiple datasets
- Data cleaning and feature engineering
- Business performance analysis
- Interactive dashboard development

---

##  Business Objectives

The project focuses on answering questions such as:

- How are sales changing over time?
- Which product categories generate the most revenue?
- How do customers behave and how many are repeat customers?
- Which sellers perform strongly?
- How concentrated is seller revenue?
- How does delivery performance affect customer satisfaction?
- What states and regions generate the most demand?
- What is the relationship between product price and quantity?
- Which categories or sellers require attention based on revenue, delivery, or reviews?

---

##  Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains approximately 100,000 orders from the Brazilian e-commerce marketplace and includes information about:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translations

### Dataset Relationships

The major relationships analyzed in the project include:

```text
Customers
    │
    └── Orders
          │
          ├── Order Items ─── Products
          │                 └── Sellers
          │
          ├── Payments
          │
          └── Reviews

Geolocation
    └── ZIP Code Prefix
