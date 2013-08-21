from lxml.html import parse
from urllib2 import urlopen
from time import time
from scraperwiki import pdftoxml
from scraperwiki.sqlite import save, select, execute, commit
from lxml.etree import fromstring, tostring
from unidecode import unidecode
import warnings
from collections import Counter

DATE = time()

def getpdfs():
    html = parse('http://www.safaricom.co.ke/index.php?id=275').getroot()
    html.make_links_absolute()
    pdf_urls = html.xpath('//table[@class="contenttable" and @width="540"]/descendant::a/@href')
    
    for url in pdf_urls:
        save(['date_scraped', 'url'], {"date_scraped": DATE, "url": url, "pdfxml": pdftoxml(urlopen(url).read())}, 'pdfs')

def parsepdfs():
    data_in = select('date_scraped, url, pdfxml from pdfs where date_scraped = (select max(date_scraped) from pdfs)')
    data_out = []
    for pdf in data_in:
        print 'Parsing ' + pdf['url']
        d = parsepdf(pdf['pdfxml'])

        # Add more information
        for row in d:
            row.update({
                'date_scraped': pdf['date_scraped'],
                'url': pdf['url']
            })

        data_out.extend(d)

    save(['date_scraped', 'url', 'PdfPage', 'PdfTop'], data_out, 'parsed')

def parsepdf(pdfxml):
    xml = fromstring(unidecode(pdfxml))
    d = []
    for page in xml.xpath('//page'):
        townboxes = page.xpath('descendant::text[text()="Town "]')
        tops, manual = row_tops(page)

        # Combine automatic and manual
        table_text = [[text.xpath('string()').strip() for text in page.xpath('descendant::text[@top="%d"]' % top)] for top in tops] + manual

        # Warn if there are multiple town boxes
        if len(page.xpath('descendant::text[text()="Town " and @top!="153"]'))> 0:
            warnings.warn('''Multiple "Town " boxes were found on page %s, but it's probably fine.''' % page.attrib['number'], UserWarning)

        # Make sure that the first is 153
        if townboxes[0].attrib['top'] != "153":
            params = (page.attrib['number'], townboxes[0].attrib['top'], "153")
            raise ValueError('''The first "Town " box on page %s has a "top" attribute of %s rather than %s.''' % params)

        # Check that the header is what I expect
        assert map(tostring, page.xpath('descendant::text[@top="%d"]' % tops[0])) == ['<text top="153" left="85" width="39" height="14" font="1">Town </text>\n', '<text top="153" left="263" width="44" height="14" font="1">Dealer </text>\n', '<text top="153" left="512" width="108" height="14" font="1">Physical Address </text>\n'], tops

        # Then delete it
        columns = table_text.pop(0)
        tops.pop(0)

        # Check that the subheader is what I expect
        if page.attrib['number'] == '1':
            assert ['', ''] == table_text[0][1:], table_text
            town = table_text.pop(0)[0]
            tops.pop(0)
        else:
            assert ['', ''] != table_text[0][1:], table_text

        for top, row in zip(tops, table_text):
            rowdata = dict(zip(columns, row))
            rowdata.update({"Region": town, "PdfPage": int(page.attrib['number']), "PdfTop": top})
            d.append(rowdata)

    return d

def row_tops(page):
    c = Counter()
    manual = []

    for top in map(int, page.xpath('descendant::text/@top')):
        c[top] += 1
    for k, v in c.items():
        if v < 3:
            del(c[k])

        # Manual corrections
        elif k == 820 and v == 4 and page.attrib['number'] == '82':
            del(c[k])
            manual.append(['Westlands', 'EP Communications', 'The Mall 2nd floor'])

        elif v > 3:
            print tostring(page)
            print c
            raise ValueError('''The counter's key "%s" is strange.''' % k)

    tops = c.keys()
    tops.sort()
    return tops, manual

# Testing
# execute('DROP TABLE parsed'); commit()
# parsepdf(select('pdfxml from pdfs where date_scraped = (select max(date_scraped) from pdfs) limit 1')[0]['pdfxml'])


# Download
getpdfs()

# Foreign key
execute('''
CREATE TABLE IF NOT EXISTS parsed (
  date_scraped REAL,
  url TEXT,
  FOREIGN KEY (date_scraped, url) REFERENCES pdfs(date_scraped, url)
)''')
commit()

# Parse
parsepdfs()