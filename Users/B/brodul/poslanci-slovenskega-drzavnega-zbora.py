###############################################################################
# 
###############################################################################

from BeautifulSoup import BeautifulSoup
import urllib
import re

import scraperwiki

URL = "http://www.dz-rs.si/index.php?id=92"
CORE_URL = "http://www.dz-rs.si"
DEBUG = 0



# retrieve a page
def make_soup(url):
    """

    """
    sock = scraperwiki.scrape(url)
    htmlSource = sock
    soup = BeautifulSoup(htmlSource)

    return soup

class Poslanec(object):
    """

    """
    def __init__(self, name):
        self.name = name

    def add_pict(self, url):
        self.pict = url

    def get_date(self, s):
        pattern = re.compile(r'\d+\s??\.\s??\d+\.\s??\d{4}')
        date = pattern.search(s).group(0)
        
        self.dborn = date.replace(" ","")
    
    def make_csv_file(file):
        pass



soup = make_soup(URL)
html_poslanci = soup.find(id="acts_modul")("a")[3:]

poslanci = []

if DEBUG:
    html_poslanci = html_poslanci[2:7]
    print "DEBUG mode on"


for html_poslanec in html_poslanci:
    poslanec = Poslanec(html_poslanec.text)
    print poslanec.name
    osebna_stran = CORE_URL + html_poslanec["href"]
    soup2 = make_soup(osebna_stran)
    for n in soup2.find("table", {"class": "main_table"})("img"):
        try:
            if n['alt']:
                poslanec.add_pict(CORE_URL + "/" + n.parent['href'].replace(' ', '%20'))
                poslanec.iname = n['alt']
        except:
            pass
    
    
    s = soup2.find("h3", {"class": "docdatatitle"}).findNextSiblings(text=True)[0]
    poslanec.get_date(s)
    poslanec.skup = soup2.find("table", {"class": "main_table"}).find("td", width="80%").contents[4].replace("-","").strip()
    poslanci.append(poslanec)



for poslanec in poslanci:
    record = { "name": poslanec.name, "picture_url": poslanec.pict, "inverted_name": poslanec.iname, "date_born": poslanec.dborn, "skupina": poslanec.skup , }
    # save records to the datastore
    scraperwiki.datastore.save(["name"], record) 
    ###############################################################################
# 
###############################################################################

from BeautifulSoup import BeautifulSoup
import urllib
import re

import scraperwiki

URL = "http://www.dz-rs.si/index.php?id=92"
CORE_URL = "http://www.dz-rs.si"
DEBUG = 0



# retrieve a page
def make_soup(url):
    """

    """
    sock = scraperwiki.scrape(url)
    htmlSource = sock
    soup = BeautifulSoup(htmlSource)

    return soup

class Poslanec(object):
    """

    """
    def __init__(self, name):
        self.name = name

    def add_pict(self, url):
        self.pict = url

    def get_date(self, s):
        pattern = re.compile(r'\d+\s??\.\s??\d+\.\s??\d{4}')
        date = pattern.search(s).group(0)
        
        self.dborn = date.replace(" ","")
    
    def make_csv_file(file):
        pass



soup = make_soup(URL)
html_poslanci = soup.find(id="acts_modul")("a")[3:]

poslanci = []

if DEBUG:
    html_poslanci = html_poslanci[2:7]
    print "DEBUG mode on"


for html_poslanec in html_poslanci:
    poslanec = Poslanec(html_poslanec.text)
    print poslanec.name
    osebna_stran = CORE_URL + html_poslanec["href"]
    soup2 = make_soup(osebna_stran)
    for n in soup2.find("table", {"class": "main_table"})("img"):
        try:
            if n['alt']:
                poslanec.add_pict(CORE_URL + "/" + n.parent['href'].replace(' ', '%20'))
                poslanec.iname = n['alt']
        except:
            pass
    
    
    s = soup2.find("h3", {"class": "docdatatitle"}).findNextSiblings(text=True)[0]
    poslanec.get_date(s)
    poslanec.skup = soup2.find("table", {"class": "main_table"}).find("td", width="80%").contents[4].replace("-","").strip()
    poslanci.append(poslanec)



for poslanec in poslanci:
    record = { "name": poslanec.name, "picture_url": poslanec.pict, "inverted_name": poslanec.iname, "date_born": poslanec.dborn, "skupina": poslanec.skup , }
    # save records to the datastore
    scraperwiki.datastore.save(["name"], record) 
    