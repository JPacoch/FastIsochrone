import os
import sys
from main.convex_hull_isochrones import ConvexHullIsochrones
from main.buffer_isochrones import BufferIsochrones
from main.detailed_isochrones import DetailedIsochrones

from main.config import networkType, tripTimes, travelSpeed, epsgCode, networkDistance

myTestInstance = ConvexHullIsochrones(networkType, tripTimes, travelSpeed, epsgCode, networkDistance)
myTestInstance.createConvexHullIsochrones(plot=True)