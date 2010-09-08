# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; encoding: utf-8 -*-

# -=-
import unittest
import sys, os
import UserDict
import shutil

sys.path.append(os.curdir + "/../../")
# -=-

from bugz.bugz import Bugz, BugzError

class testBugz( unittest.TestCase ):
    def setUp( self ):
        self.startdir = os.path.abspath( os.curdir )
        if not os.path.exists( 'data' ):
            os.mkdir( 'data' )
        os.chdir( 'data' )

        self.options = UserDict.UserDict()
        self.options.verbose = False
        self.options.debug = False
        self.options.ansi = True
        
    def tearDown( self ):
        # delete the test db
        shutil.rmtree(Bugz.BGZ_DIR_NAME)
        os.chdir( self.startdir )
        
    def testInit(self):
        """ test init """        
        args = ['init']
        b = Bugz( self.options )
        # test success
        self.assertTrue( b.run( args ))
        # the dir exists
        self.assertTrue( os.path.exists( b.BGZ_DIR ) )
        # should fail if dir exists
        self.assertRaises( BugzError, b.run, args )        

# -------
# M A I N
# -------
if __name__ == '__main__':
    # so we can run it from textmate    
    unittest.main()
            
