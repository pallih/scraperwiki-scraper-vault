# Captures latest communicable and respiratory disease incidence data
# from Royal College of General Practitioners. This is the number of
# reported cases per 100,000 people.


# We can use the PDF previewer here: https://views.scraperwiki.com/run/pdf-to-html-preview-1
# This will show us what the content of an element is and also its positional attributes.
# We can use this information to grab particular information from the PDF.

from __future__ import division

import scraperwiki
import urllib2
import lxml.etree
import lxml.html

# All PDFs are listed here
source_data_listing_url = 'http://www.rcgp.org.uk/clinical_and_research/rsc/weekly_data.aspx'

# We want to get the URL which is in a known position within the document
# NB: It might look a bit crazy to grab it this way, but it avoids
# a problem detected whereby the word "Communicable" is misspelled by RCGP :/
source_data_listing = lxml.html.parse(source_data_listing_url).getroot()
source_data_listing.make_links_absolute()
all_hyperlinks = source_data_listing.cssselect('a')
pdf_url = all_hyperlinks[35].get('href')

# Scrape the PDF and convert it to XML
pdf_data = urllib2.urlopen(pdf_url).read()
pdf_xml = scraperwiki.pdftoxml(pdf_data)

doc = lxml.etree.fromstring(pdf_xml)
pages = list(doc)

# Let's grab the most recent statistics for the various diseases listed
# on the penultimate page of the report. We can see from the PDF previewer that the
# elements are regularly arranged. This makes it easy to get what we want based
# on element attributes.

target_page = pages[-2]
all_data = []
for element in list(target_page):
    if element.attrib and 'left' in element.attrib:
        if element.attrib['left'] == '117':
            disease = str(element.text).split('(')[0].strip()
        elif element.attrib['left'] == '425':
            rate= float(element.text)
            data = {
                'disease': disease,
                'rate': rate,
            }
            # Save the scraped data
            scraperwiki.sqlite.save(unique_keys=['disease'], data=data)