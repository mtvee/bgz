
from basewriter import *
import sys
import types


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
     
