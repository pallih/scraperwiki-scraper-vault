# This scraper retrieves data from FANGRAPHS.COM: MLB TEAM BATTING STATISTICS.  For each MLB team, it retrieves:
# AT BATS (AB), RUNS (R), BATTING AVERAGE (BA), ON BASE % + SLUGGING % (OPS), & STRIKEOUT RATE (K%).
# By: Max Martin - xmarti74@uw.edu - 5/6/2013

# Variables : AT BATS (atbats), RUNS (runs), BATTING AVERAGE (batavg), ON BASE % + SLUGGING % (ops), & STRIKEOUT RATE (krate)
# Variables : Source (mlbstats), ? (root), 

import scraperwiki
import urllib
import lxml.html
import string

mlbstats = scraperwiki.scrape("http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2013&month=0&season1=2013&ind=0&team=0,ts&players=0")
print mlbstats

root = lxml.html.fromstring(mlbstats)

for thead in root.cssselect("div.LeaderBoard1_dg1 thead"):
    header = thead[0].cssselect("tr")[0].cssselect("th")[1].cssselect("a")[0].text
    print header

for tbody in root.cssselect("div.LeaderBoard1_dg1 tbody"):
    rawstats = tbody[0].cssselect("tr")[0].cssselect("td")[1].cssselect("a").attrib['href']
    rawstatsb = tbody[0].cssselect("tr")[0].cssselect("td")[1].cssselect("a")[0].text
    print rawstats
    print rawstatsb

    data ={
        'stats_header': header,
        'rawstats': rawstats,
        'rawstatsb': rawstatsb
    }
    scraperwiki.sqlite.save(unique_keys=['name'],data=data)
