import scraperwiki
import lxml.html 
import urlparse
# Blank Python

#holds facility ids
facid = ''
pageUrl=''
offset = 0


def fetchPage(url):
    
    base_url="http://decadeonline.com/"
    global pageUrl
    pageUrl = base_url + url
    html = scraperwiki.scrape(base_url + url)
    parseUrl(url) 
    return html

def parseUrl(url):
    global facid
    tempDict={}
    parsed = urlparse.urlparse(url)
    tempDict=dict(urlparse.parse_qsl(parsed.query))
    
    facid=tempDict['facid']

def changeUrl():
    global offset
    offset=offset + 50
    scrapePage(offset)
    
    #print urlparse.parse_qs(parsed.query)['facid']
def scrapePage(offset):
    print offset
    home_url="http://decadeonline.com/results.phtml?agency=ccc&offset="+str(offset)+"&businessname=%25&businessstreet=&city=&zip=&facilityid=&soundslike=&sort=FACILITY_NAME"
    html = scraperwiki.scrape(home_url)
    print home_url
    root = lxml.html.fromstring(html)
    getRecords(root)  

def getRecords(root):
    for tr in root.cssselect("table tr.backg"): 
        anchors = tr.cssselect("a") 
        for anchor in anchors:
            secondhtml= fetchPage(anchor.get('href'))
            secondroot=lxml.html.fromstring(secondhtml)
            trs = secondroot.cssselect("table tr.backg")
            
            data = []
            restuarantData={}
            try:
                for index in range(0,3):
                    tds=trs[index].cssselect("td")
                   
                    data.append(tds[1].text_content())
                restuarantData["facid"] = facid
                restuarantData["Name"] = ' '.join(data[0].split())
                restuarantData["Address"] = ' '.join(data[1].split())
                restuarantData["Phone"] = ' '.join(data[2].split())
                #print restuarantData           
            except:
                pass
                #for index in range(0,2):
                    #if len(tds) > 1:
                        #print tds[1].text_content()
                    #else:
                        #print tds[0].text_content()
    anchors=root.cssselect("a")
    for anchor in anchors:
        if anchor.text_content()=="Next Page":
            changeUrl()

scrapePage(offset) 
    #data = { 'Food Facility Name' : tds[0].text_content(), 
    #'Adress' : tds[1].text_content() } 
    #print data


