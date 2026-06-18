import requests
import pandas as pd

# ── 1. HDB Resale Prices ──────────────────────────────────
print("Fetching HDB resale prices...")

hdb_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
url = f"https://data.gov.sg/api/action/datastore_search?resource_id={hdb_id}&limit=100"

response = requests.get(url)
data = response.json()

hdb_df = pd.DataFrame(data["result"]["records"])
print("\n── HDB Resale Prices ──")
print(f"Shape: {hdb_df.shape}")
print(f"Columns: {list(hdb_df.columns)}")
print(hdb_df.head(3))

# ── 2. MRT Ridership ──────────────────────────────────────
print("\nFetching MRT ridership...")

mrt_id = "d_75248cf2fbf340de6a746dc91ec9223c"
url = f"https://data.gov.sg/api/action/datastore_search?resource_id={mrt_id}&limit=100"

response = requests.get(url)
data = response.json()

mrt_df = pd.DataFrame(data["result"]["records"])
print("\n── MRT Ridership ──")
print(f"Shape: {mrt_df.shape}")
print(f"Columns: {list(mrt_df.columns)}")
print(mrt_df.head(3))

# ── 3. Summary ────────────────────────────────────────────
print("\n\n════ SUMMARY ════")
print("\nHDB — unique towns:")
print(sorted(hdb_df["town"].unique()))
print("\nHDB — date range:")
print(hdb_df["month"].min(), "→", hdb_df["month"].max())