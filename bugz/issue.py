# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import os
import time
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
    def __init__( self, dname ):
        self.dir_name = dname
        self.data = {}
        self.comments = {}
        # default keys and values
        self.defaults = {'Id':str(uuid.uuid1()),
                    'Title':'No Title',
                    'Date':time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    'Status':'new',
                    'Author':'anon',
                    'Description':''}
        for key in self.defaults.keys():
            self.data[key] = self.defaults[key]
                
    def __str__( self ):
        """ return a short descriptive string thing """
        tmp = self['Id'].split('-')
        ret = "%s - %s/%s - %s" % (tmp[0],self['Type'],self['Status'].ljust(6),self['Title'])
        if len(ret) > 75:
            ret = ret[0:75] + "..."
        return ret
        
    def show( self ):
        """ print the whole mess """
        print '      Title: ' + self['Title']
        print '       Date: ' + self['Date']
        print '         Id: ' + self['Id']
        print '     Status: ' + self['Status']
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
        f = open( fname, 'rb' )
        self.data = pickle.load(f)
        self.comments = pickle.load(f)
        f.close()


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