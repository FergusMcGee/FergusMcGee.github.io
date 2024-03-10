from pathlib import Path
import pandas as pd
import folium
import webbrowser


root_dir = r"source\Projects\Mapping\Data\Maps"
country = "England"

region = "PeakDistrict"
map_file = "PeakDistrictTrigPoints2.csv"
region = "Lakes"
map_file = "Wainwrights.csv"

data_path = Path(root_dir)
data_path = Path.joinpath(Path.home(),data_path,country,region,map_file)
zoom_level = 10

df_map_points = pd.read_csv(data_path)
df_ticked = df_map_points.query("Ticked == 1")
try:
    map_center = [df_map_points['Latitude'].mean(), df_map_points['Longitude'].mean()]
except KeyError:
    print("Latitude/Longiyude coordinates not found.")
    exit()
        
mymap = folium.Map(location=map_center, zoom_start=zoom_level)

for _, row in df_map_points.iterrows():
    marker_color = 'darkblue' if row['Ticked'] == 1 else 'lightgray'
    marker_icon = 'star' if row['Ticked'] == 1 else 'star-empty'
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Name'],
        icon=folium.Icon(icon=marker_icon,color=marker_color)
    ).add_to(mymap)

#print (df_ticked.head())

map_file = f"{map_file}.html"
map_file = data_path.with_name(map_file)
mymap.save(map_file)

webbrowser.open(map_file)
