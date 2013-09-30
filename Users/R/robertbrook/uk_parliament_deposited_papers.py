import scraperwiki
from lxml.html import parse

# see also https://gist.github.com/861913

page = parse('http://deposits.parliament.uk/').getroot()

for tr in page.cssselect('table.DP tr'):
    if tr.get("valign") == "top":
        print "NEW RECORD"
    for td in tr.cssselect('td'):
        print td.get("class")
        print td.text_content()
    import scraperwiki
from lxml.html import parse

# see also https://gist.github.com/861913

page = parse('http://deposits.parliament.uk/').getroot()

for tr in page.cssselect('table.DP tr'):
    if tr.get("valign") == "top":
        print "NEW RECORD"
    for td in tr.cssselect('td'):
        print td.get("class")
        print td.text_content()
    