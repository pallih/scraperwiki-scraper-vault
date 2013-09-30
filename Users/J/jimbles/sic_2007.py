import scraperwiki
import lxml.html

data = scraperwiki.scrape ('http://www.companieshouse.gov.uk/infoAndGuide/sic/sic2007.shtml')
root = lxml.html.fromstring (data)
for row in root.xpath ('//tr'):
    cols = [col.text_content() for col in row.xpath('.//td')]
    if len(cols) == 2:
        if len(cols[0]) > 8:
            if cols[0][:8] == 'SECTION ':
                sec = cols[0][8:]
                scraperwiki.sqlite.save (unique_keys=['Section'], data={'Section':sec, 'Description':cols[1]}, table_name='sections', verbose=0)
        elif cols[0].isdigit():
            scraperwiki.sqlite.save (unique_keys=['SIC'], data={'Section':sec, 'SIC':cols[0], 'Description':cols[1]}, table_name='codes', verbose=0)


import scraperwiki
import lxml.html

data = scraperwiki.scrape ('http://www.companieshouse.gov.uk/infoAndGuide/sic/sic2007.shtml')
root = lxml.html.fromstring (data)
for row in root.xpath ('//tr'):
    cols = [col.text_content() for col in row.xpath('.//td')]
    if len(cols) == 2:
        if len(cols[0]) > 8:
            if cols[0][:8] == 'SECTION ':
                sec = cols[0][8:]
                scraperwiki.sqlite.save (unique_keys=['Section'], data={'Section':sec, 'Description':cols[1]}, table_name='sections', verbose=0)
        elif cols[0].isdigit():
            scraperwiki.sqlite.save (unique_keys=['SIC'], data={'Section':sec, 'SIC':cols[0], 'Description':cols[1]}, table_name='codes', verbose=0)


