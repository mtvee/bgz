
import os
import time
import pickle
import uuid
import UserDict

class Issue(UserDict.UserDict):
    """ This is a class to represent an issue of some kind """
    def __init__( self, dname ):
        self.dir_name = dname
        self.data = {}
        self.comments = {}
        self.keys = ['Id','Title','Date','Status','Author','Description']
        for key in self.keys:
            self.data[key] = ''
        self.data['Id'] = str(uuid.uuid1())
        self.data['Date'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.data['Status'] = 'new'
                
    def __str__( self ):
        """ return a short descriptive string """
        tmp = self['Id'].split('-')
        ret = "%s - %s/%s - %s" % (tmp[0],self['Type'],self['Status'].ljust(6),self['Title'])
        if len(ret) > 75:
            ret = ret[0:75] + "..."
        return ret
        
    def show( self ):
        """ print the whole mess """
        print '         Id: ' + self['Id']
        print '      Title: ' + self['Title']
        print '       Date: ' + self['Date']
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
