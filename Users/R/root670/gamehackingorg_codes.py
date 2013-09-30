import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://gamehacking.org/?s=v2&sys=35&gid=6107") #Game's code page goes here.
root = lxml.html.fromstring(html)

rowNumber = 0

for el in root.cssselect("table.codes tr"):
    rowNumber = rowNumber + 1
    title = el.cssselect("td")[0]
    codes = el.cssselect("td")[1] #This is a bad way of scraping!
    notes = el.cssselect("td")[2]
    hacker = el.cssselect("td a")[0]
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":rowNumber, "title":title.text, "codes":codes.text_content(), "notes":notes.text, "hacker":hacker.text})import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://gamehacking.org/?s=v2&sys=35&gid=6107") #Game's code page goes here.
root = lxml.html.fromstring(html)

rowNumber = 0

for el in root.cssselect("table.codes tr"):
    rowNumber = rowNumber + 1
    title = el.cssselect("td")[0]
    codes = el.cssselect("td")[1] #This is a bad way of scraping!
    notes = el.cssselect("td")[2]
    hacker = el.cssselect("td a")[0]
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":rowNumber, "title":title.text, "codes":codes.text_content(), "notes":notes.text, "hacker":hacker.text})