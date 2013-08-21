# This is my first attempt at scraping a site and saving the events listed.


import mechanize 
import lxml
import lxml.etree
import lxml.html
import re
import datetime
import urlparse
import scraperwiki
import HTMLParser
from BeautifulSoup import BeautifulSoup

# UTILITY CODE #
# It'd be good if there was a utility library with lots of handy scripts in for stripping tags etc.

class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)
    
def strip_tags(html):
    #Warning this does all including script and javascript
    x = MLStripper()
    x.feed(html)
    return x.get_fed_data()

def match(s, reg):
    p = re.compile(reg, re.IGNORECASE| re.DOTALL)
    results = p.findall(s)
    return results

def main():
    aarc()
    
def aarc():
    url = 'http://www.york.ac.uk/inst/arrc/seminars.htm'
    html = scraperwiki.scrape( url )
    soup = BeautifulSoup( html )
    seminars = [ ]
    reg = '<(p|strong) class="body">(.*?)(<hr />|BeginDate)'
    chunks = match(html, reg)
    print len(chunks), 'found'
    
    
    events = [ ]
    for chunk in chunks:
        chunk = chunk[1] #get the second item, not the p or strong
        
        event = {'url': 'http://www.york.ac.uk/inst/arrc/seminars.htm'}

        title = strip_tags( match(chunk, 'Title:(.*?)\n')[0]).strip()
        print title
        event['title'] = title
        
        try:
            speaker = strip_tags( match(chunk, 'Presenters?: (.*?)</p>')[0]).strip()
            #print "speaker:", speaker
            event['speaker'] = speaker
            print "speaker:", speaker
        except:
            pass
        
        try:
            location = strip_tags( match(chunk, 'Venue:(.*?)\n')[0])
            print "location:", location
            event['location'] = location
        except:
            pass
        
        #DATE
        date_object = None
        try:
            date = match(chunk, 'Date:(.*?)<')[0] 
            date = date.replace( '</strong>', '')#hack
            
            full_date = strip_tags( date ).strip()
            print date
            date = full_date.split(",")[1]
            date = date.replace("rd", '')
            date = date.replace("th", '')
            date = date.replace("st", '')
            date = date.replace("nd", '')
            date = date.strip()
            print "date:", date
            
            date_object = datetime.datetime.strptime(date, '%d %B %Y')
            print date_object
            
            # NEED TO ADD THE TIME PART!!! (See old code below)
            event['date'] = date_object

        except Exception, err:
            print "Date error", err
            print match(chunk, 'Date:(.*?)</p>')
            date = ''
        
        
        try:
            # Turn a textual date "Tuesday, 5th October 2010" into a datetime. This library isn't available, boo!
            # So this is effectively disabled for now...
            
            #dt = dateutil.parser.parse(date)
            dt = date_object #use the other object... 
        
        
            #TIME
            time_str = strip_tags( match(chunk, 'Time:(.*?)</p>')[0] )
            start, end =  match (time_str, '([0-9]?[0-9])\.([0-9][0-9])(am|pm)')
            shr, smin, sampm = start
            ehr, emin, eampm = end
            ##print shr, smin, sampm
            ##print  ehr, emin, eampm
        
            if sampm == 'pm':
                if int(shr) == 12:
                    pass
                else:
                    shr = str(int(shr) + 12)
            if eampm == 'pm':
                if int(ehr) == 12:
                    pass
                else:
                    ehr = str(int(ehr) + 12)
                
            #DATE RANGES
            starttimestamp = datetime.datetime( dt.year, dt.month, dt.day, int(shr), int(smin))
            endtimestamp = datetime.datetime( dt.year, dt.month, dt.day, int(ehr), int(emin))
            
            print "start date:", starttimestamp
            print "end date:", endtimestamp
            event['end date'] = endtimestamp
        except:
            
        
            #event['date'] = starttimestamp
            event['date_str'] = date
        
        
        try:
            res =match(chunk, 'Hosted by:(.*?)\n')[0]
            ##print res
            print "host:",
            res = match( res, 'href="(.*?)"')[0]
            print res
            event['host'] = res
            
        except Exception, err:
            #print err
            pass
        
        try:
            contact = strip_tags( match(chunk, 'For further  information:(.*?)</p>')[0] ).strip()
            #print "further info:", contact
            
            event['contact'] = contact
        except:
            pass
        
        print
        events.append( event )

        
        event_id = "aarc_" + title.strip() + "_" + speaker.strip() + "_" + date.strip()
        event_id = event_id.lower()
        event_id = event_id.replace("  ", "_")
        event_id = event_id.replace(" ", "_")
        event['id'] = event_id

        print "saving:", event_id
        
        scraperwiki.datastore.save([ 'id' ], event, date=date_object)
        
    return events
    
    
    
    
main()