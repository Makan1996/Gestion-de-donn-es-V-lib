import folium, pandas, ast, webbrowser
from bson.regex import Regex
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27018/")
mydb = myclient["tourpediaDB"]
mycol = mydb["ParisPlace"]

# initialize and create map
m = folium.Map(location=[48.856578, 2.351828], zoom_start=15)

query = {}
# query["address"] = Regex(u"rue de rome", "i")

projection = {}

res = mycol.find(query)#, projection=projection)

for i, x in enumerate(res):
    folium.Marker([x['lat'], x['lng']], popup=f"<i>{x['name']}</i>").add_to(m)
    if i > 100:
        break

m.save('map.html')
webbrowser.open('map.html')