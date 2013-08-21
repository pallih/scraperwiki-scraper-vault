import urllib2
import BeautifulSoup
import re
import datetime
import dateutil.parser
import scraperwiki

class Activities(object):
    def __init__(self):
        self.activities = []
        
    def create_activity(self):
        a = Activity()
        self.activities.append(a)
        return a
    
    def finish(self):
        pass
    
class Activity(object):
    def __init__(self):
        self.fields = {}
        
    def add_field(self, field_name, field_value):
        self.fields[field_name] = field_value
        
    @property
    def venue(self):
        class Decorator(object):
            def __init__(self, o):
                self.o = o
                
            def add_field(self, field_name, field_value):
                self.o.add_field("Venue-%s" % field_name, field_value)
                
        return Decorator(self)

    def hash(self, value):
        return value
    
    def finish(self):
        scraperwiki.datastore.save(['ActivitySourceID'], self.fields)

activities = Activities()
        
def scrape_page(id, url):
    ##print "scraping %s" % url
    try:
        html = urllib2.urlopen(url).read()
        page = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)

        activity = activities.create_activity()
        activity.add_field("ActivitySourceID", id)
        activity.add_field("Name", page.find(attrs={"class":"eventDetailTitle"}).contents[0])
        activity.add_field("Description", "\n".join(page.find(attrs={"class":"eventDetailDesc"}).findAll(text=True))+"\n<a href=\"http://www.plugandplay.org.uk/events/index.php?com=detail&eID="+id+"\">See the event on Worcestershire's website</a>")
        datetext = page.find(attrs={"class":"eventDetailDate"}).contents[0]
        timetext = page.find(attrs={"class":"eventDetailTime"}).contents[0]
        times = timetext.split(" - ")
        d = dateutil.parser.parse(datetext).date()
        activity.add_field("Starts", datetime.datetime.combine(d, dateutil.parser.parse(times[0]).time()).isoformat())
        activity.add_field("Ends", datetime.datetime.combine(d, dateutil.parser.parse(times[1]).time()).isoformat())
    

        l = page.find(id="eventDetailInfo").find("b", text="Location")
        n = l.parent
        for i in range(0,7):
            if i==2:
                activity.venue.add_field("Name", unicode(n))
                activity.venue.add_field("ProviderVenueID", activity.hash(unicode(n)))
            elif i==6:
                m = re.match(".*?([A-Z0-9]+ [A-Z0-9]+)", unicode(n))
                activity.venue.add_field("Postcode", m.group(1))
            n = n.nextSibling

    
        info = "".join(page.find(id="eventDetailInfo").findAll(text=True))
        m = re.search("Phone: ([0-9\(\) ]*)", info)
        if m:
            activity.add_field("ContactNumber", str(m.group(1)).translate(None, "() "))
        try:
            script = page.find(id="eventDetailInfo").script.contents[0]
            m = re.search("ename = '(.*?)'", script)
            p1 = m.group(1)
            m = re.search("edomain = '(.*?)'", script)
            p2 = m.group(1)
            #print p1+"@"+p2
            activity.add_field("ContactEmail", p1+"@"+p2)
        except: pass

    
        activity.finish()
    except Exception, ex:
        pass
    
next = None

scraped_ids = scraperwiki.metadata.get('scraped_ids', [])

while True:
    if next:
        url = next
    else:
        url = "http://www.plugandplay.org.uk/events/"
    print url
    html = urllib2.urlopen(url).read()
    page1 = BeautifulSoup.BeautifulSoup(html, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)

    next = page1.find(attrs={"title":"Browse Forward One Week"})["href"]
    i=0
    for a in page1.findAll("a", attrs={"class":"eventListTitle"}):
        m = re.match(".*ID=([0-9]+)", a["href"])
        id = m.group(1)
        #print id, a["href"]
        if id not in scraped_ids:
            scrape_page(id, a["href"])
            scraped_ids.append(id)
            scraperwiki.metadata.save('scraped_ids', scraped_ids)
