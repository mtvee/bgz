# -*- Mode: python; tab-width: 2; indent-tabs-mode: nil; encoding: utf-8 -*-

# -=-
import unittest
import sys, os
sys.path.append(os.curdir + "/../../")
# -=-

from bugz.bugz import Bugz

class testBugz( unittest.TestCase ):
    def setUp(self):
        pass

    def testSomething(self):
        pass

# -------
# M A I N
# -------
if __name__ == '__main__':
    # so we can run it from textmate    
    unittest.main()
            
