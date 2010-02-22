# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import sys

# -----------------
# B A S E
# -----------------
class BaseWriter:
    """ Basic Writer """
    def __init__( self ):
        self.data = [[]]
        self.headers = None
        self.out = sys.stdout
        self.EOL = "\n"
        
    def setData( self, data ):
        """data is an array of arrays"""
        self.data = data

    def setFile( self, fname ):
        """set the output file"""
        self.out = open( fname, "w" )

    def setHeaders( self, hdrs ):
        self.headers = hdrs

    def write( self ):
        """do it"""
        self.p( str(self.data) )

    def p( self, str ):
        """ output a line with EOL """
        self.out.write( str + self.EOL )
