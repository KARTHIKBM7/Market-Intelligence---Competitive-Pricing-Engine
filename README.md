# 📚 Competitive Market Intelligence & Price Tracker

![Python](https://img.shields.io/badge/Python-3.9-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![Status](https://img.shields.io/badge/Pipeline-Automated-success)

> **A full-stack data engineering solution that automates competitor price monitoring, providing real-time analytics via a REST API and interactive dashboards.**

---

## 🚀 Live Demo (See it in Action)

| Component | Role | Status | Link |
| :--- | :--- | :--- | :--- |
| **📊 Executive Dashboard** | **Frontend** | 🟢 Live | [**Click to View Dashboard**](https://dashboardpy-nbatutpfheggacesfqpj43.streamlit.app/) |
| **🔌 Developer API** | **Backend** | 🟢 Live | [**Click to Test API (Swagger UI)**](https://market-intelligence-competitive-pricing.onrender.com/docs) |
| **🤖 Data Pipeline** | **Automation** | 🟢 Active | *Runs daily via GitHub Actions* |

---

## 📖 Project Overview
**The Problem:** Manual price tracking is slow, error-prone, and lacks historical context.
**The Solution:** An automated ETL pipeline that scrapes competitor data daily, stores it in a cloud warehouse, and serves actionable insights to stakeholders.

### 🔑 Key Features
* **Automated ETL:** Daily extraction of pricing data using `BeautifulSoup` and `GitHub Actions`.
* **Cloud Warehousing:** Persistent storage in **PostgreSQL (Supabase)** to track historical price trends.
* **RESTful API:** A **FastAPI** microservice allowing external applications to fetch data securely (JSON).
* **Business Intelligence:** A **Streamlit** dashboard visualizing KPIs like "Average Market Price" and "Price Drop Alerts."

---

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Extraction:** BeautifulSoup4, Requests
* **Storage:** PostgreSQL (hosted on Supabase)
* **Backend:** FastAPI, Uvicorn (hosted on Render)
* **Visualization:** Streamlit Cloud, Pandas, Plotly
* **DevOps:** GitHub Actions (CI/CD), Docker (Coming Soon)

---

## 🔄 Data Architecture
1.  **Scraper (`main.py`)**: Wakes up at 8:00 AM, scrapes `books.toscrape.com`.
2.  **Transformer**: Cleans currency symbols (£), handles missing values, and formats dates.
3.  **Loader**: Pushes clean data to the **Supabase PostgreSQL** cloud database.
4.  **API Layer (`api.py`)**: Connects to the DB and serves data via HTTP endpoints.
5.  **Frontend (`dashboard.py`)**: Consumes data to display charts and tables.

---

## 💻 How to Run Locally
Want to see the code running on your machine?

```bash
# 1. Clone the repository
git clone [https://github.com/KarthikBM/Market_analyzer.git](https://github.com/KarthikBM/Market_analyzer.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API
uvicorn api:app --reload

# 4. Run the Dashboard
streamlit run dashboard.py
