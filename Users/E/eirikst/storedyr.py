# -*- coding: utf-8 -*-
import re, sys
import scraperwiki
import lxml.html
import dateutil.parser
import datetime

def getDateSorted(string):
    '''function to convert norwegian full month name dates to a more computer friendly format. Returns date object'''
    #print string
    dag = string.split(".")[0]
    month = string.split(".")[1].split(" ")[0]
    year = string.split(" ")[1].strip()
    dato = str(dag) + "/" + str(month) + "/" +str(year)
    #print dato
    date = datetime.datetime.strptime(dato, '%d/%m/%Y').date()
    return date

"""
Urls for scraping
"""
#url = "http://artsobservasjoner.no/storerovdyr/uttag_obstabell.asp"
url = "http://artsobservasjoner.no/storerovdyr/uttag_obstabell.asp?sel_intervall=100&sel_page=1&page=1&intervall=100&sistapost=&bakatpost=-95&framatpost=95"

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
relevant_row = root.xpath("//tr[@id]")  

"""
Scraping
"""
print len(relevant_row)
for row in relevant_row:
    #print lxml.html.tostring(row, pretty_print=True)
    data = {}
    data['id'] = row.xpath("@id")[0]
    data['status'] = row.xpath("td/img/@title")[0]
    data['dyr'] = row.xpath("td[2]/b/text()")[0]
    data['observert'] = row.xpath("td[3]/text()")[0].strip() # her mangler kjønnet på dyret
    data['type'] = row.xpath("td[4]/text()")[0]
    data['sted'] = row.xpath("td[5]/a/text()")[0]
    data['fylke'] = row.xpath("td[5]/b/text()")[0]
    # loc url = http://artsobservasjoner.no/storerovdyr/SiteInfo.aspx?lokalid=11035
    loc_url = "http://artsobservasjoner.no/storerovdyr/" + str(row.xpath("td[5]/a/@href")[0].split('"')[1]) # aka SiteInfo.aspx?lokalid=11342 

    html2 = scraperwiki.scrape(loc_url)
    root2 = lxml.html.fromstring(html2)
    data['lat'] = root2.xpath("//span[@id='lblCoordLatitude']/text()")[0]
    data['lon'] = root2.xpath("//span[@id='lblCoordLongitude']/text()")[0]
    data['fylke2'] = root2.xpath("//span[@id='lblCounty']/text()")[0]
    data['kommune'] = root2.xpath("//span[@id='lblMunicipality']/text()")[0]

#    print data['kommune']
 #   print repr(data['kommune'])
  #  print type(data['kommune'])
    data['landsdel'] = root2.xpath("//span[@id='lblCountryRegion']/text()")[0]
    data['presisjon'] = root2.xpath("//span[@id='lblCoordinatePrecision']/text()")[0]
    
    data['date'] = getDateSorted(row.xpath("td[6]/text()")[0].strip())
    # skip time
    data['observator'] = row.xpath("td[9]/a/text()")[0]
    # skip observator epost
    # skip bilde-url
    try:
        data['kommentar'] = row.xpath("td[11]/img/@onmouseover")[0].split("'")[3][0]
    except:
        data['kommentar'] = ''
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    #print data


print data

# for url in urls:
#     html = scraperwiki.scrape(url)
#     root = lxml.html.fromstring(html)
#     reviews = root.xpath("//div[contains(@class, 'fp-search-item')]")    
#     #print reviews
#     #print len(reviews)
#     for review in reviews:
#         data = {}
#         data['title'] = review.xpath("div/h3/a/text()")[0] #.split("'")[1]
#         data['date'] = getDateSorted(str(review.xpath("div/small/text()")).split("'")[1])
#         data['verdict'] = str(review.xpath("div/a/span/text()")).split("'")[1][-1]
#         data['url'] = str(review.xpath("div/h3/a/@href")).split("'")[1]
#         #data['hook'] = str(review.xpath("div/p/text()")).split("'")[1]
#         #data['hook'].encode('utf8')
#         #print lxml.html.tostring(review, pretty_print=True)
#         #print data['hook'].encode('utf-8')
#         scraperwiki.sqlite.save(unique_keys=['title','url'], data=data)
#         #print data['title']
#     #sys.exit("end here")



# -*- coding: utf-8 -*-
import re, sys
import scraperwiki
import lxml.html
import dateutil.parser
import datetime

def getDateSorted(string):
    '''function to convert norwegian full month name dates to a more computer friendly format. Returns date object'''
    #print string
    dag = string.split(".")[0]
    month = string.split(".")[1].split(" ")[0]
    year = string.split(" ")[1].strip()
    dato = str(dag) + "/" + str(month) + "/" +str(year)
    #print dato
    date = datetime.datetime.strptime(dato, '%d/%m/%Y').date()
    return date

"""
Urls for scraping
"""
#url = "http://artsobservasjoner.no/storerovdyr/uttag_obstabell.asp"
url = "http://artsobservasjoner.no/storerovdyr/uttag_obstabell.asp?sel_intervall=100&sel_page=1&page=1&intervall=100&sistapost=&bakatpost=-95&framatpost=95"

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
relevant_row = root.xpath("//tr[@id]")  

"""
Scraping
"""
print len(relevant_row)
for row in relevant_row:
    #print lxml.html.tostring(row, pretty_print=True)
    data = {}
    data['id'] = row.xpath("@id")[0]
    data['status'] = row.xpath("td/img/@title")[0]
    data['dyr'] = row.xpath("td[2]/b/text()")[0]
    data['observert'] = row.xpath("td[3]/text()")[0].strip() # her mangler kjønnet på dyret
    data['type'] = row.xpath("td[4]/text()")[0]
    data['sted'] = row.xpath("td[5]/a/text()")[0]
    data['fylke'] = row.xpath("td[5]/b/text()")[0]
    # loc url = http://artsobservasjoner.no/storerovdyr/SiteInfo.aspx?lokalid=11035
    loc_url = "http://artsobservasjoner.no/storerovdyr/" + str(row.xpath("td[5]/a/@href")[0].split('"')[1]) # aka SiteInfo.aspx?lokalid=11342 

    html2 = scraperwiki.scrape(loc_url)
    root2 = lxml.html.fromstring(html2)
    data['lat'] = root2.xpath("//span[@id='lblCoordLatitude']/text()")[0]
    data['lon'] = root2.xpath("//span[@id='lblCoordLongitude']/text()")[0]
    data['fylke2'] = root2.xpath("//span[@id='lblCounty']/text()")[0]
    data['kommune'] = root2.xpath("//span[@id='lblMunicipality']/text()")[0]

#    print data['kommune']
 #   print repr(data['kommune'])
  #  print type(data['kommune'])
    data['landsdel'] = root2.xpath("//span[@id='lblCountryRegion']/text()")[0]
    data['presisjon'] = root2.xpath("//span[@id='lblCoordinatePrecision']/text()")[0]
    
    data['date'] = getDateSorted(row.xpath("td[6]/text()")[0].strip())
    # skip time
    data['observator'] = row.xpath("td[9]/a/text()")[0]
    # skip observator epost
    # skip bilde-url
    try:
        data['kommentar'] = row.xpath("td[11]/img/@onmouseover")[0].split("'")[3][0]
    except:
        data['kommentar'] = ''
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    #print data


print data

# for url in urls:
#     html = scraperwiki.scrape(url)
#     root = lxml.html.fromstring(html)
#     reviews = root.xpath("//div[contains(@class, 'fp-search-item')]")    
#     #print reviews
#     #print len(reviews)
#     for review in reviews:
#         data = {}
#         data['title'] = review.xpath("div/h3/a/text()")[0] #.split("'")[1]
#         data['date'] = getDateSorted(str(review.xpath("div/small/text()")).split("'")[1])
#         data['verdict'] = str(review.xpath("div/a/span/text()")).split("'")[1][-1]
#         data['url'] = str(review.xpath("div/h3/a/@href")).split("'")[1]
#         #data['hook'] = str(review.xpath("div/p/text()")).split("'")[1]
#         #data['hook'].encode('utf8')
#         #print lxml.html.tostring(review, pretty_print=True)
#         #print data['hook'].encode('utf-8')
#         scraperwiki.sqlite.save(unique_keys=['title','url'], data=data)
#         #print data['title']
#     #sys.exit("end here")



