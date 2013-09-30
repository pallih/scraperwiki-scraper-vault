import scraperwiki           
import lxml.html
import lxml
import html5lib
import re
from bs4 import BeautifulSoup


html = scraperwiki.scrape("http://www.tsa.gov/research/reading/index.shtm")
soup = soup = BeautifulSoup(html)
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dhs (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')


results = []
## url = ("http://www.tsa.gov/research/reading/index.shtm")
url = ("http://www.dhs.gov/foia-library-frequently-requested-records")
html = scraperwiki.scrape(url,user_agent="Mozilla Firefox")
soup = BeautifulSoup(html)
pdf_url = []
pdf_title = []
library_url = []
agency_name = []
pdf_text = []
pdfs = soup.find_all(href=re.compile("pdf"))
for item in pdfs:
    record={}
    record['pdf_url']=item['href']
    record['pdf_title']=item.string
    record['library_url']=url
    record['agency_name']=soup.title.string
    print record
    scraperwiki.sqlite.save(['pdf_url'], record, table_name='tsa')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON dhs (`pdf_url`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON dhs (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()

import scraperwiki           
import lxml.html
import lxml
import html5lib
import re
from bs4 import BeautifulSoup


html = scraperwiki.scrape("http://www.tsa.gov/research/reading/index.shtm")
soup = soup = BeautifulSoup(html)
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS dhs (`pdf_url` VARCHAR PRIMARY KEY, `pdf_title` VARCHAR, `library_url` VARCHAR,  `agency_name` VARCHAR);')


results = []
## url = ("http://www.tsa.gov/research/reading/index.shtm")
url = ("http://www.dhs.gov/foia-library-frequently-requested-records")
html = scraperwiki.scrape(url,user_agent="Mozilla Firefox")
soup = BeautifulSoup(html)
pdf_url = []
pdf_title = []
library_url = []
agency_name = []
pdf_text = []
pdfs = soup.find_all(href=re.compile("pdf"))
for item in pdfs:
    record={}
    record['pdf_url']=item['href']
    record['pdf_title']=item.string
    record['library_url']=url
    record['agency_name']=soup.title.string
    print record
    scraperwiki.sqlite.save(['pdf_url'], record, table_name='tsa')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS byurl ON dhs (`pdf_url`)')
scraperwiki.sqlite.execute('CREATE INDEX IF NOT EXISTS bytitle ON dhs (`pdf_title`)')
scraperwiki.sqlite.execute('ANALYZE')
scraperwiki.sqlite.commit()

