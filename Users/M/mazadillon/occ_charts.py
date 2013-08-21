import scraperwiki
import lxml.html
from dateutil import parser
import datetime

def scrapechart(url,chart):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    data = dict()
    date = parser.parse(root.cssselect("div.template")[0].cssselect("div")[0].cssselect("h1")[0].cssselect("span")[0].text_content()[2:])
    data['date'] = date.strftime('%Y-%m-%d')
    data['chart'] = chart
    for tr in root.cssselect("tr.entry"):
        fields = tr.cssselect("td")
        data['position'] = int(fields[0].text_content())
        data['previous'] = fields[1].text_content()
        data['weeks'] = int(fields[2].text_content())
        info = fields[3].cssselect("div")[0]
        data['artist'] = info.cssselect("h4")[0].text_content()
        data['title'] = info.cssselect("h3")[0].text_content()
        data['label'] = info.cssselect("h5")[0].text_content()[1:-1] #Trim off brackets from label name
        scraperwiki.sqlite.save(['date','position','chart'],data)    

scrapechart('http://www.theofficialcharts.com/singles-chart/','singles')
scrapechart('http://www.theofficialcharts.com/albums-chart/','albums')
