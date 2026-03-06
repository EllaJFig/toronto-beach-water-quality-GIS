import folium
from folium.plugins import TimestampedGeoJson
import json


with open("data/toronto-beaches-water-quality.geojson") as f:
    wq_data = json.load(f)


counter = 0

features = []
for feature in wq_data['features']:
    props =feature['properties']
    geo = feature['geometry']
    
    #if info not there skip
    if props['collectionDate'] == None or props['eColi'] == None:
        continue
    
    counter += 1
    if counter % 50 == 0:
        continue

    #set colour based on eColi level Red >100 Green if <100
    if int(props['eColi']) > 100:
        colour = "red"
    else:
        colour = "green"

    cleanDate = str(props['collectionDate'])[:10]

    popup_html = f"<b>Beach:</b> {props['beachName']}<br><b>E.Coli:</b> {props['eColi']}"
    #create new feature using GeoJSON features
    newFeature = {
        'type': 'Feature',
        'geometry': geo,
        'properties': {
            'time': cleanDate,
            'duration': 'P1D',
            'style': {'color': colour,  'fillColor': colour, 'radius': 12},
            'icon' :'circle',
            'iconstyle': {
                'fillColor': colour,
                'color': colour,
                'fillOpacity': 0.8,
                'stroke': True,
                'radius': 10
            },
            'popup': popup_html
        }

    }
    #append to features
    features.append(newFeature)

#create map
m = folium.Map(location=[43.6548,-79.3884], zoom_start=12, tiles="CartoDB positron")

#create time stamp for map using TimestampedGeoJson
TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="P1W",
    duration='P1W',
    add_last_point=False,
    auto_play=False,
    loop=True,
    max_speed=1,    
    loop_button=True,
    date_options="YYYY-MM-DD",
    time_slider_drag_update=True
).add_to(m)

m.save("index.html")
