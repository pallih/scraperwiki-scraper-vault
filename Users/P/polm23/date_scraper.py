import scraperwiki
import re
import lxml.html

# Blank Python
dates = {}
for word in ["telephone", "catfish", "banana", "panda", "sushi", "crabapple", "corkscrew"]:
    html = scraperwiki.scrape("http://dictionary.reference.com/browse/" + word)           
    root = lxml.html.fromstring(html)
    for tr in root.cssselect(".rom-inline"):
        if re.match(r'[12]\d\d\d', tr.text_content()):
            dates[word] = tr.text_content()[0:4]

for (k,v) in dates.items():
    print v + '\t' + k
import scraperwiki
import re
import lxml.html

# Blank Python
dates = {}
for word in ["telephone", "catfish", "banana", "panda", "sushi", "crabapple", "corkscrew"]:
    html = scraperwiki.scrape("http://dictionary.reference.com/browse/" + word)           
    root = lxml.html.fromstring(html)
    for tr in root.cssselect(".rom-inline"):
        if re.match(r'[12]\d\d\d', tr.text_content()):
            dates[word] = tr.text_content()[0:4]

for (k,v) in dates.items():
    print v + '\t' + k
