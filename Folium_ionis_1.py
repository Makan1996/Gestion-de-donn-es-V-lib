import webbrowser

import folium

# On crée la map
m = folium.Map(location=[48.856, 2.294], zoom_start=12, tiles="OpenStreetMap")
#
folium.Marker(
    location=[48.85, 2.29],
    popup="<div><b>paris</b><br><a>tour eiffel</a></div>",
).add_to(m)

folium.Marker(
    location=[48.85, 2.42],
    popup="<di><b>paris</b><br><a> au hasard</a></div>",
).add_to(m)

folium.Marker(
    location=[48.84, 2.30],
    popup="<di><b>paris</b><br><a> ionis ecole</a></div>",
).add_to(m)
m.save("map1.html")

# open file in ie

# webbrowser.get('C:/Program Files/Internet Explorer/iexplore.exe %s').open('map1.html')
webbrowser.open('map1.html')  # open file in webbrowser