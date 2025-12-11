from data_processors.building_processor import process_building_data
from data_processors.aggregate_restrictions import concat_restriction_areas
from data_processors.h3_processor import generate_uber_h3_grid
from data_processors.tree_processor import process_tree_data


def main():
    process_tree_data()
    process_building_data()  # TODO: add a restiction boundary like you did for the trees
    concat_restriction_areas()

    generate_uber_h3_grid()


if __name__ == "__main__":
    main()
