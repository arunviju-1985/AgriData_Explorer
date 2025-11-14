import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import mysql.connector
import pymysql
import plotly.express as px
from sqlalchemy import create_engine

conn = pymysql.connect(
    host="localhost", 
    user="root", 
    password="aaron2013",
    database="agridata_explorer" 
)

cursor = conn.cursor()
engine = create_engine("mysql+pymysql://root:aaron2013@localhost/agridata_explorer")
query_rice = """
SELECT 
    `State Name` AS state_name,
    SUM(`RICE PRODUCTION (1000 tons)`) AS total_rice_production
FROM agridata
GROUP BY `State Name`
ORDER BY total_rice_production DESC
LIMIT 7;
"""
rice_states = pd.read_sql(query_rice, conn)

print("\nTop 7 Rice Producing States:\n", rice_states)

# Rice States Bar Plot
plt.figure(figsize=(10,6))
sns.barplot(x="state_name", y="total_rice_production", data=rice_states)
plt.title("Top 7 Rice Producing States")
plt.xticks(rotation=45)
st.pyplot(plt)

# Query for Top 5 Wheat Producing States
query_wheat = """
SELECT 
    `State Name` AS state_name,
    SUM(`WHEAT PRODUCTION (1000 tons)`) AS total_wheat_production
FROM agridata
GROUP BY `State Name`
ORDER BY total_wheat_production DESC
LIMIT 5;
"""

wheat_states = pd.read_sql(query_wheat, conn)
print("\nTop 5 Wheat Producing States:\n", wheat_states)

# --- Bar Chart ---
plt.figure(figsize=(10,6))
sns.barplot(x="state_name", y="total_wheat_production", data=wheat_states, palette="Blues_d")
plt.title("Top 5 Wheat Producing States Bar Chat")
plt.xlabel("State")
plt.ylabel("Wheat Production (1000 tons)")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# --- Pie Chart ---
plt.figure(figsize=(6,6))
plt.pie(
    wheat_states['total_wheat_production'],
    labels=wheat_states['state_name'],
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette("Blues", 5)
)
plt.title("Wheat Production Share by Top 5 States Pie Chat")
plt.tight_layout()
st.pyplot(plt)


# Query for Oilseeds Production
query_oilseeds = """
SELECT 
    `State Name` AS state_name,
    SUM(`OILSEEDS PRODUCTION (1000 tons)`) AS total_oilseeds_production
FROM agridata
GROUP BY `State Name`
ORDER BY total_oilseeds_production DESC
LIMIT 5;
"""

oilseeds_states = pd.read_sql(query_oilseeds, conn)
print("\nTop 5 Oilseeds Producing States:\n", oilseeds_states)

# --- Bar Chart ---
plt.figure(figsize=(10,6))
sns.barplot(x="state_name", y="total_oilseeds_production", data=oilseeds_states, palette="Greens_d")
plt.title("Top 5 Oilseeds Producing States")
plt.xlabel("State")
plt.ylabel("Oilseeds Production (1000 tons)")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Query for Sunflower Production
query_sunflower = """
SELECT 
    `State Name` AS state_name,
    SUM(`SUNFLOWER PRODUCTION (1000 tons)`) AS total_sunflower_production
FROM agridata
GROUP BY `State Name`
ORDER BY total_sunflower_production DESC
LIMIT 7;
"""

sunflower_states = pd.read_sql(query_sunflower, conn)
print("\nTop 7 Sunflower Producing States:\n", sunflower_states)

# --- Bar Chart ---
plt.figure(figsize=(10,6))
sns.barplot(x="state_name", y="total_sunflower_production", data=sunflower_states, palette="YlOrBr")
plt.title("Top 7 Sunflower Producing States")
plt.xlabel("State")
plt.ylabel("Sunflower Production (1000 tons)")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Query for Sugarcane Production (Last 50 Years)
query_sugarcane = """
SELECT 
    `Year` AS year,
    SUM(`SUGARCANE PRODUCTION (1000 tons)`) AS total_sugarcane_production
FROM agridata
GROUP BY `Year`
ORDER BY year;
"""

sugarcane = pd.read_sql(query_sugarcane, conn)
print("\nSugarcane Production (Last 50 Years):\n", sugarcane.head())

# --- Line Plot ---
plt.figure(figsize=(12,6))
plt.plot(sugarcane['year'], sugarcane['total_sugarcane_production'], marker='o', color="brown")
plt.title("India's Sugarcane Production (Last 50 Years)")
plt.xlabel("Year")
plt.ylabel("Production (1000 tons)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Query Rice vs Wheat Production
query = """
SELECT 
    `Year` AS year,
    SUM(`RICE PRODUCTION (1000 tons)`) AS rice_production,
    SUM(`WHEAT PRODUCTION (1000 tons)`) AS wheat_production
FROM agridata
GROUP BY `Year`
ORDER BY year;
"""

rice_wheat = pd.read_sql(query, conn)
print("\nRice vs Wheat Production (Last 50 Years):\n", rice_wheat.head())

# --- Line Plot ---
plt.figure(figsize=(12,6))
plt.plot(rice_wheat['year'], rice_wheat['rice_production'], label="Rice", color="green", marker='o')
plt.plot(rice_wheat['year'], rice_wheat['wheat_production'], label="Wheat", color="orange", marker='s')
plt.title("Rice vs Wheat Production in India (Last 50 Years)")
plt.xlabel("Year")
plt.ylabel("Production (1000 tons)")
plt.xticks(rotation=45)  # 👈 improves year label visibility
plt.grid(True)
plt.legend()
plt.tight_layout()
st.pyplot(plt)

# Query average yield by state
query = """
SELECT 
    `State Name` AS state_name,
    AVG(`RICE YIELD (Kg per ha)`) AS rice_yield,
    AVG(`WHEAT YIELD (Kg per ha)`) AS wheat_yield
FROM agridata
GROUP BY `State Name`
ORDER BY rice_yield DESC;
"""

yield_df = pd.read_sql(query, conn)
conn.close()

# --- Bar Plot ---
plt.figure(figsize=(12,6))
bar_width = 0.4
x = range(len(yield_df))

plt.bar(x, yield_df['rice_yield'], width=bar_width, label='Rice Yield', color='green')
plt.bar([i + bar_width for i in x], yield_df['wheat_yield'], width=bar_width, label='Wheat Yield', color='orange')

plt.xticks([i + bar_width/2 for i in x], yield_df['state_name'], rotation=45)
plt.title("Rice vs Wheat Yield Across States")
plt.xlabel("State")
plt.ylabel("Yield (Kg per ha)")
plt.legend()
plt.tight_layout()
st.pyplot(plt)


# Query rice production by year and state  SQL Query
query = """
SELECT 
    `Year` AS year,
    `State Name` AS state_name,
    SUM(`RICE PRODUCTION (1000 tons)`) AS rice_production
FROM agridata
GROUP BY `Year`, `State Name`
ORDER BY year;
"""
rice_df = pd.read_sql(query, engine)

# Identify Top 3 states by total rice production
top_states = rice_df.groupby('state_name')['rice_production'].sum().nlargest(3).index.tolist()
rice_top3 = rice_df[rice_df['state_name'].isin(top_states)]

# Pivot to table format
rice_table = rice_top3.pivot(index='year', columns='state_name', values='rice_production').fillna(0)

# --- Streamlit Web Output ---
st.title("Year-wise Rice Production (Top 3 States)")
st.dataframe(rice_table)   # shows interactive table in browser

# Optional: Add chart toggle
if st.checkbox("Show Line Chart"):
    st.line_chart(rice_table)