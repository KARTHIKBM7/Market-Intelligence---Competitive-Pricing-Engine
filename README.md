# 📈 Market Intelligence & Competitive Pricing Engine

## 🚀 Overview
An automated end-to-end data engineering pipeline that tracks competitor pricing in real-time. The system scrapes e-commerce data daily, stores it in a cloud data warehouse, and visualizes market trends via a live interactive dashboard.

**🔗 Live Dashboard:** https://dashboardpy-nbatutpfheggacesfqpj43.streamlit.app/

## 🛠️ Tech Stack
* **Ingestion:** Python (Requests, BeautifulSoup)
* **Automation:** GitHub Actions (CI/CD Cron Jobs)
* **Database:** PostgreSQL (Supabase Cloud)
* **Visualization:** Streamlit & Plotly
* **Deployment:** Streamlit Cloud

## ⚙️ Architecture
1.  **ETL Pipeline:** A Python script scrapes product data and simulates competitor pricing strategies.
2.  **Data Warehouse:** Data is cleaned and uploaded to a hosted PostgreSQL database.
3.  **Automation:** GitHub Actions triggers the ETL job daily (09:00 UTC) to ensure fresh data.
4.  **Frontend:** A Streamlit web app connects to the DB to render live analytics (Avg Price, Spread, Trends).

## 📊 Key Features
* **Automated Data Collection:** Zero-touch daily execution.
* **Cloud-Native:** Fully deployed on serverless infrastructure.
* **Secure:** Uses environment variables and secrets management for DB credentials.
