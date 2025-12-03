from pathlib import Path
import webbrowser
import geopandas as gpd
import folium


def visualize_data(page_name="index.html", open_browser=True):
    edges_gdf = gpd.read_file("data/roads/delft_edges.geojson")
    test_gdf = gpd.read_file("data/test.geojson")

    # NOTE: Optioneel: Herprojecteer naar WGS 84 (EPSG:4326),
    # de standaard voor webkaarten, als uw data dit nog niet is.
    # Dit zorgt voor compatibiliteit met Folium/Leaflet.
    if edges_gdf.crs and edges_gdf.crs.to_epsg() != 4326:
        edges_gdf = edges_gdf.to_crs(epsg=4326)

    center = edges_gdf.geometry.union_all().centroid
    m = folium.Map(location=[center.y, center.x], zoom_start=12)

    folium.GeoJson(
        edges_gdf.to_json(),
        name="Wegennetwerk",
        style_function=lambda x: {"color": "red", "weight": 2, "opacity": 0.7},
    ).add_to(m)

    folium.GeoJson(
        test_gdf.to_json(),
        name="test",
        style_function=lambda x: {"color": "blue", "weight": 2, "opacity": 0.7},
        tooltip=folium.features.GeoJsonTooltip(
            fields=["Naam"],
            aliases=["Testttt:"],
        ),
    ).add_to(m)

    m.save(page_name)

    if open_browser:
        dir_path = Path.cwd()
        index_file = page_name
        full_path = dir_path / index_file
        webbrowser.open(str(full_path))
