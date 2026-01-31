const MAP_SETTINGS = {
    center: [52.0116, 4.3571], // Delft
    zoom: 13,
    tiles: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'
};

const API_BASE = "http://localhost:8000/api";

const DATA_PATHS = {
    grids: (name) => `${API_BASE}/results/${name}/s1`,
    // TODO: This is not correct yet
    restrictions: `${API_BASE}/results/delft_municipality/s2`,
    results: (grid, scenario) => `${API_BASE}/results/${grid}/${scenario}`
};

const STYLE_PALETTE = {
    water: '#3498db',
    buildings: '#34495e',
    infra: '#e67e22',
    tree_restrictions: '#27ae60',
    tree_points: '#d35400'
};
