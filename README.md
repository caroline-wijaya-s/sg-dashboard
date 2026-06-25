# Singapore Housing & Transport Dashboard

A live, auto-updating dashboard tracking HDB resale price trends and public transport ridership across Singapore (2017–2026), built as a data analyst portfolio project.

🔗 **Live Dashboard:** https://sg-dashboard-caroline.streamlit.app/

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data collection, cleaning, analysis |
| pandas | Data wrangling and transformation |
| SQLite | Local database storage |
| requests | API calls to data.gov.sg |
| GitHub Actions | Automated weekly data updates |
| Streamlit | Interactive dashboard |
| Plotly | Charts and visualisations |

---

## Architecture
data.gov.sg API → collect.py → sg_dashboard.db → dashboard.py → Streamlit Cloud
1. **Data collection** — `collect.py` fetches HDB resale prices and MRT/bus ridership from data.gov.sg
2. **Storage** — data is stored in a local SQLite database (`sg_dashboard.db`)
3. **Automation** — GitHub Actions runs `collect.py` weekly and commits the updated database back to the repo
4. **Dashboard** — Streamlit reads from the database and renders interactive charts, auto-refreshing with new data

---

## Data Sources

| Dataset | Source | Update Frequency |
|---|---|---|
| HDB Resale Flat Prices (Jan 2017 onwards) | data.gov.sg | Monthly |
| Public Transport Ridership (1995–2024) | data.gov.sg | Annual |

---

## Key Insights

1. **Bukit Timah** has the highest average resale price at $782,616 — 68% above the most affordable town, Yishun ($454,028)
2. **West region** prices grew ~47% from Jan 2017 to Jun 2026, slightly behind the island average of ~53%
3. **Executive flats** offer the best value at $5,100/sqm — smaller flat types cost significantly more per sqm
4. **Post-COVID prices** are 24.7% higher than during COVID (2020–2021), reflecting Singapore's property boom
5. **MRT ridership** crashed ~30% during COVID and has since recovered to pre-COVID levels by 2024

---

## How to Run Locally

1. Clone the repo:
git clone https://github.com/caroline-wijaya-s/sg-dashboard.git
cd sg-dashboard

2. Install dependencies:
pip install -r requirements.txt
pip install streamlit sqlite3

3. Run the initial data collection:
python phase2_unify.py

4. Launch the dashboard:
streamlit run dashboard.py

---

## Project Structure
sg-dashboard/

├── dashboard.py          # Streamlit dashboard

├── collect.py            # Weekly data collector

├── phase1_explore.py     # Initial API exploration

├── phase2_unify.py       # One-time historical data load

├── phase4_analysis.ipynb # Analysis notebook

├── sg_dashboard.db       # SQLite database

├── requirements.txt      # Python dependencies

├── log.txt               # Automated run log

└── .github/

└── workflows/

└── update.yml    # GitHub Actions workflow



