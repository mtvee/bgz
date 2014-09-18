# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; encoding: utf-8 -*-

# -=-
import unittest
import sys, os
import UserDict
import shutil
import env
# -=-

from bugz.bugz import Bugz, BugzError
from bugz.issue import Issue

class testBugz( unittest.TestCase ):
    def setUp( self ):
        # save the dir we started in
        self.startdir = os.path.abspath( os.curdir )
        if not os.path.exists( 'data' ):
            os.mkdir( 'data' )
        os.chdir( 'data' )
        # delete any leftover db
        self.assureNoDb()

        self.options = UserDict.UserDict()
        self.options.verbose = False
        self.options.debug = False
        self.options.ansi = True
        
    def tearDown( self ):
        # delete the test db
        self.assureNoDb()        
        # and switch back to our orig dir
        os.chdir( self.startdir )
    
    def assureDb( self ):
        # make sure the db exists
        if not os.path.exists( Bugz.BGZ_DIR_NAME ):
            b = Bugz( self.options )
            b.run( ['init'] )           

    def assureNoDb( self ):
        # make sure the db is toast
        if os.path.exists( Bugz.BGZ_DIR_NAME ):
            shutil.rmtree(Bugz.BGZ_DIR_NAME)
          
    def testInit( self ):
        """ test init """
        self.assureNoDb()        
        args = ['init']
        b = Bugz( self.options )
        # test success
        self.assertTrue( b.run( args ))
        # the dir exists
        self.assertTrue( os.path.exists( b.BGZ_DIR ) )
        # should fail if dir exists
        self.assertFalse( b.run( args ))
        #self.assertRaises( BugzError, b.run, args )        
        # delete any leftover db
        self.assureNoDb()        

    def testAdd( self ):
        # hmm, need some way to test these commands properly a la CLI. 
        # this is no good
        self.assureDb()
        b = Bugz( self.options )
        issue = Issue( b.BGZ_DIR )
        issue['Title'] = 'Test Bug'
        issue['Description'] = 'Test description'
        issue['Type'] = 'b'
        issue['Author'] = 'unittest'
        issue.save()
        self.assertTrue( os.path.exists(os.path.join(b.BGZ_DIR, issue['Id'])))

# -------
# M A I N
# -------
if __name__ == '__main__':
    # so we can run it from textmate    
    unittest.main()
            
