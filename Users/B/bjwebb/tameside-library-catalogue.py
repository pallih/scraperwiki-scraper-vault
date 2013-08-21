import scraperwiki
import re
import urllib
from BeautifulSoup import BeautifulSoup

def bs_string(el):
    #return "".join(map(unicode, el.contents)).strip()
    return ("".join(el.findAll(text=True))).strip()

# retrieve a page
baseurl = "http://intouch.tameside.gov.uk/vubis/"
starting_url = baseurl + "List.csp?SearchT1=a"+\
    "&Index1=Keywords&Database=1&OpacLanguage=eng&NumberToRetrieve=1000"+\
    "&SearchMethod=Find_1&SearchTerm1=a"+\
    "&Profile=Default&PreviousList=Start&PageType=Start&EncodedRequest=5*89*AF*09*AB*BEB*F4*18*3D4*3B*CDtM*F9"+\
    "&WebPageNr=1&WebAction=NewSearch"

html0 = scraperwiki.scrape(starting_url)
m = re.search("ListBody.csp\?[^\"]+", html0)
if m:
    list_url = baseurl + m.group(0)
else:
    import sys
    sys.exit(0)

html = scraperwiki.scrape(list_url)
#print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll("td", attrs={"class": re.compile("listitem(Odd|Even)") }) 
oldurl = ""
for td in tds:
    if td.find("a"):
        url = unicode(td.find("a")["href"])
        if url == oldurl:
            continue
        oldurl = url
        #print baseurl + url
        html2 = scraperwiki.scrape(baseurl + url.replace(" ", "%20"))
        #print html2
        m = re.search("FullBBBody.csp\?[^\"]+", html2)
        if m:
            url2 = m.group(0)
            
            html3 = scraperwiki.scrape( baseurl + url2 )
            page = BeautifulSoup(html3)
            record = {}
            full_desc = page.find("table", summary="FullBB.Description")
            for td in full_desc.findAll("td", "descrname"):
                try:
                    k = bs_string(td)
                    v = bs_string(td.parent.find("td", "descrdata"))
                    if k != "":
                        record[k] = v
                except AttributeError:
                    pass
            record["record"] = page.find("input", attrs={"name":"Record"})["value"]
            print record
            # save records to the datastore
            scraperwiki.datastore.save(["record"], record)
    