import os
import sys
import time
import tempfile

from issue import Issue

class Bugz:
    """ this is the bugz class that handles the user """
    def __init__( self ):
        self.dir_name = '.bugz'
        self.editor_cmd = 'vi'
        try:
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
        issue = Issue(self.dir_name)
        counts = {'new':0,'open':0,'closed':0}
        for file in files:
            issue.load( file )
            counts[issue['Status']] += 1
        print 'Status'
        print counts
            
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
                if args[0].find(':') != -1:
                    for arg in args:
                        tmp = arg.split(':')
                        if tmp[0] == 's' and issue['Status'][0] == tmp[1][0]:
                            print issue
                        elif tmp[0] == 't' and issue['Type'][0] == tmp[1][0]:
                            print issue
                else:
                    if file.startswith( args[0] ):
                        issue.show()
            else:
                print issue

    def do_add( self, args ):
        """ add an issue """
        self._check_status()
        title = self._read_input('Title')
        type = self._read_input( 'Type: (b)ug, (f)eature, (t)ask?', 'b', ('b','t','f'))
        author = self._read_input('Author',os.environ['USER'])
        desc = self._read_multiline('Descr')
        comm = self._read_multiline('Comment')
        
        issue = Issue( self.dir_name )
        issue['Title'] = title
        issue['Description'] = desc
        issue['Type'] = type
        issue['Author'] = author
        issue.add_comment( comm )
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
        
    def _find_issues( self, uid ):
        """ find issues like a uid """
        files = os.listdir( self.dir_name )        
        flist = []
        for file in files:
            if file.startswith(uid):
                flist.append(file)
        return flist
        
    def _find_issue( self, uid ):
        """ find an issue with a partial uid """
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
        
    def _check_status( self ):
        """ make sure we have a database to work with """
        if not os.path.exists( self.dir_name ):
            print 'Database not found: ' + self.dir_name
            sys.exit( 1 )
    
    def _read_input( self, prompt, dflt = None, valid = None ):
        """ read one line user input """
        if dflt:
            prompt += ' [' + dflt + ']'
        inp = raw_input( prompt + ": " )
        if valid and not dflt:
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
        return "".join(lines)
        
