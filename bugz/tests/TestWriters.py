# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

from bugz import writers

def test_xml():
    xml = writers.WriterFactory().get_writer('xml')
    xml.setHeaders(["One","Two","Three","Four","Four and a Bit","Five"])
    xml.setData([["one","two \"for\" & 'five' < six > 6",3,"four",4.5,"five,"]])
    #xml.setFile('test.xml')
    xml.write()       
    assert 1 == 1