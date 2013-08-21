from StringIO import StringIO
from lxml import etree

html1 = """
<html>
<body>
<p>Test</p>
</body>
</html>
"""

html2 = """
<html>
</html>
"""

DOC = html2

fileh = StringIO(DOC)

context = etree.iterparse(fileh, events=('start', 'end'), html=True)
event, el = context.next()