
# -=-
import unittest
import sys, os
sys.path.append(os.curdir + "/../../")
# -=-

from bugz.issue import Issue

class testIssue( unittest.TestCase ):
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
            