from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import geopandas as gpd
from sqlalchemy import create_engine

app = FastAPI()

# TODO: change so that it only allow my own origin
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

engine = create_engine("postgresql://user:pass@localhost:5432/green_potential")


@app.get("/api/restrictions")
def get_restrictions():
    gdf = gpd.read_postgis(
        "SELECT * FROM restrictions_test", engine, geom_col="geometry"
    )

    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs(epsg=4326)

    return gdf.__geo_interface__


@app.get("/api/results/{grid}/{scenario}")
def get_results(grid: str, scenario: str):
    table_name = f"analysis_{grid}_{scenario}".lower()
    gdf = gpd.read_postgis(f"SELECT * FROM {table_name}", engine, geom_col="geometry")
    gdf = gdf.to_crs(epsg=4326)
    geojson = gdf.__geo_interface__

    if gdf.empty:
        raise ValueError

    geojson["tei_score"] = float(gdf["tei_score"].iloc[0])
    geojson["mean_green_score"] = float(gdf["mean_green_score"].iloc[0])
    geojson["stats"] = {
        "low_bound": float(gdf["green_score"].min()),
        "high_bound": float(gdf["green_score"].max()),
    }

    return geojson


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
