import scraperwiki
import urllib, urlparse
import lxml.html
import re, datetime


urlyear = "http://www.lottery.co.uk/results/lotto/archive-%d.asp"

def FetchYear(year):
    url = urlyear % year
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    divmain = root.cssselect("div.main")[0]
    tables = [ el  for el in divmain  if el.tag == 'table' ]
    
    ldata = [ ]
    for el in tables:
        data = { }
        tr0, tr1 = list(el)
        a = tr0[0][0][0]
        mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)", a.text)
        assert mdate, a.text
        data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
        data["link"] = urlparse.urljoin(url, a.attrib.get("href"))
        jdiv = tr0[0][1]
        jtext = jdiv.text_content()
        mjtext = re.match(u'Jackpot: \xa3([\d,]+)\s*(R?)$', jtext)
        assert mjtext, jtext
        data["jackpot"] = int(re.sub(",", "", mjtext.group(1)))
        data["rollover"] = mjtext.group(2)
        ldata.append(data)
    
    scraperwiki.sqlite.save(["date"], ldata)


def FetchPrize(date, link):
    html = urllib.urlopen(link).read()
    root = lxml.html.fromstring(html)
    divmain = root.cssselect("div.main")[0]
    tables = [ el  for el in divmain  if el.tag == 'table' ]
    prizetable = tables[1]
    rows =prizetable.cssselect("tr")
    for row in rows[1:]:
        print [ td.text_content()  for td in row ]

        print lxml.html.tostring(el)
    exit()


# scrapes the years and links
#for year in range(1994, 2013):
#    FetchYear(year)

# scrapes the page
scraperwiki.sqlite.execute("create table if not exists prizes (date text)")
missprizes = scraperwiki.sqlite.execute("select swdata.date, swdata.link from swdata left join prizes on prizes.date=swdata.date where prizes.date is null limit 5")
for date, link in missprizes["data"]:
    FetchPrize(date, link)
import scraperwiki
import urllib, urlparse
import lxml.html
import re, datetime


urlyear = "http://www.lottery.co.uk/results/lotto/archive-%d.asp"

def FetchYear(year):
    url = urlyear % year
    html = urllib.urlopen(url).read()
    root = lxml.html.fromstring(html)
    divmain = root.cssselect("div.main")[0]
    tables = [ el  for el in divmain  if el.tag == 'table' ]
    
    ldata = [ ]
    for el in tables:
        data = { }
        tr0, tr1 = list(el)
        a = tr0[0][0][0]
        mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)", a.text)
        assert mdate, a.text
        data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
        data["link"] = urlparse.urljoin(url, a.attrib.get("href"))
        jdiv = tr0[0][1]
        jtext = jdiv.text_content()
        mjtext = re.match(u'Jackpot: \xa3([\d,]+)\s*(R?)$', jtext)
        assert mjtext, jtext
        data["jackpot"] = int(re.sub(",", "", mjtext.group(1)))
        data["rollover"] = mjtext.group(2)
        ldata.append(data)
    
    scraperwiki.sqlite.save(["date"], ldata)


def FetchPrize(date, link):
    html = urllib.urlopen(link).read()
    root = lxml.html.fromstring(html)
    divmain = root.cssselect("div.main")[0]
    tables = [ el  for el in divmain  if el.tag == 'table' ]
    prizetable = tables[1]
    rows =prizetable.cssselect("tr")
    for row in rows[1:]:
        print [ td.text_content()  for td in row ]

        print lxml.html.tostring(el)
    exit()


# scrapes the years and links
#for year in range(1994, 2013):
#    FetchYear(year)

# scrapes the page
scraperwiki.sqlite.execute("create table if not exists prizes (date text)")
missprizes = scraperwiki.sqlite.execute("select swdata.date, swdata.link from swdata left join prizes on prizes.date=swdata.date where prizes.date is null limit 5")
for date, link in missprizes["data"]:
    FetchPrize(date, link)
