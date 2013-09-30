from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def scrape_table(url):
    #download=urlopen("http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm")
    download = urlopen(url)
    html_raw = download.read()
    #print html_raw

    html_lxml = fromstring(html_raw)

    #for html_table in html_lxml.cssselect('table'):
    #    print tostring(html_table)

    #print html_lxml.cssselect('table')[2].cssselect('tr')

    #for tableRow in html_lxml.cssselect('table')[2].cssselect('tr'):
    #    for column in tableRow.cssselect('td'):
    #        print tostring(column)

    html_tables = html_lxml.cssselect('table')
    #html_tableRows = html_tables[2].cssselect('tr')

    #html_tableRow = html_lxml.cssselect('table')[2].cssselect('tr')[8]
    #for html_column in html_tableRow.cssselect('td'):
    #    print html_column.text_content()

    for html_row in html_tables[2].cssselect('tr')[1:]:
        ##### converting the row into an array(???)
        col = [td.text_content() for td in html_row.cssselect('td')]
        #print COLUMN_NAMES
        #print col
        ##### combining the column names with the data and creating a dictionary
        data = dict(zip(COLUMN_NAMES, col))
        #print data
        ##### cleaning up the data
        data['num_workers'] = int(data['num_workers'])
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        #else:
            #raise ValueError('Not a State')
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
        #experimenting with a different way to get the pdf URL
        #print tostring(html_row.cssselect('td')[1].cssselect('a')[0])
        a_elements = html_row.cssselect('a')
        if len(a_elements) > 1:
            raise ValueError('Row has multiple a tags.')
        elif len(a_elements) == 1:
            data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + a_elements[0].attrib['href']
        elif len(a_elements) == 0:
            pass
        data['source_url'] = url
        #print data
        #save([], data)

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  #"http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    print url
    #scrape_table(url)


raw_pdf = urlopen('http://www.dol.gov/olms/regs/compliance/cba/private/cbrp_2448_pri.pdf').read()
#print raw_pdf
print pdftoxml(raw_pdf)

#print tostring(html_lxml)

#data = {
#    "firstname": "Tom",
#    "lastname": "Levine"
#}

#save([], data)
from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime

COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def scrape_table(url):
    #download=urlopen("http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm")
    download = urlopen(url)
    html_raw = download.read()
    #print html_raw

    html_lxml = fromstring(html_raw)

    #for html_table in html_lxml.cssselect('table'):
    #    print tostring(html_table)

    #print html_lxml.cssselect('table')[2].cssselect('tr')

    #for tableRow in html_lxml.cssselect('table')[2].cssselect('tr'):
    #    for column in tableRow.cssselect('td'):
    #        print tostring(column)

    html_tables = html_lxml.cssselect('table')
    #html_tableRows = html_tables[2].cssselect('tr')

    #html_tableRow = html_lxml.cssselect('table')[2].cssselect('tr')[8]
    #for html_column in html_tableRow.cssselect('td'):
    #    print html_column.text_content()

    for html_row in html_tables[2].cssselect('tr')[1:]:
        ##### converting the row into an array(???)
        col = [td.text_content() for td in html_row.cssselect('td')]
        #print COLUMN_NAMES
        #print col
        ##### combining the column names with the data and creating a dictionary
        data = dict(zip(COLUMN_NAMES, col))
        #print data
        ##### cleaning up the data
        data['num_workers'] = int(data['num_workers'])
        if data['location'][:2] in STATES:
            data['state'] = data['location'][:2]
        #else:
            #raise ValueError('Not a State')
        data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], '%m-%d-%y').date()
        #experimenting with a different way to get the pdf URL
        #print tostring(html_row.cssselect('td')[1].cssselect('a')[0])
        a_elements = html_row.cssselect('a')
        if len(a_elements) > 1:
            raise ValueError('Row has multiple a tags.')
        elif len(a_elements) == 1:
            data['pdf'] = 'http://www.dol.gov/olms/regs/compliance/cba/' + a_elements[0].attrib['href']
        elif len(a_elements) == 0:
            pass
        data['source_url'] = url
        #print data
        #save([], data)

urls = [ "http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm",
  #"http://www.dol.gov/olms/regs/compliance/cba/Cbau_mamh.htm",
  "http://www.dol.gov/olms/regs/compliance/cba/Cba_NfOz.htm" ]

for url in urls:
    print url
    #scrape_table(url)


raw_pdf = urlopen('http://www.dol.gov/olms/regs/compliance/cba/private/cbrp_2448_pri.pdf').read()
#print raw_pdf
print pdftoxml(raw_pdf)

#print tostring(html_lxml)

#data = {
#    "firstname": "Tom",
#    "lastname": "Levine"
#}

#save([], data)
