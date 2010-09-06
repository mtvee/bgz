# -*- Mode: python; tab-width: 4; indent-tabs-mode: nil; encoding: utf-8 -*-
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import os
import time
import datetime
import uuid
import UserDict
# storage
import pickle
from xml.dom import minidom

class Issue(UserDict.UserDict):
    """ 
    This is a class to represent an issue of some kind 
    """
    types = {'t':'Task','b':'Bug','f':'Feature'}
    
    def __init__( self, dname ):
        self.dir_name = dname
        # default keys and values
        self.defaults = {
                    'Id':str(uuid.uuid1()),
                    'Title': 'No Title',
                    'Date': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    'Status': 'new',
                    'Author': 'anon',
                    'Type': 'b',
                    'Description': ''
                    }
        self.reset()
        
    def reset( self ):
      self.data = {}
      self.comments = {}
      for key in self.defaults.keys():
          self.data[key] = self.defaults[key]
    
    def __eq__( self, other ):
      if self['Id'] == other['Id']:
        return True
      return False
              
    def __str__( self ):
        """ return a short descriptive string thing """
        return self.rep()

    def rep( self, dts = None):
        """ return a short descriptive string thing """
        tmp = self['Id'].split('-')
        tm = self.time_total(dts)
        ret = "%12s - %s/%s - %2d:%02d - %s" % (tmp[0],self['Type'][0],self['Status'].ljust(6),tm[0],tm[1],self['Title'])
        if len(ret) > 75:
            ret = ret[0:75] + "..."
        return ret
        
    def date( self ):
        return datetime.datetime.strptime( self['Date'],"%Y-%m-%dT%H:%M:%SZ")
        
    def show( self ):
        """ print the whole mess """
        print '      Title: ' + self['Title']
        print '       Date: ' + self['Date']
        print '         Id: ' + self['Id']
        print '     Status: ' + self['Status']
        print '       Type: ' + self['Type']
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
        
    def time_total( self, dts = None ):
        tm = [0,0]
        for k, v in self.comments.iteritems():
            # ignore if we have a date range and we are outside of it
            ct = datetime.datetime.fromtimestamp(k)
            if dts and (ct <= dts[0] or ct >= dts[1]):
                continue
            if v.startswith('time '):
                parts = v[5:].split(":")
                for i in range(len(parts)):
                    try:
                        tm[i] += int(parts[i])
                    except:
                        pass
        tm[0] += tm[1] / 60
        tm[1] = tm[1] % 60
        return tm
                    
            
    def add_comment( self, comment ):
        """ add a comment """
        if len(comment.strip()):
            self.comments[time.time()] = comment
        
    def save( self ):
        """ save the thing """
        self.save_xml()
        #fname = os.path.join(self.dir_name, self['Id'])
        #f = open( fname, 'wb' )
        #pickle.dump(self.data,f)
        #pickle.dump(self.comments,f)
        #f.close()
        
    def load( self, uid ):
        """ load the thing """
        try:
          self.load_pickle( uid )
        except:
          try:
            self.load_xml( uid )
          except:
            return False
        return True

    def load_pickle( self, uid ):
      """ load and old style pickle format """
      fname = os.path.join(self.dir_name, uid )
      f = open( fname, 'rb' )
      self.data = pickle.load(f)
      self.comments = pickle.load(f)
      f.close()

    def createNodeWithText( self, doc, name, value ):
      """ create and return a dome node with a text node element """
      node = doc.createElement( name )
      node.appendChild(doc.createTextNode(value))
      return node

    def save_xml( self ):
      """ save the thing to xml """
      fname = os.path.join(self.dir_name, self['Id'])
      doc = minidom.getDOMImplementation().createDocument(None,"issue",None)
      doc.documentElement.appendChild(self.createNodeWithText(doc,"id", self['Id']))
      doc.documentElement.appendChild(self.createNodeWithText(doc,"title", self['Title']))
      doc.documentElement.appendChild(self.createNodeWithText(doc,"date", self['Date']))
      doc.documentElement.appendChild(self.createNodeWithText(doc,"status", self['Status']))
      doc.documentElement.appendChild(self.createNodeWithText(doc,"type", self['Type']))
      doc.documentElement.appendChild(self.createNodeWithText(doc,"author", self['Author']))
      doc.documentElement.appendChild(self.createNodeWithText(doc,"description", self['Description']))
      comments = doc.createElement('comments')
      keys = self.comments.keys()
      keys.sort()
      for key in keys:
          comment = doc.createElement('comment')
          comment.setAttribute('date', time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(key) ) )
          comment.appendChild( doc.createTextNode(self.comments[key]))
          comments.appendChild( comment )
      doc.documentElement.appendChild( comments )
      f = open( fname, 'wb' )
      f.write( doc.toprettyxml( indent="  ") )
      f.close()


    def load_xml( self, uid ):
      """ load an issue from xml """
      fname = os.path.join(self.dir_name, uid )
      doc = minidom.parse( fname )
      self.reset()
      for node in doc.documentElement.childNodes:
        if node.nodeName == 'id':
          self['Id'] = node.childNodes[0].nodeValue.strip()
        if node.nodeName == 'title':
          self["Title"] = node.childNodes[0].nodeValue.strip()
        if node.nodeName == 'date':
          self['Date'] = node.childNodes[0].nodeValue.strip()
        if node.nodeName == 'status':
          self["Status"] = node.childNodes[0].nodeValue.strip()
        if node.nodeName == 'type':
          self['Type'] = node.childNodes[0].nodeValue.strip()
        if node.nodeName == 'author':
          self["Author"] = node.childNodes[0].nodeValue.strip()
        if node.nodeName == 'description':
          self["Description"] = node.childNodes[0].nodeValue.strip()
          
      # comments
      for node in doc.getElementsByTagName('comment'):
        dt = time.mktime(datetime.datetime.strptime(node.getAttribute('date'),"%Y-%m-%dT%H:%M:%SZ").timetuple())
        self.comments[dt] = node.childNodes[0].nodeValue.strip()
            
# ------------------
# U N I T  T E S T S
# ------------------
import unittest

class IssueTests(unittest.TestCase):
    def setUp( self ):
        pass

    def testLoadSave( self ):
      iss1 = Issue('.')
      iss1['Description'] = "This is a description\nof some stuff"
      iss1.add_comment("This is a comment")
      iss1.add_comment("This is another comment")
      iss1.save_xml()
      iid = iss1['Id']
      # another issue
      iss2 = Issue('.')
      iss2.load_xml( iid )
      iss2.show()
      self.assertEqual( iss1, iss2 )
      os.unlink( iid )
        
if __name__ == '__main__':
    unittest.main()