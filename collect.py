import requests
import pandas as pd
import sqlite3
from datetime import datetime

# 2. connect to database
conn = sqlite3.connect("sg_dashboard.db")

# 3. find the latest date already in the database
result = conn.execute("SELECT MAX(month) FROM hdb_resale").fetchone()
latest_month = result[0]
print("Latest month in database:", latest_month)

# 4. fetch only new HDB rows
# convert latest_month to YYYY-MM format for comparison
latest_str = latest_month[:7]  # takes first 7 characters: "2026-06"
print(latest_str)

# 5. fetch recent HDB data from the API
# fetch last 5000 rows from API (enough to capture any new months)
hdb_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
base_url = "https://data.gov.sg/api/action/datastore_search"
params = {"resource_id": hdb_id, "limit": 5000, "offset": 0}
response = requests.get(base_url, params=params)
data = response.json()
new_df = pd.DataFrame(data["result"]["records"])
new_df = new_df[new_df["month"] > latest_str]
print(f"New HDB rows to insert: {len(new_df)}")

# 6. insert new rows into the database
if len(new_df) > 0:
    new_df["month"] = pd.to_datetime(new_df["month"], format="%Y-%m")
    new_df["resale_price"] = pd.to_numeric(new_df["resale_price"])
    new_df["floor_area_sqm"] = pd.to_numeric(new_df["floor_area_sqm"])
    new_df.to_sql("hdb_resale", conn, if_exists="append", index=False)
else:
    print("No new rows to insert")

# 7. add a log entry
with open("log.txt", "a") as f:
    f.write(f"{datetime.now()} - HDB: {len(new_df)} new rows inserted\n")

# 8. do the same for MRT ridership
result = conn.execute("SELECT MAX(year) FROM mrt_ridership").fetchone()
latest_mrt_year = result[0]
print("Latest year in database:", latest_mrt_year)

mrt_id = "d_75248cf2fbf340de6a746dc91ec9223c"
params = {"resource_id": mrt_id, "limit": 5000, "offset": 0}
response = requests.get(base_url, params=params)
data = response.json()
new_mrt_df = pd.DataFrame(data["result"]["records"])
new_mrt_df = new_mrt_df[pd.to_numeric(new_mrt_df["year"]) > latest_mrt_year]
print(f"New MRT rows to insert: {len(new_mrt_df)}")

if len(new_mrt_df) > 0:
    new_mrt_df["year"] = pd.to_numeric(new_mrt_df["year"])
    new_mrt_df["ridership"] = pd.to_numeric(new_mrt_df["ridership"])
    new_mrt_df.to_sql("mrt_ridership", conn, if_exists="append", index=False)
else:
    print("No new rows to insert")

with open("log.txt", "a") as f:
    f.write(f"{datetime.now()} - MRT: {len(new_mrt_df)} new rows inserted\n")

conn.close()
print("Done! Database saved as sg_dashboard.db")
