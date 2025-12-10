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
