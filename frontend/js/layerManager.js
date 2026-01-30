function getScoreColor(val, low, high) {
    let ratio = Math.max(0, Math.min(1, (val - low) / (high - low)));
    const rgb = ratio < 0.5
        ? [231 + (241-231)*ratio*2, 76 + (196-76)*ratio*2, 60 + (15-60)*ratio*2]
        : [241 + (46-241)*(ratio-0.5)*2, 196 + (204-196)*(ratio-0.5)*2, 15 + (113-15)*(ratio-0.5)*2];
    return `rgb(${rgb.map(Math.floor).join(',')})`;
}

async function fetchGeoJSON(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (e) {
        console.error("Load Error:", e);
        return null;
    }
}
