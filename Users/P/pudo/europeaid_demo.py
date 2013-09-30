import scraperwiki
from lxml import html 
from itertools import count

# The URL we'll scrape from:
URL = 'http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm?lang=en&mode=SM&type=grant&order=false&direc=false&paging.offset=%s&paging.len=50'

# Download each page of the search result:
for page in count():
    url = URL % (page*50)

    # Get a web page and turn it into an abstract "document":
    html_text = scraperwiki.scrape(url)
    document = html.fromstring(html_text)

    # Go through all the rows.
    for row_element in document.findall('.//table//table//tr'):
        cells = row_element.findall('.//td')
        print cells

        data = {
            'contract_nr':  cells[0].text,
            'title':        cells[1].text,
            'dac_code':     cells[2].text,
            'theme':        cells[3].text,
            'organisation': cells[4].text,
            'nationality':  cells[5].text,
            'region':       cells[6].text,
            'action_loc':   cells[7].text,
            'amount':       cells[8].text,
            'ec_amount':    cells[9].text,
            'total_cost':   cells[10].text,
            'duration':     cells[11].text,
            }
        print data

        # Clean your data
        data['amount'] = data['amount'].replace(',', '')

        # Save it
        scraperwiki.sqlite.save(unique_keys=['contract_nr'], data=data)
        


import scraperwiki
from lxml import html 
from itertools import count

# The URL we'll scrape from:
URL = 'http://ec.europa.eu/europeaid/work/funding/beneficiaries/index.cfm?lang=en&mode=SM&type=grant&order=false&direc=false&paging.offset=%s&paging.len=50'

# Download each page of the search result:
for page in count():
    url = URL % (page*50)

    # Get a web page and turn it into an abstract "document":
    html_text = scraperwiki.scrape(url)
    document = html.fromstring(html_text)

    # Go through all the rows.
    for row_element in document.findall('.//table//table//tr'):
        cells = row_element.findall('.//td')
        print cells

        data = {
            'contract_nr':  cells[0].text,
            'title':        cells[1].text,
            'dac_code':     cells[2].text,
            'theme':        cells[3].text,
            'organisation': cells[4].text,
            'nationality':  cells[5].text,
            'region':       cells[6].text,
            'action_loc':   cells[7].text,
            'amount':       cells[8].text,
            'ec_amount':    cells[9].text,
            'total_cost':   cells[10].text,
            'duration':     cells[11].text,
            }
        print data

        # Clean your data
        data['amount'] = data['amount'].replace(',', '')

        # Save it
        scraperwiki.sqlite.save(unique_keys=['contract_nr'], data=data)
        


