import scraperwiki
import re
import lxml.etree
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
from operator import isCallable, itemgetter
from pprint import pprint


'''
03/30/2012
Scraper for Fed Meeting Logs.
v2: Incorporates PDF Text Extraction.

04/03/2012, Drew Vogel
Parse attendees and summary text from PDF file.
'''

BASE = "http://www.federalreserve.gov"
#Dictionary of Category: url pairs:
FED_MEETINGS = {
    "Systemic Designations, Enhanced Prudential Standards, and Banking Supervision and Regulation": "/newsevents/reform_systemic.htm",
    "Derivatives Markets and Products": "/newsevents/reform_derivatives.htm",
    "Interchange Fees": "/newsevents/reform_interchange.htm",
    "Payments, Settlement and Clearing Activities and Utilities": "/newsevents/reform_payments.htm",
    "Consumer Financial Protection": "/newsevents/reform_consumer.htm",
    "Resolution Framework": "/newsevents/reform_resolution.htm"
}

def tokenize(elem):
    for d in elem.iterdescendants():
        yield (d.tag, d.text)
        yield ('#text', d.tail)

def extract_names(pdftext):
    parts = re.split(r'\((.*?)\)', pdftext)
    zipped = []
    if len(parts) == 1:
        org = None
        names = splitnames(parts[0])
        zipped.append((org, names))
    else:
        for names, org in zip(parts[::2], parts[1::2]):
            org = org.strip()
            names = splitnames(names)
            zipped.append((org, names))

    return zipped

def splitnames(names):
    names = re.split(r'(?:,|\band\b)', names)
    names = [x.strip(';').strip() for x in names]
    return [x for x in names if x]

class ParseError(Exception):
    def __init__(self, msg, *args, **kwargs):
        super(ParseError, self).__init__(msg, *args, **kwargs)

def find_section_marker(tokens):
    while True:
        try:
            (tag, text) = tokens.pop(0)
            if tag == 'b' and text.strip().endswith(':'):
                return text.strip().strip(':')
        except IndexError:
            raise ParseError('Unexpected end of input while searching for section marker')

def generate_text_tokens(tokens):
    while len(tokens) > 0 and tokens[0][0] in ('text', '#text'):
        token = tokens.pop(0)
        if token[1] is not None:
            yield token

def take_while_text(tokens):
    return list(generate_text_tokens(tokens))

def organization_from(section_name):
    words = section_name.strip().split(' ')
    if len(words) > 2:
        return ' '.join(words[:-1])

    return None

def bifurcate(pred, it):
    """Returns a 2-tuple containing the list of items in `it` for 
       which pred returns a non-emtpy value and a second list of
       all other items.
    """
    ts = []
    fs = []
    for x in it:
        if pred(x):
            ts.append(x)
        else:
            fs.append(x)
    return (ts, fs)

def grouped_by(it, key):
    assert isCallable(key)
    grouped = {}
    for x in it:
        k = key(x)
        grp = grouped.get(k, [])
        grp.append(x)
        grouped[k] = grp
    return grouped

OrgAdornmentPattern = re.compile(u'^(.*) \((.*)\)$', re.UNICODE)
def adorned_name(name):
    """Returns a tuple of the attendee's name and their organization name (if any) split out."""
    m = OrgAdornmentPattern.match(name)
    if m:
        return m.groups()
    else:
        return (name, None)

def parse(tokens):
    groups = []

    while len(tokens) > 0:
        marker_name = find_section_marker(tokens)
        section_tokens = take_while_text(tokens)
        section_content = ' '.join((text.strip() for (tag, text) in section_tokens))

        if marker_name == 'Summary':
            groups.append(('Summary', section_content))
            break
        else:
            # If the section seems to have an organization name in it then
            # we have to assume everyone in the section is from that organization
            # unless the name is immediately followed by an organization in parentheses
            organization = organization_from(marker_name)
            if organization:
                names = splitnames(section_content)
                unadorned_names = []
                adorned_names = []
                for name in names:
                    m = OrgAdornmentPattern.match(name)
                    if m:
                        adorned_names.append(m.groups())
                    else:
                        unadorned_names.append(name)

                groups.append((organization, unadorned_names))

                for (adornment, adorned_names1) in grouped_by(adorned_names, itemgetter(1)).iteritems():
                    organization = organization_from(adornment)
                    groups.append((organization or adornment, [n for (n, a) in adorned_names]))

            else:
                extracted_groups = extract_names(section_content)
                groups.extend(extracted_groups)

    return groups


def main():
    for category, url in FED_MEETINGS.iteritems():
        scrape_page(BASE+url, category)


def get_pdf_text(root):
    '''
    Recursively find all the text below the root node of an XML-parsed PDF.
    '''
    text = ""
    if root.text:
        text += " "  + root.text
    for element in root:
        text += get_pdf_text(element)
    return text

def scrape_pdf(url):
    '''
    Scrape data from PDF at URL.
    '''
    try:
        pdf_data = urlopen(url).read()
    except:
        return (None, None, None)

    pdf_xml = scraperwiki.pdftoxml(pdf_data)
    root = lxml.etree.fromstring(pdf_xml)
    page0 = root.find('page')
    try:
        content = dict(parse(list(tokenize(page0))))
    except ParseError:
        content = None
    full_text = get_pdf_text(root)
    return pdf_xml, full_text, content


def scrape_page(url, category):
    '''
    Scrapes a single page of the Fed meeting logs.
    url: the page url
    category: String for the category of all meetings on page.
    '''

    raw_page = scraperwiki.scrape(url)
    page_soup = BeautifulSoup(raw_page)
    table = page_soup.find('table', {"class":"earegulate"})
    
    #Find the table and get the enry for each row.
    all_entries = []
    all_rows = table.find_all("tr")

    attendees = []

    subcategory = ""

    for row in all_rows:
        new_entry = {}
        cols = row.find_all('td')
        if len(cols) != 3: 
            header = row.find('th')
            if "Attachment" not in header.get_text(): subcategory = header.get_text()
            continue
    
        new_entry['type'] = cols[2].get_text().strip()
        if new_entry['type'].lower() != 'meeting':
            continue

        new_entry['category'] = category
        new_entry['subcategory'] = subcategory

        new_entry['fullname'] = cols[0].get_text()
        new_entry['name'] = new_entry['fullname'].replace("(PDF)", "").replace("Meeting", "").strip()
        
        link = cols[0].find('a').get('href')
        if link[:4] != 'http':
            link = BASE + link
        new_entry['link'] = link
        pdf_xml, pdf_text, content = scrape_pdf(link)
        new_entry['pdftext'] = pdf_text
        new_entry['pdfxml'] = pdf_xml

        date_raw = cols[1].get_text().strip()
        try:
            date = datetime.strptime(date_raw, "%m/%d/%Y").date()
        except:
            date = datetime.strptime(date_raw.split('-')[0], "%m/%d/%Y").date()
            print new_entry['name'] + ": " + date_raw
        new_entry['date'] = date

    

        all_entries.append(new_entry)
        if content:
            new_entry['summary'] = content.get('Summary')
            for (section, names) in content.iteritems():
                if section != 'Summary':
                    for name in names:
                        attendees.append({'category': new_entry['category'],
                                          'name': new_entry['name'],
                                          'date': new_entry['date'],
                                          'attendee_name': name,
                                          'affiliation': section})
        else:
            new_entry['summary'] = None

    #Update database:
    scraperwiki.sqlite.save(['category', 'name', 'date'], all_entries, table_name="MeetingTable1")
    scraperwiki.sqlite.save(['category', 'name', 'date', 'attendee_name'], attendees, table_name="AttendeeTable1")

main()