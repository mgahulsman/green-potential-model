import os
import logging
import geopandas as gpd
import pandas as pd
from datetime import datetime


def get_buffer_code(val):
    return f"{int(round(val * 100)):03d}"


def create_output_name(config):
    w = get_buffer_code(config["water"])
    b = get_buffer_code(config["buildings"])
    r = get_buffer_code(config["infra"])
    t = get_buffer_code(config["tree_restrictions"])
    return f"restr_w{w}b{b}r{r}t{t}.geojson"


def select_restriction_infra(df):
    restricted = [
        "rijbaan lokale weg",
        "fietspad",
        "inrit",
        "rijbaan regionale weg",
        "woonerf",
        "rijbaan autosnelweg",
        "OV-baan",
        "spoorbaan",
        "rijbaan autoweg",
        "baan voor vliegverkeer",
    ]
    return df.loc[df["bgt-functie"].isin(restricted)]


def process_restrictions(buffer_settings):
    base_folder = "C:/Users/maart/EigenMappen/Studie/laatste_bachelor_semester/bep/green-potential-model/new_structure/data/"
    raw_path = base_folder + "raw/restrictions/"

    municipality_gdf = gpd.read_file(
        base_folder + "raw/grid/delft_municipality.geojson", engine="pyogrio"
    )
    if municipality_gdf.crs != "EPSG:28992":
        municipality_gdf = municipality_gdf.to_crs("EPSG:28992")

    files = [
        "bgt_waterdeel.gml",
        "buildings.geojson",
        "bgt_wegdeel.gml",
        "bgt_vegetatieobject.gml",
    ]
    labels = ["water", "buildings", "infra", "tree_restrictions"]

    processed_layers = []

    logging.info(f"{'RESTRICTIONS':<20} | Start processing of {len(files)} layers")

    for file, label in zip(files, labels):
        layer_start = datetime.now()
        path = raw_path + file

        try:
            if not os.path.exists(path):
                logging.warning(f"{'FILE_MISSING':<20} | {file} not found")
                continue

            gdf = gpd.read_file(path, engine="pyogrio")
            if gdf.crs is None:
                gdf.set_crs("EPSG:28992", inplace=True)
            elif gdf.crs != "EPSG:28992":
                gdf = gdf.to_crs("EPSG:28992")

            # Specifieke filters
            if label == "infra":
                gdf = select_restriction_infra(gdf)
            elif label == "tree_restrictions":
                gdf = gdf.loc[gdf["plus-type"] == "boom"]
                # Voeg boompunten toe aan de lijst
                tree_points = gpd.GeoDataFrame(
                    {
                        "layer": ["tree_points"],
                        "geometry": [gdf.geometry.centroid.union_all()],
                    },
                    crs="EPSG:28992",
                )
                processed_layers.append(tree_points)

            # Buffer toepassen
            dist = buffer_settings[label]
            if dist > 0:
                gdf["geometry"] = gdf.geometry.buffer(dist)

            # Samenvoegen tot één polygoon per laag
            union_gdf = gpd.GeoDataFrame(
                {"layer": [label], "geometry": [gdf.union_all()]}, crs="EPSG:28992"
            )
            processed_layers.append(union_gdf)

            duration = (datetime.now() - layer_start).total_seconds()
            logging.info(
                f"{label.upper():<20} | Buffer: {dist:>4.2f}m | Loading time: {duration:>6.2f}s"
            )

        except Exception as e:
            logging.error(f"{'ERROR':<20} | Fout in {label}: {e}")

    if processed_layers:
        combined_gdf = gpd.GeoDataFrame(
            pd.concat(processed_layers, ignore_index=True), crs="EPSG:28992"
        )
        combined_gdf = combined_gdf.clip(municipality_gdf)
        combined_gdf = combined_gdf.to_crs(epsg=4326)

        output_filename = create_output_name(buffer_settings)
        output_path = base_folder + "processed/restrictions/" + output_filename

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        combined_gdf.to_file(output_path, driver="GeoJSON")
        logging.info(f"{'FILE_SAVE':<20} | {output_filename} saved \n")
