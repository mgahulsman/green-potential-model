from data_processors.tree_processor import process_tree_data
from visualizer import visualize_processed_data


def main():
    # tree_data = municipality_tree_loader()
    # tree_density(tree_data)
    processed_file = process_tree_data()
    visualize_processed_data(processed_file)


if __name__ == "__main__":
    main()
