import scraperwiki
from lxml import etree

url = "http://www.statistik.at/web_de/statistiken/preise/verbraucherpreisindex_vpi_hvpi/022832.html"
xpath = "/html/body/div/div[4]/div/div/div/div/div/div/div/table/tbody/tr"

html = scraperwiki.scrape(url)
tree = etree.HTML(html) 
trs = tree.xpath(xpath)
tr = trs[len(trs) - 1]
tds = tr.xpath("td")

released = tree.xpath("/html/body/div/div[4]/div/div/div/div/div/div/div/table/tfoot/tr/td/nobr")[0].text.strip(' \t\n\r')
date = tds[0].text.strip(' \t\n\r')
index = tds[2].text.strip(' \t\n\r')
data = { 'released' : released, 'date' : date, 'index' : index }

print "Latest VPI 2010 index from %s: %s released %s" % (date, index, released)

scraperwiki.sqlite.save(unique_keys=['date'], data=data)

