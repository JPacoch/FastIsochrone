
# ⒻⓐⓢⓣⒾⓢⓞⓒⓗⓡⓞⓝⓔ

FastIsochrone is a GIS tool to develop simple and detailed isochrones using just one file of geographically oriented points. Isochrones can play a great role in one's availibility or time travel analysis.

## Instalation and first use

### Python

In order to run FastIsochrone via Python on PC a short set of following libraries should be installed previosly:
```
pandas==1.1.5
matplotlib==3.3.3
networkx==2.5.1
osmnx==1.0.1
descartes==1.1.0
shapely==1.7.1
pyproj==2.2.0
geopandas==0.8.5
Fiona==1.8.18
numpy==1.19.4
```

Note that at least Python in version 3.7 is needed. 

After a successful installation of necessary libraries one can use the FastIsochrone library in a sandbox mode (using sandbox/sandbox_environment.py) by simply importing three of availible class objects and making new instances of them as follows:

```
from convex_hull_isochrones import ConvexHullIsochrones

myInstance = ConvexHullIsochrones(networkType, tripTimes, travelSpeed, epsgCode, networkDistance)

myInstance.createConvexHullIsochrones()
myInstance.export(filename='export/myFile.shp')
```

Command Line Interface app can be run after a successful installation of all of the above libraries by entering cmd.exe. cd to FastIsochrone folder and type:
>python app.py

FastIsochrone CLI should be ready to use.

### Anaconda
In order to use FastIsochrone Command Line Interface with Anaconda both Python (3.7) and Anaconda should be installed. After that simply open cmd.exe and cd to FastIsochrone folder. In cmd.exe type:
>python run_app.py

This action should ask you to install and use FastIsochrone conda environment. Type 'y' and after a successful installation FastIsochrone CLI should be ready to use.

## Usage

Three main methods of isochrone creation are availible within FastIsochrone tool: 

1. simple isochrone - which uses a convex hull methodology
2. buffer isochrone - which creates buffer zones along the network
3. detailed isochrone - complex technique to create isochrones fitted to the network grid

Both simple and detailed methods needs five arguments which can be chosen in either config.py or while creating a new class instance:

1. tripTimes - an list of integers that indicates the travel intervals in minutes
2. networkType - a string variable that determines a type of network based on chosen mode of transportation (eg. drive, walk, bike)
3. travelSpeed - an intiger of a given speed in kilometers per hour
4. epsgCode - an EPSG code that indicates the final projection of exported files
5. networkDistance - an integer of network calculation range in meters

Moreover, buffer isochrone creation method needs two additional argumeents which are:

1. edgeBuffer - an intiger that depicts size of buffer zone drawn along network edges
2. nodeBuffer - an integer that depicts size of buffer zone drawn along network nodes

### Command Line Interface
In order to use CLI properly one should specify a path to the file that contains points of choosing alongside neccessary arguments in *config.py*  file. 

Every function in CLI can be investigated simply by typing '*?*' before its name. To list all the functions use command *help*.