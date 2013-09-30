import scraperwiki
import lxml.etree, lxml.html
import mechanize
import re
import urlparse

def Main(year,region):
    url = "http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm"
    
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='searchGrants')
    br["region"] = [region]
    br["year"] = [year]

    response = br.submit()

    while True:
        print "Page", br.geturl()
        root = lxml.html.parse(response).getroot() 
        ParsePage(root, br.geturl(), year)
        lnextpage = [s.get("href")  for s in root.cssselect("a")  if s.text == 'Next']
        nextlinks = list(br.links(text_regex="Next"))

        print lnextpage
        #br.follow_link(text_regex="Next", nr=1)
        if nextlinks:
            response = br.follow_link(nextlinks[0])
        else:
            break


def ParsePage(root, baseurl, year):
    for tr in root.cssselect('tr#currencies'):        
        data = {} 
        data["Contract Nr"] = tr[0].text
        data["Title"] = tr[1].text
        data["DAC code"] = tr[2].text
        data["Theme"] = tr[3].text
        data["Organisation"] = tr[4].text
        data["Country Region"] = tr[5].text
        data["Organisation nationality"] = tr[6].text
        data["Action location"] = tr[7].text
        data["Amount in Euro"] = tr[8].text
        data["EC financing"] = tr[9].text
        data["Total cost in Euro"] = tr[10].text
        data["Duration"] = tr[11].text 
        data["Year"] = year             
        
        print(data)
        
        dd1=tr.getnext()
        
        scraperwiki.sqlite.save(["Title"], data)

# needs update for 2011               
years = ['2010','2009','2008','2007']            

for y in years:
    Main(y,"35368")    





import scraperwiki
import lxml.etree, lxml.html
import mechanize
import re
import urlparse

def Main(year,region):
    url = "http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm"
    
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='searchGrants')
    br["region"] = [region]
    br["year"] = [year]

    response = br.submit()

    while True:
        print "Page", br.geturl()
        root = lxml.html.parse(response).getroot() 
        ParsePage(root, br.geturl(), year)
        lnextpage = [s.get("href")  for s in root.cssselect("a")  if s.text == 'Next']
        nextlinks = list(br.links(text_regex="Next"))

        print lnextpage
        #br.follow_link(text_regex="Next", nr=1)
        if nextlinks:
            response = br.follow_link(nextlinks[0])
        else:
            break


def ParsePage(root, baseurl, year):
    for tr in root.cssselect('tr#currencies'):        
        data = {} 
        data["Contract Nr"] = tr[0].text
        data["Title"] = tr[1].text
        data["DAC code"] = tr[2].text
        data["Theme"] = tr[3].text
        data["Organisation"] = tr[4].text
        data["Country Region"] = tr[5].text
        data["Organisation nationality"] = tr[6].text
        data["Action location"] = tr[7].text
        data["Amount in Euro"] = tr[8].text
        data["EC financing"] = tr[9].text
        data["Total cost in Euro"] = tr[10].text
        data["Duration"] = tr[11].text 
        data["Year"] = year             
        
        print(data)
        
        dd1=tr.getnext()
        
        scraperwiki.sqlite.save(["Title"], data)

# needs update for 2011               
years = ['2010','2009','2008','2007']            

for y in years:
    Main(y,"35368")    





