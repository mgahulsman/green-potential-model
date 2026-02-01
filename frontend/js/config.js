const MAP_SETTINGS = {
    center: [52.0116, 4.3571], // Delft
    zoom: 13,
    tiles: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'
};

const DATA_PATHS = {
    grids: (name) => `../data/raw/grid/${name}.geojson`,
    restrictions: '../data/processed/restrictions/restr_w000b020r000t200.topojson',
    results: (grid, scenario) => `../data/processed/final_results/analysis_${grid}_${scenario}.geojson`
};

const STYLE_PALETTE = {
    water: '#3498db',
    buildings: '#34495e',
    infra: '#e67e22',
    tree_restrictions: '#27ae60',
    tree_points: '#d35400'
};
