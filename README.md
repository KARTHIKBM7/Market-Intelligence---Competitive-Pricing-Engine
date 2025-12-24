# 📊 Automated Market Intelligence Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dashboardpy-nbatutpfheggacesfqpj43.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue)
![Status](https://img.shields.io/badge/Pipeline-Automated-green)

### 🚀 Live Demo
**[Click here to view the Live Dashboard](https://dashboardpy-nbatutpfheggacesfqpj43.streamlit.app/)**

---

## 📖 Project Overview
This project is a fully automated **End-to-End Data Pipeline** designed to track competitor pricing in real-time. It eliminates manual data gathering by automating the **Extraction, Transformation, and Loading (ETL)** process.

The system scrapes market data daily, merges it with internal datasets, stores it in a cloud database, and visualizes actionable insights on a live dashboard.

**Key Use Case:** Helping pricing managers spot market trends and adjust strategies without opening a spreadsheet.

---

## 🏗️ Architecture & Workflow

1.  **Extract:** A Python script scrapes live pricing data from competitor websites (Requests/BeautifulSoup) and generates mock internal sales data.
2.  **Transform:** Data is cleaned, currency symbols are normalized, and datasets are merged using **Pandas**.
3.  **Load:** Processed data is securely uploaded to a **PostgreSQL Cloud Database (Supabase)**.
4.  **Automate:** **GitHub Actions** triggers this pipeline every morning at 8:00 AM UTC.
5.  **Report:** A **Streamlit** web app fetches live data from the DB to display KPIs and charts.

---

## ✨ Key Features (Reporting Focus)

* **📈 Automated ETL Pipeline:** No human intervention required; runs on a daily schedule.
* **☁️ Cloud Database Integration:** Persistent storage using PostgreSQL (Supabase) to track historical trends.
* **📊 Interactive Dashboard:**
    * **KPI Tracking:** Average Market Price, Product Count, Last Update Time.
    * **Price Distribution:** Histograms using **Plotly** to analyze price spreads.
* **📥 Export Functionality:** One-click **"Download as CSV"** feature for stakeholders to perform offline analysis in Excel.
* **🌍 Timezone Intelligence:** Automatically converts server time (UTC) to local business time (IST) for accurate reporting.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Data Manipulation:** Pandas, NumPy
* **Web Scraping:** BeautifulSoup4, Requests
* **Database:** PostgreSQL (Supabase), SQLAlchemy
* **Visualization:** Streamlit, Plotly Express
* **CI/CD & DevOps:** GitHub Actions (YAML)

---

## 💻 How to Run Locally

If you want to run this dashboard on your own machine:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Market_analyzer.git](https://github.com/your-username/Market_analyzer.git)
    cd Market_analyzer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Database Credentials:**
    * Create a file named `config.py`.
    * Add your database URL: `DB_URL = "postgresql://user:pass@host:port/db"`

4.  **Run the Dashboard:**
    ```bash
    streamlit run dashboard.py
    ```

---

## 📝 Author
**Karthik BM**
*Aspiring Reporting Specialist & Data Analyst*
