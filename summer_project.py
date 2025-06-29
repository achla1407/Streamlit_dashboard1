import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --------------------------
# CONFIGURATION
# --------------------------
st.set_page_config(page_title="Inventory Dashboard", layout="wide")

# --------------------------
# DATABASE CONNECTION (PostgreSQL)
# --------------------------
# database.py
# @st.cache_resource
# def get_engine():
#     return create_engine(st.secrets["Inventory_Management"]["url"])

# engine = create_engine("postgresql+psycopg2://postgres:achla1407@localhost:5432/Inventory_Management")
engine = create_engine("postgresql+psycopg2://postgres:[achla1407]@db.dckmjzlsjlevopkjkfcr.supabase.co:5432/postgres")


# --------------------------
# LOAD DATA
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM summerproject", engine)
    return df

df = load_data()

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.header("Filter Data")
stores = df['store_id'].dropna().unique()
products = df['product_id'].dropna().unique()

selected_store = st.sidebar.selectbox("Select Store", stores)
selected_product = st.sidebar.selectbox("Select Product", products)

filtered_df = df[(df['store_id'] == selected_store) & (df['product_id'] == selected_product)]

# --------------------------
# KPIs
# --------------------------
latest_date = df['date'].max()
latest_df = df[df['date'] == latest_date]

stockout_rate = (df[df['inventory_level'] == 0].shape[0] / df.shape[0]) * 100
avg_inventory = df['inventory_level'].mean()
avg_stock_age = df.groupby(['store_id', 'product_id'])['date'].apply(lambda x: (x.max() - x.min()).days).mean()

col1, col2, col3 = st.columns(3)
col1.metric("Stockout Rate", f"{stockout_rate:.2f}%")
col2.metric("Avg Inventory", f"{avg_inventory:.0f} units")
col3.metric("Avg Inventory Age", f"{avg_stock_age:.0f} days")

# --------------------------
# FAST vs SLOW MOVING PRODUCTS
# --------------------------
sales_by_product = df.groupby('product_id')['units_sold'].sum().reset_index()
quantile_80 = sales_by_product['units_sold'].quantile(0.8)

sales_by_product['movement'] = sales_by_product['units_sold'].apply(
    lambda x: 'Fast Moving' if x >= quantile_80 else 'Slow Moving')

st.subheader("Fast vs Slow Moving Products")
fig = px.bar(sales_by_product, x='product_id', y='units_sold', color='movement', title="Product Movement Classification")
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# INVENTORY LEVEL TREND
# --------------------------
st.subheader("Inventory Level Trend")
inventory_trend = filtered_df.groupby('date')['inventory_level'].mean().reset_index()
fig2 = px.line(inventory_trend, x='date', y='inventory_level', title="Avg Inventory Level Over Time")
st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# STOCK ADJUSTMENT RECOMMENDATIONS
# --------------------------
def recommend(row):
    if row['inventory_level'] == 0:
        return "URGENT Reorder"
    elif row['inventory_level'] > 2 * row['demand_forecast']:
        return "Reduce Holding"
    elif row['inventory_level'] < row['demand_forecast']:
        return "Reorder Soon"
    else:
        return "Stock OK"

latest_df['recommendation'] = latest_df.apply(recommend, axis=1)

st.subheader("Stock Adjustment Recommendations")
st.dataframe(latest_df[['store_id', 'product_id', 'inventory_level', 'demand_forecast', 'recommendation']])
