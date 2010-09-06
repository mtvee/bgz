# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; encoding: utf-8 -*-
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
import shutil
import UserDict

from issue import Issue

class Bugz:
    # the global rc file name
    BGZRC_GLOBAL = ".bugzrc"
    # the local rc file name
    BGZRC_LOCAL = "_bgzrc" 
    # the global projects file
    BGZRC_PROJS = ".bgzprojs"
    # the bugz folder name
    BGZ_DIR = '.bugz'
    
    """ this is the bugz class that handles the user """    
    def __init__( self, opts = UserDict.UserDict ):
        self.opts = opts
        self.editor_cmd = 'vi'
        self.user_id = os.environ['USER']
        self.user_name = self.user_id
        self._read_init()
        if self._find_bugs_dir():
            # try for a local config file            
            lconf = os.path.join(self.BGZ_DIR, 'config')
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
        """ get the database status 
        
        bgz status [all]
        """
        self._check_status()
        files = os.listdir( self.BGZ_DIR )
        counts = {'new':0,'open':0,'closed':0}
        issues = {}
        for file in files:
            issue = Issue(self.BGZ_DIR)
            if not issue.load( file ):
                continue
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
        for t in issues.keys():
            print Issue.types[t]
            print "-" * len(Issue.types[t])
            for issue in issues[t]:
                print issue
            print
            
    def do_init( self, args ):
        """ initialize the database 
        
        bgz init
        """
        if os.path.exists( self.BGZ_DIR ):
            print 'abort: repository already exists'
            return False
        os.mkdir( self.BGZ_DIR )
        print 'Initialized ' + self.BGZ_DIR
        return True

    def do_drop( self, args ):
        """ drop an issue or project
        
        bgz drop ID
        bgz drop [p]roject
        """
        self._check_status()
        if len(args) == 0:
            return False
        # drop a project
        if args[0][0] == 'p':
            self._remove_project(self.BGZ_DIR)
            return
        flist = self._find_issues(args[0])
        for f in flist:
            yn = self._read_input('Really drop ' + f, 'n', ['y','n'])
            if yn == 'y':
                os.unlink(os.path.join(self.BGZ_DIR, f))

    def do_purge( self, args ):
        """move closed issues to 'PROJECT/.bugz/purged' directory
        
        bgz purge
        """
        self._check_status()
        ppath = os.path.join(self.BGZ_DIR, 'purged')
        if not os.path.exists( ppath ):
            try:
                os.mkdir( ppath )
            except:
                print 'abort: unable to create ' + ppath
                sys.exit(2)
        count = 0
        for file in os.listdir( self.BGZ_DIR ):
            issue = Issue(self.BGZ_DIR)
            if not issue.load( file ):
                continue
            if issue['Status'][0] == 'c':
                shutil.move(os.path.join(self.BGZ_DIR,file), ppath)
                count += 1
        print 'purged %d issue(s)' % (count)
                    
    def do_open( self, args ):
        """ open an issue 
        
        bgz open ID
        """
        self._check_status()
        if len(args) == 0:
            return False
        return self._change_status(args[0],'open')

    def do_close( self, args ):
        """ close an issue 
        
        bgz close ID
        """
        self._check_status()
        if len(args) == 0:
            return False
        if self.do_comment(args, 'closed'):
            return self._change_status(args[0],'closed')
        else:
            return False

    def do_time( self, args ):
        """ add or report time 
        
        bgz time
            report on time for this week (Monday - Sunday)
            
        bgz time add ID
            add a new time entry for the given ID
            
        bgz time DATERANGE
            report on time for a DATERANGE
            a DATERANGE can be:
            tw | [thisw]eek = this week (Monday - Sunday)
            lw | [lastw]eek = last week (Monday - Sunday)
            [y]esterday     = (midnight - midnight)
            [t]oday | [n]ow = (midnight - now)
            DD/MM/YYYY[:DD/MM/YYYY]
        """
        self._check_status()
        if len(args) == 0:
            args.append("thisweek")
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
            s = 'Time Report'
            s += ' - ' + dts[0].strftime("%Y-%m-%d") + " / " + dts[1].strftime("%Y-%m-%d")
            print '-' * len(s)
            print s
            print '-' * len(s)
            projects = self._read_projects()
            gtotal = [0,0]
            for proj in projects:
                puthdr = True
                issue = Issue( proj )
                files = os.listdir( proj )
                for file in files:
                    if not issue.load( file ):
                        continue
                    tm = issue.time_total( dts ) 
                    if tm[0] > 0 or tm[1] > 0:
                        gtotal[0] += tm[0]
                        gtotal[1] += tm[1]
                        if puthdr:
                            print 'Project: ' + proj[:-(len(proj)-proj.rfind('.'))]
                            puthdr = False
                        print issue.rep( dts )
            gtotal[0] += gtotal[1]/60
            gtotal[1] = gtotal[1] % 60
            t = 'Total: %d:%02d'  % (gtotal[0],gtotal[1])
            print '=' * len(t)
            print t
            
    def do_edit( self, args ):
        """ edit an issue 
        
        bgz edit ID
        """
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
        """ add a comment 
        
        bgz comment ID
        """
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
        files = os.listdir( self.BGZ_DIR )
        issue = Issue(self.BGZ_DIR)
        for file in files:
            if not issue.load( file ):
                continue
            if len(args):
                # check for colon
                if args[0].find(':') != -1:
                    for arg in args:
                        tmp = arg.split(':')
                        if tmp[0][0] == 's' and issue['Status'][0] == tmp[1][0]:
                            print issue
                            break
                        elif tmp[0][0] == 't' and issue['Type'][0] == tmp[1][0]:
                            print issue
                            break
                        elif tmp[0][0] == 'd':
                            # date range
                            dts = dateparse.DateParser().parse_date_range( tmp[1] )
                            if issue.date() >= dts[0] and issue.date() <= dts[1]:
                                print issue
                                break
                else:
                    if args[0][0] == '/':
                      if issue['Title'].find(args[0][1:]) != -1:
                          print issue  
                    elif file.startswith( args[0] ):
                        issue.show()
            else:
                print issue

    def do_add( self, args ):
        """ add an issue 
        
        bgz add [type]
        
        where type is:
                (b)ug | (t)ask | (f)eature
        """            
        self._check_status()
        # default type
        if len(args) < 1:
            args = ['bug']
            
        if len(args) and args[0][0] in Issue.types.keys() or args[0][0] == 'p':
            type = args[0][0]
        else:
            type = self._read_input( 'Type: (b)ug, (f)eature, (t)ask | (p)roject?', 'b', ('b','t','f','p'))
            
        if type =='p':
            self._add_project( self.BGZ_DIR )
            return
        print 'Adding new ' + Issue.types[type].lower()
        title = self._read_input('Title')
        author = self._read_input('Author',self.user_id)
        #desc = self._read_multiline('Descr')
        desc = self._external_edit('\n\n### ' + title )
        
        issue = Issue( self.BGZ_DIR )
        issue['Title'] = title
        issue['Description'] = desc
        issue['Type'] = type
        issue['Author'] = author
        issue.save()        
        print 'Added: ' + str(issue)
        
    def do_help( self, args ):
        """ show help
        
        bgz help [command]
        """
        try:
            func = getattr(self,'do_' + args[0] )
            print func.__doc__
        except Exception, e:
            m = dir( self )
            print 'Available Commands (type help [command] for more info)'
            print
            for cmd in m:
                if cmd.startswith('do_'):
                    func = getattr(self, cmd)
                    print "%20s - %s" % (cmd[3:], func.__doc__.split("\n")[0])
            print
            print
        
    def do_config( self, args ):
        """ create a config file 
        
        bgz config [global]
        """
        init_file = os.path.join(self.BGZ_DIR, self.BGZRC_LOCAL)
        if len(args) and args[0][0] == 'g':            
            init_file = os.path.join(os.getenv("HOME"), self.BGZRC_GLOBAL)
        print 'Creating ' + init_file
        user = self._read_input("Your name: ", os.getenv("USER"))
        email = self._read_input("Your email: ", user + "@" + os.uname()[1])
        f = open( init_file, 'w' )
        f.write("user=" + user + "\n")
        f.write("email=" + email + "\n")
        f.close()
        print "Wrote " + init_file
        
    # -------------------------
    # protected/private methods
    # -------------------------
    def _debug( msg ):
        """ do some logging """
        if self.opts.debug:
            print "DEBUG: " + msg
    
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
        files = os.listdir( self.BGZ_DIR )        
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
            if not os.path.exists(os.path.join(self.BGZ_DIR,'general.' + self.user_name)):
                gen = Issue(self.BGZ_DIR)
                gen['Id'] = 'general.' + self.user_name
                gen['Title'] = 'General Project Catchall'
                gen['Author'] = self.user_id
                gen['Type'] = 'task'
                gen['Status'] = 'open'
                gen.save()
        flist = self._find_issues( uid )
        if len(flist) == 1:
            iss = Issue(self.BGZ_DIR)
            if not iss.load( flist[0] ):
                return None
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

    def _home_dir( self ):
        """ return path to the users home folder """
        # return os.path.expanduser('~') <- does this work in Win??
        return os.getenv("USERPROFILE") or os.getenv("HOMEPATH") or os.getenv("HOME") or '.'
        
    def _read_init( self ):
        """ try and find the init file and read it """
        init_file = os.path.join(self._home_dir(), self.BGZRC_GLOBAL)
        local_init_file = os.path.join(self.BGZ_DIR, self.BGZRC_LOCAL)
        if os.path.exists( init_file ):
            self._read_config( init_file )
        if os.path.exists( local_init_file ):
            self._read_config( local_init_file )
        
    def _find_bugs_dir( self ):
        """this walks up the path and tries to find the bugs dir"""
        curpath = os.path.abspath(os.curdir)
        while len(curpath):
            if os.path.exists(os.path.join(curpath, self.BGZ_DIR)):
                self.BGZ_DIR = os.path.join(curpath, self.BGZ_DIR)
                return True
            curpath = curpath[0:curpath.rfind('/')]
        return False

    def _check_status( self ):
        """ make sure we have a data dir to work with """
        if not os.path.exists( self.BGZ_DIR ):
            print 'abort: No bugz repository found (%s)' %  self.BGZ_DIR
            sys.exit( 1 )
                
    def _read_projects( self ):
        """ read in the projects list, if any """
        projects = [self.BGZ_DIR]
        proj_file = os.path.join(self._home_dir(), self.BGZRC_PROJS)
        if os.path.exists( proj_file ):
            projects = open( proj_file ).read().splitlines()
        return projects
    
    def _save_projects( self, projects ):
        """ save a list of project directories """
        proj_file = os.path.join(self._home_dir(), self.BGZRC_PROJS)
        try:
            f = open( proj_file, 'w' )
            for proj in projects:
                f.write( proj + "\n" )
            f.close()
        except Exception, e:
            print e
        
    def _add_project( self, proj_path ):
        """ add a project to the project path list """
        ppath = os.path.expanduser( proj_path )
        ppath = os.path.abspath( ppath )
        projects = self._read_projects()
        for proj in projects:
            if ppath == proj:
                print 'Project exists: ' + ppath
                return
        projects.append( ppath )
        print 'Added project: ' + ppath
        self._save_projects( projects )
        
    def _remove_project( self, proj_path ):
        """ remove a project from the project path list """
        ppath = os.path.expanduser( proj_path )
        ppath = os.path.abspath( ppath )
        projects = self._read_projects()
        for proj in projects:
            if ppath == proj:
                projects.remove( ppath )
                print 'Dropped project: ' + ppath
        self._save_projects( projects )
        
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
