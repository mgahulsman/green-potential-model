import logging
import s1_h3_generator
import s2_restriction_processor
import s3_analyzer


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    logging.getLogger("fiona").setLevel(logging.WARNING)
    logging.getLogger("pyogrio").setLevel(logging.WARNING)
    logging.getLogger("geopandas").setLevel(logging.WARNING)

    logging.info(f"{'ACTIE':<20} | {'RESULTAAT/DETAILS':<40}")
    logging.info("-" * 65)

    s1_h3_generator.generate_h3_grid(resolutions=[8, 9, 10])

    s2_restriction_processor.process_restrictions(
        buffer_settings={
            "water": 0.00,
            "buildings": 0.20,
            "infra": 0.00,
            "tree_restrictions": 2.00,
        }
    )

    s3_analyzer.run_s3_analysis()
