// frontend/js/config.js

// Basislaag configuratie
const BASE_LAYER_URL = 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png';
const BASE_LAYER_ATTRIBUTION = '© OpenStreetMap contributors & © CARTO';

// Kaart Initiële Weergave Configuratie
const INITIAL_VIEW_COORDINATES = [52.00, 4.36];
const INITIAL_ZOOM_LEVEL = 13;
const MAX_ZOOM = 19

// Overlays (GeoJSON Lagen)
const OVERLAY_LAYERS_CONFIG = [
    {
        name: 'Tree Area',
        url: '../data/processed/merged_tree_area.geojson',
        addToMap: true,
        style: {
            fillColor: '#1A9988',
            fillOpacity: 1,
            weight: 1
        }
    },
    {
        name: 'Building Buffer',
        url: '../data/processed/merged_building_area_buffer.geojson',
        addToMap: true,
        style: {
            fillColor: '#E9EDEE',
            fillOpacity: 1,
            weight: 1
        }
    },
    {
        name: 'Restriction Area',
        url: '../data/processed/total_restriction_area.geojson',
        addToMap: false,
        style: {
            color: '#EB5600',
            fillColor: '#EB5600',
            fillOpacity: 0,
            weight: 3
        }
    },
    // **NIEUWE LAAG VOOR JE GRID/BUURTEN**
    {
        name: 'Neighborhood Grid',
        url: '../data/processed/neighborhood_grid.geojson', // Zorg dat dit bestand bestaat
        addToMap: false,
        style: {
            color: '#0070FF',
            fillColor: '#0070FF',
            fillOpacity: 0.2,
            weight: 2
        }
    }
];
