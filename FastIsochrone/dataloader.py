from .config import entryData

entryData['lon'] = entryData['geometry'].x
entryData['lat'] = entryData['geometry'].y

latitude = entryData['lat']
longitude = entryData['lon']
latlonTuple = list(zip(latitude, longitude))