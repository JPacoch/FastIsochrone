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

class BufferIsochrones(InitClass):
    def __init__(self, networkType, tripTimes, travelSpeed):
        super().__init__(networkType, tripTimes, travelSpeed)

    def createBufferIsochrones(self, plot=False):
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

            def make_iso_polys(G, edge_buff=150, node_buff=10, infill=False):
                for tripTime in sorted(self.tripTimes, reverse=True):
                    self.egoGraph = nx.ego_graph(self.G, self.centerNode, radius=tripTime, distance='time')
                    self.nodePoints = [Point((data['x'], data['y'])) for node, data in self.egoGraph.nodes(data=True)]
                    self.nodesGDF = gpd.GeoDataFrame({'id': self.egoGraph.nodes()}, geometry=self.nodePoints)
                    self.nodesGDF = self.nodesGDF.set_index('id')

                    self.edgeLines = []
                    for n_fr, n_to in self.egoGraph.edges():
                        f = self.nodesGDF.loc[n_fr].geometry
                        t = self.nodesGDF.loc[n_to].geometry
                        self.edgeLookup = G.get_edge_data(n_fr, n_to)[0].get('geometry',  LineString([f,t]))
                        self.edgeLines.append(self.edgeLookup)

                    n = self.nodesGDF.buffer(node_buff).geometry
                    e = gpd.GeoSeries(self.edgeLines).buffer(edge_buff).geometry
                    all_gs = list(n) + list(e)
                    new_iso = gpd.GeoSeries(all_gs).unary_union
                    
                    # try to fill in surrounded areas so shapes will appear solid and blocks without white space inside them
                    if infill:
                        new_iso = Polygon(new_iso.exterior)
                    self.isochronePolygons.append(new_iso)
                return self.isochronePolygons

            self.isochronePolygonsVis = make_iso_polys(self.G, edge_buff=150, node_buff=10, infill=False)
            fig, ax = ox.plot_graph(self.G, show=False, close=False, edge_color='#999999', edge_alpha=0.2,
                                    node_size=0, bgcolor='k')
            for polygon, fc in zip(self.isochronePolygonsVis, self.isochroneColours):
                patch = PolygonPatch(polygon, fc=fc, ec='none', alpha=0.6, zorder=-1)
                ax.add_patch(patch)

            if plot:        
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


    def export(self, filename):
        #zapisanie poligonów izochron do georamki danych
        exportGdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(self.isochronePolygons))
        exportGdf = exportGdf.set_crs(epsg=32633)
        exportGdf["TravelTime"] = [next(self.timeTable) for time in range(len(exportGdf))]
        exportGdf.to_file(f"export/{filename}.shp") #zapis do pliku w formacie ESRI Shapefile 