import folium
import pandas


volcanoes_data=pandas.read_csv("Volcanoes.txt")


map=folium.Map(location=[43.643466,-79.379056], zoom_start=5, tiles="Stamen Terrain")

#individual lists of separate volcano data
name = list(volcanoes_data["NAME"])
latitude = list(volcanoes_data["LAT"])
longitude = list(volcanoes_data["LON"])
elevation = list(volcanoes_data["ELEV"])
types = list(volcanoes_data["TYPE"])

wiki = """
<b>Volcano Name:</b><br><a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
<b>Type of Volcano:</b> %s
<br>
<b>Height:</b> %s m
"""

#function for determining the color depending on the elevation range
def elev_range(el):
    if el < 1500:
        return 'green'
    elif 1500<=el<=2500:
        return 'orange'
    else:
        return 'red'

volcano_features= folium.FeatureGroup(name="Volcanoes in America")
population_features=folium.FeatureGroup(name="Populations by Country")
#features.add_child(folium.Marker(location=[43.643466,-79.379056], popup="Volcano", icon=folium.Icon(color='red')))

for name,typ,elev,lat,long in zip(name,types,elevation,latitude,longitude):
    iframe = folium.IFrame(html= wiki % (name,name,typ,elev), width=200, height=200)

    volcano_features.add_child(folium.CircleMarker(location=[lat,long], radius=6, popup=folium.Popup(iframe), tooltip=name, icon=folium.Icon(color=elev_range(elev)),
      fill_color=elev_range(elev), color='black', fill_opacity=0.5))
            
#add polygons to map by loading the json data into a file object
population_features.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000 else 'yellow' if 10000000<= x['properties']['POP2005']<50000000
else 'orange' if 50000000<=x['properties']['POP2005']<100000000 else 'red'}))


map.add_child(volcano_features)
map.add_child(population_features)
map.add_child(folium.LayerControl()) #options to switch between layers/maps. 
#NOTE: LayerControl() must be added AFTER feature groups

map.save("Volcanoes Map.html")
