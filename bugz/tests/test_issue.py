# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; encoding: utf-8 -*-

# -=-
import unittest
import sys, os
import env
# -=-

from bugz.issue import Issue

class testIssue( unittest.TestCase ):
    def setUp(self):
        if not os.path.exists( 'data' ):
            os.mkdir( 'data' )

    def tearDown( self ):
        pass
        
    def testLoadSaveXml( self ):
      dir_name = 'data'
      
      iss1 = Issue( dir_name )
      iss1['Description'] = "This is a description\nof some stuff"
      iss1.add_comment("This is a comment")
      iss1.add_comment("This is another comment")
      iss1.save_xml()
      iid = iss1['Id']
      
      # another issue
      iss2 = Issue( dir_name )
      iss2.load_xml( iid )
      self.assertEqual( iss1, iss2 )
      
      # delete this thing
      fname = os.path.join( dir_name, iid )
      os.unlink( fname )

# -------
# M A I N
# -------
if __name__ == '__main__':
    # so we can run it from textmate    
    unittest.main()
            
