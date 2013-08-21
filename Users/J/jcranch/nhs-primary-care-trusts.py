"""
Gets information on all NHS Primary Care Trusts and their hospitals, doctors,
dentists, pharmacies, opticians and other services.

Includes geolocating.

Obtained from:
    http://www.nhs.uk/ServiceDirectories/Pages/PrimaryCareTrustListing.aspx

All records have a "type" field:
  "main" means it's the data for the PCT itself
  "service" is the generic stuff off the front page (including hospitals)
  "doctor"
  "dentist"
  "pharmacy"
  "optician" are all self-explanatory



Current failings:
  - doesn't deep-scrape the information on the individual facilities pages yet
  - doesn't grab some odd information on the PCT main pages yet
  - bit slow to parse pages
     - partly because we have underspecified our search paths
     - partly because we make multiple passes
"""



from scraperwiki import datastore, scrape, geo
from html5lib import HTMLParser, treebuilders
from lxml import etree
import urlparse
import scraperwiki
import lxml
import lxml.html



debug = False



def main():
    pct_links = ListOfTrusts()
    for link, name in pct_links[:3]:
        scrape_pct(link, name)

def main():
    url = "http://www.nhs.uk/ServiceDirectories/Pages/PrimaryCareTrustListing.aspx"  
    doc = lxml.html.parse(url)
    root = doc.getroot()
    pct_links = []
    for trust in root.cssselect("ul.trust-list a"):
        pct_links.append((urlparse.urljoin(url, trust.get("href")), trust.text))
        
    for link, pct_name in pct_links:
        print link
        

def scrape_pct(link,pct_name):
    """
    Scrapes the data associated with the PCT, and calls functions to scrape
    data associated with the services.
    """
    
    print
    print
    print pct_name
    print "-"*len(pct_name)

    url = "http://www.nhs.uk" + link
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url))
    root = page.getroot()

    d = {}

    # basic contact details
    d["PCT"] = pct_name
    d["type"] = "main"
    d["name"] = pct_name
    address = root.find("body/div/form/div/div/p").text
    d["address"] = address
    postcode = geo.extract_gb_postcode(address)
    d["postcode"] = postcode
    d["latlng"] = geo.gb_postcode_to_latlng(postcode)
    d["info HTML"] = url

    # quality
    for t in root.findall("body/div/form/div/div/div/div/div/div/div[@class='service-feedback clear']"):
        k = t.find("div/h4").text.strip()
        v = t.find("div/img").attrib["alt"]
        d[k] = v

    # head honcho
    for t in root.findall("body/div/form/div/div/div/div/div/div/div/p[@class='profiles-picture-caption']"):
        d["Boss"] = t.text.replace("<br />",", ")

    # boring text
    for t in root.findall("body/div/form/div/div/div/div/div/div/p"):
        if t.text:
            if t.attrib.get("class",False)=="intro":
                d["intro text"] = t.text
            else:
                d["boilerplate"] = d.get("boilerplate","")+"\n"+t.text

    datastore.save(unique_keys=["PCT","type","name","address"], data=d, latlng=d.get("latlng"))

    scrape_facilities(pct_name,root)
    scrape_others(pct_name,url)



def scrape_facilities(pct_name,root):
    """
    Scrapes all the data about services listed on the PCT's main page.
    """
    s = root.find("body/div/form/div/div/div/div/div/div/div/dl[@class='clear']")
    extract_table_data(pct_name,s,"service")



def scrape_others(pct_name,url):
    types = ["doctor","dentist","pharmacy","optician"]
    for facility_type,i in zip(types,range(2,6)):
        parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
        page = parser.parse(scrape(url+"&v=%d"%i))
        root = page.getroot()

        s = root.find("body/div/form/div/div/div/div/div/dl")
        extract_table_data(pct_name,s,facility_type)



def extract_table_data(pct_name,s,facility_type):
    """
    Extracts data from a list of PCT facilities
    """

    services = []
    d = {}
    for t in s.getchildren():
        if t.tag=="dt":
            if d != {}:
                services.append(d)
            d = {"PCT":pct_name, "type":"service"}
            u = t.find("a")
            if u != None:
                t = u
                d["info HTML"] = "http://www.nhs.uk" + t.attrib["href"]
            name = (t.text or "").strip()
            d["name"] = name
            print name
        elif t.text[:4]=="tel:":
            d["telephone"]=t.text[5:]
        else:
            address = t.text
            d["address"] = address
            postcode = geo.extract_gb_postcode(address)
            d["postcode"] = postcode
            d["latlng"] = geo.gb_postcode_to_latlng(postcode)
            
    for d in services:
        if "info HTML" in d:
            scrape_extra(d,facility_type)
        datastore.save(unique_keys=["PCT","type","name","address"], data=d)



def scrape_extra(d,facility_type):
    """
    Scrapes all the data listed on a PCT's separate page.
    """
    ### not implemented yet



main()

