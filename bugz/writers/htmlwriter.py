
from basewriter import *
import sys

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
