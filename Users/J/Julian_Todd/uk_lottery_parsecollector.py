import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

lotterygrantfields = ["url text", "recipient text", "description text", "amount real", "date text", "localauthority text", "distributor text"]


fetchstep = 5

def QuickQuery():
    print scraperwiki.sqlite.execute("select count(1), sum(amount) from lotterygrants")
    print scraperwiki.sqlite.execute("select count(1), sum(amount), localauthority from lotterygrants group by localauthority")


def Main():
    scraperwiki.sqlite.execute("drop table if exists lotterygrants")
    scraperwiki.sqlite.execute("create table lotterygrants (%s)" % ",".join(lotterygrantfields))
    print scraperwiki.sqlite.attach("uk_lottery_scrapedownload", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.lotterydayindex limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

    QuickQuery()


def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(html):
    root = lxml.html.fromstring(html)
    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]
    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(lotterygrantsurl, row[0][0].attrib.get('href'))
        
        scraperwiki.sqlite.execute("insert into lotterygrants values (?,?,?,?,?,?,?)", 
                      (data["url"], data["Recipient"], data["Project description"], data["Grant amount"], data["Grant date"].isoformat(), 
                       data["Local authority"], data["Distributing body"]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

lotterygrantfields = ["url text", "recipient text", "description text", "amount real", "date text", "localauthority text", "distributor text"]


fetchstep = 5

def QuickQuery():
    print scraperwiki.sqlite.execute("select count(1), sum(amount) from lotterygrants")
    print scraperwiki.sqlite.execute("select count(1), sum(amount), localauthority from lotterygrants group by localauthority")


def Main():
    scraperwiki.sqlite.execute("drop table if exists lotterygrants")
    scraperwiki.sqlite.execute("create table lotterygrants (%s)" % ",".join(lotterygrantfields))
    print scraperwiki.sqlite.attach("uk_lottery_scrapedownload", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.lotterydayindex limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

    QuickQuery()


def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(html):
    root = lxml.html.fromstring(html)
    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]
    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(lotterygrantsurl, row[0][0].attrib.get('href'))
        
        scraperwiki.sqlite.execute("insert into lotterygrants values (?,?,?,?,?,?,?)", 
                      (data["url"], data["Recipient"], data["Project description"], data["Grant amount"], data["Grant date"].isoformat(), 
                       data["Local authority"], data["Distributing body"]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

lotterygrantfields = ["url text", "recipient text", "description text", "amount real", "date text", "localauthority text", "distributor text"]


fetchstep = 5

def QuickQuery():
    print scraperwiki.sqlite.execute("select count(1), sum(amount) from lotterygrants")
    print scraperwiki.sqlite.execute("select count(1), sum(amount), localauthority from lotterygrants group by localauthority")


def Main():
    scraperwiki.sqlite.execute("drop table if exists lotterygrants")
    scraperwiki.sqlite.execute("create table lotterygrants (%s)" % ",".join(lotterygrantfields))
    print scraperwiki.sqlite.attach("uk_lottery_scrapedownload", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.lotterydayindex limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

    QuickQuery()


def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(html):
    root = lxml.html.fromstring(html)
    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]
    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(lotterygrantsurl, row[0][0].attrib.get('href'))
        
        scraperwiki.sqlite.execute("insert into lotterygrants values (?,?,?,?,?,?,?)", 
                      (data["url"], data["Recipient"], data["Project description"], data["Grant amount"], data["Grant date"].isoformat(), 
                       data["Local authority"], data["Distributing body"]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

lotterygrantfields = ["url text", "recipient text", "description text", "amount real", "date text", "localauthority text", "distributor text"]


fetchstep = 5

def QuickQuery():
    print scraperwiki.sqlite.execute("select count(1), sum(amount) from lotterygrants")
    print scraperwiki.sqlite.execute("select count(1), sum(amount), localauthority from lotterygrants group by localauthority")


def Main():
    scraperwiki.sqlite.execute("drop table if exists lotterygrants")
    scraperwiki.sqlite.execute("create table lotterygrants (%s)" % ",".join(lotterygrantfields))
    print scraperwiki.sqlite.attach("uk_lottery_scrapedownload", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.lotterydayindex limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

    QuickQuery()


def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(html):
    root = lxml.html.fromstring(html)
    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]
    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(lotterygrantsurl, row[0][0].attrib.get('href'))
        
        scraperwiki.sqlite.execute("insert into lotterygrants values (?,?,?,?,?,?,?)", 
                      (data["url"], data["Recipient"], data["Project description"], data["Grant amount"], data["Grant date"].isoformat(), 
                       data["Local authority"], data["Distributing body"]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

lotterygrantfields = ["url text", "recipient text", "description text", "amount real", "date text", "localauthority text", "distributor text"]


fetchstep = 5

def QuickQuery():
    print scraperwiki.sqlite.execute("select count(1), sum(amount) from lotterygrants")
    print scraperwiki.sqlite.execute("select count(1), sum(amount), localauthority from lotterygrants group by localauthority")


def Main():
    scraperwiki.sqlite.execute("drop table if exists lotterygrants")
    scraperwiki.sqlite.execute("create table lotterygrants (%s)" % ",".join(lotterygrantfields))
    print scraperwiki.sqlite.attach("uk_lottery_scrapedownload", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.lotterydayindex limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

    QuickQuery()


def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(html):
    root = lxml.html.fromstring(html)
    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]
    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(lotterygrantsurl, row[0][0].attrib.get('href'))
        
        scraperwiki.sqlite.execute("insert into lotterygrants values (?,?,?,?,?,?,?)", 
                      (data["url"], data["Recipient"], data["Project description"], data["Grant amount"], data["Grant date"].isoformat(), 
                       data["Local authority"], data["Distributing body"]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
