#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by J Knight on 2010-02-16.
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import os
import sys
import getopt

from bugz.bugz import Bugz


help_message = '''
A simple command line bug tracking thingy so I can keep bugs and stuff with
the project, in the repo, and don't need any fancy bullshit to deal with it.

bugz [OPTIONS] [COMMAND] [ARGS...]
where OPTIONS are:
  --help            - print this screen
  
where COMMANDS are:
  init              - initialize a new db
  add               - add a new issue
  status            - get the db status
  drop [ID]         - drop an issue
  edit [ID]         - edit an issue
  comment [ID]      - comment on an issue
  show [ID|FIELD]   - show an issue. FIELD like s:open OR t:bug
  open [ID]         - open an issue
  close [ID]        - close an issue
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output=","verbose"])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option in ("-v","--verbose"):
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value

        b = Bugz()
        b.run( args )
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        return 2


if __name__ == "__main__":
    sys.exit(main())
