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

# Full backtrace is given with DOC = html2, DOC = html1 just produces "segmentation fault"
DOC = html2

# Problem only occurs when html param is set to True
HTML = True

# Segfault occurs with either of these configurations
EVENTS = ['start']
#EVENTS = ['start', 'end']

# Neither of these produce the segfault
#EVENTS = ['end']
#EVENTS = None

fileh = StringIO(DOC)
context = etree.iterparse(fileh, events=EVENTS, html=HTML)
event, el = context.next()
print event, el