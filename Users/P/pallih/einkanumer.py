import scraperwiki,re
from lxml import etree
import lxml.html

url = 'http://www.us.is/Apps/WebObjects/US.woa/wa/dp?id=3045'



html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

#//tr/td

urls = root.xpath ('//form/div[1]/ul/li/a/@href')

for i in urls:
    record ={}
    url = 'http://www.us.is' + i
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    numer = root.xpath ( '//tr/td/text()')
    for n in numer:
        record['numer'] = n
        print record
        scraperwiki.sqlite.save(['numer'], data=record, table_name='einkanumer')
import scraperwiki,re
from lxml import etree
import lxml.html

url = 'http://www.us.is/Apps/WebObjects/US.woa/wa/dp?id=3045'



html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

#//tr/td

urls = root.xpath ('//form/div[1]/ul/li/a/@href')

for i in urls:
    record ={}
    url = 'http://www.us.is' + i
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    numer = root.xpath ( '//tr/td/text()')
    for n in numer:
        record['numer'] = n
        print record
        scraperwiki.sqlite.save(['numer'], data=record, table_name='einkanumer')
