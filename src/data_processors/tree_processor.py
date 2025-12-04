from pathlib import Path
import geopandas as gpd
import pandas as pd
from src.config import UTM_CRS, WGS84_CRS, TREE_BUFFER_METER, BUFFER_RESOLUTIE


def process_tree_data() -> Path:
    dir_path = Path.cwd()
    raw_path = dir_path / "data" / "raw" / "trees"
    processed_path = dir_path / "data" / "processed"
    output_file = processed_path / "merged_tree_area.geojson"

    filepaths = {"Delft": "delft_trees.geojson"}
    tree_gdfs = []

    for city in filepaths.keys():
        tree_gdf = gpd.read_file(raw_path / filepaths[city])
        tree_gdfs.append(tree_gdf)

    final_gdf = pd.concat(tree_gdfs, ignore_index=True)

    gdf_geprojecteerd = final_gdf.to_crs(UTM_CRS)

    geometrie_cirkels = gdf_geprojecteerd["geometry"].buffer(
        TREE_BUFFER_METER, resolution=BUFFER_RESOLUTIE
    )

    merged_polygon = geometrie_cirkels.unary_union

    merged_gs = gpd.GeoSeries([merged_polygon], crs=UTM_CRS)
    merged_gs_wgs84 = merged_gs.to_crs(epsg=WGS84_CRS)

    gdf_final_merged = gpd.GeoDataFrame(
        data={"id": [1], "description": ["Joint restiction area"]},
        geometry=merged_gs_wgs84,
        crs=merged_gs_wgs84.crs,
    )

    gdf_final_merged.to_file(output_file, driver="GeoJSON")

    return output_file
