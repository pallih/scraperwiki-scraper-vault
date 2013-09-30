import scraperwiki
import lxml.html
import lxml.etree

xml = scraperwiki.scrape("http://www.abc.net.au/triplej/feeds/playout/unearthed_playout.xml")
root = lxml.etree.fromstring(xml)
for item in root.xpath('//item'):
    data = {
        'title' : item.xpath(".//title/text()"),
        'playedtime' : item.xpath(".//playedtime/text()"),
        'duration' : item.xpath(".//duration/text()"),
        'artistname' : item.xpath(".//artistname/text()"),
        'artistid' : item.xpath(".//artistid/text()"),
        'albumimage' : item.xpath(".//albumimage/text()"),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['playedtime'], data=data)import scraperwiki
import lxml.html
import lxml.etree

xml = scraperwiki.scrape("http://www.abc.net.au/triplej/feeds/playout/unearthed_playout.xml")
root = lxml.etree.fromstring(xml)
for item in root.xpath('//item'):
    data = {
        'title' : item.xpath(".//title/text()"),
        'playedtime' : item.xpath(".//playedtime/text()"),
        'duration' : item.xpath(".//duration/text()"),
        'artistname' : item.xpath(".//artistname/text()"),
        'artistid' : item.xpath(".//artistid/text()"),
        'albumimage' : item.xpath(".//albumimage/text()"),
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['playedtime'], data=data)