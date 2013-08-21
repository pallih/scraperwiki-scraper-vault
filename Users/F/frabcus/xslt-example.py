# Example of calling XSLT transformations in Python

from lxml import etree
from StringIO import StringIO

f = StringIO('''

 <xsl:stylesheet version="1.0"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
     <xsl:template match="/">
         <foo><xsl:value-of select="/a/b/text()" /></foo>
     </xsl:template>
</xsl:stylesheet>

''')

xslt_doc = etree.parse(f)
transform = etree.XSLT(xslt_doc)


f = StringIO('<a><b>Text</b></a>')
doc = etree.parse(f)
result_tree = transform(doc)

print str(result_tree)
