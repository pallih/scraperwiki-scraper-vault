import scraperwiki
import lxml.html
import re




def getCountries():
    page=scraperwiki.scrape("http://www.equinux.com/us/products/tubestick/tuningmap.html")
    root = lxml.html.fromstring(page)
    countries=root.cssselect("#tttm_iso option")
    return map(lambda x: x.get("value"), countries)
    


def getChannels(content):
    root = lxml.html.fromstring(content)
    iframe=root.cssselect("iframe")[0]
    
    page=scraperwiki.scrape("http://www.equinux.com"+iframe.get("src"))
    
    root = lxml.html.fromstring(page)
    channels=root.cssselect("#locationchannelcontent td.channellist li")
    
    l= []
    for li in channels:
        l.append(li.text_content())

    return l


countries=getCountries()
data=[]

for c in countries:
    page=scraperwiki.scrape("http://www.equinux.com/tttmap/displaymap.php?iso="+c)
    
    root = lxml.html.fromstring(page)
    
    script=root.cssselect("script")[1]
    
    script=script.text_content()
    
    mpoints= re.findall('(?s)(mPointA\[.*?)var point', script)
    
    mPointA={}
    
    for mpoint in mpoints:
        mpoint=mpoint.replace("new Array()","{}")
        exec mpoint.lstrip().rstrip()
    
    
    for k,v in mPointA.iteritems():
        v["country"]=c
        v["zip"]=k
        if 0==len(scraperwiki.sqlite.select("zip from zip_location where zip='%(zip)s' and country='%(country)s' limit 1"%v)):
            try: 
                channels=getChannels(v["content"])
                del v["content"]
                data=[]
                for chan in channels:
                    chandata={}
                    chandata["country"]=c
                    chandata["zip"]=v["zip"]
                    chandata["channel"]=chan
                    data.append(chandata)
                scraperwiki.sqlite.save(unique_keys=['zip','country','channel'], data=data);
                scraperwiki.sqlite.save(unique_keys=['zip','country',], data=v, table_name="zip_location");
            except:
                print "error fetchin %(zip)s"%vimport scraperwiki
import lxml.html
import re




def getCountries():
    page=scraperwiki.scrape("http://www.equinux.com/us/products/tubestick/tuningmap.html")
    root = lxml.html.fromstring(page)
    countries=root.cssselect("#tttm_iso option")
    return map(lambda x: x.get("value"), countries)
    


def getChannels(content):
    root = lxml.html.fromstring(content)
    iframe=root.cssselect("iframe")[0]
    
    page=scraperwiki.scrape("http://www.equinux.com"+iframe.get("src"))
    
    root = lxml.html.fromstring(page)
    channels=root.cssselect("#locationchannelcontent td.channellist li")
    
    l= []
    for li in channels:
        l.append(li.text_content())

    return l


countries=getCountries()
data=[]

for c in countries:
    page=scraperwiki.scrape("http://www.equinux.com/tttmap/displaymap.php?iso="+c)
    
    root = lxml.html.fromstring(page)
    
    script=root.cssselect("script")[1]
    
    script=script.text_content()
    
    mpoints= re.findall('(?s)(mPointA\[.*?)var point', script)
    
    mPointA={}
    
    for mpoint in mpoints:
        mpoint=mpoint.replace("new Array()","{}")
        exec mpoint.lstrip().rstrip()
    
    
    for k,v in mPointA.iteritems():
        v["country"]=c
        v["zip"]=k
        if 0==len(scraperwiki.sqlite.select("zip from zip_location where zip='%(zip)s' and country='%(country)s' limit 1"%v)):
            try: 
                channels=getChannels(v["content"])
                del v["content"]
                data=[]
                for chan in channels:
                    chandata={}
                    chandata["country"]=c
                    chandata["zip"]=v["zip"]
                    chandata["channel"]=chan
                    data.append(chandata)
                scraperwiki.sqlite.save(unique_keys=['zip','country','channel'], data=data);
                scraperwiki.sqlite.save(unique_keys=['zip','country',], data=v, table_name="zip_location");
            except:
                print "error fetchin %(zip)s"%v