

import datetime
import time

class DateParser:
    def __init__( self ):
        pass
        
    
    def parse( self, dt ):
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
                        # idiotic american/canadian format
                        str = "%%m%s%%d%s%%Y" % (dlim,dlim)
                        ret = datetime.datetime.strptime( dt, str )
                    except:
                        pass
        return ret
        