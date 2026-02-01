import geopandas as gpd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost:5432/green_potential")

tabel_naam = "restriction_buildings"
gdf = gpd.read_postgis(f"SELECT * FROM {tabel_naam}", engine, geom_col="geometry")

print("--- Kolommen ---")
print(gdf.columns.tolist())
print("\n--- Inhoud eerste rij ---")
print(gdf.iloc[0])
