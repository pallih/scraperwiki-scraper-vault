import scraperwiki
#import codecs,string
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
        if href.find('csv')>-1 and href.find('@dh')==-1:
            urls.append(href)
    return urls

def grabCSV(url):
    #f =codecs.open(url, "r", "utf-8-sig") 
    f = urllib.urlopen(url)
    reader = csv.DictReader(f)
    
    bigdata=[]
    for row in reader:
        data={}
        for item in row:
            udata=item.decode("utf-8")
            data[udata.encode("ascii","ignore").strip('"')]=row[item]
        bigdata.append(data.copy())
        #scraperwiki.sqlite.save(unique_keys=[], table_name='MentalHealthCommunityTeam', data=data,verbose=0)
        if len(bigdata)>1000:
            scraperwiki.sqlite.save(unique_keys=[], table_name='MentalHealthCommunityTeam', data=bigdata,verbose=0)
            bigdata=[]
    scraperwiki.sqlite.save(unique_keys=[], table_name='MentalHealthCommunityTeam', data=bigdata,verbose=0)
    scraperwiki.sqlite.save(unique_keys=['url'],table_name='scrapesTable',data={'url':url})

url='http://transparency.dh.gov.uk/2012/06/21/mental-health-community-teams-activity-data-downloads/'
sURLs=grabCSVlinks(url,'a')

for sURL in sURLs:
    if sURL not in scrapes:
        print "grabbing",sURL
        grabCSV(sURL)




