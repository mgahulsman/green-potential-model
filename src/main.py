from dataloaders.municipality_trees import municipality_tree_loader
from tree_density import tree_density
from visualizer import visualize_data


def main():
    tree_data = municipality_tree_loader()
    tree_density(tree_data)
    visualize_data()


if __name__ == "__main__":
    main()
