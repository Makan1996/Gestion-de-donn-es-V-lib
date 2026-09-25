import folium
import pymongo
import webbrowser
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# 1. Initialiser le géocodeur Nominatim
geolocator = Nominatim(user_agent="application_velib_ionis_student")

# 2. Demander l'adresse de départ à l'utilisateur
adresse = input("Entrez une adresse ou une ville (ex: Créteil ou Paris Gare de Lyon) : ")

# 3. Récupérer les coordonnées de l'adresse
location = geolocator.geocode(adresse)

if location:
    print(f"\n✅ Adresse trouvée : {location.address}")
    print(f"📍 Latitude : {location.latitude}, Longitude : {location.longitude}\n")

    # 4. Créer la carte avec des tuiles Esri / CartoDB (qui ne bloquent pas l'accès 403)
    m = folium.Map(location=[location.latitude, location.longitude], zoom_start=15, tiles=None)

    # Ajouter la couche de carte Esri World Street Map (utilisée par le professeur)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri",
        name="Esri World Street Map"
    ).add_to(m)

    # Ajouter le marqueur vert de la position de départ
    folium.Marker(
        [location.latitude, location.longitude],
        popup=f"<b>Votre position de départ :</b><br>{adresse}",
        icon=folium.Icon(color='green', icon='info-sign')
    ).add_to(m)

    # 5. Connexion à votre base MongoDB locale
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["VélibDB"]
    col = db["velibCol"]

    stations = list(col.find())
    stations_trouvees = 0

    # 6. Parcourir toutes les stations et calculer la distance
    for station in stations:
        coord = station.get('coordonnees_geo')
        if not coord:
            continue
        
        # Récupération de lat et lon selon la structure des documents
        lat = coord.get('lat') if isinstance(coord, dict) else coord[0]
        lon = coord.get('lon') if isinstance(coord, dict) else coord[1]

        # Calcul de la distance en mètres entre l'adresse et la station
        distance = geodesic((location.latitude, location.longitude), (lat, lon)).meters

        # Filtrer les stations proches (ex: à moins de 800 mètres)
        if distance <= 800:
            stations_trouvees += 1
            nom = station.get('name', 'Station Vélib')
            ebikes = station.get('ebike', 0)
            mecaniques = station.get('mechanical', 0)
            docks = station.get('numdocksavailable', 0)

            street_view_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"

            # Fenêtre popup HTML de la station
            html_popup = f"""
            <div style="font-family: Arial, sans-serif; width: 220px;">
                <h4 style="color: #2c3e50; margin: 0 0 8px 0;">{nom}</h4>
                <p style="margin: 3px 0;">⚡ <b>E-bikes :</b> {ebikes}</p>
                <p style="margin: 3px 0;">🚲 <b>Mécaniques :</b> {mecaniques}</p>
                <p style="margin: 3px 0;">🅿️ <b>Docks libres :</b> {docks}</p>
                <p style="margin: 5px 0; color: #7f8c8d;">📏 <b>Distance :</b> {int(distance)} m</p>
                <a href="{street_view_url}" target="_blank" style="display: inline-block; background-color: #3498db; color: white; padding: 6px 10px; text-decoration: none; border-radius: 4px; margin-top: 6px; font-size: 12px;">Voir dans Street View</a>
            </div>
            """

            folium.Marker(
                [lat, lon],
                popup=folium.Popup(html_popup, max_width=300),
                icon=folium.Icon(color='blue', icon='bike', prefix='fa')
            ).add_to(m)

    # 7. Sauvegarder et ouvrir la carte dans le navigateur
    m.save("carte_velib_interactive.html")
    print(f"🗺️ {stations_trouvees} stations trouvées dans un rayon de 800m.")
    print("🌍 Ouverture de la carte interactive 'carte_velib_interactive.html' dans votre navigateur...")
    webbrowser.open("carte_velib_interactive.html")

else:
    print("❌ Adresse non trouvée, veuillez réessayer.")