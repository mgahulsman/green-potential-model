import pathlib
import geopandas
import pandas as pd


def municipality_tree_loader() -> geopandas:
    """'
    In this function all the filepaths are defined. Only the most important columns are saved.
    """
    script_dir = pathlib.Path(__file__).parent
    filepaths = {
        "Delft": "delft_trees.geojson",
        # "The Hague": "the_hague_trees.csv" # https://data.overheid.nl/dataset/bomen-csv#metadata,
        # NOTE the data of The Hague doesn't look correct when I compare it with:
        # https://experience.arcgis.com/experience/60100b5ce8444943a7ff4fd8f577f5d1/?org=DDH#data_s=id%3A6cb9371f18584708b01723d9c72714c2-Natuur_en_landschapsbeheer_5488%3A1621
    }
    tree_gdfs = []
    for city in filepaths.keys():
        tree_gdf = geopandas.read_file(
            script_dir.parent.parent / "data/trees" / filepaths[city]
        )[["BUURT", "WIJK"]]
        tree_gdf["GEMEENTE"] = city
        tree_gdf[["GEMEENTE", "BUURT", "WIJK"]]
        tree_gdfs.append(tree_gdf)

    return pd.concat(
        tree_gdfs, ignore_index=True
    )  # NOTE: when using multiple datasets make sure all columns have the same meaning


def load_wijken():
    ...  # delft wijken source: https://data.delft.nl/datasets/59174e8dc90c4f6ba028f985d4c0ac42_0/explore
