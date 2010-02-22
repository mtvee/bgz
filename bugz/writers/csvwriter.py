
from basewriter import *

import sys
import types

# -----------------
# C S V
# -----------------
class CSVWriter( BaseWriter ):
    def __init__( self ):
        BaseWriter.__init__( self ) 

    def write( self ):
        """ output the info """
        if self.headers:
            self.writeLine( self.headers )
        for line in self.data:
            self.writeLine( line )
                        
    def writeLine( self, line ):
        """output an array/line"""
        s = ""
        for item in line:
            if type(item) in (types.IntType,types.FloatType):
                s += str(item) + ","
            else:
                s += '"' + self.escape(str(item)) + '",'
        self.p(s[:-1])

    def escape( self, str ):
        return str.replace('"','""')
