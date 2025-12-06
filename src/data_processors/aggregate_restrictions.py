import os
from pathlib import Path
import geopandas as gpd
import pandas as pd
from src.config import UTM_CRS, WGS84_CRS


def concat_restriction_areas():
    """This function creates a union of restriction areas to reduce data."""
    dir_path = Path.cwd()
    processed_path = dir_path / "data" / "processed"
    output_file = processed_path / "total_restriction_area.geojson"

    tree_restriction_file = processed_path / "merged_tree_area.geojson"
    building_restriction_file = processed_path / "merged_building_area_buffer.geojson"

    # Set the GeoJSON object size limit to 0 (no limit) to be able to read very large/complex geometries.
    os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
    tree_gdf = gpd.read_file(tree_restriction_file)
    building_gdf = gpd.read_file(building_restriction_file)

    if tree_gdf.crs != UTM_CRS:
        tree_gdf = tree_gdf.to_crs(UTM_CRS)

    if building_gdf.crs != UTM_CRS:
        building_gdf = building_gdf.to_crs(UTM_CRS)

    restriction_gdfs = [tree_gdf, building_gdf]
    final_gdf_utm = pd.concat(restriction_gdfs, ignore_index=True)

    merged_polygon = final_gdf_utm["geometry"].unary_union

    merged_gs = gpd.GeoSeries([merged_polygon], crs=UTM_CRS)
    merged_gs_wgs84 = merged_gs.to_crs(epsg=WGS84_CRS)

    gdf_final_merged = gpd.GeoDataFrame(
        data={"id": [1], "description": ["Total restriction area"]},
        geometry=merged_gs_wgs84,
        crs=merged_gs_wgs84.crs,
    )

    gdf_final_merged.to_file(output_file, driver="GeoJSON")
