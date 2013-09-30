import scraperwiki
import re
import time
from BeautifulSoup import BeautifulSoup, Tag

def a_to_z(url):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in letters:
        yield url % letter

def absolute(url):
    return "http://www.dft.gov.uk/dsa/%s" % url

index_urls = a_to_z(absolute("dsa_theory_test_az.asp?letter=%s&CAT=-1&s=&TypeID=18&TestType="))

def first(gen):
    for a in gen:
        yield a
        return

def all(gen):
    for a in gen:
        yield a

def scrape(url):
    html = scraperwiki.scrape(url)
    time.sleep(2)
    return html

process = all

def soup_strip_html(st):
        return ' '.join([e.strip() for e in st.recursiveChildGenerator() if isinstance(e,unicode)])

def soup_strip_html_preserve_brs(st):
    def munge(e):
        if isinstance(e,unicode):
            return e.strip()
        elif isinstance(e,Tag) and e.name == "br":
            return "\n"
        else:
            return ""

    return ''.join([ munge(e) for e in st.recursiveChildGenerator()]).strip("\n")    

center_urls = []
for url in process(index_urls):
    html = scrape(url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a',attrs = {"href": re.compile("^dsa_theory_test_details")})
    for link in links:
        url = link["href"]
        name = link.text
        center_urls.append((url,name))
    
for url,town in process(center_urls):
    html = scrape(absolute(url))
    soup = BeautifulSoup(html)
    titles = soup.findAll('h3')
    for title in titles:
        if title.text <> "":
            center_name = title.text
            address = soup_strip_html_preserve_brs(title.findNextSibling("p"))
            postcode = address.split("\n")[-1]
            scraperwiki.datastore.save(unique_keys=['url'], data= { "url":url,
                                           "town":town,"center_name":center_name,
                                           "address":address,"postcode":postcode})
                import scraperwiki
import re
import time
from BeautifulSoup import BeautifulSoup, Tag

def a_to_z(url):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in letters:
        yield url % letter

def absolute(url):
    return "http://www.dft.gov.uk/dsa/%s" % url

index_urls = a_to_z(absolute("dsa_theory_test_az.asp?letter=%s&CAT=-1&s=&TypeID=18&TestType="))

def first(gen):
    for a in gen:
        yield a
        return

def all(gen):
    for a in gen:
        yield a

def scrape(url):
    html = scraperwiki.scrape(url)
    time.sleep(2)
    return html

process = all

def soup_strip_html(st):
        return ' '.join([e.strip() for e in st.recursiveChildGenerator() if isinstance(e,unicode)])

def soup_strip_html_preserve_brs(st):
    def munge(e):
        if isinstance(e,unicode):
            return e.strip()
        elif isinstance(e,Tag) and e.name == "br":
            return "\n"
        else:
            return ""

    return ''.join([ munge(e) for e in st.recursiveChildGenerator()]).strip("\n")    

center_urls = []
for url in process(index_urls):
    html = scrape(url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a',attrs = {"href": re.compile("^dsa_theory_test_details")})
    for link in links:
        url = link["href"]
        name = link.text
        center_urls.append((url,name))
    
for url,town in process(center_urls):
    html = scrape(absolute(url))
    soup = BeautifulSoup(html)
    titles = soup.findAll('h3')
    for title in titles:
        if title.text <> "":
            center_name = title.text
            address = soup_strip_html_preserve_brs(title.findNextSibling("p"))
            postcode = address.split("\n")[-1]
            scraperwiki.datastore.save(unique_keys=['url'], data= { "url":url,
                                           "town":town,"center_name":center_name,
                                           "address":address,"postcode":postcode})
                