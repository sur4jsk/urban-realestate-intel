import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Urban Real Estate Intelligence",
    page_icon="🏙️",
    layout="wide"
)

# ─── DB CONNECTION ───
@st.cache_resource
def get_engine():
    return create_engine(
        "postgresql+psycopg2://neondb_owner:npg_AIcXn0ajsbS7@ep-young-union-ad8r9swu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
    )

@st.cache_data(ttl=3600)
def load_data(query):
    engine = get_engine()
    return pd.read_sql(query, engine)

# ─── LOAD DATA ───
try:
    price_trends = load_data("SELECT * FROM analytics.mart_price_trends ORDER BY week_start")
    city_comparison = load_data("SELECT * FROM analytics.mart_city_comparison")
    affordability = load_data("SELECT * FROM analytics.mart_affordability ORDER BY month")
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# ─── HEADER ───
st.title("🏙️ Urban Real Estate Intelligence Platform")
st.markdown("**Bangalore vs Dubai** — Live market data pipeline")
st.divider()

# ─── FILTERS ───
col1, col2 = st.columns([2, 1])
with col1:
    markets = st.multiselect(
        "Select Markets",
        options=["bangalore", "dubai"],
        default=["bangalore", "dubai"]
    )

# Filter data
filtered_trends = price_trends[price_trends["market"].isin(markets)]
filtered_afford = affordability[affordability["market"].isin(markets)]

# ─── KPI CARDS ───
st.subheader("Market Overview")
cols = st.columns(4)

for i, market in enumerate(city_comparison["market"].tolist()):
    row = city_comparison[city_comparison["market"] == market].iloc[0]
    with cols[i * 2]:
        st.metric(
            label=f"{market.title()} — Avg Index",
            value=f"{row['avg_index_1y']:,.0f}",
            delta=f"{row['pct_growth_1y']}% growth"
        )
    with cols[i * 2 + 1]:
        st.metric(
            label=f"{market.title()} — 1Y Range",
            value=f"{row['range_1y']:,.0f}",
        )

st.divider()

# ─── CHART 1: PRICE TRENDS ───
st.subheader("Price Trends Over Time")
fig1 = px.line(
    filtered_trends,
    x="week_start",
    y="avg_index",
    color="market",
    title="Weekly Average Index — Bangalore vs Dubai",
    labels={"week_start": "Week", "avg_index": "Index Value", "market": "Market"},
    color_discrete_map={"bangalore": "#00b4d8", "dubai": "#ff6b35"}
)
fig1.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white",
    legend_title="Market"
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ─── CHART 2: CITY COMPARISON ───
col1, col2 = st.columns(2)

with col1:
    st.subheader("City Comparison")
    fig2 = px.bar(
        city_comparison,
        x="market",
        y="avg_index_1y",
        color="market",
        title="Average Index Value (1 Year)",
        labels={"market": "Market", "avg_index_1y": "Avg Index"},
        color_discrete_map={"bangalore": "#00b4d8", "dubai": "#ff6b35"}
    )
    fig2.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("1-Year Growth")
    fig3 = px.bar(
        city_comparison,
        x="market",
        y="pct_growth_1y",
        color="market",
        title="% Growth Over 1 Year",
        labels={"market": "Market", "pct_growth_1y": "Growth %"},
        color_discrete_map={"bangalore": "#00b4d8", "dubai": "#ff6b35"}
    )
    fig3.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ─── CHART 3: MONTH OVER MONTH GROWTH ───
st.subheader("Month over Month Growth (%)")
filtered_afford_clean = filtered_afford.dropna(subset=["mom_growth_pct"])
fig4 = px.line(
    filtered_afford_clean,
    x="month",
    y="mom_growth_pct",
    color="market",
    title="Monthly Growth Rate — Bangalore vs Dubai",
    labels={"month": "Month", "mom_growth_pct": "MoM Growth %", "market": "Market"},
    color_discrete_map={"bangalore": "#00b4d8", "dubai": "#ff6b35"}
)
fig4.add_hline(y=0, line_dash="dash", line_color="gray")
fig4.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ─── CHART 4: SENTIMENT ───
st.divider()
st.subheader("📰 News Sentiment Analysis")

sentiment = load_data("SELECT * FROM analytics.mart_sentiment_trends ORDER BY week_start")
filtered_sentiment = sentiment[sentiment["market"].isin(markets)]

if not filtered_sentiment.empty:
    fig5 = px.line(
        filtered_sentiment,
        x="week_start",
        y="avg_sentiment",
        color="market",
        title="Weekly News Sentiment Score — Bangalore vs Dubai",
        labels={
            "week_start": "Week",
            "avg_sentiment": "Sentiment Score (-1 to +1)",
            "market": "Market"
        },
        color_discrete_map={"bangalore": "#00b4d8", "dubai": "#ff6b35"}
    )
    fig5.add_hline(y=0, line_dash="dash", line_color="gray")
    fig5.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white"
    )
    st.plotly_chart(fig5, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Article Volume")
        fig6 = px.bar(
            filtered_sentiment.groupby("market")["article_count"].sum().reset_index(),
            x="market",
            y="article_count",
            color="market",
            color_discrete_map={"bangalore": "#00b4d8", "dubai": "#ff6b35"}
        )
        fig6.update_layout(
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
            showlegend=False
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        st.subheader("Average Sentiment by Market")
        latest = filtered_sentiment.groupby("market")[
            ["avg_positive", "avg_negative", "avg_sentiment"]
        ].mean().round(4).reset_index()
        st.dataframe(latest, use_container_width=True)
else:
    st.info("No sentiment data yet — run the sentiment scraper first.")
    
# ─── FOOTER ───
st.caption("Data pipeline: Python → Airflow → PostgreSQL → dbt → Streamlit | Built by Suraj Kartha")