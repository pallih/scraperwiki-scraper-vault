"""
Scrapes the website of the Federal Reserve for meetings related to the
implementation of Dodd-Frank. It outputs data in a format that is more
easily consumable for our Dodd-Frank Tracker[1]. The data provided here
is still pretty raw, but easily consumable by other tools.

[1] http://reporting.sunlightfoundation.com/doddfrank/
"""

import scraperwiki
import re
import lxml.etree
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
from operator import isCallable, itemgetter
from pprint import pprint


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


CompanySuffixPattern1 = re.compile(r', (LLC|LLP|MLP|Corp|Corporation|Inc)[.]?', re.IGNORECASE)
CompanySuffixPattern2 = re.compile(r'& Co(mpany|\.)?', re.IGNORECASE)
def fix_company_suffixes(s):
    t = CompanySuffixPattern1.sub(r' \1', s)
    u = CompanySuffixPattern2.sub(r'', t)
    return u


def taketokens(tokens, oftype=None):
    def gen():
        while len(tokens) > 0:
            (toktype, text) = tokens[0]
            if oftype is None:
                yield tokens.pop(0)
            elif oftype == toktype:
                yield tokens.pop(0)
            else:
                return
    return list(gen())

def tokenize(elem, url=''):
    def stage1(elem):
        """Yields text fragments, accounting for the .text/.tail etree quirk."""
        for d in elem.iterdescendants():
            for text in [d.text, d.tail]:
                if text is not None and len(text.strip()) > 0:
                    # This used to split text on semicolons (;). I don't even remember 
                    # why it did so, but it was causing 'Michael William' and 'Annette Nazareth'
                    # to be merged in this doc:
                    # http://www.federalreserve.gov/newsevents/files/creditsuisse_meeting__20101108b.pdf
                    yield text

    def stage2(tokens):
        """Finds section markers."""
        for text in tokens:
            colon_offset = text.find(':')
            if colon_offset == -1 or text[colon_offset:].startswith('://'):
                # Don't split on colons that are part of a URL scheme
                if text == 'Summary':
                    yield ('section_marker', text)
                else:
                    yield ('text', text)
            else:
                stripped = text.strip()
                if stripped.endswith('):'):
                    yield ('text', stripped[:-1])
                elif stripped.lower().endswith('footnote:'):
                    # Documents like this one have footnotes that mimic section markers:
                    # http://www.federalreserve.gov/newsevents/files/credit_suisse_meeting__20100920.pdf
                    yield ('text', text)
                else:
                    prefix = text[:colon_offset].strip()
                    rest = text[colon_offset+1:].strip()
                    if prefix:
                        yield ('section_marker', prefix)
                    if rest:
                        yield ('text', rest)

    def stage3(tokens):
        """Differentiates section content vs the prelude, accounting for special sections."""
        section_name = None
        for (toktype, text) in tokens:
            if toktype == 'text':
                if section_name is None:
                    yield ('prelude', text)
                elif section_name in ('Summary', 'Meeting Summary'):
                    yield ('summary_text', text)
                else:
                    # Some PDFs have URLs embedded in the list of names
                    # E.g. http://www.federalreserve.gov/newsevents/files/CAC_Meeting_20110615.pdf
                    text = URLPattern.sub('', text)
                    yield ('section_content', text)
            elif toktype == 'section_marker':
                section_name = text
                yield (toktype, text)
            else:
                yield (toktype, text)

    def participants_style(tokens):
        """
        While most PDFs use a participant list style like:
            first_name1 last_name1 (org_name1), first_name2 last_name2 (org_name2)
        Others use PDFs like this though:
            first_name1 last_name1, title1, org_name1
            first_name2 last_name2, title2, org_name2
        Examples of the latter style:
            http://www.federalreserve.gov/newsevents/files/CUNA_meeting_20110218.pdf
            http://www.federalreserve.gov/newsevents/files/TCH_meeting_20110204.pdf
        This one erroneously triggers the parsing logic for the latter style but returns
        proper results due to the technically empty Participants section:
            http://www.federalreserve.gov/newsevents/files/GE_Capital_meeting_20101217.pdf
        TODO: This PDF thwarts the current logic:
            http://www.federalreserve.gov/newsevents/files/commerce_meeting_102710.pdf
            http://www.federalreserve.gov/newsevents/files/shadow-financial-regulatory-committee-20120212.pdf
        HUH?:
            http://www.federalreserve.gov/newsevents/files/odfr-meeting-20111004.pdf           (See attached two Attendee Lists)
            http://www.federalreserve.gov/newsevents/files/SIFMA_Meeting_20110510.pdf          (See attached)
            http://www.federalreserve.gov/newsevents/files/OTC_industry_meeting_20110127.pdf   (See attached participant list)
            http://www.federalreserve.gov/newsevents/files/ODRF_meeting_20101102.pdf           (See attached three Attendee Lists)
        """
        section_name = ''
        has_participants_section = False
        participants_section_empty = True
        and_word_seen = False
        open_paren_seen = False
        closing_paren_seen = False
        for (toktype, text) in tokens:
            if toktype == 'section_marker':
                section_name = text
                if section_name == 'Participants':
                    has_participants_section = True
            elif toktype == 'section_content' and section_name == 'Participants':
                if participants_section_empty == True:
                    participants_section_empty = len(text.strip()) == 0
                if open_paren_seen == False:
                    open_paren_seen = '(' in text
                if closing_paren_seen == False:
                    closing_paren_seen = ')' in text
                if and_word_seen == False:
                    and_word_seen = re.search(r'\band\b', text) is not None
        return 'b' if (has_participants_section and not participants_section_empty and not open_paren_seen and not closing_paren_seen and not and_word_seen) else 'a'

    def stage4_a(tokens):
        """Collapses section content."""
        accum = []
        for (toktype, text) in tokens:
            if toktype == 'section_marker':
                joined = ' '.join(accum)
                accum = []
                yield ('section_content', joined)
                yield (toktype, text)
            elif toktype == 'section_content':
                accum.append(text.strip())
            else:
                yield (toktype, text)

    def stage4_b(tokens):
        """Collapses section content."""
        accum = []
        section_name = ''
        for (toktype, text) in tokens:
            if toktype == 'section_marker':
                section_name = text
                joined = ' '.join(accum)
                accum = []
                yield ('section_content', joined)
                yield (toktype, text)
            elif toktype == 'section_content' and section_name != 'Participants':
                accum.append(text.strip())
            else:
                yield (toktype, text)

    def stage5_a(tokens):
        """Identifies organization names that adorn names in the name sections."""
        for (toktype, text) in tokens:
            if toktype == 'section_content':
                if text:
                    names = splitnames(text)
                    for name in names:
                        (name, adornment) = extract_adornment(name)
                        if name:
                            yield ('name', name)
                        if adornment:
                            adornment = fix_company_suffixes(adornment)
                            if adornment:
                                yield ('adornment', adornment)

            else:
                yield (toktype, text)

    def stage5_b(tokens):
        """Identifies organization names that adorn names in the name sections."""
        for (toktype, text) in tokens:
            if toktype == 'section_content':
                if text:
                    parts = text.split(',')
                    yield ('name', parts[0].strip())
                    if len(parts) > 1:
                        adornment = fix_company_suffixes(parts[-1].strip())
                        if adornment:
                            yield ('adornment', adornment)

            else:
                yield (toktype, text)

    early_stage = list(stage3(stage2(stage1(elem))))
    if participants_style(early_stage) == 'a':
        return stage5_a(stage4_a(stage3(stage2(stage1(elem)))))
    else:
        print "Using parsing path B for {url}".format(url=url)
        return stage5_b(stage4_b(stage3(stage2(stage1(elem)))))


# The mr|mrs|ms gets swallowed as a split as a work-around for python 
# not supporting variable-width negative look-behinds.
# http://www.federalreserve.gov/newsevents/files/Meeting-between-Governor-Tarullo-and-Paul-Volcker-20111020.pdf
# This PDF requires the 'including' separator:
# http://www.federalreserve.gov/newsevents/files/CME_meeting_20100824.pdf
# 'PC' stands for professional corporation, seen here:
# http://www.federalreserve.gov/newsevents/files/financial-services-roundtable-meeting-20111120.pdf
NameSplitPattern = re.compile(r'(\([^)]*\(.*?\).*?\))|(\(.*?\))|[;]|(?:(?:mr|mrs|ms)\.)|(?<!\b[A-Z])\. |,(?! (?:I{1,3}\b|jr|sr|esq|inc|corp|llc|p\.?c\.?))|(?:, )?\b(?:and|including)\b', re.IGNORECASE)
def splitnames(names):
    names = NameSplitPattern.split(names)
    names = [n1 
             for n1 in 
             (n.strip() for n in names if n and n.strip())
             if n1 != '.'] # We want to keep trailing periods on abbreviations but not sentence enders.
    return names

class ParseError(Exception):
    def __init__(self, msg, *args, **kwargs):
        super(ParseError, self).__init__(msg, *args, **kwargs)


def find_section_marker(tokens):
    while True:
        try:
            token = tokens.pop(0)
            (toktype, text) = token
            if toktype == 'section_marker':
                return text
        except IndexError:
            raise ParseError('Unexpected end of input while searching for section marker')



OrgAdornmentSuffixPattern = re.compile(u'([^()]*? )?\((.*?)\)$', re.UNICODE)
def extract_adornment(text):
    m = OrgAdornmentSuffixPattern.match(text)
    if m is None:
        return (text, None)
    else:
        # Some documents quote the organization name. E.g.
        # http://www.federalreserve.gov/newsevents/files/NAREIT-meeting-120611.pdf
        return (m.group(1), m.group(2).strip('"').strip("'"))


def is_plural(text):
    lc_text = text.lower()
    if lc_text.endswith(' staff'):
        return True
    if lc_text.endswith(' board'):
        return True
    if lc_text.endswith('s') and not lc_text.endswith('ss'):
        return True
    return False


def parse(tokens, merge_sections=True):
    groups = []

    taketokens(tokens, oftype='prelude')

    while len(tokens) > 0:
        section_name = find_section_marker(tokens)
        if section_name == 'Summary':
            summary_text = ' '.join((text.strip() 
                                     for (toktype, text) in taketokens(tokens, 
                                                                       oftype='summary_text')))
            groups.append(('Summary', summary_text))
            break

        else:
            while True:
                names = [text for (toktype, text) in taketokens(tokens, oftype='name')]
                if len(names) == 0:
                    break
                adornments = taketokens(tokens, oftype='adornment')
                if len(adornments) == 0:
                    groups.append((section_name, names))
                elif len(adornments) >= 1:
                    (_, orgname) = adornments[-1]
                    if is_plural(orgname) or len(names) == 1 or section_name == 'Participants':
                        groups.append((orgname, names))
                    else:
                        if names:
                            groups.append((section_name, names[:-1]))
                        groups.append((orgname, [names[-1]]))

    if merge_sections == True:
        merged = defaultdict(list)
        for (section_name, section_content) in groups:
            if section_name == 'Summary':
                merged['Summary'] = section_content
            else:
                merged[section_name].extend(section_content)
        return merged.items()

    return groups



def main():
    for category, url in FED_MEETINGS.iteritems():
        print "Scraping category {0}".format(category)
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
        #pdf_data = urlopen(url).read()
        pdf_data = scraperwiki.scrape(url)
    except:
        return (None, None, None)

    pdf_xml = scraperwiki.pdftoxml(pdf_data)
    root = lxml.etree.fromstring(pdf_xml)
    page0 = root.find('page')
    try:
        content = dict(parse(list(tokenize(page0, url))))
    except ParseError:
        content = None
    full_text = get_pdf_text(root)
    return pdf_xml, full_text, content


SubCategoryPrefixPattern = re.compile(r'^[a-z]\. ')

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
            if "Attachment" not in header.get_text():
                subcategory = SubCategoryPrefixPattern.sub('', header.get_text().strip())
                print "Subcategory: {0!r} vs {1!r}".format(subcategory, header.get_text().strip())
            continue
    
        new_entry['type'] = cols[2].get_text().strip()
        if new_entry['type'].lower() not in ('meeting', 'communication', 'presentation'):
            continue

        new_entry['category'] = category
        new_entry['subcategory'] = subcategory

        new_entry['fullname'] = cols[0].get_text().strip()
        new_entry['name'] = (new_entry['fullname'].replace("(PDF)", "")
                                                  .replace("Meeting", "")
                                                  .strip())
        
        link = cols[0].find('a').get('href')
        if link[:4] != 'http':
            link = BASE + link
        new_entry['link'] = link
        pdf_xml, pdf_text, content = scrape_pdf(link)
        #new_entry['pdftext'] = pdf_text
        #new_entry['pdfxml'] = pdf_xml

        date_raw = cols[1].get_text().strip()
        try:
            date = datetime.strptime(date_raw, "%m/%d/%Y").date()
        except:
            date = datetime.strptime(date_raw.split('-')[0], "%m/%d/%Y").date()
            print new_entry['name'] + ": " + date_raw
        new_entry['date'] = date

    

        all_entries.append(new_entry)
        if content:
            # This PDF is erroneously skipped by this logic:
            # http://www.federalreserve.gov/newsevents/files/ALTA_Meeting_20113131.pdf
            summary = content.get('Summary')
            if summary is not None:
                new_entry['summary'] = summary
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
                print "Skipping participant extract for {type} on {date} because the first PDF page has no summary section ({link}).".format(**new_entry)
        else:
            new_entry['summary'] = None

    for meeting in all_entries:
        for (k, v) in meeting.iteritems():
            if isinstance(v, unicode):
                meeting[k] = v.replace(u'\xa0', ' ')


    #Update database:
    scraperwiki.sqlite.save(['category', 'name', 'date'], all_entries, table_name="MeetingTable1")
    scraperwiki.sqlite.save(['category', 'name', 'date', 'attendee_name'], attendees, table_name="AttendeeTable1")

URLPattern = re.compile(ur'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')

if __name__ == "scraper":
    main()


