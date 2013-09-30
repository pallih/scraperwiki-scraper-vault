import lxml,lxml.html,urllib2,scraperwiki
from datetime import datetime
BASE_URI = "http://www.racc.org/resources/summer-arts-camps-2011"

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

f = urllib2.urlopen(BASE_URI).read()
l = lxml.html.fromstring(f)
ps = l.cssselect("p strong")
for p in ps:
    year = 2011
    start_date = None
    end_date = None
    date_range = removeNonAscii(p.text_content())
    link = p.getnext()
    title = removeNonAscii(link.text_content())
    link_url = link.attrib['href']
    # find start date
    dates = removeNonAscii(date_range.strip().strip('nbsp;')).split("-")
    if len(dates) < 0:
        next
    elif len(dates) == 1:
        start_date_str = "%s/%s" %(dates[0],year)
        end_date_str = "%s/%s" %(dates[0],year)
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
    elif len(dates) == 2:
        start_month_day = dates[0].split("/")
        end_month_day = dates[1].split("/")

        start_date_str = "%s-%s-%s" %(year,start_month_day[0],start_month_day[1])
        end_date_str = "%s-%s-%s" %((year,
            end_month_day[0] if len(end_month_day) == 2 else start_month_day[0],
            end_month_day[1] if len(end_month_day) == 2 else end_month_day[0]))
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        next
    data = {
        'title' : title,
        'link_url' : link_url,
        'start_date': start_date,
        'end_date': end_date,
        'updated': datetime.now()
    }
    scraperwiki.sqlite.save(unique_keys=['title','start_date','end_date'], data=data)
scraperwiki.sqlite.commit()
import lxml,lxml.html,urllib2,scraperwiki
from datetime import datetime
BASE_URI = "http://www.racc.org/resources/summer-arts-camps-2011"

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

f = urllib2.urlopen(BASE_URI).read()
l = lxml.html.fromstring(f)
ps = l.cssselect("p strong")
for p in ps:
    year = 2011
    start_date = None
    end_date = None
    date_range = removeNonAscii(p.text_content())
    link = p.getnext()
    title = removeNonAscii(link.text_content())
    link_url = link.attrib['href']
    # find start date
    dates = removeNonAscii(date_range.strip().strip('nbsp;')).split("-")
    if len(dates) < 0:
        next
    elif len(dates) == 1:
        start_date_str = "%s/%s" %(dates[0],year)
        end_date_str = "%s/%s" %(dates[0],year)
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
    elif len(dates) == 2:
        start_month_day = dates[0].split("/")
        end_month_day = dates[1].split("/")

        start_date_str = "%s-%s-%s" %(year,start_month_day[0],start_month_day[1])
        end_date_str = "%s-%s-%s" %((year,
            end_month_day[0] if len(end_month_day) == 2 else start_month_day[0],
            end_month_day[1] if len(end_month_day) == 2 else end_month_day[0]))
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        next
    data = {
        'title' : title,
        'link_url' : link_url,
        'start_date': start_date,
        'end_date': end_date,
        'updated': datetime.now()
    }
    scraperwiki.sqlite.save(unique_keys=['title','start_date','end_date'], data=data)
scraperwiki.sqlite.commit()
