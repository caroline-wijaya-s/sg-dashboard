import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd
from datetime import datetime
import os

conn = sqlite3.connect("sg_dashboard.db")

st.title("Singapore Housing & Transport Dashboard")
st.write("Exploring HDB resale price trends and public transport ridership across Singapore (2017–2026)")

db_modified = os.path.getmtime("sg_dashboard.db")
last_updated = datetime.fromtimestamp(db_modified).strftime("%d %b %Y")
st.caption(f"Data last updated: {last_updated}")

# Query 1: Average resale price by town
df = pd.read_sql_query('''
                       SELECT ROUND(AVG(resale_price),0) AS avg_resale_price,
                       town
                       FROM hdb_resale
                       GROUP BY town 
                       ORDER BY avg_resale_price DESC
                       ''', conn)
df["avg_resale_price"] = df["avg_resale_price"].astype(int)

# Query 2: West vs island indexed growth
west_towns = ('JURONG WEST', 'JURONG EAST', 'BUKIT BATOK', 'BUKIT PANJANG', 'CHOA CHU KANG')

df_west = pd.read_sql_query(f'''
                       SELECT ROUND(AVG(resale_price),0) AS avg_resale_price,
                       month
                       FROM hdb_resale
                       WHERE town IN {west_towns}
                       GROUP BY month 
                       ORDER BY month''', conn)
df_west["avg_resale_price"] = df_west["avg_resale_price"].astype(int)

df_island = pd.read_sql_query('''
                       SELECT ROUND(AVG(resale_price),0) AS avg_resale_price,
                       month
                       FROM hdb_resale
                       GROUP BY month 
                       ORDER BY month''', conn)
df_island["avg_resale_price"] = df_island["avg_resale_price"].astype(int)

df_west["west_indexed_%"] = ((df_west["avg_resale_price"]-df_west["avg_resale_price"].iloc[0])/ df_west["avg_resale_price"].iloc[0]) * 100
df_island["island_indexed_%"] = ((df_island["avg_resale_price"]-df_island["avg_resale_price"].iloc[0]) / df_island["avg_resale_price"].iloc[0]) * 100
df_indexed = df_west.merge(df_island, on='month', suffixes=("_west", "_island"))
df_indexed["island_lead_%"] = df_indexed["island_indexed_%"] - df_indexed["west_indexed_%"]

df_indexed = df_indexed.rename(columns={
    "west_indexed_%": "West Region",
    "island_indexed_%": "Island Average"
})

# Query 3: COVID vs post-COVID
df_resale_price_COVID = pd.read_sql_query('''
                                              SELECT ROUND(AVG(resale_price), 0) AS avg_resale_price
                                              FROM hdb_resale
                                              WHERE month BETWEEN '2020-01-01' AND '2021-12-01'
                                              ''', conn)

df_resale_price_aft_COVID = pd.read_sql_query('''
                                              SELECT ROUND(AVG(resale_price), 0) AS avg_resale_price
                                              FROM hdb_resale
                                              WHERE month > '2021-12-31'
                                              ''', conn)

resale_price_COVID = df_resale_price_COVID["avg_resale_price"].iloc[0]
resale_price_aft_COVID = df_resale_price_aft_COVID["avg_resale_price"].iloc[0]
pct_change = (resale_price_aft_COVID - resale_price_COVID) / resale_price_COVID * 100

# Query 4: MRT ridership
df_ridership = pd.read_sql_query('''
                                 SELECT year,
                                 SUM(ridership) AS total_ridership
                                 FROM mrt_ridership
                                 GROUP BY year
                                 ORDER BY year
                                 ''', conn)

conn.close()

# Metric Cards
highest_town = df.iloc[0]["town"]
highest_price = f"${df.iloc[0]['avg_resale_price']:,}"
lowest_town = df.iloc[-1]["town"]
lowest_price = f"${df.iloc[-1]['avg_resale_price']:,}"
west_growth = f"{df_indexed['West Region'].iloc[-1]:.1f}%"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Highest Avg Price", value=highest_town, delta=highest_price)
with col2:
    st.metric(label="Most Affordable Town", value=lowest_town, delta=lowest_price)
with col3:
    st.metric(label="Post-COVID Price Increase", value=f"+{pct_change:.1f}%")
with col4:
    st.metric(label="West Region Growth (2017→now)", value=west_growth)

# Chart 1: Average resale price by town
fig1 = px.bar(df, 
             x="avg_resale_price", 
             y="town", 
             orientation="h",
             title="Average Resale Price by Town",
             labels={"avg_resale_price": "Average Resale Price (SGD)", "town": "Town"})
st.plotly_chart(fig1)

# Chart 2: West vs island indexed growth
fig2 = px.line(df_indexed, 
             x="month", 
             y=["West Region", "Island Average"],
             title="West Region vs Island Average — Price Growth Since Jan 2017 (%)",
             labels={"value": "Price Growth (%)", "month": "Month", "variable": "Region"})
st.plotly_chart(fig2)
st.caption("West region grew ~47% vs island average ~53% from Jan 2017 to Jun 2026")

# Chart 3: COVID vs post-COVID comparison
df_covid_compare = pd.DataFrame({
    "Period": ["During COVID (2020–2021)", "Post-COVID (2022–present)"],
    "avg_resale_price": [int(resale_price_COVID), int(resale_price_aft_COVID)]
})

fig3 = px.bar(df_covid_compare,
              x="Period",
              y="avg_resale_price",
              title="Average Resale Price: COVID vs Post-COVID",
              labels={"avg_resale_price": "Average Resale Price (SGD)", "Period": ""},
              text=df_covid_compare["avg_resale_price"].apply(lambda x: f"${x:,}"))
st.plotly_chart(fig3)
st.caption(f"Post-COVID prices are {pct_change:.1f}% higher than during COVID")

# Chart 4: MRT ridership trend
fig4 = px.line(df_ridership, 
             x="year", 
             y="total_ridership",
             title="Total Ridership", 
             labels={"year": "Year", "total_ridership": "Total Ridership"})
st.plotly_chart(fig4)
st.caption("Ridership crashed ~30% during COVID (2020-2021) and has since recovered to pre-COVID levels by 2024")