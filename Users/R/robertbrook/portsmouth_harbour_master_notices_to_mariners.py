import scraperwiki
import lxml.html

url = "http://www.qhmportsmouth.com/port-lntm"

root = lxml.html.parse(url).getroot()
trs = root.cssselect("div.lntm tr")

for tr in trs:
    tds = tr.cssselect("td")
    for td in tds:
        print td.text, td.attrib


