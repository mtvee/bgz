# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

from bugz.dateparse import DateParser

def test_simple():
    dp = DateParser()
    tm = dp.parse('2010-02-22')
    assert "2010-02-22 00:00:00" == str(tm) 
    