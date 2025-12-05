import webbrowser
from data_processors.building_processor import process_building_data
from data_processors.tree_processor import process_tree_data
from src.config import open_browser


def main():
    process_tree_data()
    process_building_data()  # TODO: add a restiction boundary like you did for the trees
    open_new_map()


def open_new_map() -> None:
    if open_browser:
        webbrowser.open(str("index.html"))


if __name__ == "__main__":
    main()
