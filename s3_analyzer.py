import geopandas as gpd
import pandas as pd
import numpy as np
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

logger = logging.getLogger(__name__)


class GreenPotentialAnalyzer:
    def __init__(self, restriction_path: Path, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        os.environ["OGR_GEOJSON_MAX_OBJ_SIZE"] = "0"

        self.restr_gdf = gpd.read_file(restriction_path, engine="pyogrio").to_crs(
            "EPSG:28992"
        )
        self.tree_points = self.restr_gdf[
            self.restr_gdf["layer"] == "tree_points"
        ].explode(index_parts=False)

        self.scenarios = {
            "s1": {"layers": [], "desc": "Unconstrained Baseline"},
            "s2": {
                "layers": ["water", "buildings", "infra"],
                "desc": "Large Areal Constraints",
            },
            "s3": {
                "layers": ["water", "buildings", "infra", "tree_restrictions"],
                "desc": "Full Constraints",
            },
        }

    @staticmethod
    def calculate_tei(scores: pd.Series):
        s_sorted = np.sort(scores.values)
        m = len(s_sorted)
        if m == 0 or np.mean(s_sorted) == 0:
            return 0.0, 0.0

        mean_sg = np.mean(s_sorted)
        indices = np.arange(1, m + 1)
        total_sum = np.sum(indices * (s_sorted - mean_sg))
        return float((2 / (m**2 * mean_sg)) * total_sum), float(mean_sg)

    def process_single_grid(self, grid_path: Path):
        grid_name = grid_path.stem
        logging.info(f"{'GRID_START':<20} | Initiating analysis for {grid_name}")

        grid_gdf = gpd.read_file(grid_path, engine="pyogrio").to_crs("EPSG:28992")
        grid_gdf["cell_id"] = grid_gdf.index
        grid_gdf["area_total"] = grid_gdf.geometry.area

        trees_in_cells = gpd.sjoin(
            self.tree_points, grid_gdf, how="inner", predicate="within"
        )
        tree_counts = trees_in_cells.groupby("cell_id").size()
        grid_gdf["tree_count"] = grid_gdf["cell_id"].map(tree_counts).fillna(0)

        for sid, info in self.scenarios.items():
            logging.info(
                f"{sid.upper() + '_PROCESS':<20} | Computing scenario for {grid_name}"
            )
            temp_gdf = grid_gdf.copy()

            if sid == "s1":
                temp_gdf["area_restricted"] = 0.0
            else:
                subset = self.restr_gdf[self.restr_gdf["layer"].isin(info["layers"])]
                intersections = gpd.overlay(subset, grid_gdf, how="intersection")
                res_area = intersections.groupby("cell_id").geometry.apply(
                    lambda x: x.area.sum()
                )
                temp_gdf["area_restricted"] = (
                    temp_gdf["cell_id"].map(res_area).fillna(0)
                )

            temp_gdf["area_potential"] = (
                temp_gdf["area_total"] - temp_gdf["area_restricted"]
            ).clip(lower=0)
            temp_gdf["green_score"] = np.where(
                temp_gdf["area_potential"] > 0,
                temp_gdf["tree_count"] / temp_gdf["area_potential"],
                0.0,
            )

            tei, mean_sg = self.calculate_tei(temp_gdf["green_score"])
            self._save_results(temp_gdf, sid, grid_name, info, tei, mean_sg)

        logging.info(f"{'GRID_COMPLETE':<20} | All scenarios finished for {grid_name}")

    def _save_results(self, gdf, sid, grid_name, info, tei, mean_sg):
        output_path = self.output_dir / f"analysis_{grid_name}_{sid}.geojson"
        cols = [
            "area_total",
            "area_restricted",
            "tree_count",
            "area_potential",
            "green_score",
            "geometry",
        ]
        if "h3_index" in gdf.columns:
            cols.append("h3_index")

        final_gdf = gdf[cols].to_crs(epsg=4326)
        result_json = json.loads(final_gdf.to_json())
        result_json.update(
            {
                "tei_score": tei,
                "mean_green_score": mean_sg,
                "metadata": {
                    "grid": grid_name,
                    "scenario": sid,
                    "timestamp": datetime.now().isoformat(),
                },
            }
        )

        with open(output_path, "w") as f:
            json.dump(result_json, f)
        logging.info(f"{'FILE_SAVE':<20} | {output_path.name}")


def run_worker(grid_file, restriction_file, output_dir):
    analyzer = GreenPotentialAnalyzer(restriction_file, output_dir)
    analyzer.process_single_grid(grid_file)


def run_s3_analysis():
    base_path = Path(
        "C:/Users/maart/EigenMappen/Studie/laatste_bachelor_semester/bep/green-potential-model/new_structure/data"
    )
    grid_dir = base_path / "raw/grid"
    restr_file = base_path / "processed/restrictions/restr_w000b020r000t200.geojson"
    output_dir = base_path / "processed/final_results"

    grid_files = list(grid_dir.glob("*.geojson"))

    logging.info(f"{'POOL_START':<20} | Deploying {len(grid_files)} parallel workers")
    with ProcessPoolExecutor() as executor:
        executor.map(
            run_worker,
            grid_files,
            [restr_file] * len(grid_files),
            [output_dir] * len(grid_files),
        )
    logging.info(f"{'ANALYSIS_DONE':<20} | Processing pipeline completed")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )

    run_s3_analysis()
