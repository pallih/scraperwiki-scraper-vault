import requests
import lxml.html
import scraperwiki
import dateutil.parser
import urllib

def scrape_contributions(tables):
   records = [] 
   for table in tables:
       rows = table.cssselect('tr')
       record = dict()
       for row in rows:
           recipient = row[0].text_content().strip().replace('"', '')
           contributor, contributor_type  = row[1].text_content().strip().split('/', 1)
           contributor = contributor.strip()
           contributor_type = contributor_type.strip()
           address = row[2].text_content().strip().strip()
           date = dateutil.parser.parse(row[3].text_content().strip())
           amount = row[4].text_content().strip()
           record.update({'recipient': recipient, 'contributor': contributor, 
                          'contributor_type': contributor_type,
                        'address': address, 'date': date, 'amount': amount})
       records.append(record)
   scraperwiki.sqlite.save(records[0].keys(), records)
   print repr(records)


def scrape_page(url, page_no):
    print "Scraping %s %d" % (url, page_no)
    html = requests.get(url + "&whichpage=%d" % page_no).text
    print html
    doc = lxml.html.fromstring(html)
    scrape_contributions(doc.cssselect('form[name=SearchResult] table')[2:17])
    scraperwiki.sqlite.save_var('page_no', page_no)
    scrape_page(URL, page_no + 1) #eww

BASE_URL = "http://ocf.dc.gov"
URL = ("http://ocf.dc.gov/dsearch/searchresultcon.asp?mf1=&ml1=&ms1=&mo1=N&mc1=&xa=0&sa=&ea=&ca=N&sc=G&"
"mf3=&ml3=&ms3=&mc3=&mf4=&ml4=&ms4=&mo4=N&d1=0&m1=0&y1=0&d2=0&m2=0&y2=0&d3=0&m3=0&y3=0&mo5=N&sc5="
"&ob1=cast(con_exp_date%20as%20datetime)&ob2=&ob3=&asc=desc&sr=6&type=pcc&confirsttimeflag=Y&searchtype=amt&pagesize=15")

page_no = scraperwiki.sqlite.get_var('page_no', 1)
scrape_page(URL, 2)
import requests
import lxml.html
import scraperwiki
import dateutil.parser
import urllib

def scrape_contributions(tables):
   records = [] 
   for table in tables:
       rows = table.cssselect('tr')
       record = dict()
       for row in rows:
           recipient = row[0].text_content().strip().replace('"', '')
           contributor, contributor_type  = row[1].text_content().strip().split('/', 1)
           contributor = contributor.strip()
           contributor_type = contributor_type.strip()
           address = row[2].text_content().strip().strip()
           date = dateutil.parser.parse(row[3].text_content().strip())
           amount = row[4].text_content().strip()
           record.update({'recipient': recipient, 'contributor': contributor, 
                          'contributor_type': contributor_type,
                        'address': address, 'date': date, 'amount': amount})
       records.append(record)
   scraperwiki.sqlite.save(records[0].keys(), records)
   print repr(records)


def scrape_page(url, page_no):
    print "Scraping %s %d" % (url, page_no)
    html = requests.get(url + "&whichpage=%d" % page_no).text
    print html
    doc = lxml.html.fromstring(html)
    scrape_contributions(doc.cssselect('form[name=SearchResult] table')[2:17])
    scraperwiki.sqlite.save_var('page_no', page_no)
    scrape_page(URL, page_no + 1) #eww

BASE_URL = "http://ocf.dc.gov"
URL = ("http://ocf.dc.gov/dsearch/searchresultcon.asp?mf1=&ml1=&ms1=&mo1=N&mc1=&xa=0&sa=&ea=&ca=N&sc=G&"
"mf3=&ml3=&ms3=&mc3=&mf4=&ml4=&ms4=&mo4=N&d1=0&m1=0&y1=0&d2=0&m2=0&y2=0&d3=0&m3=0&y3=0&mo5=N&sc5="
"&ob1=cast(con_exp_date%20as%20datetime)&ob2=&ob3=&asc=desc&sr=6&type=pcc&confirsttimeflag=Y&searchtype=amt&pagesize=15")

page_no = scraperwiki.sqlite.get_var('page_no', 1)
scrape_page(URL, 2)
