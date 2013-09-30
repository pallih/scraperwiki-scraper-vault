# RSS view for Rightmove house scrapers. 
from datetime import datetime
import time
import scraperwiki      
     
scraperwiki.sqlite.attach("rightmove")
bad_houses = scraperwiki.sqlite.select(           
    '''* from rightmove.swdata 
    where stop is not ''
    order by pubDate desc'''
)

def totimestamp(dt):
    return time.mktime(dt.timetuple()) + dt.microsecond/1e6
def timeAsrfc822(theTime):
    import rfc822
    return rfc822.formatdate(totimestamp(theTime))

scraperwiki.utils.httpresponseheader("Content-Type", "text/rss+xml")

# Print our RSS of good houses. 
rss_text = '<?xml version="1.0" encoding="utf-8" ?>\n'
rss_text +='<rss version="2.0">\n'
rss_text += """<channel>
<title>Bad Houses - Anna + Tom's House Scraper</title>
<description>Houses with views near stations</description>
<link>http://www.scraperwiki.com</link>
<lastBuildDate>"""+timeAsrfc822(datetime.now())+"</lastBuildDate>\n"
rss_text +="<pubDate>"+timeAsrfc822(datetime.now())+"</pubDate>\n"
for house_item in bad_houses:
    house_found_time = datetime.strptime(house_item["pubDate"], "%Y-%m-%dT%H:%M:%S.%f")
    rss_text +="<item>\n"
    rss_text +="<title>"+ house_item['title'] +"</title>\n"
    rss_text +="<description><![CDATA["+house_item["description"]+"]]></description>\n"
    #rss_text +="<content:encoded><![CDATA["+house_item["description"]+"]]></content>\n"
    rss_text +="<link>"+house_item["link"]+"</link>\n"
    rss_text +="<pubDate>"+timeAsrfc822(house_found_time)+"</pubDate>\n"
    rss_text +="<guid>"+house_item["link"]+"</guid>\n"
    rss_text +="</item>\n"
rss_text +="</channel>\n</rss>\n"
#rss_text = rss_text.encode('utf8')
print rss_text# RSS view for Rightmove house scrapers. 
from datetime import datetime
import time
import scraperwiki      
     
scraperwiki.sqlite.attach("rightmove")
bad_houses = scraperwiki.sqlite.select(           
    '''* from rightmove.swdata 
    where stop is not ''
    order by pubDate desc'''
)

def totimestamp(dt):
    return time.mktime(dt.timetuple()) + dt.microsecond/1e6
def timeAsrfc822(theTime):
    import rfc822
    return rfc822.formatdate(totimestamp(theTime))

scraperwiki.utils.httpresponseheader("Content-Type", "text/rss+xml")

# Print our RSS of good houses. 
rss_text = '<?xml version="1.0" encoding="utf-8" ?>\n'
rss_text +='<rss version="2.0">\n'
rss_text += """<channel>
<title>Bad Houses - Anna + Tom's House Scraper</title>
<description>Houses with views near stations</description>
<link>http://www.scraperwiki.com</link>
<lastBuildDate>"""+timeAsrfc822(datetime.now())+"</lastBuildDate>\n"
rss_text +="<pubDate>"+timeAsrfc822(datetime.now())+"</pubDate>\n"
for house_item in bad_houses:
    house_found_time = datetime.strptime(house_item["pubDate"], "%Y-%m-%dT%H:%M:%S.%f")
    rss_text +="<item>\n"
    rss_text +="<title>"+ house_item['title'] +"</title>\n"
    rss_text +="<description><![CDATA["+house_item["description"]+"]]></description>\n"
    #rss_text +="<content:encoded><![CDATA["+house_item["description"]+"]]></content>\n"
    rss_text +="<link>"+house_item["link"]+"</link>\n"
    rss_text +="<pubDate>"+timeAsrfc822(house_found_time)+"</pubDate>\n"
    rss_text +="<guid>"+house_item["link"]+"</guid>\n"
    rss_text +="</item>\n"
rss_text +="</channel>\n</rss>\n"
#rss_text = rss_text.encode('utf8')
print rss_text