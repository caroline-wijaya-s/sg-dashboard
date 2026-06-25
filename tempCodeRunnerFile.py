df_flat["avg_resale_price"] = df_flat["avg_resale_price"].round(0).astype(int)
df_flat["avg_floor_area_sqm"] = df_flat["avg_floor_area_sqm"].round(0).astype(int)
df_flat["price_per_sqm"] = df_flat["price_per_sqm"].round(0).astype(int)