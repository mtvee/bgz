# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; encoding: utf-8 -*-

"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

# -=-
import unittest
import sys, os
sys.path.append(os.curdir + "/../../")
# -=-

from bugz.dateparse import DateParser
import datetime
import time

# -=-
class testDateParser( unittest.TestCase ):
    def setUp(self):
        self.parser = DateParser()
        
    def test_date_parse(self):
        """ ^ """
        tm = self.parser.parse_date('2010-02-22')
        self.assertEqual( "2010-02-22 00:00:00", str(tm) )
    
    def test_range_parse_today(self):
        """ ^ """
        dt = self.parser.parse_date_range('today')
        now = datetime.datetime.now()
        midnite = datetime.datetime.combine(now.date(),datetime.time(0,0,0,0))
        # first date should be midnite today
        self.assertEqual((midnite-dt[0]).seconds, 0)
        self.assertEqual((midnite-dt[0]).days, 0)
        # second date should be now + some microseconds
        self.assertEqual((now-dt[1]).seconds, 0)
        self.assertEqual((now-dt[1]).days, 0)

    def test_range_parse_yesterday(self):
        """ ^ """
        dt = self.parser.parse_date_range('yesterday')
        yest = datetime.datetime.now() - datetime.timedelta(days=1)
        start = datetime.datetime.combine(yest.date(),datetime.time(0,0,0,0))
        end = datetime.datetime.combine(yest.date(),datetime.time(23,59,59,0))
        # first date should be midnite today
        self.assertEqual((start-dt[0]).seconds, 0)
        self.assertEqual((start-dt[0]).days, 0)
        # second date should be now + some microseconds
        self.assertEqual((end-dt[1]).seconds, 0)
        self.assertEqual((end-dt[1]).days, 0)

    def test_range_parse_thisweek(self):
        """ ^ """
        dt = self.parser.parse_date_range('thisweek')
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=now.weekday())
        start = datetime.datetime.combine(start.date(),datetime.time(0,0,0,0))
        end = datetime.datetime.now()
        # first date should be midnite today
        self.assertEqual((start-dt[0]).seconds, 0)
        self.assertEqual((start-dt[0]).days, 0)
        # second date should be now + some microseconds
        self.assertEqual((end-dt[1]).seconds, 0)
        self.assertEqual((end-dt[1]).days, 0)


    def test_range_parse_lastweek(self):
        """ ^ """
        dt = self.parser.parse_date_range('lastweek')
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=now.weekday(),weeks=1)
        start = datetime.datetime.combine(start.date(),datetime.time(0,0,0,0))
        end = start + datetime.timedelta(7) - datetime.timedelta(seconds=1)
        # first date should be midnite today
        self.assertEqual((start-dt[0]).seconds, 0)
        self.assertEqual((start-dt[0]).days, 0)
        # second date should be now + some microseconds
        self.assertEqual((end-dt[1]).seconds, 0)
        self.assertEqual((end-dt[1]).days, 0)


# -------
# M A I N
# -------
if __name__ == '__main__':
    # so we can run it from textmate    
    unittest.main()