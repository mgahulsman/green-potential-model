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
                        // Haal de basisstijl op uit config.js
                        const baseStyle = layerConfig.style; //

                        // Controleer of de 'cel_color' eigenschap bestaat in de GeoJSON feature
                        if (feature.properties && feature.properties.cel_color) {
                            const dataColor = feature.properties.cel_color; //

                            // Return een nieuwe stijl: kopieer de basisstijl, maar overschrijf de kleuren
                            return {
                                ...baseStyle, // Behoud eigenschappen zoals weight en fillOpacity
                                color: dataColor, // Gebruik de kleur uit de data voor de rand
                                fillColor: dataColor // Gebruik de kleur uit de data voor de vulling
                            };
                        }

                        // Val terug op de standaardstijl uit config.js
                        return baseStyle;
                    },
                    pointToLayer: function (feature, latlng) {
                        // De stijl wordt opgehaald via de bovenstaande functie
                        const style = this.options.style(feature);
                        return L.circleMarker(latlng, style);
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
