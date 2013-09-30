'''Pulls data in from http://www.sasra.go.ke/downloads/licensedsaccos.pdf for Microfinance Information eXchange'''

from lxml.etree import fromstring
from scraperwiki.sqlite import save, select, execute, commit
from urllib2 import urlopen
from time import time
from scraperwiki import pdftoxml
from unidecode import unidecode
import datetime
from json import dumps
import re

COLUMN_NAMES = ['NUMBER', 'NAME_OF_SOCIETY', 'POSTAL_ADDRESS', 'DATE_LICENSED']

def parsepage(page, tops, lastpage = False):
    tops = map(int, tops)
    tops.sort()

    data = []
    problems = []

    for top in tops:
        cell_values = [text.xpath('string()') for text in page.xpath('descendant::text[@top="%d"]' % top)]
        cell_values = filter(None, [v.strip() for v in cell_values])

        # Split up concatonated fields
        if len(cell_values) > 1 and 'P.O' in cell_values[1]:
            name, post = cell_values[1].split('P.O')
            if post[0] == '.':
                post = post[1:]
            cell_values = [cell_values[0].strip(), name, 'P.O. ' + post.strip()] + cell_values[2:]
    
        if cell_values in [ ['th'], ['nd'], ['rd'], ['LTD'], [] ]:
            continue

        elif len(cell_values) == 5:
            row = dict(zip(COLUMN_NAMES[0:3], cell_values[0:3]))
            row[COLUMN_NAMES[3]] = datetime.datetime.strptime(cell_values[3] + ', ' + cell_values[4], '%d, %B, %Y').date()

            row['NUMBER'] = int(row['NUMBER'].replace('.', ''))
            row['city'] = row['POSTAL_ADDRESS'].split(' ')[-1]
        elif len(cell_values) == 1:
            skipped = data[-1]['NUMBER'] + 1
            msg = "Extra row near row %d: %s" % (skipped, dumps(cell_values))
            problems.append(msg)
            continue

        elif "Dated" in cell_values[0] and lastpage:
            print "Stopping after row %d on page %s" % (data[-1]['NUMBER'], page.attrib['number'])
            break
        else:
            previous = data[-1]['NUMBER']
            raise ValueError("The row after %d is weird: %s" % (previous, dumps(cell_values)))

        if data == []:
            data.append(row)
        elif data[-1]['NUMBER'] + 1 == row['NUMBER']:
            data.append(row)
        else:
            skipped = data[-1]['NUMBER'] + 1
            raise ValueError('We skipped licensee number %d on page %s.' % (skipped, page.attrib['number']))

    for row in data:
        row['page'] = int(page.attrib['number'])
        row['page-problems'] = '\n'.join(problems)
        row['date_scraped'] = DATE
        postal_code = re.match('.*([0-9]{0,5}-?[0-9]{5})', row['POSTAL_ADDRESS'])
        if postal_code:
            row['postal-code'] = postal_code.group(1)
        else:
            print "No postal code for", row

    return data

def parse(pdfxml):
    print pdfxml
    xml = fromstring(unidecode(pdfxml))
    data = []

    # First page
    page = xml.xpath('//page[position()=1]')[0]

    # Check the first page's headers
    keytops = xml.xpath('//text[i[b[text()="NAME OF SOCIETY " or text()="POSTAL ADDRESS " or text()="DATE LICENSED "]]]/@top')
    assert len(keytops) == 3 and len(set(keytops)) == 1, keytops

    keylefts = xml.xpath('//text[i[b[text()="NAME OF SOCIETY " or text()="POSTAL ADDRESS " or text()="DATE LICENSED "]]]/@left')
    assert len(keylefts) == 3 and len(set(keylefts)) == 3, keylefts

    tops = set(page.xpath('descendant::text[@top > "%s"]/@top' % keytops[0]))
    data.extend(parsepage(page, tops))

    # Middle pages
    for page in xml.xpath('//page[position()>1 and position() < last()]'):
        tops = set(page.xpath('descendant::text/@top'))
        data.extend(parsepage(page, tops))

    # Last page
    page = xml.xpath('//page[position() = last()]')[0]
    tops = set(page.xpath('descendant::text/@top'))
    data.extend(parsepage(page, tops, lastpage = True))

    return data

def download():
    url = 'http://www.sasra.go.ke/downloads/licensedsaccos.pdf'
    pdfblob = urlopen(url).read()
    pdfxml = pdftoxml(pdfblob)
    save(['date_scraped'], {"date_scraped": DATE, "pdfxml": pdfxml}, 'pdfxml')
    return pdfxml

def dbload():
    row = select('date_scraped, pdfxml from pdfxml order by date_scraped desc limit 1')[0]
    return row['pdfxml'], row['date_scraped']


#execute('DROP TABLE societies'); commit(); assert False

if __name__ == "scraper":
    DATE = time()
    #pdfxml = download()
    pdfxml, DATE = dbload()
    data = parse(pdfxml)
    save(['date_scraped', 'NUMBER'], data, 'societies')'''Pulls data in from http://www.sasra.go.ke/downloads/licensedsaccos.pdf for Microfinance Information eXchange'''

from lxml.etree import fromstring
from scraperwiki.sqlite import save, select, execute, commit
from urllib2 import urlopen
from time import time
from scraperwiki import pdftoxml
from unidecode import unidecode
import datetime
from json import dumps
import re

COLUMN_NAMES = ['NUMBER', 'NAME_OF_SOCIETY', 'POSTAL_ADDRESS', 'DATE_LICENSED']

def parsepage(page, tops, lastpage = False):
    tops = map(int, tops)
    tops.sort()

    data = []
    problems = []

    for top in tops:
        cell_values = [text.xpath('string()') for text in page.xpath('descendant::text[@top="%d"]' % top)]
        cell_values = filter(None, [v.strip() for v in cell_values])

        # Split up concatonated fields
        if len(cell_values) > 1 and 'P.O' in cell_values[1]:
            name, post = cell_values[1].split('P.O')
            if post[0] == '.':
                post = post[1:]
            cell_values = [cell_values[0].strip(), name, 'P.O. ' + post.strip()] + cell_values[2:]
    
        if cell_values in [ ['th'], ['nd'], ['rd'], ['LTD'], [] ]:
            continue

        elif len(cell_values) == 5:
            row = dict(zip(COLUMN_NAMES[0:3], cell_values[0:3]))
            row[COLUMN_NAMES[3]] = datetime.datetime.strptime(cell_values[3] + ', ' + cell_values[4], '%d, %B, %Y').date()

            row['NUMBER'] = int(row['NUMBER'].replace('.', ''))
            row['city'] = row['POSTAL_ADDRESS'].split(' ')[-1]
        elif len(cell_values) == 1:
            skipped = data[-1]['NUMBER'] + 1
            msg = "Extra row near row %d: %s" % (skipped, dumps(cell_values))
            problems.append(msg)
            continue

        elif "Dated" in cell_values[0] and lastpage:
            print "Stopping after row %d on page %s" % (data[-1]['NUMBER'], page.attrib['number'])
            break
        else:
            previous = data[-1]['NUMBER']
            raise ValueError("The row after %d is weird: %s" % (previous, dumps(cell_values)))

        if data == []:
            data.append(row)
        elif data[-1]['NUMBER'] + 1 == row['NUMBER']:
            data.append(row)
        else:
            skipped = data[-1]['NUMBER'] + 1
            raise ValueError('We skipped licensee number %d on page %s.' % (skipped, page.attrib['number']))

    for row in data:
        row['page'] = int(page.attrib['number'])
        row['page-problems'] = '\n'.join(problems)
        row['date_scraped'] = DATE
        postal_code = re.match('.*([0-9]{0,5}-?[0-9]{5})', row['POSTAL_ADDRESS'])
        if postal_code:
            row['postal-code'] = postal_code.group(1)
        else:
            print "No postal code for", row

    return data

def parse(pdfxml):
    print pdfxml
    xml = fromstring(unidecode(pdfxml))
    data = []

    # First page
    page = xml.xpath('//page[position()=1]')[0]

    # Check the first page's headers
    keytops = xml.xpath('//text[i[b[text()="NAME OF SOCIETY " or text()="POSTAL ADDRESS " or text()="DATE LICENSED "]]]/@top')
    assert len(keytops) == 3 and len(set(keytops)) == 1, keytops

    keylefts = xml.xpath('//text[i[b[text()="NAME OF SOCIETY " or text()="POSTAL ADDRESS " or text()="DATE LICENSED "]]]/@left')
    assert len(keylefts) == 3 and len(set(keylefts)) == 3, keylefts

    tops = set(page.xpath('descendant::text[@top > "%s"]/@top' % keytops[0]))
    data.extend(parsepage(page, tops))

    # Middle pages
    for page in xml.xpath('//page[position()>1 and position() < last()]'):
        tops = set(page.xpath('descendant::text/@top'))
        data.extend(parsepage(page, tops))

    # Last page
    page = xml.xpath('//page[position() = last()]')[0]
    tops = set(page.xpath('descendant::text/@top'))
    data.extend(parsepage(page, tops, lastpage = True))

    return data

def download():
    url = 'http://www.sasra.go.ke/downloads/licensedsaccos.pdf'
    pdfblob = urlopen(url).read()
    pdfxml = pdftoxml(pdfblob)
    save(['date_scraped'], {"date_scraped": DATE, "pdfxml": pdfxml}, 'pdfxml')
    return pdfxml

def dbload():
    row = select('date_scraped, pdfxml from pdfxml order by date_scraped desc limit 1')[0]
    return row['pdfxml'], row['date_scraped']


#execute('DROP TABLE societies'); commit(); assert False

if __name__ == "scraper":
    DATE = time()
    #pdfxml = download()
    pdfxml, DATE = dbload()
    data = parse(pdfxml)
    save(['date_scraped', 'NUMBER'], data, 'societies')