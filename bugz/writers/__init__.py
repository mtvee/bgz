# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""


# -----------------
# F A C T O R Y
# -----------------
class WriterFactory:
    def __init__( self ):
        pass
        
    def get_writer( self, which ):
        if which == 'xml':
            from xmlwriter import ExcelXMLWriter
            return ExcelXMLWriter()
        elif which == 'csv':
            from csvwriter import CSVWriter
            return CSVWriter()
        elif which == 'html':
            from htmlwriter import HTMLWriter
            return HTMLWriter()