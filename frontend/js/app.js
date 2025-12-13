// frontend/js/app.js

var map;
var baseLayer;
var overlayLayers = {};

/**
 * Initialiseert de kaart en de basislaag.
 */
function initializeMap() {
map = L.map('map').setView(INITIAL_VIEW_COORDINATES, INITIAL_ZOOM_LEVEL);
    baseLayer = L.tileLayer(BASE_LAYER_URL, {
        maxZoom: MAX_ZOOM,
        attribution: BASE_LAYER_ATTRIBUTION
    }).addTo(map);
}

/**
 * Laadt alle overlays en voegt de Layer Control toe.
 */
function loadAndControlLayers() {
    // Maak een array van Promises voor elke overlay
    const layerPromises = OVERLAY_LAYERS_CONFIG.map(config => {
        return loadGeoJsonLayer(config)
            .then(layer => {
                // Sla de Leaflet laag op met de geconfigureerde naam
                overlayLayers[config.name] = layer;

                // Voeg de laag toe aan de kaart indien geconfigureerd
                if (config.addToMap) {
                    layer.addTo(map);
                }
                return layer;
            });
    });

    // Wacht tot alle lagen geladen zijn
    Promise.all(layerPromises)
        .then(() => {
            const baseMaps = {
                "CARTO Light": baseLayer
            };

            // Voeg de Leaflet Layer Control toe
            L.control.layers(baseMaps, overlayLayers).addTo(map);
            console.log("Alle GeoJSON lagen succesvol geladen en Layer Control toegevoegd.");
        })
        .catch(error => {
            console.error("Een of meerdere GeoJSON lagen konden niet geladen worden:", error);
        });
}

// Start de applicatie
document.addEventListener('DOMContentLoaded', () => {
    initializeMap();
    loadAndControlLayers();
});


document.getElementById('run-btn').addEventListener('click', () => {
    const btn = document.getElementById('run-btn');
    btn.disabled = true;
    btn.innerText = "Bezig met rekenen...";

    // Gebruik de sync versie als je wilt wachten tot het klaar is om de kaart te verversen
    fetch('http://127.0.0.1:8000/run-analysis-sync', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        alert("Klaar! De kaart wordt ververst.");

        // Herlaad de pagina of herlaad specifiek de lagen
        location.reload();
    })
    .catch(error => {
        console.error('Er ging iets mis:', error);
        alert("Fout tijdens uitvoeren analyse.");
    })
    .finally(() => {
        btn.disabled = false;
        btn.innerText = "Draai Analyse";
    });
});
