# -*- coding: UTF-8 -*-

import scraperwiki
import lxml.html
import dateutil.parser
import datetime
import time

months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

def get_value(root, select):
    ref = root.cssselect(select)
    return ref[0].text_content().strip()

def scrape_harder(url):
    for n in [1, 2, 3]:
        try:
            return scraperwiki.scrape(url).decode('utf-8')
        except:
            time.sleep(1)
            continue
    return scraperwiki.scrape(url).decode('utf-8')

def parse_doffin_entry(month, seq, url, html):
    root = lxml.html.fromstring(html)
    titleref = root.cssselect("html title")
    title = titleref[0].text_content()
    if -1 != title.find('Sideparametere ugyldige - Doffin'):
        print "Invalid entry"
        return None
    contentref = root.cssselect("div.notice")
    abstract = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblAbstract")
    pubdate = get_value(root,"span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblPubDate")
    appdocdeadline = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblAppdeadline")
    appdeadlinedate = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblDeadlineDate")
    appdeadlinetime = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblDeadlineTime")
    title = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblTitle")
    publisher = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblAuth")
    apptype = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblDocType")

    data = {
        'month' : month,
        'seq' : seq,
        'scrapedurl'  : url,
        'title'       : title,
        'abstract'    : abstract,
        'publisher'   : publisher,
        'publishdate' : dateutil.parser.parse(pubdate, dayfirst=True).date(),
        'scrapestamputc' : datetime.datetime.now(),
        'apptype'     : apptype,
    }
    # FIXME Figure out how to handle canceled tenders
    if appdeadlinedate is not None and appdeadlinedate != "" and appdeadlinedate != "Kansellert":
        #print "'%s'" % appdeadlinedate
        data['appdeadline'] = dateutil.parser.parse(appdeadlinedate + " " + appdeadlinetime, dayfirst=True)
    if appdocdeadline is not None and appdocdeadline != "":
        data['appdocdeadline'] = dateutil.parser.parse(appdocdeadline, dayfirst=True).date()
    print data
    
    return data

def fetch_doffin_entry(month, seq, datastore):
    url = "http://www.doffin.no/search/show/search_view.aspx?ID=" + month + str(seq)
    print "Fetching from " + url
    html = scrape_harder(url)
    entry = parse_doffin_entry(month, seq, url, html)
    if entry is not None:
        datastore.append(entry)
        return True
    return False

def scrape(start, curmon, end, step = 1):
    datastore = []
    for seq in range(start, end, step):
        if fetch_doffin_entry(curmon, seq, datastore):
            if 0 == len(datastore) % 10:
                scraperwiki.sqlite.save(unique_keys=['month', 'seq'], data=datastore)
                datastore = []
        else:
            if 0 < len(datastore):
                scraperwiki.sqlite.save(unique_keys=['month', 'seq'], data=datastore)
                datastore = []
            if fetch_doffin_entry(nextmonth(curmon, step), seq, datastore):
                curmon = nextmonth(curmon, step)
    if 0 < len(datastore):
        scraperwiki.sqlite.save(unique_keys=['month', 'seq'], data=datastore)

def nextmonth(mon, direction = 1):
    i = 0
    while i < len(months):
        #print "if " + mon + " == " + months[i]
        if mon == months[i]:
            break
        i = i + 1
    if i == len(months):
        raise ValueError("Unknown month string " + mon)
    #print i, months[i]
    nexti = (i + direction) % (len(months))
    #print nexti, months[nexti]
    return months[nexti]

def fix_old(count):
    tmp = scraperwiki.sqlite.select("seq, month from swdata where seq = (select min(seq) from swdata where scrapestamputc <= '2012-06-15 09:47:11' and appdocdeadline like '(d%')")
    if 0 < len(tmp):
        min = tmp[0]['seq']
        curmon = tmp[0]['month']
        print "Updating old entries, starting with ", min, curmon, min+count
        return scrape(min, curmon, min+count, 1)

print "Starting Doffin scraper"

fix_old(1000)

# Random valid number near the time this scraper was created, to bootstrap
# the scraper
curmon = "JUN"
max = 179504

# Another random valid id in 2007, unreachable using this code 2012-06-20 DEC070629

fetchperrun = 200

try:
    tmp = scraperwiki.sqlite.select("seq, month from swdata where seq = (select max(seq) from swdata)")
    max = tmp[0]['seq']
    curmon = tmp[0]['month']
    print "Starting with " + curmon + " " + str(max)
except scraperwiki.sqlite.SqliteError, e:
    print "No sqlite entries found, using default."
    pass

scrape(max+1, curmon, max+fetchperrun)

# Example of non-valid entry
#fetch_doffin_entry("APR", "100000", datastore)

# Got all the old ones, skip trying to find more [pere 2012-06-19]?
exit(0)

fetchperrun = 1000

try:
    tmp = scraperwiki.sqlite.select("seq, month from swdata where seq = (select min(seq) from swdata)")
    min = tmp[0]['seq']
    curmon = tmp[0]['month']
    print "Starting with " + curmon + " " + str(min)
    if min > 0:
        scrape(min-1, curmon, min-fetchperrun, -1)
    else:
        print "Reaching the begining, not parsing backwards."
except scraperwiki.sqlite.SqliteError, e:
    print "No sqlite entries found, not parsing backwards"
# -*- coding: UTF-8 -*-

import scraperwiki
import lxml.html
import dateutil.parser
import datetime
import time

months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
          'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

def get_value(root, select):
    ref = root.cssselect(select)
    return ref[0].text_content().strip()

def scrape_harder(url):
    for n in [1, 2, 3]:
        try:
            return scraperwiki.scrape(url).decode('utf-8')
        except:
            time.sleep(1)
            continue
    return scraperwiki.scrape(url).decode('utf-8')

def parse_doffin_entry(month, seq, url, html):
    root = lxml.html.fromstring(html)
    titleref = root.cssselect("html title")
    title = titleref[0].text_content()
    if -1 != title.find('Sideparametere ugyldige - Doffin'):
        print "Invalid entry"
        return None
    contentref = root.cssselect("div.notice")
    abstract = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblAbstract")
    pubdate = get_value(root,"span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblPubDate")
    appdocdeadline = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblAppdeadline")
    appdeadlinedate = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblDeadlineDate")
    appdeadlinetime = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblDeadlineTime")
    title = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblTitle")
    publisher = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblAuth")
    apptype = get_value(root, "span#ctl00_ContentPlaceHolder1_tab_StandardNoticeView1_notice_introduction1_lblDocType")

    data = {
        'month' : month,
        'seq' : seq,
        'scrapedurl'  : url,
        'title'       : title,
        'abstract'    : abstract,
        'publisher'   : publisher,
        'publishdate' : dateutil.parser.parse(pubdate, dayfirst=True).date(),
        'scrapestamputc' : datetime.datetime.now(),
        'apptype'     : apptype,
    }
    # FIXME Figure out how to handle canceled tenders
    if appdeadlinedate is not None and appdeadlinedate != "" and appdeadlinedate != "Kansellert":
        #print "'%s'" % appdeadlinedate
        data['appdeadline'] = dateutil.parser.parse(appdeadlinedate + " " + appdeadlinetime, dayfirst=True)
    if appdocdeadline is not None and appdocdeadline != "":
        data['appdocdeadline'] = dateutil.parser.parse(appdocdeadline, dayfirst=True).date()
    print data
    
    return data

def fetch_doffin_entry(month, seq, datastore):
    url = "http://www.doffin.no/search/show/search_view.aspx?ID=" + month + str(seq)
    print "Fetching from " + url
    html = scrape_harder(url)
    entry = parse_doffin_entry(month, seq, url, html)
    if entry is not None:
        datastore.append(entry)
        return True
    return False

def scrape(start, curmon, end, step = 1):
    datastore = []
    for seq in range(start, end, step):
        if fetch_doffin_entry(curmon, seq, datastore):
            if 0 == len(datastore) % 10:
                scraperwiki.sqlite.save(unique_keys=['month', 'seq'], data=datastore)
                datastore = []
        else:
            if 0 < len(datastore):
                scraperwiki.sqlite.save(unique_keys=['month', 'seq'], data=datastore)
                datastore = []
            if fetch_doffin_entry(nextmonth(curmon, step), seq, datastore):
                curmon = nextmonth(curmon, step)
    if 0 < len(datastore):
        scraperwiki.sqlite.save(unique_keys=['month', 'seq'], data=datastore)

def nextmonth(mon, direction = 1):
    i = 0
    while i < len(months):
        #print "if " + mon + " == " + months[i]
        if mon == months[i]:
            break
        i = i + 1
    if i == len(months):
        raise ValueError("Unknown month string " + mon)
    #print i, months[i]
    nexti = (i + direction) % (len(months))
    #print nexti, months[nexti]
    return months[nexti]

def fix_old(count):
    tmp = scraperwiki.sqlite.select("seq, month from swdata where seq = (select min(seq) from swdata where scrapestamputc <= '2012-06-15 09:47:11' and appdocdeadline like '(d%')")
    if 0 < len(tmp):
        min = tmp[0]['seq']
        curmon = tmp[0]['month']
        print "Updating old entries, starting with ", min, curmon, min+count
        return scrape(min, curmon, min+count, 1)

print "Starting Doffin scraper"

fix_old(1000)

# Random valid number near the time this scraper was created, to bootstrap
# the scraper
curmon = "JUN"
max = 179504

# Another random valid id in 2007, unreachable using this code 2012-06-20 DEC070629

fetchperrun = 200

try:
    tmp = scraperwiki.sqlite.select("seq, month from swdata where seq = (select max(seq) from swdata)")
    max = tmp[0]['seq']
    curmon = tmp[0]['month']
    print "Starting with " + curmon + " " + str(max)
except scraperwiki.sqlite.SqliteError, e:
    print "No sqlite entries found, using default."
    pass

scrape(max+1, curmon, max+fetchperrun)

# Example of non-valid entry
#fetch_doffin_entry("APR", "100000", datastore)

# Got all the old ones, skip trying to find more [pere 2012-06-19]?
exit(0)

fetchperrun = 1000

try:
    tmp = scraperwiki.sqlite.select("seq, month from swdata where seq = (select min(seq) from swdata)")
    min = tmp[0]['seq']
    curmon = tmp[0]['month']
    print "Starting with " + curmon + " " + str(min)
    if min > 0:
        scrape(min-1, curmon, min-fetchperrun, -1)
    else:
        print "Reaching the begining, not parsing backwards."
except scraperwiki.sqlite.SqliteError, e:
    print "No sqlite entries found, not parsing backwards"
