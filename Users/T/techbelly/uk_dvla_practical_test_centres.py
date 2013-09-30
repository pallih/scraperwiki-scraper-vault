# http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?Cat=-1&TestType=car&TypeID=17
# http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?letter=G&CAT=-1&s=&TypeID=17&TestType=car

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

index_urls = a_to_z(absolute("AtoZservices_Bannered.asp?letter=%s&CAT=-1&s=&TypeID=17&TestType="))

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

def soup_strip_html_preserve_brs(st):
    if st is None:
        return '' 

    def munge(e):
        if isinstance(e,unicode):
            return e.strip()
        elif isinstance(e,Tag) and e.name == "br":
            return "\n"
        else:
            return ""

    return ''.join([ munge(e) for e in st.recursiveChildGenerator()]).replace("&nbsp;"," ").strip("\n").strip()


center_urls = set()
for url in process(index_urls):
    html = scrape(url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a',attrs = {"href": re.compile("^AddressDetails_Bannered.asp")})
    for link in links:
        url = link["href"]
        name = link.text
        center_urls.add((url,name))

for url,p_title in process(center_urls):
    html = scrape(absolute(url))
    soup = BeautifulSoup(html)
    title = soup.find('h3')
    if title.text <> "":
        addressNode = title.findNextSibling("p")
        center_name = title.text
        address = soup_strip_html_preserve_brs(addressNode)
        postcode = address.split("\n")[-1]

        def has_details_node():
            next_h3 = addressNode.findNextSibling("h3")
            if next_h3 is None:
                return None
            elif next_h3.text == "":
                return None
            else:
                return next_h3
        
        def is_test_type(line):
            return ":" in line and line.split(":")[0] in ["Car","Motorcycle Module 2","Motorcycle Module 1","Taxi","Vocational"]


        if has_details_node():
            detailsNode = addressNode.findNextSibling("p")
            additional_details = soup_strip_html_preserve_brs(detailsNode)
            testsNode = detailsNode.findNextSibling("p").findNextSibling("p")
        else:
            additional_details = ""      
            testsNode = addressNode.findNextSibling("p").findNextSibling("p") 

        if addressNode.findNextSibling("strong"):
            additional_details = None
            startNode = addressNode
            test_types = []
            while True:
                testNode = startNode.findNextSibling("strong")
                if testNode is None:
                    break
                test = testNode.text.strip(" :")  
                details = testNode.nextSibling.replace("&nbsp;"," ").replace(": ","").strip()
                test_types.append([test,details])
                startNode = testNode.nextSibling
        else:                 
            tests = soup_strip_html_preserve_brs(testsNode)
            test_types = [line.split(":") for line in tests.split("\n") if is_test_type(line)]

        data = {
            "url": url,
            "title": p_title,
            "center_name": center_name,
            "address": address,
            "postcode": postcode,
            "additional_details": additional_details,
            "on_offer": ",".join([t[0] for t in test_types])
        }

        for t in test_types:
             data[t[0].lower()+"_avail"] = t[1]  
                  

        scraperwiki.sqlite.save(unique_keys=['url'], data= data)


# http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?Cat=-1&TestType=car&TypeID=17
# http://www.dft.gov.uk/dsa/AtoZservices_Bannered.asp?letter=G&CAT=-1&s=&TypeID=17&TestType=car

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

index_urls = a_to_z(absolute("AtoZservices_Bannered.asp?letter=%s&CAT=-1&s=&TypeID=17&TestType="))

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

def soup_strip_html_preserve_brs(st):
    if st is None:
        return '' 

    def munge(e):
        if isinstance(e,unicode):
            return e.strip()
        elif isinstance(e,Tag) and e.name == "br":
            return "\n"
        else:
            return ""

    return ''.join([ munge(e) for e in st.recursiveChildGenerator()]).replace("&nbsp;"," ").strip("\n").strip()


center_urls = set()
for url in process(index_urls):
    html = scrape(url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a',attrs = {"href": re.compile("^AddressDetails_Bannered.asp")})
    for link in links:
        url = link["href"]
        name = link.text
        center_urls.add((url,name))

for url,p_title in process(center_urls):
    html = scrape(absolute(url))
    soup = BeautifulSoup(html)
    title = soup.find('h3')
    if title.text <> "":
        addressNode = title.findNextSibling("p")
        center_name = title.text
        address = soup_strip_html_preserve_brs(addressNode)
        postcode = address.split("\n")[-1]

        def has_details_node():
            next_h3 = addressNode.findNextSibling("h3")
            if next_h3 is None:
                return None
            elif next_h3.text == "":
                return None
            else:
                return next_h3
        
        def is_test_type(line):
            return ":" in line and line.split(":")[0] in ["Car","Motorcycle Module 2","Motorcycle Module 1","Taxi","Vocational"]


        if has_details_node():
            detailsNode = addressNode.findNextSibling("p")
            additional_details = soup_strip_html_preserve_brs(detailsNode)
            testsNode = detailsNode.findNextSibling("p").findNextSibling("p")
        else:
            additional_details = ""      
            testsNode = addressNode.findNextSibling("p").findNextSibling("p") 

        if addressNode.findNextSibling("strong"):
            additional_details = None
            startNode = addressNode
            test_types = []
            while True:
                testNode = startNode.findNextSibling("strong")
                if testNode is None:
                    break
                test = testNode.text.strip(" :")  
                details = testNode.nextSibling.replace("&nbsp;"," ").replace(": ","").strip()
                test_types.append([test,details])
                startNode = testNode.nextSibling
        else:                 
            tests = soup_strip_html_preserve_brs(testsNode)
            test_types = [line.split(":") for line in tests.split("\n") if is_test_type(line)]

        data = {
            "url": url,
            "title": p_title,
            "center_name": center_name,
            "address": address,
            "postcode": postcode,
            "additional_details": additional_details,
            "on_offer": ",".join([t[0] for t in test_types])
        }

        for t in test_types:
             data[t[0].lower()+"_avail"] = t[1]  
                  

        scraperwiki.sqlite.save(unique_keys=['url'], data= data)


