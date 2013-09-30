import scraperwiki
import lxml.html
import re

url = 'http://www.senato.it/japp/bgt/showdoc/frame.jsp?tipodoc=ListEmendc&leg=17&id=40632'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

t = root.cssselect('b')
for i in t:
    if i.text and ( re.match("^\d+\.\d+", i.text) or re.match("^G/\d+/\d+/\d+", i.text) ):
        record = {
            "id" : i.text,
        }
        scraperwiki.sqlite.save(unique_keys=["id"], data=record)
    

import scraperwiki
import lxml.html
import re

url = 'http://www.senato.it/japp/bgt/showdoc/frame.jsp?tipodoc=ListEmendc&leg=17&id=40632'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

t = root.cssselect('b')
for i in t:
    if i.text and ( re.match("^\d+\.\d+", i.text) or re.match("^G/\d+/\d+/\d+", i.text) ):
        record = {
            "id" : i.text,
        }
        scraperwiki.sqlite.save(unique_keys=["id"], data=record)
    

