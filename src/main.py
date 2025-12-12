import logging
from data_processors.aggregate_restrictions import concat_restriction_areas
from data_processors.building_processor import process_building_data
from data_processors.h3_processor import generate_uber_h3_grid
from data_processors.tree_processor import process_tree_data


def main():
    logging.basicConfig(
        level=logging.INFO,  # Zorgt ervoor dat INFO-berichten zichtbaar zijn
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Set the level to WARNING, so that only warnings and errors are shown
    logging.getLogger("pyogrio").setLevel(logging.WARNING)

    logging.info("Applicatie gestart.")

    process_tree_data()
    process_building_data()  # TODO: add a restiction boundary like you did for the trees
    concat_restriction_areas()

    generate_uber_h3_grid()

    logging.info("Loaded all geojsons successfully.")


if __name__ == "__main__":
    main()
