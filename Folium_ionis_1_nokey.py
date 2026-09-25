import folium
import webbrowser

m = folium.Map(
    location=[48.8566, 2.3522],
    zoom_start=12,
    tiles=None
)

folium.TileLayer(
    tiles=(
        "https://server.arcgisonline.com/ArcGIS/rest/services/"
        "World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    ),
    attr="Tiles © Esri",
    name="Esri World Street Map"
).add_to(m)

folium.Marker(
    location=[48.8584, 2.2945],
    popup="<b>Paris</b><br>Tour Eiffel",
    tooltip="Tour Eiffel"
).add_to(m)

folium.Marker(
    location=[48.85, 2.42],
    popup="<b>Paris</b><br>Point au hasard",
    tooltip="Point au hasard"
).add_to(m)

folium.Marker(
    location=[48.84, 2.30],
    popup="<b>Paris</b><br>IONIS École",
    tooltip="IONIS École"
).add_to(m)

m.save("map45.html")
webbrowser.open("map45.html")