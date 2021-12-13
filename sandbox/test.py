import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

from descartes import PolygonPatch
from shapely.geometry import Point, LineString, Polygon
from config import latlonTuple

ox.config(log_console=True, use_cache=True)
ox.__version__

networkType = 'drive' #okreslenie sieci; walk, drive etc
tripTimes = [5,10,15,20,25] #zakres izochrony w minutach
travelSpeed = 50 #predkosc podrozy w kmh
isochronePolygons = []
#główna pętla programu - tworzenie grafu oraz zapisywanie utworzonych izochron dla każdego punktu
for railwayStation in latlonTuple:
    G = ox.graph_from_point(railwayStation, dist=30000,
     dist_type='network',
      network_type=networkType) 
    #graph_from_point, czyli utworzenie grafu i pobranie danych
    #przez okreslone miejsce (punkt) w przygotowanej georamce danych 

    gdfNodes = ox.graph_to_gdfs(G, edges=False) #przeniesienie pobranego grafu do georamki danych

    x, y = gdfNodes['geometry'].unary_union.centroid.xy #wyszukiwanie węzła w sieci najbliższego współrzędnym punktu (stacj)
    centerNode = ox.get_nearest_node(G, (y[0], x[0])) #punkt w sieci najbliższy wybranej stacji kolejowej

    G = ox.project_graph(G) #reprojekcja grafu do odpowiedniego układu współrzędnych WGS84 UTM - dla obszaru badań
    #jest do WGS84/UTM ZONE 33N (epsg:32633)

    metersPerMinute = travelSpeed * 1000 / 60 #przeliczenie kmh na mpm (meters per minute)
    for u, v, k, data in G.edges(data=True, keys=True):
        data['time'] = data['length'] / metersPerMinute #utworzenie atrybutu stanowiącego czas przejścia każdego odcinka w sieci drogowej

    isochroneColours = ox.plot.get_colors(n=len(tripTimes), cmap='plasma', start=0, return_hex=True)
    #utworzenie palety kolorów zależnej od czasu podróży dla izochron

    #tworzenie mapy węzłów na sieci (nodes) oznaczonych odpowiednio kolorem izochrony
    nodeColours = {}
    for tripTime, colour in zip(sorted(tripTimes, reverse=True), isochroneColours):
        #utworzenie podsieci wykorzystując obiekt NetworkX
        #obrazującej przebyty dystans na podstawie przyjętych parametrów czasu podróży
        egoGraph = nx.ego_graph(G, centerNode, radius=tripTime, distance='time') 

        #przypisanie dla każdego węzła odpowiedniego koloru odpowiadającego izochronie (czasowi podróży)
        for singleNode in egoGraph.nodes():
            nodeColours[singleNode] = colour

    #określenie koloru węzła na mapie (zależne od koloru) izochrony
    plotNodeColour = [nodeColours[singleNode] if singleNode in nodeColours else 'none' for singleNode in G.nodes()] 

    #określenie wielkości węzła na mapie
    plotNodeSize = [12 if node in nodeColours else 0 for node in G.nodes()] 

    #utworzenie wykresu (mapy) węzłów o kolorze izochron
    #fig, ax = ox.plot_graph(G, node_color=plotNodeColour, node_size=plotNodeSize, node_alpha=0.6, node_zorder=2,
    #                        bgcolor='k', edge_linewidth=0.5, edge_color='#999999')


     #lista będąca punktem wyjścia do zapisu poligonów izochron

    #tworzenie wygladzonych izochron w postaci poligonow
    for tripTime in sorted(tripTimes, reverse=True):
        egoGraph = nx.ego_graph(G, centerNode, radius=tripTime, distance='time')
        nodePoints = [Point((data['x'], data['y'])) for node, data in egoGraph.nodes(data=True)]

        #utworzenie izochrony (poligonu) jako otoczki wypukłej zbioru węzłów tej samej wartości czasu podróży (convex hull)
        boundingPolygons = gpd.GeoSeries(nodePoints).unary_union.convex_hull 

        #dodanie kolejnych izochron do listy ógolnej
        isochronePolygons.append(boundingPolygons)

    #utworzenie wykresu (mapy) wygładzonych izochron
    fig, ax = ox.plot_graph(G, show=False, close=False, edge_color='#999999', edge_alpha=0.3,
                            node_size=0.1, bgcolor='k')
    for polygon, fColour in zip(isochronePolygons, isochroneColours):
        polyPatch = PolygonPatch(polygon, fc=fColour, ec='none', alpha=0.6, zorder=-1)
        ax.add_patch(polyPatch)
    #plt.show()

#zapisanie poligonów izochron do georamki danych
exportGdf = gpd.GeoSeries(isochronePolygons)
exportGdf = exportGdf.set_crs(epsg=32633) #ustawienie odpowiedniego układu współrzędnych UTM 33N
exportGdf.to_file("isochrones.shp") #zapis do pliku w formacie ESRI Shapefile