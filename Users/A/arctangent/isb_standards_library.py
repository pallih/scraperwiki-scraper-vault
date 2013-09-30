# This scraper extracts summary standard information from the ISB Standards Library

import scraperwiki
import lxml.html

# Get a list of all ISB standards
url_all_standards = 'http://www.isb.nhs.uk/library/all'

# Scrape the summary page and construct a parser object
doc = lxml.html.parse(url_all_standards).getroot()

# Naughty web developers sometimes don't provide absolute URLs
# in the href attribute of their anchor tags. We can fix this.
doc.make_links_absolute()

# We want to iterate over the rows of the table,
# but we need to skip the first one because it
# doesn't contain any td elements.
table_rows = iter(doc.cssselect('table[class="listing"] tr'))
table_rows.next()

# Helper function to get the URL from the href attribute
# of the first anchor tag inside an element.
def get_first_anchor_destination(element):
    # Sometimes there is no link, so we need to handle that
    if element.cssselect('a'):
        return element.cssselect('a')[0].get('href')
    else:
        return ''

# Iterate over the table rows and extract the data
for tr in table_rows:
    # Get all td elements
    tds = tr.cssselect('td')
    # Construct the information we want to save
    data = {
        'standard_number': tds[0].text_content(),
        'standard_title': tds[1].text_content(),
        'standard_link': get_first_anchor_destination(tds[1]),
        'current_release': tds[2].text_content(),
        'current_release_link': get_first_anchor_destination(tds[2]),
        'status': tds[3].text_content(),
        'link_to_docs': get_first_anchor_destination(tds[4]),
    }
    # Save the scraped data
    scraperwiki.sqlite.save(unique_keys=['standard_number'], data=data)# This scraper extracts summary standard information from the ISB Standards Library

import scraperwiki
import lxml.html

# Get a list of all ISB standards
url_all_standards = 'http://www.isb.nhs.uk/library/all'

# Scrape the summary page and construct a parser object
doc = lxml.html.parse(url_all_standards).getroot()

# Naughty web developers sometimes don't provide absolute URLs
# in the href attribute of their anchor tags. We can fix this.
doc.make_links_absolute()

# We want to iterate over the rows of the table,
# but we need to skip the first one because it
# doesn't contain any td elements.
table_rows = iter(doc.cssselect('table[class="listing"] tr'))
table_rows.next()

# Helper function to get the URL from the href attribute
# of the first anchor tag inside an element.
def get_first_anchor_destination(element):
    # Sometimes there is no link, so we need to handle that
    if element.cssselect('a'):
        return element.cssselect('a')[0].get('href')
    else:
        return ''

# Iterate over the table rows and extract the data
for tr in table_rows:
    # Get all td elements
    tds = tr.cssselect('td')
    # Construct the information we want to save
    data = {
        'standard_number': tds[0].text_content(),
        'standard_title': tds[1].text_content(),
        'standard_link': get_first_anchor_destination(tds[1]),
        'current_release': tds[2].text_content(),
        'current_release_link': get_first_anchor_destination(tds[2]),
        'status': tds[3].text_content(),
        'link_to_docs': get_first_anchor_destination(tds[4]),
    }
    # Save the scraped data
    scraperwiki.sqlite.save(unique_keys=['standard_number'], data=data)