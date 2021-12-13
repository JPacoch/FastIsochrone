import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

from descartes import PolygonPatch
from shapely.geometry import Point, LineString, Polygon
from dataloader import latlonTuple
from mainclass import InitClass

ox.config(log_console=True, use_cache=True)
ox.__version__

class ConvexHullIsochrones(InitClass):
    def __init__(self, networkType, tripTimes, travelSpeed):
        super().__init__(networkType, tripTimes, travelSpeed)

    def createConvexHullIsochrones(self, plot=False):
        for railwayStation in latlonTuple:
            self.G = ox.graph_from_point(railwayStation, dist=30000,
            dist_type='network',
            network_type=self.networkType) 
            #graph_from_point, czyli utworzenie grafu i pobranie danych
            #przez okreslone miejsce (punkt) w przygotowanej georamce danych 

            self.gdfNodes = ox.graph_to_gdfs(self.G, edges=False) #przeniesienie pobranego grafu do georamki danych

            x, y = self.gdfNodes['geometry'].unary_union.centroid.xy #wyszukiwanie węzła w sieci najbliższego współrzędnym punktu (stacj)
            self.centerNode = ox.get_nearest_node(self.G, (y[0], x[0])) #punkt w sieci najbliższy wybranej stacji kolejowej

            self.G = ox.project_graph(self.G) #reprojekcja grafu do odpowiedniego układu współrzędnych WGS84 UTM - dla obszaru badań
            #jest do WGS84/UTM ZONE 33N (epsg:32633)

            self.metersPerMinute = self.travelSpeed * 1000 / 60 #przeliczenie kmh na mpm (meters per minute)
            for u, v, k, data in self.G.edges(data=True, keys=True):
                data['time'] = data['length'] / self.metersPerMinute #utworzenie atrybutu stanowiącego czas przejścia każdego odcinka w sieci drogowej

            #tworzenie wygladzonych izochron w postaci poligonow
            for tripTime in sorted(self.tripTimes, reverse=True):
                self.egoGraph = nx.ego_graph(self.G, self.centerNode, radius=tripTime, distance='time')
                self.nodePoints = [Point((data['x'], data['y'])) for node, data in self.egoGraph.nodes(data=True)]

                #utworzenie izochrony (poligonu) jako otoczki wypukłej zbioru węzłów tej samej wartości czasu podróży (convex hull)
                self.boundingPolygons = gpd.GeoSeries(self.nodePoints).unary_union.convex_hull 
                self.isochronePolygons.append(self.boundingPolygons)

            if plot:
                fig, ax = ox.plot_graph(self.G, show=False, close=False, edge_color='#999999', edge_alpha=0.3,
                            node_size=0.1, bgcolor='k')
                for polygon, fColour in zip(self.isochronePolygons, self.isochroneColours):
                    polyPatch = PolygonPatch(polygon, fc=fColour, ec='none', alpha=0.6, zorder=-1)
                    ax.add_patch(polyPatch)
                plt.show()
            else:
                continue

    def plotPointIsochrone(self):
            #tworzenie mapy węzłów na sieci (nodes) oznaczonych odpowiednio kolorem izochrony
            nodeColours = {}
            for tripTime, colour in zip(sorted(self.tripTimes, reverse=True), self.isochroneColours):
                #utworzenie podsieci wykorzystując obiekt NetworkX
                #obrazującej przebyty dystans na podstawie przyjętych parametrów czasu podróży
                self.egoGraph = nx.ego_graph(self.G, self.centerNode, radius=tripTime, distance='time') 

                #przypisanie dla każdego węzła odpowiedniego koloru odpowiadającego izochronie (czasowi podróży)
                for singleNode in self.egoGraph.nodes():
                    nodeColours[singleNode] = colour

            #określenie koloru węzła na mapie (zależne od koloru) izochrony
            self.plotNodeColour = [nodeColours[singleNode] if singleNode in nodeColours else 'none' for singleNode in self.G.nodes()] 

            #określenie wielkości węzła na mapie
            self.plotNodeSize = [12 if node in nodeColours else 0 for node in self.G.nodes()] 

            #utworzenie wykresu (mapy) węzłów o kolorze izochron
            fig, ax = ox.plot_graph(self.G, node_color=self.plotNodeColour, node_size=self.plotNodeSize, node_alpha=0.6, node_zorder=2,
                                    bgcolor='k', edge_linewidth=0.5, edge_color='#999999')
            plt.show()

    def plotConvexHullIsochrone(self):
            #utworzenie wykresu (mapy) wygładzonych izochron
        fig, ax = ox.plot_graph(self.G, show=False, close=False, edge_color='#999999', edge_alpha=0.3,
                                node_size=0.1, bgcolor='k')
        for polygon, fColour in zip(self.isochronePolygons, self.isochroneColours):
            self.polyPatch = PolygonPatch(polygon, fc=fColour, ec='none', alpha=0.6, zorder=-1)
            ax.add_patch(self.polyPatch)
        plt.show()

    def export(self, filename):
        #zapisanie poligonów izochron do georamki danych
        exportGdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(self.isochronePolygons))
        exportGdf = exportGdf.set_crs(epsg=32633)
        exportGdf["TravelTime"] = [next(self.timeTable) for time in range(len(exportGdf))]
        exportGdf.to_file(f"export/{filename}.shp") #zapis do pliku w formacie ESRI Shapefile 
