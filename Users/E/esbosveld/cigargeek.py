import scraperwiki
import requests
import re
from bs4 import BeautifulSoup
from urlparse import urlparse

# DISABLED AT THE CONTENT OWNER'S REQUEST
exit()

maxPages = 686
baseUrl = 'http://www.cigargeeks.com/cigardb/'
searchUrl = 'default.asp?action=srchrslt&page='
recordCount = 0
startPage = scraperwiki.sqlite.get_var('last_page') if scraperwiki.sqlite.get_var('last_page') else 1
#url = 'http://httpbin.org/cookies'
cookies = dict(password='E9C8BFED692953590CD0D091DE742285A1A97142', username='railrunner', bbsmid='903')

for page in range(1, maxPages):
    r = requests.get(baseUrl + searchUrl + str(page), cookies=cookies)
    soup = BeautifulSoup(r.text)
    table = soup.find("table", "bbstable")
    rows = table.find_all("tr")
    lastPageLink = soup.find("a", text=re.compile("Next >"))
    #print lastPageLink
    print "Loading page "+ str(page)
    scraperwiki.sqlite.save_var('last_page', page) 
    for i in range(2, len(rows)):
        recordCount += 1
        row = rows[i]
        foundUrl = row.find("a").get('href')
        parsedUrl = urlparse(foundUrl)
        queryString = parsedUrl[4].split("&")
        id = queryString[1].split('=')[1]
        dbResult = scraperwiki.sqlite.execute("select id from swdata where id='"+id+"'")
        if not dbResult['data']:
            requestUrl = parsedUrl[2] + "?" + queryString[0] + "&" + queryString[1]
            rc = requests.get(baseUrl + requestUrl, cookies=cookies)
            csoup = BeautifulSoup(rc.text)
            ctable = csoup.find("table", "bbstable")
            brand = ctable.find(text=re.compile("Brand"))
            name = ctable.find(text=re.compile("Cigar Name"))
            length = ctable.find(text=re.compile("Length"))
            gauge = ctable.find(text=re.compile("Ring Gauge"))
            manufactured = ctable.find(text=re.compile("Country Manufactured"))
            filler = ctable.find(text=re.compile("Filler"))
            binder = ctable.find(text=re.compile("Binder"))
            wrapper = ctable.find(text=re.compile("Wrapper"))
            color = ctable.find(text=re.compile("Color"))
            strength = ctable.find(text=re.compile("Strength"))
            shape = ctable.find(text=re.compile("Shape"))
            data = {
                'id': id,
                'brand': brand.find_parent("tr")("td")[1].get_text(strip=True) if brand else "",
                'name' : name.find_parent("tr")("td")[1].get_text(strip=True) if name else "",
                'length' : length.find_parent("tr")("td")[1].get_text(strip=True) if length else "",
                'gauge' : gauge.find_parent("tr")("td")[1].get_text(strip=True) if gauge else "",
                'manufactured' : manufactured.find_parent("tr")("td")[1].get_text(strip=True) if manufactured else "",
                'filler' : filler.find_parent("tr")("td")[1].get_text(strip=True) if filler else "",
                'binder' : binder.find_parent("tr")("td")[1].get_text(strip=True) if binder else "",
                'wrapper' : wrapper.find_parent("tr")("td")[1].get_text(strip=True) if wrapper else "",
                'color' : color.find_parent("tr")("td")[1].get_text(strip=True) if color else "",
                'strength' : strength.find_parent("tr")("td")[1].get_text(strip=True) if strength else "",
                'shape' : shape.find_parent("tr")("td")[1].get_text(strip=True) if shape else ""
            }
            print "Saving cigar "+ str(recordCount) +" - "+ data['brand'] + " " + data['name'] + " ("+ id +")"
            
            # DISABLED AT THE CONTENT OWNER'S REQUEST
            # scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        
        





