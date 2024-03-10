from pathlib import Path
from PyBNG import PyBNG
import pandas as pd

# Back Tor 
# https://www.geograph.org.uk/location.php?gridref=SK1990&setref=Show+>&gridsquare=SK&eastings=24&northings=83
#
# Easting/Northing: 419500, 390500
# Lat/Long (decimal): 53.410955, -1.708114

# SK 18043 79421
# (4)18043 (3)79421

# Shining Tor
# https://www.geograph.org.uk/gridref/SJ9973
# Lat/Long (decimal): 53.258504, -2.008954
# Easting/Northing: 399500, 373500 [meters]
# SJ 99463 73739
# (3)99463 (3)73739

# Alphin Pike
# OSGB36: SE0029602817 [1 m precision]
# Easting/Northing: 400296, 402817 [meters]
# WGS84: 53:31.3213N 1:59.8203W
# Lat/Long (decimal): 53.522022, -1.997005

# Win Hill
# OSGB36: SK1867885093External link [1 m precision]
# Easting/Northing: 418678, 385093 [meters]
# WGS84: 53:21.7430N 1:43.2479W
# Lat/Long (decimal): 53.362384, -1.720798


root_dir = r"C:\Users\Fergu\source\Projects\Mapping\Data\Maps"
country = "England"
region = "PeakDistrict"
file = "PeakDistrictTrigPoints.csv"
data_path = Path(root_dir)
data_path = Path.joinpath(data_path,country,region,file)

df_trigs = pd.read_csv(data_path)
print (df_trigs.head())

def grid_to_latlong(grid_ref):
    # this function is used for populating the datframe
    _, _, lat, lon = convert_grid_reference(grid_ref)
    return lat, lon    
def convert_grid_reference(grid_ref):
    l_gref = grid_ref.split()
    map_grid = l_gref[0]
    eastings = l_gref[1]
    northings = l_gref[2]

    if map_grid == "SK":
        eastings = int(f'4{eastings}')
        northings = int(f'3{northings}')
    elif map_grid == "SJ":
        eastings = int(f'3{eastings}')
        northings = int(f'3{northings}')
    elif map_grid == "SE":
        eastings = int(f'4{eastings}')
        northings = int(f'4{northings}')
        
    bng = PyBNG(easting = eastings,northing = northings)
    lat_lon = bng.get_latlon()         
    lat = lat_lon[0] 
    lon = lat_lon[1]
    return eastings,northings,lat,lon

#df_trigs = df_trigs[['Lat', 'Long']] = df_trigs['Grid Reference'].apply(lambda x: pd.Series(convert_grid_reference(x)))
df_trigs[['Lat', 'Long']] = df_trigs['Grid Reference'].apply(
    lambda x: pd.Series(grid_to_latlong(x))
)

file = "PeakDistrictTrigPoints2.csv"
new_data_path = data_path.with_name(file)
df_trigs.to_csv(new_data_path, index=False)



# 52.76539938,-1.72462255
# 53.3624007,-1.72079693
# 53.362384, -1.720798

