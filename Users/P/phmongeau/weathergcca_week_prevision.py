from datetime import datetime, timedelta
import scraperwiki
from lxml.html import fromstring

class Prevision(object):
    def __init__(self):
        return

today = datetime.now()


def parse(html):
    doc = fromstring(html)

    els = doc.find_class("fperiod")

    date = today
    d = timedelta(days = 1)
    for e in els:
        ul = e.find("ul")
        img = e.find("img")
        p = Prevision()
        p.high = ul.cssselect(".high")[0].text.strip()
        p.low = ul.cssselect(".low")[0].text.strip()
        p.pop = ul.cssselect(".pop")[0].text.strip()
        p.day = date.strftime("%A")
        p.condition = img.get("title").strip()

        data = {
            "day": p.day,
            "date": date.strftime("%F"),
            "high": p.high,
            "low": p.low,
            "pop": p.pop,
            "condition": p.condition
        }
        scraperwiki.sqlite.save(unique_keys=["date"], data = data)
        date += d

try:
    #url for montreal
    html = scraperwiki.scrape("http://meteo.gc.ca/city/pages/qc-147_metric_f.html")
    parse(html.decode("utf-8"))
except:
    pass

