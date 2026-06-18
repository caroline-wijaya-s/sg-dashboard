import requests
import pandas as pd
import sqlite3
import time

# ── 1. Fetch ALL HDB resale records via pagination ──────────────────────────
print("Fetching HDB resale prices (this will take a minute)...")

hdb_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
base_url = "https://data.gov.sg/api/action/datastore_search"

all_records = []
offset = 0
batch_size = 1000

while True:
    params = {"resource_id": hdb_id, "limit": batch_size, "offset": offset}
    response = requests.get(base_url, params=params)
    data = response.json()

    if "result" not in data:
        print("  API error, retrying in 5 seconds:", data)
        time.sleep(5)
        continue  # retry the same offset

    records = data["result"]["records"]
    if not records:
        break  # no more data

    all_records.extend(records)
    offset += batch_size
    print(f"  Fetched {len(all_records)} rows so far...")

    time.sleep(1)  # slightly longer pause to avoid rate limits

hdb_df = pd.DataFrame(all_records)
print(f"\nTotal HDB rows fetched: {len(hdb_df)}")
print(hdb_df.head(3))


# ── 2. Clean & type-cast HDB data ────────────────────────────────────────────
print("\nCleaning HDB data...")

hdb_df["month"] = pd.to_datetime(hdb_df["month"], format="%Y-%m")
hdb_df["resale_price"] = pd.to_numeric(hdb_df["resale_price"])
hdb_df["floor_area_sqm"] = pd.to_numeric(hdb_df["floor_area_sqm"])
hdb_df["lease_commence_date"] = pd.to_numeric(hdb_df["lease_commence_date"])

print(hdb_df.dtypes)


# ── 3. Fetch MRT ridership (small dataset, no pagination needed) ────────────
print("\nFetching MRT ridership...")

mrt_id = "d_75248cf2fbf340de6a746dc91ec9223c"
params = {"resource_id": mrt_id, "limit": 1000}
response = requests.get(base_url, params=params)
data = response.json()

mrt_df = pd.DataFrame(data["result"]["records"])
mrt_df["year"] = pd.to_numeric(mrt_df["year"])
mrt_df["ridership"] = pd.to_numeric(mrt_df["ridership"])

print(f"Total MRT rows fetched: {len(mrt_df)}")
print(mrt_df.head(3))


# ── 4. Store both in SQLite ──────────────────────────────────────────────────
print("\nSaving to SQLite database...")

conn = sqlite3.connect("sg_dashboard.db")

hdb_df.to_sql("hdb_resale", conn, if_exists="replace", index=False)
mrt_df.to_sql("mrt_ridership", conn, if_exists="replace", index=False)

conn.close()
print("Done! Database saved as sg_dashboard.db")