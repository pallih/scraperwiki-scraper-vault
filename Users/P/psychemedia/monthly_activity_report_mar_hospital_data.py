import scraperwiki
import csv,urllib,lxml.html


scrapes=[]
try:
    scrapesdata=scraperwiki.sqlite.select("url from scrapesTable")
    for scrape in scrapesdata:
        scrapes.append(str(scrape['url']))
except: pass


def grabCSVlinks(URL,selector):
    urls=[]
    html = scraperwiki.scrape(URL)
    print html
    root = lxml.html.fromstring(html)
    links = root.cssselect(selector)
    for link in links:
        href=link.attrib.get('href')
        if href.find('csv')>-1:
            urls.append(href)
    return urls

def grabCSV(url):
    f = urllib.urlopen(url)
    f.readline()
    f.readline()
    reader = csv.DictReader(f)
    bigdata=[]
    for row in reader:
        data={}
        for item in row:
            item2=item.replace('&',' and ')
            item2=item2.replace('(','')
            item2=item2.replace(')','')
            data[item2]=row[item]
        bigdata.append(data.copy())
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=[], table_name='MAR', data=bigdata,verbose=0)
            bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name='MAR', data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['url'],table_name='scrapesTable',data={'url':url})

url='http://transparency.dh.gov.uk/2012/07/05/monthly-hospital-activity/'
sURLs=grabCSVlinks(url,'a')

for sURL in sURLs:
    if sURL not in scrapes:
        print "grabbing",sURL
        grabCSV(sURL)




import scraperwiki
import csv,urllib,lxml.html


scrapes=[]
try:
    scrapesdata=scraperwiki.sqlite.select("url from scrapesTable")
    for scrape in scrapesdata:
        scrapes.append(str(scrape['url']))
except: pass


def grabCSVlinks(URL,selector):
    urls=[]
    html = scraperwiki.scrape(URL)
    print html
    root = lxml.html.fromstring(html)
    links = root.cssselect(selector)
    for link in links:
        href=link.attrib.get('href')
        if href.find('csv')>-1:
            urls.append(href)
    return urls

def grabCSV(url):
    f = urllib.urlopen(url)
    f.readline()
    f.readline()
    reader = csv.DictReader(f)
    bigdata=[]
    for row in reader:
        data={}
        for item in row:
            item2=item.replace('&',' and ')
            item2=item2.replace('(','')
            item2=item2.replace(')','')
            data[item2]=row[item]
        bigdata.append(data.copy())
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=[], table_name='MAR', data=bigdata,verbose=0)
            bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name='MAR', data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['url'],table_name='scrapesTable',data={'url':url})

url='http://transparency.dh.gov.uk/2012/07/05/monthly-hospital-activity/'
sURLs=grabCSVlinks(url,'a')

for sURL in sURLs:
    if sURL not in scrapes:
        print "grabbing",sURL
        grabCSV(sURL)




