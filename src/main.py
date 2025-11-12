from dataloader import dataloader
from tree_density import tree_density


def main():
    tree_data = dataloader()
    tree_density(tree_data)


if __name__ == "__main__":
    main()
