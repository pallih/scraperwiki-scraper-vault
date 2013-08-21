import scraperwiki
import lxml.html
a=[
#university domains
]
b=0
person=str
email=str
while b !=145: 
    html = scraperwiki.scrape('http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName='+str(a[b])+'&outputFormat=xml&userName=mauriforonda&password=inmortalitywhois')
    root = lxml.html.fromstring(html)
    for el in root.cssselect("registryData administrativeContact"):
        for el1 in el.cssselect("name"):
            person=el1.text
        for el2 in el.cssselect("email"):
            email=el2.text
        for el3 in el.cssselect("city"):
            city=el3.text
        for el4 in el.cssselect("country"):
            country=el4.text
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'person':person,'city':city,'country':country,'email':email})
    city=""
    country=""
    person=""
    email=""
    b=b+1


