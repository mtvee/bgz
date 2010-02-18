# encoding: utf-8
"""
bgz
http://github.com/mtvee/bgz
License Mozilla Public License 1.1 (MPL 1.1)
Copyright (c) 2010 J. Knight. All rights reserved.
"""

import sys
import types

# -----------------
# F A C T O R Y
# -----------------
class WriterFactory:
    def __init__( self ):
        pass
        
    def get_writer( self, which ):
        if which == 'xml':
            return ExcelXMLWriter()
        elif which == 'csv':
            return CSVWriter()
        elif which == 'html':
            return HTMLWriter()

# -----------------
# B A S E
# -----------------
class BaseWriter:
    """ Basic Writer """
    def __init__( self ):
        self.data = [[]]
        self.headers = None
        self.out = sys.stdout
        self.EOL = "\n"
        
    def setData( self, data ):
        """data is an array of arrays"""
        self.data = data

    def setFile( self, fname ):
        """set the output file"""
        self.out = open( fname, "w" )

    def setHeaders( self, hdrs ):
        self.headers = hdrs

    def write( self ):
        """do it"""
        self.p( str(self.data) )

    def p( self, str ):
        """ output a line with EOL """
        self.out.write( str + self.EOL )

# -----------------
# C S V
# -----------------
class CSVWriter( BaseWriter ):
    def __init__( self ):
        BaseWriter.__init__( self ) 

    def write( self ):
        """ output the info """
        if self.headers:
            self.writeLine( self.headers )
        for line in self.data:
            self.writeLine( line )
                        
    def writeLine( self, line ):
        """output an array/line"""
        s = ""
        for item in line:
            if type(item) in (types.IntType,types.FloatType):
                s += str(item) + ","
            else:
                s += '"' + self.escape(str(item)) + '",'
        self.p(s[:-1])

    def escape( self, str ):
        return str.replace('"','""')

# -----------------
# H T M L
# -----------------
class HTMLWriter( BaseWriter ):
    """An HTML writer"""
    def __init__( self ):
        BaseWriter.__init__( self )

    def write( self ):
        self.p( self.header() )
        self.p('<table>')
        for line in self.data:
            self.p('      <tr>')
            for item in line:
                self.p('<td>' + self.escape(str(item))  + "</td>")
            self.p('      </tr>')
        self.p('</table>')
        self.p( self.footer() )
        if self.out != sys.stdout:
            self.out.close()

    def escape( self, str ):
        str = str.replace('&','&amp;')
        str = str.replace('<','&lt;')
        str = str.replace('>','&gt;')
        return str


    def header( self ):
        return """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

        <head>
        	<title></title>
        	<!-- style -->
        	<style type="text/css">
        	</style>

        	<!-- meta -->
        	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        	<meta name="keywords" content="" />
        	<meta name="author" content="" />
        	<meta name="generator" content="" />
        	<meta name="description" content="" />	
        </head>
        <body>
        """

    def footer( self ):
        return """ 
        </body>
        </html>"""

# -----------------
# X M L (Excel)
# -----------------
class ExcelXMLWriter( BaseWriter ):
    """ An Excel XML 2004 Writer """
    def __init__( self ):
        BaseWriter.__init__( self )
                
    def write( self ):
        self.p( self.header() )
        # we can output column widths here, before the data starts
        # i think the default width is 50 and I'm not sure what happens
        # or if you can skip unaffected columns at the start
        self.p('      <Column ss:AutoFitWidth="0" ss:Width="48.0" />')
        self.p('      <Column ss:AutoFitWidth="0" ss:Width="50.0" />')
        self.p('      <Column ss:AutoFitWidth="0" ss:Width="200.0" />')
        
        # data begins
        self.p('      <Row ss:StyleID="s22">')
        self.p('        ' + self.cell('Report Title'))
        self.p('      </Row>')
        self.p('      <Row>')
        self.p('        ' + self.cell('Report Sub-Title', 's21'))
        self.p('      </Row>')
        for line in self.data:
            self.p('      <Row>')
            for item in line:
                self.p('        ' + self.cell( item ))
            self.p('      </Row>')
        self.p(self.footer())
        if self.out != sys.stdout:
            self.out.close()
     
    def escape( self, str ):
        str = str.replace('&','&amp;')
        str = str.replace('<','&lt;')
        str = str.replace('>','&gt;')
        str = str.replace('"','&quot;')
        str = str.replace("'",'&apos;')
        return str
     
    def cell( self, data, style=None ):
        cell = '<Cell'
        if style:
            cell += ' ss:StyleID="' + style + '"'
        cell += '><Data ss:Type="'
        if type(data) in (types.IntType,types.FloatType):
            cell += 'Number'
        else:
            cell += 'String'
        cell += '">' + self.escape(str(data)) + '</Data></Cell>'
        return cell
     
    def footer( self ):
        return """    </Table>
  </Worksheet>
</Workbook>"""
     
    def header( self ):
        return """<?xml version="1.0"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" 
 xmlns:o="urn:schemas-microsoft-com:office:office" 
 xmlns:x="urn:schemas-microsoft-com:office:excel" 
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" 
 xmlns:html="http://www.w3.org/TR/REC-html40"> 
 <DocumentProperties xmlns="urn:schemas-microsoft-com:office:office" > 
   <Author></Author> 
   <LastAuthor></LastAuthor> 
   <Created></Created> 
   <LastSaved></LastSaved> 
   <Company></Company> 
   <Version></Version> 
 </DocumentProperties> 
 <OfficeDocumentSettings xmlns="urn:schemas-microsoft-some:office:office"> 
 </OfficeDocumentSettings> 
 <ExcelWorkbook xmlns="urn:schemas-microsoft-some:office:excel"> 
 </ExcelWorkbook> 
 <Styles> 
   <Style ss:ID="Default" ss:Name="Normal"> 
    <Alignment ss:Vertical="Bottom" /> 
    <Borders />
    <Font ss:FontName="Verdana"/>
    <Interior />
    <NumberFormat />
    <Protection />
   </Style>
   <Style ss:ID="s21">
    <Font ss:FontName="Verdana" ss:Bold="1"/>
   </Style>
   <Style ss:ID="s22">
    <Font ss:FontName="Verdana" ss:Size="14.0" ss:Bold="1"/>
    <Interior ss:Color="#DDDDDD" ss:Pattern="Solid" />
   </Style>
   <Style ss:ID="s23">
    <Alignment ss:Vertical="Bottom" ss:WrapText="1" />
   </Style>
 </Styles> 
 <Worksheet ss:Name="%s">
   <Table ss:ExpandedColumnCount="%d"
          ss:ExcpanedRowCount="%d"
          x:FullColumns="1" x:FullRows="1">""" % ('Excel',len(self.data[0]),len(self.data))
     
     
# ------------------
# U N I T  T E S T S
# ------------------
import unittest

class WriterTests(unittest.TestCase):
    def setUp( self ):
        pass
     
    def testSomething( self ):
        xml = WriterFactory().get_writer('html')
        xml.setHeaders(["One","Two","Three","Four","Four and a Bit","Five"])
        xml.setData([["one","two \"for\" & 'five' < six > 6",3,"four",4.5,"five,"]])
        #xml.setFile('test.xml')
        xml.write()       
        self.assertEqual(1,1)
        
if __name__ == '__main__':
    unittest.main()
    
