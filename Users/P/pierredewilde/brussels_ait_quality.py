import scraperwiki
import lxml.html

end_date = "20111002"
year = 2011

html = scraperwiki.scrape("http://deus.irceline.be/~celinair/index/index_air.php?lan=en&dat=%s" % end_date)

root = lxml.html.fromstring(html)

iLine = 0
timeline = []
for tr in root.cssselect("table tr"):
    iLine += 1
    tds = tr.cssselect("td")
    if not tds:
        continue
    if iLine == 1: # first line contains timeline formatted as dd/mm
        for td in tds[1:]:
            ddmm = td.text_content() # dd/mm
            day = ddmm[0:2]
            month = ddmm[3:5]
            date = "%d-%s-%s" % (year, month, day)
            timeline.append(date)
        print timeline
        #scraperwiki.sqlite.save(unique_keys=['country'], data=data)
