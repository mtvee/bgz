# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""
import os
import sys
import time
import tempfile
import re
import datetime
import dateparse

from issue import Issue

class Bugz:
    """ this is the bugz class that handles the user """
    def __init__( self ):
        self.dir_name = '.bugz'
        self.editor_cmd = 'vi'
        self.user_id = os.environ['USER']
        self.user_name = self.user_id
        self._read_init()
        if self._find_bugs_dir():
            # try for a local config file            
            lconf = os.path.join(self.dir_name, 'config')
            if os.path.exists(lconf):
                self._read_config( lconf )
        try:
            # readline is nice
            import readline
        except:
            pass
        
    def run( self, args ):
        """ run a command """
        cmd = 'status'
        if len(args) > 0:
            cmd = args[0]
            args = args[1:]
        try:
            func = getattr(self,'do_' + cmd)
            return func(args)
        except AttributeError, e:
            print e
            print 'Unknown command: [' + cmd + ']'
            return False
        except KeyboardInterrupt:
            print "\n"
            return False

    def do_status( self, args ):
        """ get the database status """
        self._check_status()
        files = os.listdir( self.dir_name )
        counts = {'new':0,'open':0,'closed':0}
        issues = {}
        for file in files:
            issue = Issue(self.dir_name)
            issue.load( file )
            counts[issue['Status']] += 1
            if not issues.has_key( issue['Type'] ):
                issues[issue['Type'][0]] = []
            if next((a for a in args if a == 'all'),None):
                issues[issue['Type'][0]].append( issue )
            elif issue['Status'][0] != 'c':
                issues[issue['Type'][0]].append( issue )
        print 'Status: ',
        for k in counts.keys():
            print k + "/" + str(counts[k]) + " ",
        print
        types = {'b':'Bug','t':'Task','f':'Feature'}
        for t in issues.keys():
            print types[t]
            print "-" * len(types[t])
            for issue in issues[t]:
                print issue
            print
            
    def do_init( self, args ):
        """ initialize the database """
        if os.path.exists( self.dir_name ):
            print 'Database already exists'
            return False
        os.mkdir( self.dir_name )
        print 'Initialized ' + self.dir_name
        return True

    def do_drop( self, args ):
        """ drop an issue """
        self._check_status()
        if len(args) == 0:
            return False
        flist = self._find_issues(args[0])
        for f in flist:
            yn = self._read_input('Really drop ' + f, 'n', ['y','n'])
            if yn == 'y':
                os.unlink(os.path.join(self.dir_name, f))

    def do_open( self, args ):
        """ open an issue """
        self._check_status()
        if len(args) == 0:
            return False
        return self._change_status(args[0],'open')

    def do_close( self, args ):
        """ close an issue """
        self._check_status()
        if len(args) == 0:
            return False
        if self.do_comment(args, 'closed'):
            return self._change_status(args[0],'closed')
        else:
            return False

    def do_time( self, args ):
        """ add or report time """
        self._check_status()
        if len(args) == 0:
            return False
        if args[0] == 'add':
            if len(args) < 2:
                return False
            dur = self._read_input( "Duration (0:0)", None, lambda x: re.match("\d?:\d+", x) )
            if len(dur) and self.do_comment(args[1:], 'time ' + dur ):
                return True
            else:
                return False
        else:
            # QnD report
            dts = dateparse.DateParser().parse_date_range( args[0] )
            files = os.listdir( self.dir_name )
            s = 'Time Report'
            s += ' - ' + dts[0].strftime("%Y-%m-%d") + " / " + dts[1].strftime("%Y-%m-%d")
            print '-' * len(s)
            print s
            print '-' * len(s)
            issue = Issue(self.dir_name)
            for file in files:
                issue.load( file )
                tm = issue.time_total( dts ) 
                if tm[0] > 0 or tm[1] > 0:
                    print issue.rep( dts )
                    
            
    def do_edit( self, args ):
        """ edit the issue """
        self._check_status()
        if len(args) == 0:
            return False
        iss = self._find_issue(args[0])
        if iss:
            iss['Description'] = self._external_edit(iss['Description'])
            iss.save()
            return True
        return False
            
    def do_comment( self, args, prepend = None ):
        """ add a comment """
        self._check_status()
        if len(args) == 0:
            return False
        iss = self._find_issue(args[0])
        if iss:
            comm = self._read_multiline('Comment')
            if prepend:
                comm = prepend + ": " + comm
            iss.add_comment( comm )
            iss.save()
            return True
        return False

    def do_show( self, args ):
        """ show stuff """
        self._check_status()
        files = os.listdir( self.dir_name )
        issue = Issue(self.dir_name)
        for file in files:
            issue.load( file )
            if len(args):
                # check for colon
                if args[0].find(':') != -1:
                    for arg in args:
                        tmp = arg.split(':')
                        if tmp[0][0] == 's' and issue['Status'][0] == tmp[1][0]:
                            print issue
                        elif tmp[0][0] == 't' and issue['Type'][0] == tmp[1][0]:
                            print issue
                        elif tmp[0][0] == 'd':
                            # date range
                            dts = dateparse.DateParser().parse_date_range( tmp[1] )
                            if issue.date() >= dts[0] and issue.date() <= dts[1]:
                                print issue
                else:
                    if args[0][0] == '/':
                      if issue['Title'].find(args[0][1:]) != -1:
                          print issue  
                    elif file.startswith( args[0] ):
                        issue.show()
            else:
                print issue

    def do_add( self, args ):
        """ add an issue """
        self._check_status()
        title = self._read_input('Title')
        type = self._read_input( 'Type: (b)ug, (f)eature, (t)ask?', 'b', ('b','t','f'))
        author = self._read_input('Author',self.user_id)
        #desc = self._read_multiline('Descr')
        desc = self._external_edit('\n\n### ' + title )
        
        issue = Issue( self.dir_name )
        issue['Title'] = title
        issue['Description'] = desc
        issue['Type'] = type
        issue['Author'] = author
        issue.save()        
        print 'Added: ' + str(issue)
        
    def _change_status( self, uid, status ):
        """ change the status on an issue """
        iss = self._find_issue(uid)
        if iss:
            iss['Status'] = status
            iss.save()
            return True
        return False
        
    def _find_issues( self, uid = None ):
        """ find issues like a uid """
        files = os.listdir( self.dir_name )        
        flist = []
        for file in files:
            if uid:
                if file.startswith(uid):
                    flist.append(file)
            else:
                flist.append( file )
        return flist
        
    def _find_issue( self, uid ):
        """ find an issue with a partial uid """
        if uid.startswith('g'):
            if not os.path.exists(os.path.join(self.dir_name,'general.' + self.user_name)):
                gen = Issue(self.dir_name)
                gen['Id'] = 'general.' + self.user_name
                gen['Title'] = 'General Project Catchall'
                gen['Author'] = self.user_id
                gen['Type'] = 'task'
                gen['Status'] = 'open'
                gen.save()
        flist = self._find_issues( uid )
        if len(flist) == 1:
            iss = Issue(self.dir_name)
            iss.load( flist[0] )
            return iss
        elif len(flist) > 1:
            print 'Please be more specific: '
            for f in flist:
                print f
        return None
    
    def _read_input( self, prompt, dflt = None, valid = None ):
        """ read one line user input """
        if dflt:
            prompt += ' [' + dflt + ']'
        inp = raw_input( prompt + ": " )
        if valid and not dflt:
            if hasattr( valid, '__call__'):
                while inp.strip() and not valid(inp.strip()):
                    inp = raw_input( prompt + ": " )                                
            else:
                while inp.strip() not in valid:
                    inp = raw_input( prompt + ": " )            
        if dflt and inp.strip() == '':
            inp = dflt
        return inp.strip()
        
    def _read_multiline( self, prompt ):
        """ read multi-line user input """
        resp = ""
        inp = raw_input( prompt + ': ' )
        while inp.strip() != '.':
            resp += inp + "\n"
            inp = raw_input( (' ' * len(prompt)) + '> ' )
        return resp
        
    def _external_edit( self, dflt, strip_trailing = True ):
        """ run external editor """
        tfile = tempfile.mktemp()
        f = open( tfile, 'w')
        f.write( dflt )
        f.close()
        os.system( "%s %s" % (self.editor_cmd, tfile) )
        f = open( tfile, 'r' )
        data = f.readlines()            
        f.close()
        os.unlink( tfile )
        lines = data
        if strip_trailing:
            lines = []
            for line in data:
                if not line.startswith('###'):
                    lines.append(line)
        return "".join(lines).rstrip()

    def _read_init( self ):
        """ try and find the init file and read it """
        if os.name != 'posix':
            return
        init_file = os.path.join(os.getenv("HOME"), ".bugzrc")
        if not os.path.exists( init_file ):
            # this would be annoying to some, perhaps
            print "Init file not found, creating [%s]..." % init_file
            user = self._read_input("Your name: ", os.getenv("USER"))
            email = self._read_input("Your email: ", user + "@" + os.uname()[1])
            f = open( init_file, 'w' )
            f.write("user=" + user + "\n")
            f.write("email=" + email + "\n")
            f.close()
            print "Created " + init_file
        self._read_config( init_file )
        
    def _find_bugs_dir( self ):
        """this walks up the path and tries to find the bugs dir"""
        curpath = os.path.abspath(os.curdir)
        while len(curpath):
            if os.path.exists(os.path.join(curpath, self.dir_name)):
                self.dir_name = os.path.join(curpath, self.dir_name)
                return True
            curpath = curpath[0:curpath.rfind('/')]
        return False

    def _check_status( self ):
        """ make sure we have a database to work with """
        if not os.path.exists( self.dir_name ):
            print 'Database not found: ' + self.dir_name
            sys.exit( 1 )
                
    def _read_config( self, conf ):
        """ read in a config file """
        f = open( conf, 'r' )
        lines = f.readlines()
        f.close()
        user = self.user_id
        email = ''
        for line in lines:
            line = line.strip()
            if line[0] == '#' or line[0] == ';':
                continue
            tmp = line.split('=')
            if(tmp[0] == 'user'):
                user = tmp[1].strip()
            if(tmp[0] == 'email'):
                email = tmp[1].strip()
            if(tmp[0] == 'editor'):
                self.editor_cmd = tmp[1].strip()
        self.user_name = user.lower().replace(' ','_')
        self.user_id = user
        if len(email):
            self.user_id += ' <' + email + '>'
