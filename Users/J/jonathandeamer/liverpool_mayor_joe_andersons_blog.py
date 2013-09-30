#So-called "blog" is just a regularly updated static page with no RSS feed. So making one.

import scraperwiki
import lxml.html
import datetime
#scraperwiki.sqlite.execute("""create table swdata(id INTEGER PRIMARY KEY AUTOINCREMENT, `title` text)""")

url = "http://www.liverpoollabour.org/JoesJournal.aspx"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
title = root.cssselect("span[id='ControlID_4_rpTeam_ctl01_lblTitle']")[0].text
content = lxml.html.tostring(root.cssselect("span[id='ControlID_4_rpTeam_ctl01_lblContent']")[0])


all_titles = []
for each in scraperwiki.sqlite.select('''title from swdata'''):
    all_titles.append(str(each['title']))

if title not in all_titles:
    scraperwiki.sqlite.save(unique_keys=[], data={"title":title, "content":content,"date_scraped":datetime.date.today(),"url_scraped":url})
    print "Scraped new post."
else:
    print "Nothing new."#So-called "blog" is just a regularly updated static page with no RSS feed. So making one.

import scraperwiki
import lxml.html
import datetime
#scraperwiki.sqlite.execute("""create table swdata(id INTEGER PRIMARY KEY AUTOINCREMENT, `title` text)""")

url = "http://www.liverpoollabour.org/JoesJournal.aspx"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
title = root.cssselect("span[id='ControlID_4_rpTeam_ctl01_lblTitle']")[0].text
content = lxml.html.tostring(root.cssselect("span[id='ControlID_4_rpTeam_ctl01_lblContent']")[0])


all_titles = []
for each in scraperwiki.sqlite.select('''title from swdata'''):
    all_titles.append(str(each['title']))

if title not in all_titles:
    scraperwiki.sqlite.save(unique_keys=[], data={"title":title, "content":content,"date_scraped":datetime.date.today(),"url_scraped":url})
    print "Scraped new post."
else:
    print "Nothing new."