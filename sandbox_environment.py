import os
import sys
from FastIsochrone.convex_hull_isochrones import ConvexHullIsochrones
from FastIsochrone.buffer_isochrones import BufferIsochrones
from FastIsochrone.detailed_isochrones import DetailedIsochrones

from FastIsochrone.config import networkType, tripTimes, travelSpeed, epsgCode, networkDistance

myTestInstance = ConvexHullIsochrones(networkType, tripTimes, travelSpeed, epsgCode, networkDistance)
myTestInstance.createConvexHullIsochrones(plot=True)