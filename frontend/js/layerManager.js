// frontend/js/layerManager.js

/**
 * Laadt een GeoJSON bestand en maakt een Leaflet GeoJSON layer aan.
 * @param {object} layerConfig - De configuratie van de laag (naam, url, style).
 * @returns {Promise<L.GeoJSON>} Een Promise die resolved met de Leaflet GeoJSON laag.
 */
function loadGeoJsonLayer(layerConfig) {
    return new Promise((resolve, reject) => {
        fetch(layerConfig.url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status} for ${layerConfig.url}`);
                }
                return response.json();
            })
            .then(data => {
                var geoJsonLayer = L.geoJson(data, {
                    style: function (feature) {
                        // Kan uitgebreid worden voor datagedreven styling (bijv. op basis van feature.properties)
                        return layerConfig.style;
                    },
                    pointToLayer: function (feature, latlng) {
                        return L.circleMarker(latlng, layerConfig.style);
                    },
                    onEachFeature: function(feature, layer) {
                        // Optioneel: voeg een popup toe
                        if (feature.properties && feature.properties.name) {
                            layer.bindPopup(feature.properties.name);
                        }
                    }
                });

                resolve(geoJsonLayer);
            })
            .catch(error => {
                console.error(`Error loading GeoJSON from ${layerConfig.url}:`, error);
                reject(error);
            });
    });
}
