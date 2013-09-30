import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
import scraperwiki
import mechanize
import lxml.etree, lxml.html
import datetime
import re
import urlparse

print dir(mechanize)

def sqliteexecute(val1, val2=None):
    return scraperwiki.sqlite.execute(val1, val2)

def sqlitecommit():
    return scraperwiki.sqlite.commit()


lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"
scrapedate = datetime.datetime.now()

# MainIndex gets batches of index pages
# MainEntries gets the individual page entries for the days that are referenced in the index

# The parsing to happen by joining on from a parsing scraper that drops table and fills in all the values


lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]
lotteryentryfields = ["url text", "ldirowid integer", "tablerownumber integer", "html text", "scrapedate text"]

#sqlitecommand("execute", "create table lotterydayindex (%s)" % ",".join(lotterydayindexfields))
#sqlitecommand("execute", "create table lotteryentrytable (%s)" % ",".join(lotteryentryfields))


def lxmlgetroot(url):
    for i in range(3):
        try:
            return lxml.html.parse(url).getroot()
        except IOError, e:
            time.sleep(1)
            print "Failed", i, url
    raise e

batchsize = 20

def MainEntries():
    lns = sqliteexecute("select count(*) from lotterydayindex").get("data")[0][0]
    print "pageentries:", lns
    for i in range(lns-batchsize, -1, -batchsize):
        print "batch:", i
        res = sqliteexecute("select rowid, lotterydayindex.html from lotterydayindex limit ? offset ?", (batchsize, max(0, i),))
        for r in res["data"]:
            root = lxml.html.fromstring(r[1])
            rows = root.cssselect('table.tblSearchResults tr')
            for i, tr in enumerate(rows):
                if i == 0:
                    continue
                url = urlparse.urljoin(lotterygrantsurl, tr[0][0].attrib.get('href'))
                if sqliteexecute("select rowid from lotteryentrytable where url=?", (url,)).get("data"):
                    continue
                print i, tr
                proot = lxmlgetroot(url)
                phtml = lxml.html.tostring(proot.cssselect('table.tblResultData')[0])
    
                sqliteexecute("insert into lotteryentrytable values (?,?,?,?,?)", 
                              (url, r[0], i, phtml, scrapedate.isoformat()), verbose=0)
            
        sqlitecommit()
    

def MainIndex():
    lotterydayindexfields = ["datefrom text", "dateto text", "page integer", "html text", "scrapedate text"]

    sminmaxdates = sqliteexecute("select min(datefrom), max(dateto) from lotterydayindex").get("data")
    smindatefrom = sminmaxdates and sminmaxdates[0][0] or "2008-01-01"
    mindatefrom = datetime.datetime.strptime(smindatefrom, "%Y-%m-%d").date()

    smaxdateto = sminmaxdates and sminmaxdates[0][1] or "2008-01-01"
    maxdateto = datetime.datetime.strptime(smaxdateto, "%Y-%m-%d").date()

    datefrom = mindatefrom - datetime.timedelta(4)
    dateto = mindatefrom - datetime.timedelta(1)
    print datefrom, dateto
    ScrapeLottery(datefrom, dateto)

    # scrape forward too

def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    page = 1
    while True:
        sqliteexecute("insert into lotterydayindex values (?,?,?,?,?)", 
                      (datefrom.isoformat(), dateto.isoformat(), 0, response.read(), scrapedate.isoformat()))
        br.select_form(name="aspnetForm")
#        try:
        response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')
#        except ClientForm.ControlNotFoundError:
#            break
        page += 1

    sqlitecommit()


for i in range(100):
    MainIndex()
MainEntries()
