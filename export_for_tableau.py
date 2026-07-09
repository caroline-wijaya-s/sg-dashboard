import sqlite3
import pandas as pd

conn = sqlite3.connect("sg_dashboard.db")
df = pd.read_sql_query('''
    SELECT town, ROUND(AVG(resale_price), 0) AS avg_resale_price
    FROM hdb_resale
    GROUP BY town
    ORDER BY avg_resale_price DESC
''', conn)
df["avg_resale_price"] = df["avg_resale_price"].astype(int)
conn.close()

# Latitude and longitude for each Singapore HDB town
coordinates = {
    "ANG MO KIO": (1.3691, 103.8454),
    "BEDOK": (1.3236, 103.9273),
    "BISHAN": (1.3526, 103.8352),
    "BUKIT BATOK": (1.3590, 103.7637),
    "BUKIT MERAH": (1.2819, 103.8239),
    "BUKIT PANJANG": (1.3774, 103.7719),
    "BUKIT TIMAH": (1.3294, 103.8021),
    "CENTRAL AREA": (1.2897, 103.8501),
    "CHOA CHU KANG": (1.3840, 103.7470),
    "CLEMENTI": (1.3162, 103.7649),
    "GEYLANG": (1.3201, 103.8918),
    "HOUGANG": (1.3612, 103.8863),
    "JURONG EAST": (1.3329, 103.7436),
    "JURONG WEST": (1.3404, 103.7090),
    "KALLANG/WHAMPOA": (1.3100, 103.8651),
    "MARINE PARADE": (1.3021, 103.9071),
    "PASIR RIS": (1.3721, 103.9493),
    "PUNGGOL": (1.4043, 103.9022),
    "QUEENSTOWN": (1.2942, 103.7861),
    "SEMBAWANG": (1.4491, 103.8185),
    "SENGKANG": (1.3868, 103.8914),
    "SERANGOON": (1.3554, 103.8679),
    "TAMPINES": (1.3496, 103.9568),
    "TOA PAYOH": (1.3343, 103.8563),
    "WOODLANDS": (1.4382, 103.7890),
    "YISHUN": (1.4304, 103.8354),
}

df["latitude"] = df["town"].map(lambda t: coordinates[t][0])
df["longitude"] = df["town"].map(lambda t: coordinates[t][1])

df.to_csv("hdb_by_town.csv", index=False)
print(df)
print("Saved to hdb_by_town.csv")