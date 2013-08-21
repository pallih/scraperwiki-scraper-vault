from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save, select
import re

def loadraw():
    text = urlopen('http://www.jfychicago.org/student/stu_resources.html').read()
    for section in text.split('<hr>')[1:]:
        html = fromstring(section)
        titles = [b.text_content() for b in html.cssselect('p font b')]
        #assert len(titles) == 1 or 'locations' in titles[1].lower(), titles
        title = titles[0]
        d = [{'raw': p.text_content(), 'section': title} for p in html.cssselect('p')]
        save([], d, 'raw')

#loadraw()
for row in select('* from raw'):
    print re.sub(r'\s', '', row['raw'])