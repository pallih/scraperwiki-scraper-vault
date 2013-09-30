import scraperwiki
import re, ast, cgi, os
import datetime
from dateutil import parser

sourcescraper = 'imdb_rating_percent_changed_1'
scraperwiki.sqlite.attach(sourcescraper, "imdb")
_params_ = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))



def main():
    time = _params_.get("time")
    render = _params_.get("render")
    if render == "text":
        scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain; charset=utf-8')
        showVotesDeltaText(time)
    elif render == "rss":
        link = "http://www.imdb.com/chart/top"
        if time == "month":
            title = "IMDb Monthly Increments"
            showRssFeed(monthlyFeed, title, link)
        else:
            title = "IMDb Daily Increments"
            showRssFeed(dailyFeed, title, link)
    else:
        showVotesDeltaHtml(time)




def monthlyFeed():
    def description():
        print "<div><p>"
        showTableHtml(name, columns[2:], array)
        print "</p></div>"
    date = datetime.date.today()
    if date.day>4: return 
    res = scraperwiki.sqlite.select("date from imdb.monthly order by date desc limit 2")
    for d in res:
        (data, success) = getVotesDeltaSnapshot(d["date"], ["monthly"])
        if not success: break
        date = data["date"]
        columns = getSortColumns(data)
        for key, name in columns:
            array = sortedVotesDelta(data, key)[:50]
            title = "IMDb %s order by %s" % (date, key==name and key or "%s days"%name)
            link = "https://views.scraperwiki.com/run/imdb_votes_increment_view/?time=%s" % date
            showRssItem(title, title, link, utcfmt(data["time"]), description)


def dailyFeed():
    def description():
        print "<div><p>"
        for key, name in columns:
            try:
                if float(name)>300: continue
            except: pass
            array = sortedVotesDelta(data, key)[:20]
            showTableHtml(name, columns[2:], array)
        print "</p></div>"
    date = datetime.date.today()
    for i in range(3):
        (data, success) = getVotesDeltaSnapshot(date)
        if not success: break
        date = data["date"]
        columns = getSortColumns(data)
        title = "IMDb Daily %s" % date
        link = "https://views.scraperwiki.com/run/imdb_votes_increment_view/?time=%s" % date
        showRssItem(title, title, link, utcfmt(data["time"]), description)
        date += datetime.timedelta(days=-1)




def showRssItem(guid, title, link, time, description):
    print """
    <item>
        <title>%s</title>
        <link>%s</link>
        <pubDate>%s</pubDate>
        <guid isPermaLink="false">%s</guid>
        <description><![CDATA[
""" % (title, link, time, guid)
    if callable(description): description()
    else: print description
    print "]]></description></item>"


def showRssFeed(itemsbuilder, title, link, description=None):
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')
    now = datetime.datetime.now()
    print """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <pubDate>%s</pubDate>
    <generator>ScraperWiki subsi</generator>
""" % (title, link, description or title, utcfmt(now))
    itemsbuilder()
    print "</channel></rss>"



def showVotesDeltaHtml(date=None):
    if not date: date = datetime.date.today()
    (data, success) = getVotesDeltaSnapshot(date)
    if not success: return
    columns = getSortColumns(data)
    print "<div><h3>%s</h3><p>" % data["date"]
    for key, name in columns:
        array = sortedVotesDelta(data, key)[:10]
        showTableHtml(name, columns[2:], array)
    print "</p></div>"


def showTableHtml(name, columns, array):
    arr = ['<div><table class="imdbdelta" border="1" style="border-collapse:collapse; width:520px;"><tbody>']
    ths = "</th><th>".join(["#","idx","rating","votes"] + [b for a,b in columns] + ["title"])
    arr.append("<tr style='background:#dddddd'><th>%s</th></tr>" % re.sub(r"(>%s<)"%name, r" style='color:red'\1", ths))
    for i, film in enumerate(array):
        arr.append("<tr><td>%d</td>" % (i+1))
        arr.append("<td>%(index)s</td> <td>%(rating)s</td> <td>%(votes)s</td>" % film)
        arr.extend([ "<td>%s</td>" % film.get(k, '-') for k,n in columns])
        arr.append("<td> <a target='_blank' href='http://www.imdb.com/title/tt%(id)s/' style='font-size:0.7em'>%(title)s (%(year)s)</a> </td></tr>" % film)
    arr.append("</tbody></table><br/></div>")
    print "".join(arr)


def showVotesDeltaText(date=None):
    if not date: date = datetime.date.today()
    (data, success) = getVotesDeltaSnapshot(date)
    if not success: return
    columns = getSortColumns(data)
    for key, name in columns:
        array = sortedVotesDelta(data, key)[:10]
        print key, "="*80
        print columns[2:]
        for i, film in enumerate(array):
            print i+1, [film.get(k) for k,n in columns[2:]], film["title"], film


def sortedVotesDelta(data, key):
    if key=="rating": return data["items"][:50]
    return sorted(data["items"], reverse=True, 
            key=lambda film: int(film.get(key, 0)) )[:50]

def getSortColumns(data):
    a = ["rating", "votes"]
    a = zip(a, a)
    b = [("delta%d"%i, col) for i, col in enumerate(data["columns"])]
    return a + b


def getVotesDeltaSnapshot(date, tables=["daily", "monthly"]):
    try:
        date = parser.parse(str(date)).date()
        for table in tables:
            res = scraperwiki.sqlite.select("* from imdb.%s where date<='%s' order by date desc limit 1" % (table, date))
            if res:
                base = res[0]
                break
        base["items"] = ast.literal_eval(base["items"])
        base["date"] = parser.parse(base["date"]).date()
        base["time"] = parser.parse(base["time"])
        base["columns"] = ast.literal_eval(base["columns"])
        return (base, True)
    except Exception, e:
        return (None, False)


def utcfmt(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z+0000")



#########
main()

import scraperwiki
import re, ast, cgi, os
import datetime
from dateutil import parser

sourcescraper = 'imdb_rating_percent_changed_1'
scraperwiki.sqlite.attach(sourcescraper, "imdb")
_params_ = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))



def main():
    time = _params_.get("time")
    render = _params_.get("render")
    if render == "text":
        scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain; charset=utf-8')
        showVotesDeltaText(time)
    elif render == "rss":
        link = "http://www.imdb.com/chart/top"
        if time == "month":
            title = "IMDb Monthly Increments"
            showRssFeed(monthlyFeed, title, link)
        else:
            title = "IMDb Daily Increments"
            showRssFeed(dailyFeed, title, link)
    else:
        showVotesDeltaHtml(time)




def monthlyFeed():
    def description():
        print "<div><p>"
        showTableHtml(name, columns[2:], array)
        print "</p></div>"
    date = datetime.date.today()
    if date.day>4: return 
    res = scraperwiki.sqlite.select("date from imdb.monthly order by date desc limit 2")
    for d in res:
        (data, success) = getVotesDeltaSnapshot(d["date"], ["monthly"])
        if not success: break
        date = data["date"]
        columns = getSortColumns(data)
        for key, name in columns:
            array = sortedVotesDelta(data, key)[:50]
            title = "IMDb %s order by %s" % (date, key==name and key or "%s days"%name)
            link = "https://views.scraperwiki.com/run/imdb_votes_increment_view/?time=%s" % date
            showRssItem(title, title, link, utcfmt(data["time"]), description)


def dailyFeed():
    def description():
        print "<div><p>"
        for key, name in columns:
            try:
                if float(name)>300: continue
            except: pass
            array = sortedVotesDelta(data, key)[:20]
            showTableHtml(name, columns[2:], array)
        print "</p></div>"
    date = datetime.date.today()
    for i in range(3):
        (data, success) = getVotesDeltaSnapshot(date)
        if not success: break
        date = data["date"]
        columns = getSortColumns(data)
        title = "IMDb Daily %s" % date
        link = "https://views.scraperwiki.com/run/imdb_votes_increment_view/?time=%s" % date
        showRssItem(title, title, link, utcfmt(data["time"]), description)
        date += datetime.timedelta(days=-1)




def showRssItem(guid, title, link, time, description):
    print """
    <item>
        <title>%s</title>
        <link>%s</link>
        <pubDate>%s</pubDate>
        <guid isPermaLink="false">%s</guid>
        <description><![CDATA[
""" % (title, link, time, guid)
    if callable(description): description()
    else: print description
    print "]]></description></item>"


def showRssFeed(itemsbuilder, title, link, description=None):
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')
    now = datetime.datetime.now()
    print """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <pubDate>%s</pubDate>
    <generator>ScraperWiki subsi</generator>
""" % (title, link, description or title, utcfmt(now))
    itemsbuilder()
    print "</channel></rss>"



def showVotesDeltaHtml(date=None):
    if not date: date = datetime.date.today()
    (data, success) = getVotesDeltaSnapshot(date)
    if not success: return
    columns = getSortColumns(data)
    print "<div><h3>%s</h3><p>" % data["date"]
    for key, name in columns:
        array = sortedVotesDelta(data, key)[:10]
        showTableHtml(name, columns[2:], array)
    print "</p></div>"


def showTableHtml(name, columns, array):
    arr = ['<div><table class="imdbdelta" border="1" style="border-collapse:collapse; width:520px;"><tbody>']
    ths = "</th><th>".join(["#","idx","rating","votes"] + [b for a,b in columns] + ["title"])
    arr.append("<tr style='background:#dddddd'><th>%s</th></tr>" % re.sub(r"(>%s<)"%name, r" style='color:red'\1", ths))
    for i, film in enumerate(array):
        arr.append("<tr><td>%d</td>" % (i+1))
        arr.append("<td>%(index)s</td> <td>%(rating)s</td> <td>%(votes)s</td>" % film)
        arr.extend([ "<td>%s</td>" % film.get(k, '-') for k,n in columns])
        arr.append("<td> <a target='_blank' href='http://www.imdb.com/title/tt%(id)s/' style='font-size:0.7em'>%(title)s (%(year)s)</a> </td></tr>" % film)
    arr.append("</tbody></table><br/></div>")
    print "".join(arr)


def showVotesDeltaText(date=None):
    if not date: date = datetime.date.today()
    (data, success) = getVotesDeltaSnapshot(date)
    if not success: return
    columns = getSortColumns(data)
    for key, name in columns:
        array = sortedVotesDelta(data, key)[:10]
        print key, "="*80
        print columns[2:]
        for i, film in enumerate(array):
            print i+1, [film.get(k) for k,n in columns[2:]], film["title"], film


def sortedVotesDelta(data, key):
    if key=="rating": return data["items"][:50]
    return sorted(data["items"], reverse=True, 
            key=lambda film: int(film.get(key, 0)) )[:50]

def getSortColumns(data):
    a = ["rating", "votes"]
    a = zip(a, a)
    b = [("delta%d"%i, col) for i, col in enumerate(data["columns"])]
    return a + b


def getVotesDeltaSnapshot(date, tables=["daily", "monthly"]):
    try:
        date = parser.parse(str(date)).date()
        for table in tables:
            res = scraperwiki.sqlite.select("* from imdb.%s where date<='%s' order by date desc limit 1" % (table, date))
            if res:
                base = res[0]
                break
        base["items"] = ast.literal_eval(base["items"])
        base["date"] = parser.parse(base["date"]).date()
        base["time"] = parser.parse(base["time"])
        base["columns"] = ast.literal_eval(base["columns"])
        return (base, True)
    except Exception, e:
        return (None, False)


def utcfmt(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z+0000")



#########
main()

