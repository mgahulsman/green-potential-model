import pathlib
import geopandas


def dataloader(filepath: str) -> geopandas:
    script_dir = pathlib.Path(__file__).parent
    path_to_data = script_dir.parent / filepath
    gdf = geopandas.read_file(path_to_data)

    return gdf
