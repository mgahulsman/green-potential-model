from dataloader import dataloader


def main():
    delft_tree_data_path = "data/delft_trees.geojson"
    delft_tree_data = dataloader(delft_tree_data_path)
    print(delft_tree_data)


if __name__ == "__main__":
    main()
