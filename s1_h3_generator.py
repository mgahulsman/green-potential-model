import os
import logging
import geopandas as gpd
import h3


def generate_h3_grid(resolutions: list[int]):
    base_folder = "C:/Users/maart/EigenMappen/Studie/laatste_bachelor_semester/bep/green-potential-model/new_structure/data/"
    municipality_file = base_folder + "raw/grid/delft_municipality.geojson"

    # Set the GeoJSON object size limit to 0 (no limit) to be able to read very large/complex geometries.
    os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"
    municipality_gdf = gpd.read_file(municipality_file)

    minx, miny, maxx, maxy = municipality_gdf.total_bounds

    # Lon, Lan switch, since leaflet (frontend) uses Lat, Lon and h3 Lon, Lat
    bbox_polygon = h3.LatLngPoly(
        [
            (miny, minx),  # (Lat, Lon)
            (maxy, minx),  # (Lat, Lon)
            (maxy, maxx),  # (Lat, Lon)
            (miny, maxx),  # (Lat, Lon)
        ]
    )

    for resolution in resolutions:
        logging.info(f"{'H3_GENERATE':<20} | Resolutie {resolution} gestart")

        h3_indices = h3.h3shape_to_cells(bbox_polygon, res=resolution)
        data = []
        for h3_index in h3_indices:
            shape = h3.cells_to_h3shape([h3_index])
            data.append({"geometry": shape, "h3_index": h3_index})

        h3_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")
        h3_gdf = gpd.overlay(municipality_gdf, h3_gdf, how="intersection")

        output_file = base_folder + f"raw/grid/res_{resolution}.geojson"

        h3_gdf.to_file(output_file, driver="GeoJSON")
        logging.info(f"{'FILE_SAVE':<20} | {output_file.split('/')[-1]} saved \n")


if __name__ == "__main__":
    generate_h3_grid(resolutions=[8, 9, 10])
