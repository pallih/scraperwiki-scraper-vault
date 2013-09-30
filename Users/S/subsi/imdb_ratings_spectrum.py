import scraperwiki
import lxml.html
import re, ast
import datetime

today = datetime.datetime.utcnow()

def main():
    films = fetchFilmList()
    for film in films[:31]:
        changed = False
        spectrum = getStoredSpectrum(film)
        newSpectrum = fetchRatingsSpectrum(film)
        for idx, key, value, votes in newSpectrum:
            if not spectrum.has_key(key):
                spectrum[key] = {}
            item = spectrum[key]
            item["votes"] = votes
            item["index"] = idx
            if value != item.get("value"):
                changed = True
                if item.has_key("history"):
                    item["history"].append((item["vstart"], item["value"], item["date"]))
                    del item["history"][10:]
                else:
                    item["history"] = []
                item["vstart"] = votes
                item["value"] = value
                item["date"] = str(today.date())
        film["updateTime"] = str(today)
        if changed:
            film["modifiedDate"] = str(today.date())
        scraperwiki.sqlite.save(['id'], film, "films")

        #print film 
        #for key, item in sorted(spectrum.items(), key=lambda x: x[1]["index"]): print key, item




def getStoredSpectrum(film):
    try:
        data = scraperwiki.sqlite.select("* from films where id=?", film["id"])[0]
        film["modifiedDate"] = data["modifiedDate"]
        film["spectrum"] = ast.literal_eval(data["spectrum"])
    except Exception, e:
        print "=== %s" % e
        film["spectrum"] = {}
    return film["spectrum"]


def fetchRatingsSpectrum(film):
    url = "http://www.imdb.com/title/tt%s/ratings" % film["id"]
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    data = []
    for p in root.cssselect("div#tn15content p"):
        text = p.text_content()
        r = re.search(r"\b(\d+) IMDb users.+ average vote of ([\d\.]+) ", text)
        if r:
            data.append(("Weighted average", r.group(2), int(r.group(1))))
            continue
        r = re.search(r"Arithmetic mean\D+([\d\.]+)\.\D+([\d\.]+)", text)
        if r:
            data.append(("Arithmetic mean", r.group(1), ""))
            data.append(("Median", r.group(2), ""))
            continue
        r = re.search(r"#(\d+) in the top 250", text)
        if r:
            data.append(("Top 250 Rank", r.group(1), ""))
            continue
    for table in root.cssselect("div#tn15content table"):
        trs = table.cssselect("tr")
        if len(trs)<10: continue
        text = trs[0].text_content()
        r = re.search("Votes[\s\S]+Percentage", text)
        if r:
            for tr in trs[1:]:
                cols = [td.text_content().strip() for td in tr.cssselect("td")]
                data.append(("Rating %s"%cols[2], cols[1], int(cols[0])))
        r = re.search(r"Votes[\s\S]+Average", text)
        if r:
            for tr in trs[1:]:
                cols = [td.text_content().strip() for td in tr.cssselect("td")]
                if len(cols)<3: continue
                data.append((cols[0], cols[2], int(cols[1])))
    data = [(i,)+r for i,r in enumerate(data)]
    return data



def fetchFilmList():
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
    trs = getTableItems()
    items = [parseTableItem(tr) for tr in trs]
    for i, item in enumerate(items):
        item["rank"] = i+1
    return items


##########
main()
import scraperwiki
import lxml.html
import re, ast
import datetime

today = datetime.datetime.utcnow()

def main():
    films = fetchFilmList()
    for film in films[:31]:
        changed = False
        spectrum = getStoredSpectrum(film)
        newSpectrum = fetchRatingsSpectrum(film)
        for idx, key, value, votes in newSpectrum:
            if not spectrum.has_key(key):
                spectrum[key] = {}
            item = spectrum[key]
            item["votes"] = votes
            item["index"] = idx
            if value != item.get("value"):
                changed = True
                if item.has_key("history"):
                    item["history"].append((item["vstart"], item["value"], item["date"]))
                    del item["history"][10:]
                else:
                    item["history"] = []
                item["vstart"] = votes
                item["value"] = value
                item["date"] = str(today.date())
        film["updateTime"] = str(today)
        if changed:
            film["modifiedDate"] = str(today.date())
        scraperwiki.sqlite.save(['id'], film, "films")

        #print film 
        #for key, item in sorted(spectrum.items(), key=lambda x: x[1]["index"]): print key, item




def getStoredSpectrum(film):
    try:
        data = scraperwiki.sqlite.select("* from films where id=?", film["id"])[0]
        film["modifiedDate"] = data["modifiedDate"]
        film["spectrum"] = ast.literal_eval(data["spectrum"])
    except Exception, e:
        print "=== %s" % e
        film["spectrum"] = {}
    return film["spectrum"]


def fetchRatingsSpectrum(film):
    url = "http://www.imdb.com/title/tt%s/ratings" % film["id"]
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    data = []
    for p in root.cssselect("div#tn15content p"):
        text = p.text_content()
        r = re.search(r"\b(\d+) IMDb users.+ average vote of ([\d\.]+) ", text)
        if r:
            data.append(("Weighted average", r.group(2), int(r.group(1))))
            continue
        r = re.search(r"Arithmetic mean\D+([\d\.]+)\.\D+([\d\.]+)", text)
        if r:
            data.append(("Arithmetic mean", r.group(1), ""))
            data.append(("Median", r.group(2), ""))
            continue
        r = re.search(r"#(\d+) in the top 250", text)
        if r:
            data.append(("Top 250 Rank", r.group(1), ""))
            continue
    for table in root.cssselect("div#tn15content table"):
        trs = table.cssselect("tr")
        if len(trs)<10: continue
        text = trs[0].text_content()
        r = re.search("Votes[\s\S]+Percentage", text)
        if r:
            for tr in trs[1:]:
                cols = [td.text_content().strip() for td in tr.cssselect("td")]
                data.append(("Rating %s"%cols[2], cols[1], int(cols[0])))
        r = re.search(r"Votes[\s\S]+Average", text)
        if r:
            for tr in trs[1:]:
                cols = [td.text_content().strip() for td in tr.cssselect("td")]
                if len(cols)<3: continue
                data.append((cols[0], cols[2], int(cols[1])))
    data = [(i,)+r for i,r in enumerate(data)]
    return data



def fetchFilmList():
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
    trs = getTableItems()
    items = [parseTableItem(tr) for tr in trs]
    for i, item in enumerate(items):
        item["rank"] = i+1
    return items


##########
main()
