import logging
from pathlib import Path
import geopandas as gpd
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine


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
    engine = create_engine("postgresql://user:pass@localhost:5432/green_potential")

    base_folder = Path(__file__).resolve().parent / "data"
    raw_path = base_folder / "raw/restrictions"
    municipality_path = base_folder / "raw/grid/delft_municipality.geojson"

    municipality_gdf = gpd.read_file(municipality_path, engine="pyogrio")
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
        path = raw_path / file

        try:
            if not path.exists():
                logging.warning(f"{'FILE_MISSING':<20} | {file} not found")
                continue

            gdf = gpd.read_file(path, engine="pyogrio")
            if gdf.crs is None:
                gdf.set_crs("EPSG:28992", inplace=True)
            elif gdf.crs != "EPSG:28992":
                gdf = gdf.to_crs("EPSG:28992")

            if label == "infra":
                gdf = select_restriction_infra(gdf)
            elif label == "tree_restrictions":
                gdf = gdf.loc[gdf["plus-type"] == "boom"]
                tree_points = gpd.GeoDataFrame(
                    {
                        "layer": ["tree_points"],
                        "geometry": [gdf.geometry.centroid.union_all()],
                    },
                    crs="EPSG:28992",
                ).to_crs("EPSG:4326")
                processed_layers.append(tree_points)

            dist = buffer_settings[label]
            if dist > 0:
                gdf["geometry"] = gdf.geometry.buffer(dist)

            union_gdf = gpd.GeoDataFrame(
                {"layer": [label], "geometry": [gdf.union_all()]}, crs="EPSG:28992"
            )
            union_gdf = union_gdf.clip(municipality_gdf).to_crs("EPSG:4326")

            processed_layers.append(union_gdf)
            # union_gdf.to_postgis(f"layer_{label}", engine, if_exists="replace", index=False)

            duration = (datetime.now() - layer_start).total_seconds()
            logging.info(
                f"{label.upper():<20} | Buffer: {dist:>4.2f}m | Loading time: {duration:>6.2f}s"
            )

        except Exception as e:
            logging.error(f"{'ERROR':<20} | Fout in {label}: {e}")

    if processed_layers:
        combined_gdf = gpd.GeoDataFrame(
            pd.concat(processed_layers, ignore_index=True), crs="EPSG:4326"
        )
        combined_gdf = combined_gdf.clip(municipality_gdf)
        combined_gdf = combined_gdf.to_crs(epsg=4326)
        # union = combined_gdf.union_all()
        combined_gdf.to_postgis(
            "restrictions_test", engine, if_exists="replace", index=True
        )
        logging.info(
            f"{'DB_SAVE':<20} | Data succesvol opgeslagen in tabel 'restrictions'"
        )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    process_restrictions(
        buffer_settings={
            "water": 0.00,
            "buildings": 0.20,
            "infra": 0.00,
            "tree_restrictions": 2.00,
        }
    )
