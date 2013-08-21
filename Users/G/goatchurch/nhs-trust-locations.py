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



from scraperwiki import sqlite, scrape, geo
import lxml.html
import urllib2, re

 

debug = False



def main():
    "Acquires list of PCTs and scrapes each in turn"

    url = "http://www.nhs.uk/ServiceDirectories/Pages/PrimaryCareTrustListing.aspx"
    root = lxml.html.parse(url).getroot()
    pct_links = []

    for t in root.cssselect("body div form div div div div ul li a"):
        if t.text != "return to top" and len(t.text)>1:
            pct_links.append((t.attrib["href"],t.text))

    if debug:
        pct_links = pct_links[:3]

    print "There are", len(pct_links), "trusts"
    for i in range(70, len(pct_links)):
        link,name = pct_links[i]
        print "Trust", i, name
        scrape_pct(link,name)



def scrape_pct(link,pct_name):
    """
    Scrapes the data associated with the PCT, and calls functions to scrape
    data associated with the services.
    """
    
    url = "http://www.nhs.uk" + link
    root = lxml.html.parse(url).getroot()

    d = {}

    # basic contact details
    d["PCT"] = pct_name
    d["type"] = "main"
    d["name"] = pct_name
    print lxml.html.tostring(root)
    address = root.cssselect("div.panel-content div.pad p")[0].text
    d["address"] = address
    d["postcode"]= geo.extract_gb_postcode(address)
    try:
        d["lat"], d["lng"] = geo.gb_postcode_to_latlng(d["postcode"])
    except:
        print "Postcode not found", d["postcode"]
    d["info HTML"] = url

    colour = "green"
    # quality
    for t in root.findall("body/div/form/div/div/div/div/div/div/div[@class='service-feedback clear']"):
        k = t.find("div/h4").text.strip()
        v = t.find("div/img").attrib["alt"]
        d[k] = v
        if k == "Fair":
            colour = "yellow"
    d["colour"] = colour

    # head honcho
    for t in root.findall("body/div/form/div/div/div/div/div/div/div/p[@class='profiles-picture-caption']"):
        d["Boss"] = t.text.replace("<br />",", ")

    # boring text
    for t in root.findall("body/div/form/div/div/div/div/div/div/p"):
        if t.text:
            if t.attrib.get("class",False)=="intro":
                d["intro text"] = t.text
            else:
                d["boilerplate"] = (d.get("boilerplate","")+"\n"+t.text).strip()

    sqlite.save(unique_keys=["PCT","type","name"], data=d)
    
    scrape_facilities(pct_name,root)
    scrape_others(pct_name,url)



def scrape_facilities(pct_name,root):
    """
    Scrapes all the data about services listed on the PCT's main page.
    """
    s = root.find("body/div/form/div/div/div/div/div/div/div/dl[@class='clear']")
    if s:
        extract_table_data(pct_name,s,"service")



def scrape_others(pct_name,url):
    types = ["doctor","dentist","pharmacy","optician"]
    for facility_type,i in zip(types,range(2,6)):
        root = lxml.html.fromstring(scrape(url+"&v=%d"%i))

        s = root.find("body/div/form/div/div/div/div/div/dl")
        if s:
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
            d["name"] = (t.text or "").strip()
        elif t.text[:4]=="tel:":
            d["telephone"]=t.text[5:]
        else:
            address = t.text
            d["address"] = address
            d["postcode"] = geo.extract_gb_postcode(address)
            d["latlng"] = maxmanderspostcode(d["postcode"])
            
    for d in services:
        if "info HTML" in d:
            scrape_extra(d,facility_type)
        datastore.save(unique_keys=["PCT","type","name"], data=d, latlng=d.get("latlng"))



def scrape_extra(d,facility_type):
    """
    Scrapes all the data listed on a PCT's separate page.
    """
    ### not implemented yet



main()

