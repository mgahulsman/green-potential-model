import os
from pathlib import Path
import geopandas as gpd
import h3
from src.config import UTM_CRS, UBERH3_RESOLUTION


def generate_uber_h3_grid():
    """
    Genereert een GeoJSON-bestand met Uber Hexagons (H3 grid met een grovere resolutie)
    op basis van het bounding box van de totale restrictiegebied.
    """
    dir_path = Path.cwd()
    processed_path = dir_path / "data" / "processed"
    restriction_area_file = processed_path / "total_restriction_area.geojson"
    output_file = processed_path / f"h3_grid_res{UBERH3_RESOLUTION}_uber.geojson"

    # Set the GeoJSON object size limit to 0 (no limit) to be able to read very large/complex geometries.
    os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
    restriction_gdf = gpd.read_file(restriction_area_file)

    # Bounding box of restriction area
    minx, miny, maxx, maxy = restriction_gdf.total_bounds

    bbox_polygon = h3.LatLngPoly(
        [(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny), (minx, miny)]
    )

    h3_indices = h3.h3shape_to_cells(bbox_polygon, res=UBERH3_RESOLUTION)
    shapes = [h3.cells_to_h3shape([h3_index]) for h3_index in h3_indices]
    h3_gdf = gpd.GeoDataFrame({"geometry": shapes}, crs=UTM_CRS)

    h3_gdf.to_file(output_file, driver="GeoJSON")
    print(
        f"Succesvol H3 grid (resolutie {UBERH3_RESOLUTION}) gegenereerd naar {output_file}"
    )
