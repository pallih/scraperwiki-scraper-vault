import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup


url = "http://espn.go.com/college-sports/basketball/recruiting/playerrankings/_/order/true"

scraperwiki.sqlite.execute("drop table if exists swdata")

scraperwiki.sqlite.execute("create table if not exists swdata (decision string)")

page = urlopen(url)

soup = BeautifulSoup(page)

school_data = soup.find("div",{"class":"school-logo"})

school = soup.find("div",{"class":"school-logo"}).getText()

decision = None

if school == "List":
    decision = "Not yet"
else:
    decision = school_data.find("span", {"class":"school-name"}).getText()

print decision

results = scraperwiki.sqlite.select("* from swdata limit 10")
print len(results)

if len(results) == 0:
    scraperwiki.sqlite.execute("insert into swdata values (?)", (decision))
else:
    scraperwiki.sqlite.execute("update swdata set decision = (?)", (decision))

scraperwiki.sqlite.commit()

import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup


url = "http://espn.go.com/college-sports/basketball/recruiting/playerrankings/_/order/true"

scraperwiki.sqlite.execute("drop table if exists swdata")

scraperwiki.sqlite.execute("create table if not exists swdata (decision string)")

page = urlopen(url)

soup = BeautifulSoup(page)

school_data = soup.find("div",{"class":"school-logo"})

school = soup.find("div",{"class":"school-logo"}).getText()

decision = None

if school == "List":
    decision = "Not yet"
else:
    decision = school_data.find("span", {"class":"school-name"}).getText()

print decision

results = scraperwiki.sqlite.select("* from swdata limit 10")
print len(results)

if len(results) == 0:
    scraperwiki.sqlite.execute("insert into swdata values (?)", (decision))
else:
    scraperwiki.sqlite.execute("update swdata set decision = (?)", (decision))

scraperwiki.sqlite.commit()

