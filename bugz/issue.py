# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import os
import time
import datetime
import pickle
import uuid
import UserDict


class Issue(UserDict.UserDict):
    """ 
    This is a class to represent an issue of some kind 
    TODO
    - it would be nice if the storage format were human but for now
      pickle is fast and easy.
    """
    types = {'t':'Task','b':'Bug','f':'Feature'}
    
    def __init__( self, dname ):
        self.dir_name = dname
        self.data = {}
        self.comments = {}
        # default keys and values
        self.defaults = {'Id':str(uuid.uuid1()),
                    'Title': 'No Title',
                    'Date': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    'Status': 'new',
                    'Author': 'anon',
                    'Type': 'b',
                    'Description': ''}
        for key in self.defaults.keys():
            self.data[key] = self.defaults[key]
                
    def __str__( self ):
        """ return a short descriptive string thing """
        return self.rep()

    def rep( self, dts = None):
        """ return a short descriptive string thing """
        tmp = self['Id'].split('-')
        tm = self.time_total(dts)
        ret = "%12s - %s/%s - %2d:%02d - %s" % (tmp[0],self['Type'][0],self['Status'].ljust(6),tm[0],tm[1],self['Title'])
        if len(ret) > 75:
            ret = ret[0:75] + "..."
        return ret
        
    def date( self ):
        return datetime.datetime.strptime( self['Date'],"%Y-%m-%dT%H:%M:%SZ")
        
    def show( self ):
        """ print the whole mess """
        print '      Title: ' + self['Title']
        print '       Date: ' + self['Date']
        print '         Id: ' + self['Id']
        print '     Status: ' + self['Status']
        print '       Type: ' + self['Type']
        print '     Author: ' + self['Author']
        print 'Description: ' 
        print '-----------'
        print self['Description']
        print '-----------'
        keys = self.comments.keys()
        keys.sort()
        for key in keys:
            print time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(key) )
            print self.comments[key].strip()
            print
        
    def time_total( self, dts = None ):
        tm = [0,0]
        for k, v in self.comments.iteritems():
            # ignore if we have a date range and we are outside of it
            ct = datetime.datetime.fromtimestamp(k)
            if dts and (ct <= dts[0] or ct >= dts[1]):
                continue
            if v.startswith('time '):
                parts = v[5:].split(":")
                for i in range(len(parts)):
                    try:
                        tm[i] += int(parts[i])
                    except:
                        pass
        tm[0] += tm[1] / 60
        tm[1] = tm[1] % 60
        return tm
                    
            
    def add_comment( self, comment ):
        """ add a comment """
        if len(comment.strip()):
            self.comments[time.time()] = comment
        
    def save( self ):
        """ save the thing """
        fname = os.path.join(self.dir_name, self['Id'])
        f = open( fname, 'wb' )
        pickle.dump(self.data,f)
        pickle.dump(self.comments,f)
        f.close()
        
    def load( self, uid ):
        """ load the thing """
        fname = os.path.join(self.dir_name, uid )
        try:
            f = open( fname, 'rb' )
            self.data = pickle.load(f)
            self.comments = pickle.load(f)
            f.close()
        except:
            return False
        return True


# ------------------
# U N I T  T E S T S
# ------------------
import unittest

class IssueTests(unittest.TestCase):
    def setUp( self ):
        pass

    def testSomething( self ):
        self.assertEquals( 1, 1 )
        
if __name__ == '__main__':
    unittest.main()