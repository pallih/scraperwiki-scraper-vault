###############################################################################
# Basic scraper
###############################################################################

import scraperwiki, re, HTMLParser
from BeautifulSoup import BeautifulSoup

class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    #Warning this does all including script and javascript
    x = MLStripper()
    x.feed(html)
    return x.get_fed_data()
# new bit
def match(s, reg):
    p = re.compile(reg, re.IGNORECASE| re.DOTALL)
    results = p.findall(s)
    return results

# retrieve a page
starting_url = 'http://www.stats19.org.uk/html/local_authority_codes.html'
html = scraperwiki.scrape(starting_url)

soup = BeautifulSoup(html)
tds = soup.findAll('td') 

td1 = tds[ 35 ] # the left TD
td2 = tds[ 40 ] # the right TD

data = str(td1) + str(td2)

chunks = match(data, '<font face="Verdana,Tahoma,Arial,Helvetica,Sans-serif,sans-serif">.*?<b>(.*?)</p>(.*?)<p align="LEFT"><font face="Verdana,Tahoma,Arial,Helvetica,Sans-serif,sans-serif">&nbsp;</font></p>' )

print len(chunks), "chunks found"

for region, subchunkdata in chunks:
    region = strip_tags(region)
    subregion = match(subchunkdata, '<p align="LEFT"><font face="Verdana,Tahoma,Arial,Helvetica,Sans-serif,sans-serif"></font><font size="-1" face="Arial,Helvetica,Geneva,Sans-serif,sans-serif">(\d*) (.*?)</font></p>')
    for code, name in subregion:
        print region, code, name
        record = {'id': name+ "_" + code, 'name':name, 'region':region, 'code':code } 
        scraperwiki.sqlite.save([ 'id' ], record)
    print
    
    
    
    
           

    