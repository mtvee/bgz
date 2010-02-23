# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import datetime
import time

class DateParser:
    """ English date parsing class """
    def __init__( self ):
        pass
            
    def parse_date_range( self, args ):
        dts = args.split(':')
        if len(dts) > 1:
            sdate = self.parse_date( dts[0] )
            edate = self.parse_date( dts[1] ) 
        else:
            if dts[0].startswith('lastw') or dts[0].startswith('lw'):
                # lastweek, starting monday before last
                now = datetime.datetime.now()
                sdate = now - datetime.timedelta(days=now.weekday(), weeks=1)
                edate = sdate + datetime.timedelta(7)
            elif dts[0].startswith('y'):
                # y[esterday]
                sdate = datetime.datetime.now() - datetime.timedelta(1)
                sdate = sdate.replace(hour=0,minute=0,second=0,microsecond=0)
                edate = sdate + datetime.timedelta(1)
            elif dts[0].startswith('t') or dts[0].startswith('n'):
                # t[oday]
                sdate = datetime.datetime.now()
                sdate = sdate.replace(hour=0,minute=0,second=0,microsecond=0)
                edate = datetime.datetime.now()
            else:
                # startdate
                sdate = self.parse_date( dts[0] )
                edate = datetime.datetime.now()
        return (sdate,edate)
                    
    def parse_date( self, dt ):
        """ parse some englishy date into a datetime.datetime """
        ret = datetime.datetime.now()
        # guess a delimiter
        dlim = '/'
        if dt.find('.') != -1:
            dlim = '.'
        if dt.find('-') != -1:
            dlim = '-'
        if dt.find(':') != -1:
            dlim = ':'
        try:
            # sortable
            str = "%%Y%s%%m%s%%d" % (dlim,dlim)
            ret = datetime.datetime.strptime( dt, str )
        except:
            try:
                # sensible
                str = "%%d%s%%m%s%%Y" % (dlim,dlim)
                ret = datetime.datetime.strptime( dt, str )
            except:
                try:         
                    # idiotic american/canadian/sheep format
                    str = "%%m%s%%d%s%%Y" % (dlim,dlim)
                    ret = datetime.datetime.strptime( dt, str )
                except:
                    pass
        return ret
        
# ------------------
# U N I T  T E S T S
# ------------------
import unittest

class DateParseTests(unittest.TestCase):
    def setUp( self ):
        pass

    def testSomething( self ):
        dp = DateParser()
        tm = dp.parse_date_range("lw")
        print tm

if __name__ == '__main__':
    unittest.main()
                    
        