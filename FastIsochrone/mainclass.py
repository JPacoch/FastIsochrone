import networkx as nx
import osmnx as ox
from itertools import cycle

ox.config(log_console=True, use_cache=True)
ox.__version__

class InitClass():
    def __init__(self, networkType, tripTimes, travelSpeed, epsgCode, networkDistance):
        self.isochronePolygons = []
        self.networkType = networkType
        self.tripTimes = tripTimes
        self.travelSpeed = travelSpeed
        self.epsgCode = epsgCode
        self.networkDistance = networkDistance
        self.timeTable = cycle([25,20,15,10,5]) 
        self.isochroneColours = ox.plot.get_colors(n=len(self.tripTimes), cmap='plasma', start=0, return_hex=True)