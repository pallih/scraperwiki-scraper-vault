# This scraper extracts a list of new standards and updates made
# to specific standards from the ISB Standards Library, ordered by date

import scraperwiki
import lxml.html

# Get a list of all ISB standards
url_all_ISNs = 'http://www.isb.nhs.uk/library/isn/all'

# Scrape the summary page and construct a parser object
doc = lxml.html.parse(url_all_ISNs).getroot()

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
        'date_published': tds[0].text_content(),
        'standard_number': tds[1].text_content(),
        'release_number': tds[2].text_content(),
        'standard_title': tds[3].text_content(),
        'standard_link': get_first_anchor_destination(tds[3]),
        'release_title': tds[4].text_content(),
        'release_link': get_first_anchor_destination(tds[4]),
        'implementation_completion_date': tds[5].text_content(),
        'link_to_docs': get_first_anchor_destination(tds[6]),
    }
    # Save the scraped data
    scraperwiki.sqlite.save(unique_keys=['standard_number'], data=data)