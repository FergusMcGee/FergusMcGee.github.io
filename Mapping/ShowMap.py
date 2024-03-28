from pathlib import Path
import pandas as pd
import folium
import webbrowser


root_dir = r"source\FergusMcGee.github.io\Mapping\Data\Maps"
country = "England"

region = "PeakDistrict"
map_file = "PeakDistrictTrigPoints2.csv"
map_file = "PeakDistrictTrigPoints.json"
# region = "Lakes"
# map_file = "Wainwrights.csv"

data_path = Path(root_dir)
data_path = Path.joinpath(Path.home(),data_path,country,region,map_file)
zoom_level = 10

color_map = {
    'X': 'cadetblue',
    'Y': 'darkblue'
}

df_map_points = pd.read_json(data_path)
#df_ticked = df_map_points.query("Ticked != ''")
try:
    map_center = [df_map_points['Latitude'].mean(), df_map_points['Longitude'].mean()]
    
except KeyError:
    try:
        map_center = [df_map_points['Lat'].mean(), df_map_points['Long'].mean()]
    except KeyError:
        print("Latitude/Longitude coordinates not found.")
        exit()
        
mymap = folium.Map(location=map_center, zoom_start=zoom_level)

for _, row in df_map_points.iterrows():
    marker_color = color_map.get(row['Ticked'], 'lightgray')
    marker_icon = 'star' if row['Ticked'] == 'Y' else 'star-empty'
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Name'],
        tooltip=row['Name'],
        icon=folium.Icon(icon=marker_icon,color=marker_color)
    ).add_to(mymap)

#print (df_ticked.head())

map_file = map_file.replace("json","html")
map_file = data_path.with_name(map_file)
mymap.save(map_file)

webbrowser.open(map_file)
