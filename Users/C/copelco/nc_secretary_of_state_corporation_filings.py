import csv
import urlparse
import datetime
import mechanize
import scraperwiki
import logging


START_DAYS_AGO = 3
PAGE_SIZE = 2
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
        r = br.submit(label='Download Corporations List')
        download_link = list(br.links(url_regex=r'txt$'))[0]
        # url is relative, e.g. ../imaging/Dime/20120425/07748597.txt, which
        # confuses mechanize, so join it with BASE_URL
        url = urlparse.urljoin(BASE_URL, download_link.url[3:])
        print 'Downloading {0}'.format(url)
        f = br.retrieve(url)[0]
        print 'Saved temporary file {0}'.format(f)
        with open(f) as csv_file:
            reader = csv.DictReader(csv_file, delimiter='\t')
            for row in reader:
                if row['SOSID']:
                    try:
                        save_row(row)
                    except Exception, e:
                        logging.exception(e)

counties = ['All Counties']
download_files(counties)
