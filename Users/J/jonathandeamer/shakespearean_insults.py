import scraperwiki
import lxml.html 

print scraperwiki.sqlite.select('''count(insult) from swdata''')

def get_insults():
    html = scraperwiki.scrape("http://www.pangloss.com/seidel/Shaker/index.html?")
    root = lxml.html.fromstring(html)
    if len(root.cssselect("body b")) > 0:
        insult = root.cssselect("body font")[0]
        play = root.cssselect("body b")[0]
        scraperwiki.sqlite.save(unique_keys=["insult"], data={"insult":insult.text,"play":play.text})

for each in range(1,100):
    get_insults()

print scraperwiki.sqlite.select('''count(insult) from swdata''')import scraperwiki
import lxml.html 

print scraperwiki.sqlite.select('''count(insult) from swdata''')

def get_insults():
    html = scraperwiki.scrape("http://www.pangloss.com/seidel/Shaker/index.html?")
    root = lxml.html.fromstring(html)
    if len(root.cssselect("body b")) > 0:
        insult = root.cssselect("body font")[0]
        play = root.cssselect("body b")[0]
        scraperwiki.sqlite.save(unique_keys=["insult"], data={"insult":insult.text,"play":play.text})

for each in range(1,100):
    get_insults()

print scraperwiki.sqlite.select('''count(insult) from swdata''')