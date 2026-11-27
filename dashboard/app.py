from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Change this line if train_clean.csv is somewhere else
DATA = Path(__file__).parent.parent / "data" / "train_clean.csv"

if not DATA.exists():
    st.error(f"File not found: {DATA}")
    st.stop()

df = pd.read_csv(DATA, parse_dates=["order_date"], dtype={"postal_code": str})

st.title("Sales Dashboard")

years = sorted(df.order_date.dt.year.unique(), reverse=True)
year = st.sidebar.selectbox("Year", years)
regions = sorted(df.region.unique())
chosen = st.sidebar.multiselect("Region", regions, default=regions)

data = df[(df.order_date.dt.year == year) & df.region.isin(chosen)]
if data.empty:
    st.warning("No sales match these filters.")
    st.stop()

a, b, c = st.columns(3)
a.metric("Sales", f"${data.sales.sum():,.0f}")
b.metric("Orders", f"{data.order_id.nunique():,}")
c.metric("Average order value", f"${data.sales.sum() / data.order_id.nunique():,.0f}")

monthly = data.resample("MS", on="order_date").sales.sum().reset_index()
st.plotly_chart(px.line(monthly, x="order_date", y="sales", title="Monthly sales"))

left, right = st.columns(2)
for col, field in [(left, "region"), (right, "category")]:
    totals = data.groupby(field, as_index=False).sales.sum()
    col.plotly_chart(px.bar(totals, x=field, y="sales", title=f"Sales by {field}"))