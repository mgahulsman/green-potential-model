import logging
import os
import geopandas as gpd
import h3
from src.shared import Paths
from src.config import UTM_CRS, UBERH3_RESOLUTION


def generate_uber_h3_grid():
    """
    Genereert een GeoJSON-bestand met Uber Hexagons (H3 grid met een grovere resolutie)
    op basis van het bounding box van de totale restrictiegebied.
    """
    paths = Paths()
    restriction_area_file = paths.processed / "total_restriction_area.geojson"
    output_file = (
        paths.processed / "grid" / f"h3_grid_res{UBERH3_RESOLUTION}_uber.geojson"
    )

    # Set the GeoJSON object size limit to 0 (no limit) to be able to read very large/complex geometries.
    os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
    restriction_gdf = gpd.read_file(restriction_area_file)

    # TODO: use the bbox of the municapllity since this doesn't include all edges,
    # because the restriction area != the total area
    # Bounding box of restriction area
    minx, miny, maxx, maxy = restriction_gdf.total_bounds

    # Lon, Lan switch, since leaflet uses Lat, Lon and h3 Lon, Lat
    bbox_polygon = h3.LatLngPoly(
        [
            (miny, minx),  # (Lat, Lon)
            (maxy, minx),  # (Lat, Lon)
            (maxy, maxx),  # (Lat, Lon)
            (miny, maxx),  # (Lat, Lon)
            (miny, minx),  # (Lat, Lon)
        ]
    )

    h3_indices = h3.h3shape_to_cells(bbox_polygon, res=UBERH3_RESOLUTION)
    shapes = [h3.cells_to_h3shape([h3_index]) for h3_index in h3_indices]
    h3_gdf = gpd.GeoDataFrame({"geometry": shapes}, crs=UTM_CRS)

    h3_gdf.to_file(output_file, driver="GeoJSON")

    logging.info(f"Saved {output_file.relative_to(paths.dir_path)}")
