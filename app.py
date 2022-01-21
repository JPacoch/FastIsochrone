"""
Command line interface - interactive.

"""

import sys
import os
from cmd import Cmd
from main.convex_hull_isochrones import ConvexHullIsochrones
from main.detailed_isochrones import DetailedIsochrones
from main.buffer_isochrones import BufferIsochrones
from main.config import PROJECT_DIR, networkType, tripTimes, travelSpeed, epsgCode, networkDistance


class CLI(Cmd):

    intro = """
    
███████╗░█████╗░░██████╗████████╗██╗░██████╗░█████╗░░█████╗░██╗░░██╗██████╗░░█████╗░███╗░░██╗███████╗
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██║██╔════╝██╔══██╗██╔══██╗██║░░██║██╔══██╗██╔══██╗████╗░██║██╔════╝
█████╗░░███████║╚█████╗░░░░██║░░░██║╚█████╗░██║░░██║██║░░╚═╝███████║██████╔╝██║░░██║██╔██╗██║█████╗░░
██╔══╝░░██╔══██║░╚═══██╗░░░██║░░░██║░╚═══██╗██║░░██║██║░░██╗██╔══██║██╔══██╗██║░░██║██║╚████║██╔══╝░░
██║░░░░░██║░░██║██████╔╝░░░██║░░░██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██║░░██║╚█████╔╝██║░╚███║███████╗
╚═╝░░░░░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚══╝╚══════╝

    Welcome to FastIsochrone 0.2.2
    Creator's homepage:                              https://jpacoch.github.io
    Help is availible with the command:              help
    When ready to quit, enter:                       quit

    Type ? to list commands."""
    prompt = 'FastIsochrone 0.2.2> '

    def do_create_convexhull_iso(self, empty_args):
        """
        Create simple convex hull isochrones for given points and export to ESRI Shapefile.

        Arguments to use:
            No arguments required.

        Usage:
            Enter command: do_create_convexhull_iso
            Result: Convex hull isochrones are made from ESRI Shapefile input file with point layer.

        Optional actions:
            - Plotting single convex hull isochrone (y/n)
            - Plotting single point isochrone (y/n)
            - Naming the export files.
        """
        x = ConvexHullIsochrones(networkType, tripTimes, travelSpeed, epsgCode, networkDistance)
        x.createConvexHullIsochrones()

        print('Would you like to plot single convex hull isochrone?')
        print('y/n')
        q1 = input()

        if q1 == 'y':
            x.plotConvexHullIsochrone()

        print('Would you like to plot single point isochrone?')
        print('y/n')
        q2 = input()

        if q2 == 'y':
            x.plotPointIsochrone()

        print('Enter export file name:')
        filename = input()
        x.export(filename=filename)

    def do_create_detailed_iso(self, empty_args):
        """
        Create detailed isochrones fitted to the network for given points and export to ESRI Shapefile.

        Arguments to use:
            No arguments required.

        Usage:
            Enter command: do_create_detailed_iso
            Result: Detailed isochrones are made from ESRI Shapefile input file with point layer.

        Optional actions:
            - Plotting single detailed isochrone (y/n)
            - Plotting single point isochrone (y/n)
            - Naming the export files.
        """
        y = DetailedIsochrones(networkType, tripTimes, travelSpeed, epsgCode, networkDistance)
        y.createDetailedIsochrones()

        print('Would you like to plot detailed isochrone?')
        print('y/n')
        q1 = input()

        if q1 == 'y':
            y.plotDetailedIsochrone()

        print('Would you like to plot single point isochrone?')
        print('y/n')
        q2 = input()

        if q2 == 'y':
            y.plotPointIsochrone()

        print('Enter export file name:')
        filename = input()
        y.export(filename=filename)

    def do_create_buffer_iso(self, empty_args):
        """
        Create buffers that create simple isochrones along the network and export to ESRI Shapefile.

        Arguments to use:
            No arguments required.

        Usage:
            Enter command: do_create_buffer_iso
            Result: Buffer isochrones are made from ESRI Shapefile input file with point layer.

        Optional actions:
            - Plotting single buffer isochrone (y/n)
            - Plotting single point isochrone (y/n)
            - Naming the export files.
        """
        print('Please provide a value of edge buffer:')
        edgeBuffer = int(input())
        
        print('Please provide a value of node buffer:')
        nodeBuffer = int(input())

        y = BufferIsochrones(networkType, tripTimes, travelSpeed, epsgCode, networkDistance, edgeBuffer, nodeBuffer)
        y.createBufferIsochrones()

        print('Would you like to plot single buffer isochrone?')
        print('y/n')
        q1 = input()

        if q1 == 'y':
            y.plotBufferIsochrone()
        
        print('Would you like to plot single point isochrone?')
        print('y/n')
        q2 = input()

        if q2 == 'y':
            y.plotPointIsochrone()

        print('Enter export file name:')
        filename = input()
        y.export(filename=filename)

    def do_quit(self, empty_args):
        """
        Quit the command line interface.

        Arguments to use:
            No arguments required.

        Usage:
            Enter command: quit
            Result: Quit the command line interface.      
        """
        sys.exit()


if __name__ == '__main__':
    CLI().cmdloop()