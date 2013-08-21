import scraperwiki
import lxml.html 
import time

# Blank Python
html = scraperwiki.scrape("https://www.secumd.org/rates-calculators.aspx")
root = lxml.html.fromstring(html)
rows= root.xpath("//table[@class='compare-rates secu tab4_0']/tr")
now = time.strftime("%Y-%m-%d ", time.gmtime())

for row in rows:
    cols= row.xpath('td')
    if len(cols) >3:
        data = {'date': now, 'term': cols[0].text, 'rate': cols[1].text, 'points': cols[2].text}
        scraperwiki.sqlite.save(unique_keys=['date', 'rate', 'term', 'points'], data=data)
