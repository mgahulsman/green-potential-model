from pathlib import Path
import geopandas
import pandas as pd


def tree_processor() -> None:
    """'
    In this function all the tree filepaths are defined. A restriction area is added by adding circle
    """
    # NOTE: this function is build in such a way that more municipalities can be added
    dir_path = Path.cwd()
    data_folder = "data"
    raw_folder = "raw"
    tree_folder = "trees"
    processed_folder = "processed"
    raw_path = dir_path / data_folder / raw_folder / tree_folder
    processed_path = dir_path / data_folder / processed_folder

    filepaths = {
        "Delft": "delft_trees.geojson",
    }
    tree_gdfs = []
    for city in filepaths.keys():
        tree_gdf = geopandas.read_file(raw_path / filepaths[city])[["geometry"]]
        # TODO: Create a circel
        tree_gdfs.append(tree_gdf)

    tree_gdf = pd.concat(tree_gdfs, ignore_index=True)

    tree_gdf.to_file(processed_path / "trees.geojson", driver="GeoJSON")
