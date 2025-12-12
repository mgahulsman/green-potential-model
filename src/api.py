# src/api.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging

# Importeer je bestaande functies
from src.data_processors.aggregate_restrictions import concat_restriction_areas
from src.data_processors.building_processor import process_building_data
from src.data_processors.h3_processor import generate_uber_h3_grid
from src.data_processors.tree_processor import process_tree_data

# Initialiseer de app
app = FastAPI()

# CORS configuratie (zodat je frontend erbij mag)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In productie zet je hier de specifieke URL van je frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)


def run_pipeline():
    """Voert de volledige pijplijn uit zoals in je oude main.py"""
    logging.info("Start verwerking via API...")
    process_tree_data()
    process_building_data()
    concat_restriction_areas()
    generate_uber_h3_grid()
    logging.info("Verwerking voltooid.")


@app.post("/run-analysis")
async def run_analysis(background_tasks: BackgroundTasks):
    """
    Endpoint die de frontend kan aanroepen.
    We gebruiken BackgroundTasks zodat de API direct 'OK' antwoordt
    terwijl de zware berekening op de achtergrond draait.
    """
    background_tasks.add_task(run_pipeline)
    return {"message": "Analyse gestart, dit kan even duren."}


# Optioneel: Een synchrone versie als je wilt wachten op het resultaat voordat je de kaart ververst
@app.post("/run-analysis-sync")
def run_analysis_sync():
    run_pipeline()
    return {"message": "Analyse voltooid en bestanden bijgewerkt."}
