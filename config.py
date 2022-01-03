import os
import geopandas as gpd

PROJECT_DIR = os.path.abspath(".")
entryData = gpd.read_file("input/test.shp")

networkType = 'drive' #okreslenie sieci; walk, drive etc
tripTimes = [5,10,15,20,25] #zakres izochrony w minutach
travelSpeed = 50 #predkosc podrozy w kmh