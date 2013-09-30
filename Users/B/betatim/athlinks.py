import time
import scipy
import scipy.stats

import scraperwiki
import lxml.html


# cotswold 2011
base_url = "http://athlinks.com/time.aspx?eventid=161246&courseid=220920&genderpage=m%i"
sports = {"run": 16, "bike": 12, "swim": 8}
pages = (1,2,3)

# blenheim 2011 results
#base_url = "http://athlinks.com/time.aspx?eventid=167716&courseid=241355&genderpage=m%i"
#sports = {"run": 16, "bike": 12, "swim": 8}
#pages = xrange(1, 31)

times = {}
for sport in sports:
    times[sport] = []

print "runnnnning"
for i in pages:
    html = scraperwiki.scrape(base_url%i)
    time.sleep(4)
    root = lxml.html.fromstring(html)
    #rows = root.cssselect("div.clsPadTop10 tr")
    result_rows = root.cssselect("tr.clsResult")

    for result_row in result_rows:
        cells = [e.text_content() for e in result_row]
        #print cells
        # Only 25-29 age group
        if cells[6] != "25":
            #continue
            pass

        for sport,idx in sports.items():
            times[sport].append(cells[idx])


def tomins(s):
    k = s.split(":")
    if len(k) == 3:
        h,m,s = k
        return int(h)*60 + int(m) + int(s)/60.

    elif len(k) == 2:
        m,s = k
        return int(m) + int(s)/60.

    return 0

def avg(times):
    times = [tomins(x) for x in times]
    return sum(x for x in times) / len([1 for x in times if x > 0])

def fmt(b):
    return "%i:%02i"%(b/60, b%60)

print "Average times:"
for sport, times_ in times.items():
    a = avg(times_)
    times_ = [tomins(x) for x in times_ if tomins(x) > 0]
    print sport, a, "mins", fmt(a), [fmt(scipy.stats.scoreatpercentile(times_, i)) for i in (10, 20, 30, 40, 50, 60, 70)]

    import time
import scipy
import scipy.stats

import scraperwiki
import lxml.html


# cotswold 2011
base_url = "http://athlinks.com/time.aspx?eventid=161246&courseid=220920&genderpage=m%i"
sports = {"run": 16, "bike": 12, "swim": 8}
pages = (1,2,3)

# blenheim 2011 results
#base_url = "http://athlinks.com/time.aspx?eventid=167716&courseid=241355&genderpage=m%i"
#sports = {"run": 16, "bike": 12, "swim": 8}
#pages = xrange(1, 31)

times = {}
for sport in sports:
    times[sport] = []

print "runnnnning"
for i in pages:
    html = scraperwiki.scrape(base_url%i)
    time.sleep(4)
    root = lxml.html.fromstring(html)
    #rows = root.cssselect("div.clsPadTop10 tr")
    result_rows = root.cssselect("tr.clsResult")

    for result_row in result_rows:
        cells = [e.text_content() for e in result_row]
        #print cells
        # Only 25-29 age group
        if cells[6] != "25":
            #continue
            pass

        for sport,idx in sports.items():
            times[sport].append(cells[idx])


def tomins(s):
    k = s.split(":")
    if len(k) == 3:
        h,m,s = k
        return int(h)*60 + int(m) + int(s)/60.

    elif len(k) == 2:
        m,s = k
        return int(m) + int(s)/60.

    return 0

def avg(times):
    times = [tomins(x) for x in times]
    return sum(x for x in times) / len([1 for x in times if x > 0])

def fmt(b):
    return "%i:%02i"%(b/60, b%60)

print "Average times:"
for sport, times_ in times.items():
    a = avg(times_)
    times_ = [tomins(x) for x in times_ if tomins(x) > 0]
    print sport, a, "mins", fmt(a), [fmt(scipy.stats.scoreatpercentile(times_, i)) for i in (10, 20, 30, 40, 50, 60, 70)]

    