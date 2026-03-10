# 🏙️ Urban Real Estate Intelligence Platform

A end-to-end data engineering pipeline tracking real estate market indicators 
and news sentiment for **Bangalore** and **Dubai** — two of the fastest growing 
property markets in Asia.

🔴 **[Live Dashboard →](YOUR_STREAMLIT_URL_HERE)**

---

## What This Project Does

This pipeline automatically collects, transforms, and visualises:
- **Market index data** — Nifty 50 (Bangalore proxy) and EEM ETF (Dubai proxy)
- **News sentiment** — Real estate news scored using NLP sentiment analysis
- **Market comparisons** — Side by side Bangalore vs Dubai analytics
- **Trend analysis** — Weekly price trends and month over month growth

Data refreshes daily via automated Airflow orchestration.

---

## Architecture
```
Data Sources → Python Ingestion → PostgreSQL (Neon) → dbt → Streamlit Dashboard
     ↑                                                          
Apache Airflow (daily schedule)                               
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Ingestion | Python, yfinance, NewsAPI |
| Orchestration | Apache Airflow 3.0 |
| Storage | PostgreSQL (Neon cloud) |
| Transformation | dbt (5 models) |
| Sentiment Analysis | VADER NLP |
| Dashboard | Streamlit + Plotly |
| Deployment | Streamlit Cloud |
| Version Control | Git + GitHub |

---

## Project Structure
```
urban-realestate-intel/
├── ingestion/          # Data ingestion scripts
│   └── fetch_macro.py  # Market index data fetcher
├── sentiment/          # Sentiment analysis
│   └── fetch_sentiment.py  # News sentiment scraper
├── db/                 # Database utilities
│   └── loader.py       # PostgreSQL loader
├── realestate_dbt/     # dbt transformation project
│   └── models/
│       ├── staging/    # Raw data cleaning
│       └── marts/      # Business logic models
├── dashboard/          # Streamlit dashboard
│   └── app.py
└── dags/               # Airflow DAG definitions
```

---

## dbt Models

| Model | Type | Description |
|-------|------|-------------|
| `stg_macro_indicators` | View | Cleaned raw market data |
| `mart_price_trends` | View | Weekly price aggregations |
| `mart_city_comparison` | View | Bangalore vs Dubai metrics |
| `mart_affordability` | View | Month over month growth |
| `mart_sentiment_trends` | View | Weekly sentiment scores |

---

## Key Insights

- **Dubai** showed **68% index growth** vs Bangalore's **18.8%** over 1 year
- **Bangalore** news sentiment scored higher (0.44) vs Dubai (0.28)
- Dubai generates significantly more real estate news volume globally
- Both markets show positive sentiment — no negative average weeks recorded

---

## Setup & Run Locally

**Prerequisites:** Python 3.12, PostgreSQL, WSL2 (Windows)
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/urban-realestate-intel.git
cd urban-realestate-intel

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env

# Run the pipeline
python -m ingestion.fetch_macro
python -m sentiment.fetch_sentiment

# Run dbt transformations
cd realestate_dbt && dbt run

# Launch dashboard
streamlit run dashboard/app.py
```

---

## Environment Variables

Create a `.env` file with:
```
NEWS_API_KEY=your_newsapi_key
```

---

Built by **Vaisakh** | [LinkedIn](YOUR_LINKEDIN_URL)
```

Save the file.

---

## Part 2 — Create .env.example

Create a new file `.env.example` in your project root:
```
NEWS_API_KEY=your_newsapi_key_here
