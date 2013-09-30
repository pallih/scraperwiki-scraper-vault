import lxml.html
import urlparse
import datetime
import mechanize
import scraperwiki
import logging


START_DAYS_AGO = 9526
PAGE_SIZE = 25
BASE_URL = 'http://www.secretary.state.nc.us/'


def generate_dates():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=START_DAYS_AGO)
    while start < today:
        end = start + datetime.timedelta(days=PAGE_SIZE)
        yield (start, end)
        start = end


def save_row(row):
    row['SOSID'] = int(row['SOSID'])
    row['DateFormed'] = datetime.datetime.strptime(row['DateFormed'], '%m/%d/%Y %I:%M:%S %p')
    scraperwiki.sqlite.save(unique_keys=['SOSID'], data=row)


def download_files(counties):
    for start, end in generate_dates():
        br = mechanize.Browser()
        br.open(urlparse.urljoin(BASE_URL, '/Corporations/SearchChgs.aspx'))
        br.select_form(nr=0)
        br['County'] = counties
        br['From'] = start.strftime('%m/%d/%Y')
        br['To'] = end.strftime('%m/%d/%Y')
        print 'Searching {0}-{1} in {2} counties'.format(br['From'], br['To'],
                                                         br['County'])
        r = br.submit(label='Search')
        download_link = list(br.links(url_regex=r'PItemId'))[0]
        print (download_link)
        url = urlparse.urljoin(BASE_URL, 'corporations/'download_link.url[0:])
        print 'Downloading {0}'.format(url)
        f = br.retrieve(url)[0]
        print 'Saved temporary file {0}'.format(f)
        root=lxml.html.parse(url)
        print root.cssselect("table #SosContent_SosContent_WucDocuments1_GridView1")[0]
        print(url)



counties = ['All Counties']
download_files(counties)import lxml.html
import urlparse
import datetime
import mechanize
import scraperwiki
import logging


START_DAYS_AGO = 9526
PAGE_SIZE = 25
BASE_URL = 'http://www.secretary.state.nc.us/'


def generate_dates():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=START_DAYS_AGO)
    while start < today:
        end = start + datetime.timedelta(days=PAGE_SIZE)
        yield (start, end)
        start = end


def save_row(row):
    row['SOSID'] = int(row['SOSID'])
    row['DateFormed'] = datetime.datetime.strptime(row['DateFormed'], '%m/%d/%Y %I:%M:%S %p')
    scraperwiki.sqlite.save(unique_keys=['SOSID'], data=row)


def download_files(counties):
    for start, end in generate_dates():
        br = mechanize.Browser()
        br.open(urlparse.urljoin(BASE_URL, '/Corporations/SearchChgs.aspx'))
        br.select_form(nr=0)
        br['County'] = counties
        br['From'] = start.strftime('%m/%d/%Y')
        br['To'] = end.strftime('%m/%d/%Y')
        print 'Searching {0}-{1} in {2} counties'.format(br['From'], br['To'],
                                                         br['County'])
        r = br.submit(label='Search')
        download_link = list(br.links(url_regex=r'PItemId'))[0]
        print (download_link)
        url = urlparse.urljoin(BASE_URL, 'corporations/'download_link.url[0:])
        print 'Downloading {0}'.format(url)
        f = br.retrieve(url)[0]
        print 'Saved temporary file {0}'.format(f)
        root=lxml.html.parse(url)
        print root.cssselect("table #SosContent_SosContent_WucDocuments1_GridView1")[0]
        print(url)



counties = ['All Counties']
download_files(counties)