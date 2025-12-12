import logging
import geopandas as gpd
from src.shared import Paths
from src.config import UTM_CRS, WGS84_CRS, BUILDING_BUFFER_METER


def process_building_data() -> None:
    paths = Paths()
    output_file = paths.processed / "merged_building_area_buffer.geojson"
    building_gdf = gpd.read_file(paths.raw / "osm" / "buildings.geojson")

    if building_gdf.crs != UTM_CRS:
        building_gdf = building_gdf.to_crs(UTM_CRS)

    building_gdf["geometry"] = building_gdf.buffer(
        BUILDING_BUFFER_METER, join_style="mitre"
    )

    merged_polygon = building_gdf["geometry"].unary_union

    merged_gs = gpd.GeoSeries([merged_polygon], crs=UTM_CRS)
    merged_gs_wgs84 = merged_gs.to_crs(epsg=WGS84_CRS)

    gdf_final_merged = gpd.GeoDataFrame(
        data={"id": [1], "description": ["Merged building area"]},
        geometry=merged_gs_wgs84,
        crs=merged_gs_wgs84.crs,
    )

    gdf_final_merged.to_file(output_file, driver="GeoJSON")
    logging.info(f"Saved {output_file.relative_to(paths.dir_path)}")
