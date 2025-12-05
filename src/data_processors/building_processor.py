from pathlib import Path
import geopandas as gpd
from src.config import UTM_CRS, WGS84_CRS


def process_building_data() -> None:
    dir_path = Path.cwd()
    raw_path = dir_path / "data" / "raw" / "osm"
    processed_path = dir_path / "data" / "processed"
    output_file = processed_path / "merged_building_area.geojson"

    filepath = "buildings.geojson"

    building_gdf = gpd.read_file(raw_path / filepath)

    if building_gdf.crs != UTM_CRS:
        building_gdf = building_gdf.to_crs(UTM_CRS)

    merged_polygon = building_gdf["geometry"].unary_union

    merged_gs = gpd.GeoSeries([merged_polygon], crs=UTM_CRS)
    merged_gs_wgs84 = merged_gs.to_crs(epsg=WGS84_CRS)

    gdf_final_merged = gpd.GeoDataFrame(
        data={"id": [1], "description": ["Merged building area"]},
        geometry=merged_gs_wgs84,
        crs=merged_gs_wgs84.crs,
    )

    gdf_final_merged.to_file(output_file, driver="GeoJSON")
