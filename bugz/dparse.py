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
            
    def parse( self, dt ):
        """ parse some enlishy date into a datetime.datetime """
        ret = datetime.datetime.now()
        if dt.startswith('y'):
            ret = ret - datetime.timedelta(1)
        elif dt.startswith('lastw') or dt.startswith('lw'):
            ret = ret - datetime.timedelta(7)
        elif dt.startswith('lastm') or dt.startswith('lm'):
            ret = ret - datetime.timedelta(30)
        else:
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
        tm = dp.parse('2010-02-22')
        self.assertEquals( "2010-02-22 00:00:00", str(tm) )
        tm = dp.parse("lw")

if __name__ == '__main__':
    unittest.main()
                    
        