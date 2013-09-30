import scraperwiki
import lxml.html           

def scrape(letter):
    url = "http://www.noswearing.com/dictionary/%s"
    html = scraperwiki.scrape(url % letter)
    print html
    root = lxml.html.fromstring(html)
    for swearword in root.cssselect("table b"):
        if swearword.text_content() != "More Slang Translators:":
            yield swearword.text_content()


for letter in "abcdefghijklmnopqrstuvwxyz":
    for word in scrape(letter):
        scraperwiki.sqlite.save(unique_keys=['word'], data = {"word":word})import scraperwiki
import lxml.html           

def scrape(letter):
    url = "http://www.noswearing.com/dictionary/%s"
    html = scraperwiki.scrape(url % letter)
    print html
    root = lxml.html.fromstring(html)
    for swearword in root.cssselect("table b"):
        if swearword.text_content() != "More Slang Translators:":
            yield swearword.text_content()


for letter in "abcdefghijklmnopqrstuvwxyz":
    for word in scrape(letter):
        scraperwiki.sqlite.save(unique_keys=['word'], data = {"word":word})