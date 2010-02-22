# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import writers

# ------------------
# U N I T  T E S T S
# ------------------
import unittest

class WriterTests(unittest.TestCase):
    def setUp( self ):
        pass
     
    def testSomething( self ):
        xml = writers.WriterFactory().get_writer('xml')
        xml.setHeaders(["One","Two","Three","Four","Four and a Bit","Five"])
        xml.setData([["one","two \"for\" & 'five' < six > 6",3,"four",4.5,"five,"]])
        #xml.setFile('test.xml')
        xml.write()       
        self.assertEqual(1,1)
        
if __name__ == '__main__':
    unittest.main()
    
