import scraperwiki
import lxml.html
import datetime
import dateutil.parser
import md5
import urllib2

from datetime import date

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html
    
def save_data(url, html, year):
    num_saved = 0
    root = lxml.html.fromstring(html)    
    num_tr = 0
    for tr in root.cssselect(".hoeringsrapport-table tr"):
        num_tr += 1
        if num_tr == 1:
            continue
        
        title_a = tr.cssselect("a")[0]
        hoering_url = title_a.get("href")
        tittel = title_a.text.strip()

        departement = tr.cssselect("td")[1].text.strip()
        utsendt = dateutil.parser.parse(tr.cssselect("td")[2].text.strip(), dayfirst=True)
        hoeringsfrist = dateutil.parser.parse(tr.cssselect("td")[3].text.strip(), dayfirst=True)
        dager = tr.cssselect("td")[4].text.strip()
        tema = tr.cssselect("td")[5].text.strip()
        status = tr.cssselect("td")[6].text.strip()
        
        data = {
            'tittel' : tittel,
            'url' : hoering_url,
            'aar' : year,
            'departement' : departement,
            'hoeringsfrist' : hoeringsfrist,
            'utsendt' : utsendt,
            'antallhoeringsdager' : dager,
            'status' : status,
            #'hash' : md5.new(tittel).digest(),
            #'resultat_tittel' : result_title,
            #'resultat_url' : result_url,
            'scrapedurl' : url,
            'scrapestamputc' : datetime.datetime.now()
        }
            
        scraperwiki.sqlite.save(unique_keys=['tittel', 'aar'], data=data)
        num_saved += 1
        #print "Saved %s" % tittel

    return num_saved

def has_from_year(year):
    try:
        res = scraperwiki.sqlite.select("aar from swdata where aar = '?' limit 1", year)
        return (res > 0)
    except sqllite3.Error, e:
        return False

url = "http://www.regjeringen.no/nb/dok/hoeringer/horingsfristrapport/horingsfrister-for-%s.html"

#html = fetch_url(url)
#save_data(url, html, "2007")

now = datetime.datetime.now()

# first, scrape historic data
for year in range(2007, now.year):
    num_fetched_year = scraperwiki.sqlite.get_var("year_%s" % year)
    if not num_fetched_year or year == now.year:
        year_url = url % year
        html = fetch_url(year_url)
        num_saved = save_data(year_url, html, year)
        if num_saved > 0:
            print "Saved %s for %s" % (num_saved, year)
            scraperwiki.sqlite.save_var("year_%s" % year, num_saved)
        else:
            print "None saved for %s" % year
    else:
        print "Ignoring %s" % year

# second, scrape current year
# TODO: scrape the hole last year, but could be more efficient
current_year_url = "http://www.regjeringen.no/nb/dok/hoeringer/horingsfristrapport.html"
html = fetch_url(current_year_url)
num_saved = save_data(current_year_url, html, now.year)
print "Saved %s for %s" % (num_saved, now.year)
#print res



import scraperwiki
import lxml.html
import datetime
import dateutil.parser
import md5
import urllib2

from datetime import date

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html
    
def save_data(url, html, year):
    num_saved = 0
    root = lxml.html.fromstring(html)    
    num_tr = 0
    for tr in root.cssselect(".hoeringsrapport-table tr"):
        num_tr += 1
        if num_tr == 1:
            continue
        
        title_a = tr.cssselect("a")[0]
        hoering_url = title_a.get("href")
        tittel = title_a.text.strip()

        departement = tr.cssselect("td")[1].text.strip()
        utsendt = dateutil.parser.parse(tr.cssselect("td")[2].text.strip(), dayfirst=True)
        hoeringsfrist = dateutil.parser.parse(tr.cssselect("td")[3].text.strip(), dayfirst=True)
        dager = tr.cssselect("td")[4].text.strip()
        tema = tr.cssselect("td")[5].text.strip()
        status = tr.cssselect("td")[6].text.strip()
        
        data = {
            'tittel' : tittel,
            'url' : hoering_url,
            'aar' : year,
            'departement' : departement,
            'hoeringsfrist' : hoeringsfrist,
            'utsendt' : utsendt,
            'antallhoeringsdager' : dager,
            'status' : status,
            #'hash' : md5.new(tittel).digest(),
            #'resultat_tittel' : result_title,
            #'resultat_url' : result_url,
            'scrapedurl' : url,
            'scrapestamputc' : datetime.datetime.now()
        }
            
        scraperwiki.sqlite.save(unique_keys=['tittel', 'aar'], data=data)
        num_saved += 1
        #print "Saved %s" % tittel

    return num_saved

def has_from_year(year):
    try:
        res = scraperwiki.sqlite.select("aar from swdata where aar = '?' limit 1", year)
        return (res > 0)
    except sqllite3.Error, e:
        return False

url = "http://www.regjeringen.no/nb/dok/hoeringer/horingsfristrapport/horingsfrister-for-%s.html"

#html = fetch_url(url)
#save_data(url, html, "2007")

now = datetime.datetime.now()

# first, scrape historic data
for year in range(2007, now.year):
    num_fetched_year = scraperwiki.sqlite.get_var("year_%s" % year)
    if not num_fetched_year or year == now.year:
        year_url = url % year
        html = fetch_url(year_url)
        num_saved = save_data(year_url, html, year)
        if num_saved > 0:
            print "Saved %s for %s" % (num_saved, year)
            scraperwiki.sqlite.save_var("year_%s" % year, num_saved)
        else:
            print "None saved for %s" % year
    else:
        print "Ignoring %s" % year

# second, scrape current year
# TODO: scrape the hole last year, but could be more efficient
current_year_url = "http://www.regjeringen.no/nb/dok/hoeringer/horingsfristrapport.html"
html = fetch_url(current_year_url)
num_saved = save_data(current_year_url, html, now.year)
print "Saved %s for %s" % (num_saved, now.year)
#print res



