import folium
import json


with open("data/ambulance-station.json") as f:
    data = json.load(f)

m = folium.Map(location=[43.6548,-79.3884], zoom_start=12, tiles="CartoDB positron")

folium.GeoJson(
   data,
   name = "ambulance station locations",
   marker = folium.CircleMarker(
       radius=5,
       color = 'blue',
       fill = True,
       fill_color = 'blue',
       fill_opacity = 0.7,
   ),
   tooltip=folium.GeoJsonTooltip(fields = ['PLACE_N9'], aliases= ['Faculty: '])
).add_to(m)

m.save("index.html")
print("Done!")