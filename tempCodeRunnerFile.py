import sqlite3
import pandas as pd

conn = sqlite3.connect("sg_dashboard.db")
df = pd.read_sql_query('''
                       SELECT ROUND(AVG(resale_price),0) AS avg_resale_price,
                       town
                       FROM hdb_resale
                       GROUP BY town 
                       ORDER BY avg_resale_price DESC
                       ''', conn)
df["avg_resale_price"] = df["avg_resale_price"].astype(int)
print(df)

df.to_csv("hdb_by_town.csv", index=False)