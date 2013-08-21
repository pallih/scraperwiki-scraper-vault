import scraperwiki
import lxml.html
import os, re, ast
import datetime
from datetime import timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta



def main():
    fetchAndSaveToday()
    #showVotesDeltaText()



def showVotesDeltaText(date=None):
    if not date: date = datetime.date.today()
    (data, saved) = getVotesDeltaSnapshot(date)
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



def getVotesDeltaResults(data):
    def addSortedList(key, name=None):
        if not name: name=key
        array = sorted(data["items"], reverse=True, 
            key=lambda film: int(film.get(key, 0)) )[:20]
        results.append((key, name, array))
    films = data["items"]
    results = [("rating", "rating", films[:20])]
    addSortedList("votes")
    for i, col in enumerate(data["columns"]):
        addSortedList("delta%d"%i, col)
    return results


def getVotesDeltaSnapshot(date):
    try:
        date = parser.parse(str(date)).date()
        for table in ["daily", "monthly"]:
            res = scraperwiki.sqlite.select("* from %s where date<='%s' order by date desc limit 1" % (table, date))
            if res:
                base = res[0]
                break
    except Exception, e:
        print "=== "+str(e)
        return (None, True)
    base["items"] = ast.literal_eval(base["items"])
    base["date"] = parser.parse(base["date"]).date()
    base["time"] = parser.parse(base["time"])
    if base.get("columns"):
        base["columns"] = ast.literal_eval(base["columns"])
        return (base, True)
    dataset = getRelativeDataset(base["date"])
    calcVotesDelta(base, dataset)
    return (base, False)


def calcVotesDelta(base, dataset):
    films = base["items"]
    filmdict = {}
    columns = []
    for i, film in enumerate(films):
        id = film["id"]
        film["index"] = i+1
        filmdict[id] = film
    for col, data in enumerate(dataset):
        colname = "delta%d" % col
        daydelta = (base["time"] - data["time"]).total_seconds() / 86400
        if daydelta<3:
            columns.append(str(round(daydelta,1)))
        else:
            columns.append(str(int(round(daydelta,0))))
        for item in data["items"]:
            id = item["id"]
            if filmdict.has_key(id):
                film = filmdict[id]
                film[colname] = int((film["votes"] - item["votes"]) / daydelta)
    base["columns"] = columns
    return base


def getRelativeDataset(basedate):
    def fillDataset(sql):
        try:
            res = scraperwiki.sqlite.select(sql)
            dataset.extend(res)
            return len(res)==1
        except scraperwiki.sqlite.SqliteError, e:
            print "=== "+str(e)
            return False
    dataset = []
    firstday = datetime.date(basedate.year, basedate.month, 1)
    delta = basedate.day>15 and -2 or -3
    sql = "* from daily where date<='%s' order by date desc limit 1"
    fillDataset(  sql % ( basedate + timedelta(days=-1 ) ))
    fillDataset(  sql % ( basedate + timedelta(days=-7 ) ))
    b=fillDataset(sql % ( basedate + timedelta(days=-30) ))
    if not b:
        fillDataset("* from monthly where date<'%s' order by date desc limit 1" % (basedate + timedelta(days=-15)))

    sql = "* from monthly where date='%s'"
    fillDataset(sql % ( firstday + relativedelta(months=delta) ))
    fillDataset(sql % ( firstday + relativedelta(years=-1) ))
    fillDataset(sql % ( firstday + relativedelta(years=-2) ))
    fillDataset(sql % ( firstday + relativedelta(years=-3) ))
    fillDataset(sql % ( firstday + relativedelta(years=-5) ))

    s = set()
    array = []
    for data in dataset:
        if data["date"] in s: continue
        s.add(data["date"])
        data["time"] = parser.parse(data["time"])
        data["date"] = parser.parse(data["date"]).date()
        data["items"] = ast.literal_eval(data["items"])
        array.append(data)
    return sorted(array, reverse=True, key=lambda item: item["date"])


def fetchAndSaveToday():
    def getTableItems():
        html = scraperwiki.scrape("http://www.imdb.com/chart/top")
        root = lxml.html.fromstring(html)
        for table in root.cssselect("div#main table"):
            trs = table.cssselect("tr");
            if len(trs)>100: return trs[1:]
    def parseTableItem(tr):
        tds = tr.cssselect("td")
        link = tr.cssselect("td a")[0]
        return {
            "id": re.search(r"/tt(\d+)", link.attrib["href"]).group(1),
            "title": link.text,
            "year": re.sub(r"[\( \)]", "", link.tail),
            "rating": tds[1].text_content(),
            "votes": int(tds[3].text_content().replace(',', ''))
        }
    time = datetime.datetime.utcnow()
    trs = getTableItems()
    items = [parseTableItem(tr) for tr in trs]
    data = {
        "date": time.date(),
        "items": items,
        "time": time,
    }
    dataset = getRelativeDataset(data["date"])
    calcVotesDelta(data, dataset)
    saveDailyData(data)
    trySaveMonthlyData(data)
    return data



def fetchAndSaveHistory():
    print "removed"
    pass


def fetchAndSaveHistorySnapshot(url, time, date=None):
    print time, url
    firstday = datetime.date(time.year, time.month, 1)
    try:
        dataset = scraperwiki.sqlite.select("date from monthly where date='%s'" % firstday)
    except scraperwiki.sqlite.SqliteError, e:
        dataset = []
    if dataset:
        print "SKIP"
        return
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    if date is None:
        trweb = root.cssselect("table.snapshot tr")[2]
        tdweb = trweb.cssselect("td")[1]
        if len(tdweb.attrib["title"])<9:
            print "=== no web data"
            return
        date = firstday
    table = root.cssselect("table")[1]
    trs = table.cssselect("tr")
    def parseItem(tr):
        tds = tr.cssselect("td")
        return {
            "id": tds[1].text,
            "title": tr.cssselect("th a")[0].text,
            "year": tds[5].text,
            "rating": tds[3].text,
            "votes": int(tds[4].text),
        }
    items = [parseItem(tr) for tr in trs]
    data = {
        "date": date,
        "items": items,
        "time": time,
    }
    trySaveMonthlyData(data)
    return data



def trySaveMonthlyData(data, force=False):
    today = data["date"]
    if today.day>5: return
    firstday = datetime.date(today.year, today.month, 1)
    if not force:
        try:
            dataset = scraperwiki.sqlite.select("date from monthly where date='%s' limit 1" % firstday)
        except scraperwiki.sqlite.SqliteError, e:
            dataset = []
            print "=== " + str(e)
        if dataset: return
    data["date"] = firstday
    scraperwiki.sqlite.save(['date'], data, "monthly")
    data["date"] = today
    print "SAVED data to monthly"


def saveDailyData(data):
    scraperwiki.sqlite.save(['date'], data, "daily")
    lastmonth = data["date"] + timedelta(days=-36)
    scraperwiki.sqlite.execute("delete from daily where date<'%s'" % lastmonth)   
    scraperwiki.sqlite.commit()


def resetAllMonthlyDelta():
    dataset = scraperwiki.sqlite.select("date from monthly")
    for item in dataset:
        (data, saved) = getVotesDeltaSnapshot(item["date"])
        if not saved:
            trySaveMonthlyData(data, True)


##########
main()