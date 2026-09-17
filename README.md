#  Olist E-Commerce Analytics Dashboard

An end-to-end **Brazilian e-commerce data analysis and business intelligence project** built using Python, Pandas, Plotly, and Streamlit.

This project analyzes the Brazilian E-Commerce Public Dataset by Olist to understand sales performance, customer behavior, product categories, seller performance, delivery efficiency, and customer satisfaction.

The analysis is transformed into an interactive dashboard that allows users to explore the business data using dynamic filters and visualizations.

---
##  Live Dashboard

**[Open Live Dashboard](https://olist-ecommerce-analytics.onrender.com)**

The dashboard is deployed using Render and built with Streamlit.

---
##  Dashboard Preview

The interactive dashboard includes:

- 📈 Sales & Revenue Analysis
- 👥 Customer Analysis
- 📦 Product & Category Analysis
- 🏪 Seller Performance
- 🚚 Delivery Performance
- ⭐ Customer Reviews & Satisfaction
- 💡 Business Insights

Users can filter the dashboard by year, customer state, and product category.
<img width="1912" height="975" alt="Screenshot 2026-09-17 150225" src="https://github.com/user-attachments/assets/88fd7514-0c00-4240-b156-629f27c867de" />
<img width="1903" height="972" alt="Screenshot 2026-09-17 151841" src="https://github.com/user-attachments/assets/093ee467-f05a-4dab-80de-ba2c71e11756" />
<img width="1917" height="970" alt="Screenshot 2026-09-17 152042" src="https://github.com/user-attachments/assets/5a748d3a-44ef-4537-857c-b9c7f7538968" />
<img width="1917" height="973" alt="Screenshot 2026-09-17 152220" src="https://github.com/user-attachments/assets/cb58d24d-52b7-4b5e-a6da-a127aa1f8854" />


---
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

##  Deployment

The Streamlit dashboard is deployed on **Render**.

The Olist dataset is downloaded at runtime using **KaggleHub**, so the large raw CSV files do not need to be stored in the GitHub repository.

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

##  Project Status

### Completed
- Data understanding and validation
- Multi-dataset relationship analysis
- Data cleaning and feature engineering
- Exploratory Data Analysis
- Business insights
- Interactive Streamlit dashboard
- GitHub repository
- Live deployment

### Future Development
- Machine Learning for delivery delay prediction
- Customer segmentation
- Repeat purchase prediction
- Review score prediction
- ML integration into the Streamlit dashboard

 --- 

### Dataset Relationships

The major relationships analyzed in the project include:

``` text 
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

```

 --- 
## Author

Prathamesh Jadhav

Mechatronics Engineering Student
Interested in Data Analytics, Machine Learning, AI, and Robotics.

## Project Status

EDA & Interactive Dashboard — Completed

Machine Learning Extension — Planned
