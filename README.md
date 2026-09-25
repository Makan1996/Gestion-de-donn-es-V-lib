# Projet Big Data : MongoDB, Hadoop MapReduce et Visualisation Folium

[![GitHub](https://img.shields.io/badge/GitHub-Makan1996-blue?logo=github)](https://github.com/Makan1996)
**Auteur :** Jordan NJOBEN  
**Formation :** Master 2 - IONIS-STM  
**Module :** Gestion des Données & Hadoop  

---

## 📌 Présentation du Projet

Ce projet a pour objectif de traiter et d'analyser des données de mobilité urbaine (données en temps réel des stations Vélib Île-de-France) ainsi que des données transactionnelles à travers deux paradigmes complémentaires :
1. **Base de données NoSQL (MongoDB + Navicat)** : Ingestion, filtrage et agrégations MapReduce en JavaScript.
2. **Calcul Distribué (Hadoop MapReduce in Java)** : Compilation et exécution de jobs MapReduce sous un environnement Hadoop.
3. **Restitution Cartographique (Python + Folium)** : Géocodage et génération de cartes interactives avec intégration Google Street View.

---

## 📁 Inventaire des Fichiers du Projet

| Fichier | Catégorie | Description |
| :--- | :--- | :--- |
| `velib-disponibilite-en-temps-reel.json` | Données | Jeu de données source contenant l'état des stations Vélib (3 036 stations). |
| `donnees.csv` | Données | Jeu de données transactionnel (100 000 lignes) pour l'analyse de co-occurrences. |
| `_mongodb_requetes_M2.docx` | Documentation | Consignes et requêtes NoSQL / MapReduce pour MongoDB. |
| `MonDriver.java` | Hadoop Java | Classe Driver configurant et soumettant le Job Hadoop MapReduce. |
| `MonMapper.java` | Hadoop Java | Classe Mapper effectuant l'extraction des paires de clés/valeurs. |
| `MonReducer.java` | Hadoop Java | Classe Reducer effectuant l'agrégation et le tri des fréquences associées. |
| `mongod6.py` | Python | Connexion à MongoDB (`pymongo`) et extraction des documents. |
| `Folium_ionis_1.py` | Python | Script de démonstration de génération de cartes avec des marqueurs simples. |
| `Folium2.py` | Python | Connexion MongoDB ➔ Folium avec affichage sur carte HTML. |
| `yutopia_velib_geopy_final_revu.py` | Python | Script complet de géocodage (`geopy`), calcul de distance géodésique et carte interactive Folium (fonds Esri). |

---

## 🛠️ 1. Traitements MongoDB (Navicat)

### Ingestion et Filtrage (`find`)
- **Base :** `VélibDB` | **Collection :** `velibCol`
- **Exemples de requêtes :**
  ```javascript
  // Consultation globale
  db.velibCol.find()

  // Filtrage des stations de Créteil
  db.velibCol.find({"nom_arrondissement_communes": "Créteil"})

  // Filtrage combiné : Paris + e-bikes > 10
  db.getCollection("velibCol").find(
    {"nom_arrondissement_communes": "Paris", "ebike": {$gt : 10}},
    {"name":1, "capacity":1, "_id":0, "ebike":1, "coordonnees_geo":1}
  ).sort({"ebike": -1})
  ```

### Agrégations MapReduce NoSQL
- **Nombre de stations par commune (`nb_station_velib_commune_ionis`)**
- **Nombre d'e-bikes par commune (`nb_ebike_commune_ionis`)**
- **Capacité totale par commune (`nb_velibmaxi_commune`)**
- **Liste des stations par commune (`liste_rue_commune`)**

---

## 🚀 2. Traitement Hadoop MapReduce (Java & Docker)

Le traitement MapReduce Java s'appuie sur les classes de l'enseignant : `MonDriver.java`, `MonMapper.java`, et `MonReducer.java`.

### Compilation et Packaging
Les classes sont compilées en bytecode Java 8 et empaquetées dans l'archive JAR :

```powershell
javac -source 1.8 -target 1.8 -cp "hadoop-common.jar;hadoop-mapreduce-client-core.jar" MonMapper.java MonReducer.java MonDriver.java
jar -cvf MonPremierMapReduce.jar MonMapper.class MonReducer.class MonDriver.class "MonReducer$1.class"
```

### Exécution sous Hadoop (Docker)
Le Job est soumis sur le conteneur Hadoop (`hadoop-single-node`) :

```bash
# 1. Copier les données et le JAR dans le conteneur
docker cp MonPremierMapReduce.jar hadoop-single-node:/tmp/
docker cp donnees.csv hadoop-single-node:/tmp/

# 2. Préparer le dossier d'entrée dans /mpmr/input
docker exec -u root hadoop-single-node mkdir -p /mpmr/input
docker exec -u root hadoop-single-node cp /tmp/donnees.csv /mpmr/input/
docker exec -u root hadoop-single-node rm -rf /mpmr/output

# 3. Lancer le Job MapReduce Hadoop
docker exec hadoop-single-node /opt/hadoop/bin/hadoop jar /tmp/MonPremierMapReduce.jar MonDriver

# 4. Consulter les résultats générés par le Reducer
docker exec hadoop-single-node head -n 20 /mpmr/output/part-r-00000
```

---

## 🗺️ 3. Visualisation Cartographique Interactive (Folium)

Le script Python `yutopia_velib_geopy_final_revu.py` permet de générer une carte HTML interactive personnalisée.

### Fonctionnement :
1. **Géocodage** : Conversion de l'adresse saisie en coordonnées `(latitude, longitude)` grâce à `geopy.geocoders.Nominatim`.
2. **Calcul de proximité** : Filtrage des stations Vélib dans un rayon défini avec `geopy.distance.geodesic`.
3. **Fonds de carte Esri** : Utilisation du service de tuiles Esri (`World_Street_Map`) pour éviter tout blocage d'accès `403`.
4. **Popups HTML & Street View** : Affichage du nombre d'e-bikes, vélos mécaniques, docks disponibles et lien direct Google Maps Street View.

### Commande de lancement :
```powershell
python yutopia_velib_geopy_final_revu.py
```
*Saisissez une adresse (ex: `Créteil` ou `Paris Gare de Lyon`), et le fichier `map.html` s'ouvrira automatiquement dans le navigateur.*

---

## 📊 Résumé des Résultats

- **MongoDB** : 3 036 documents analysés, filtrages par commune et agrégations JavaScript réussies.
- **Hadoop MapReduce** : 100 000 lignes de transactions analysées, 719 630 paires générées et regroupées par le Reducer.
- **Folium** : Affichage cartographique temps réel fluide des stations Vélib à proximité de l'utilisateur.

---
*Projet hébergé sur GitHub : [https://github.com/Makan1996](https://github.com/Makan1996)*
