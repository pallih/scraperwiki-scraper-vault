"""
This script is intended to be run on ScraperWiki. Follow these directions
to get a local development version of the scraperwiki package:

http://www.christophermanning.org/writing/save-scraperwiki-data-to-local-sqlite-database/
"""

import requests
import re
import hashlib
import logging
import lxml.html
import scraperwiki


def scrape():
    meetings = scrape_page_listing()
    save_meetings(meetings)


def slurp(url, params={}, method='GET'):
    response = requests.request(method, url, data=params)
    assert response.status_code == 200, 'Unable to retrieve {0}, method {1}, status {2}'.format(url, method, response.status_code)
    return lxml.html.fromstring(response.content)


def scrape_page_listing():
    listing_url = 'http://www.treasury.gov/initiatives/wsr/Pages/transparency.aspx'
    doc = slurp(listing_url)
    doc.make_links_absolute(listing_url)

    link_text_pattern = re.compile(r'Disclosure of Dodd-Frank Implementation Meetings \((?P<month_name>[A-Za-z]+) (?P<year>20\d\d)\)')

    page_links = [(match.group('month_name'), 
                   match.group('year'), 
                   a.attrib['href'])
                   for (a, match) in
                   ((a, link_text_pattern.match(a.text.strip()))
                    for a in doc.cssselect('a') 
                    if a.text is not None)
                   if match]

    meetings = []
    for (month_name, year, href) in page_links:
        doc = slurp(href)
        month_meetings = scrape_month_page(month_name, year, href, doc)
        if month_meetings:
            meetings.extend(month_meetings)

    return meetings


def save_meetings(meetings):
    meeting_records = []
    attendee_records = []

    for meeting in meetings:
        """
        The scraperwiki and sqlite storage model is far more efficient if you
        let it write all of the data in one call. It can fail if there's too
        much data, but this scraper is unlikely to hit those limits.
        """
        attendee_hash = hashlib.md5()
        for official in meeting['Officials']:
            attendee_hash.update(official['name'].encode('utf-8'))
        for visitor in meeting['Visitors']:
            attendee_hash.update(visitor['name'].encode('utf-8'))

        meeting_records.append({
            'MonthName': meeting['MonthName'],
            'Year': meeting['Year'],
            'Url': meeting['Url'],
            'Date': meeting['Date'],
            'Topics': meeting['Topics'],
            'AttendeeHash': attendee_hash.hexdigest()
        })

        for official in meeting['Officials']:
            attendee_records.append({
                'MonthName': meeting['MonthName'],
                'Year': meeting['Year'],
                'Date': meeting['Date'],
                'Topics': meeting['Topics'],
                'AttendeeHash': attendee_hash.hexdigest(),
                'Attendee': official['name'],
                'Org': official['org']
            })
            

        for visitor in meeting['Visitors']:
            attendee_records.append({
                'MonthName': meeting['MonthName'],
                'Year': meeting['Year'],
                'Date': meeting['Date'],
                'Topics': meeting['Topics'],
                'AttendeeHash': attendee_hash.hexdigest(),
                'Attendee': visitor['name'],
                'Org': visitor['org']
            })


    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['MonthName',
                                         'Year',
                                         'Date',
                                         'Topics',
                                         'AttendeeHash'],
                            data=meeting_records)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['MonthName',
                                         'Year',
                                         'Date',
                                         'Topics',
                                         'AttendeeHash',
                                         'Attendee',
                                         'Org'],
                            data=attendee_records)


def scrape_month_page(month_name, year, href, doc):
    print "Scraping {0}, {1}: {2}".format(month_name, year, href)

    asp_ctls_tables = [tbl for tbl in doc.cssselect('table')
                       if 'xmlns:ddwrt2' in tbl.attrib]
    assert len(asp_ctls_tables) in (1, 2), 'Unable to find table listing meetings for {0} {1} in {2}.'.format(month_name, year, href)

    
    if len(asp_ctls_tables) > 1:
        next_images = asp_ctls_tables[1].cssselect('img[src="/_layouts/1033/images/next.gif"]')
        prev_images = asp_ctls_tables[1].cssselect('img[src="/_layouts/1033/images/prev.gif"]')
        assert len(next_images) > 0 or len(prev_images) > 0, 'Meeting list page has a second ASP.NET control table but it doesn\'t contain a previous or next button. The page layout has probably changed.'


        if len(next_images) > 0:
            next_anchor = next_images[0].getparent()
            assert next_anchor.tag == 'a', 'Unable to find next page link.'
            next_onclick = next_anchor.attrib.get('onclick')
            next_href = next_anchor.attrib.get('href')
            assert next_onclick or next_href, 'No onclick or href attribute found on the next page link.'
        else:
            next_anchor = None
            next_onclick = None
            next_href = None


    rows = HtmlTableIterator(asp_ctls_tables[0])

    meetings = []
    for row in MeetingRowIterator(rows):
        (cell, text) = row['Treasury Official']
        officials = [{'name': name, 'org': 'Treasury'} 
                      for name in scrape_names(cell)]

        (cell, text) = row['Visitor and Affiliation']
        visitors = [parse_name_and_org(name)
                    for name in scrape_names(cell)]

        meetings.append({
            'MonthName': month_name,
            'Year': year,
            'Url': href,
            'Date': row['Date'][1],
            'Topics': row['Topics'][1].strip(),
            'Officials': officials,
            'Visitors': visitors
        })
    print "Found {0} meetings.".format(len(meetings))

    if len(asp_ctls_tables) > 1 and len(next_images) > 0:
        if next_onclick:
            next_meetings = mimic_onclick(month_name, year, next_onclick)
        elif next_href:
            next_meetings = mimic_page_refresh(month_name, year, href, doc, next_href)
        else:
            next_meetings = []

        meetings.extend(next_meetings)

    return meetings


def mimic_onclick(month_name, year, next_onclick):
    """
    Some pages use a RefreshPageTo JS function that updates the
    window.location property. This mimics that behavior by
    pulling the URL out of the JS function parameter.
    """
    next_url = ('http://www.treasury.gov' 
                + re.compile(r'.*"([^"]+)".*').match(next_onclick).group(1).replace('\\u0026', '&'))
    meetings = scrape_month_page(month_name, year, next_url, slurp(next_url))
    assert len(meetings) > 0, 'There was a second page of meetings for {0}, {1} but no meetings were found on that page.'.format(month_name, year)
    return meetings


def mimic_page_refresh(month_name, year, href, doc, next_href):
    """
    Some pages use a __doPostBack JS function that submits a form
    with specific form parameters. This branch mimics that form
    be pulling the JS function parameters out of the callback
    invocation.
    """
    match = re.compile(r'javascript: __doPostBack\("(.*?)","(.*?)"\)').match(next_href)
    assert match is not None, 'Unable to parse parameters from cal to __doPostBack'
    digest_value = [e.value
                    for e in doc.iterdescendants()
                    if hasattr(e, 'name')
                    and e.name == '__REQUESTDIGEST'][0]
    params = {
        '__EVENTTARGET': match.group(1),
        '__EVENTARGUMENT': match.group(2),
        '__REQUESTDIGEST': digest_value
    }
    doc = slurp(href, params, method='POST')
    meetings = scrape_month_page(month_name, year, href, doc)
    assert len(meetings) > 0, 'There was a second page of meetings for {0}, {1} but no meetings were found on that page.'.format(month_name, year)
    return meetings


def parse_name_and_org(name):
    name = re.compile(r', (Jr|Sr|I{2,3})', re.IGNORECASE).sub(r' \1', name)
    name = re.compile(r', (LLC|LLP|MLP|Corp|Corporation|Inc)[.]?', re.IGNORECASE).sub(r' \1', name)
    name = re.compile(r'& Co(mpany|\.)?', re.IGNORECASE).sub(r'', name)

    if ',' in name:
        """If there is a comma, it's trivial"""
        (name, org) = name.split(',', 1)
        return {
            'name': name.strip(),
            'org': org.strip()
        }
    else:
        """
        If there is no comma then the name is either the
        first two words or the first three in the case that
        the second ends with a period or is only 1 letter.
        """

        def without_periods(s):
            return re.compile(r'\.').sub('', s)

        words = name.strip().split(' ')
        if words[1].endswith('.') or len(without_periods(words[1])) == 1:
            return {
                'name': ' '.join(words[:3]),
                'org': ' '.join(words[3:])
            }
        else:
            return {
                'name': ' '.join(words[:2]),
                'org': ' '.join(words[2:])
            }


def scrape_names(cell):
    def gen_names():
        for elem in cell.iterdescendants():
            if elem.text:
                text = elem.text.strip()
                if text:
                    yield text
            if elem.tail:
                tail = elem.tail.strip()
                if tail:
                    yield tail

    return list(gen_names())


class MeetingRowIterator(object):
    """
    Iterates over a sequence of objects representing
    meetings. It filters out rows used for formatting
    by checking for required column names, correcting
    known errors.
    """

    def __init__(self, rows):
        self.rows = enumerate(iter(rows))

    def __iter__(self):
        return self

    def next(self):
        for (idx, row) in self.rows:

            """
            Some months list the Date field as DateType.
            """
            if 'Date' not in row and 'DateType' in row:
                row['Date'] = row['DateType']
                del row['DateType']


            """
            Formatting rows should have missing values for at
            least one of the required fields.
            """
            required_fields = ('Date', 
                               'Topics', 
                               'Treasury Official', 
                               'Visitor and Affiliation')
            missing_fields = [fld
                              for fld in required_fields
                              if row.get(fld) is None]
            if len(missing_fields) > 0:
                logging.debug('Row {0} lacks a value for these fields: {1}.'.format(idx, ', '.join(missing_fields)))
                continue

            return row
        raise StopIteration


class HtmlTableIterator(object):
    """
    Takes a lxml.html table element. It iterates over the
    rows in the table returning objects with keys that correspond
    to the text in header elements.
    """

    def __init__(self, dom):
        self.dom = dom
        self.rows = iter(dom.cssselect('tr'))
        self.headers = None

    def __iter__(self):
        return self

    def _set_headers(self, ths):
        self.headers = [th.text_content().strip() for th in ths]
        logging.debug('Headers found: {0}'.format(self.headers))

    def next(self):
        row = self.rows.next()

        ths = row.cssselect('th')
        if len(ths) > 0:
            self._set_headers(ths)
            return self.next()

        cells = row.cssselect('td')
        if not cells:
            return self.next()

        if not self.headers:
            return [(cell, cell.text_content().strip()) 
                    for cell in row.cssselect('td')]

        obj = dict(((hdr, None) for hdr in self.headers))
        obj.update(((self.headers[idx], (cell, cell.text_content()))
                    for (idx, cell) in enumerate(cells)))
        return obj


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    logging.basicConfig(level=logging.DEBUG)
    scrape_page_listing()

if __name__ == "scraper":
    scrape()
"""
This script is intended to be run on ScraperWiki. Follow these directions
to get a local development version of the scraperwiki package:

http://www.christophermanning.org/writing/save-scraperwiki-data-to-local-sqlite-database/
"""

import requests
import re
import hashlib
import logging
import lxml.html
import scraperwiki


def scrape():
    meetings = scrape_page_listing()
    save_meetings(meetings)


def slurp(url, params={}, method='GET'):
    response = requests.request(method, url, data=params)
    assert response.status_code == 200, 'Unable to retrieve {0}, method {1}, status {2}'.format(url, method, response.status_code)
    return lxml.html.fromstring(response.content)


def scrape_page_listing():
    listing_url = 'http://www.treasury.gov/initiatives/wsr/Pages/transparency.aspx'
    doc = slurp(listing_url)
    doc.make_links_absolute(listing_url)

    link_text_pattern = re.compile(r'Disclosure of Dodd-Frank Implementation Meetings \((?P<month_name>[A-Za-z]+) (?P<year>20\d\d)\)')

    page_links = [(match.group('month_name'), 
                   match.group('year'), 
                   a.attrib['href'])
                   for (a, match) in
                   ((a, link_text_pattern.match(a.text.strip()))
                    for a in doc.cssselect('a') 
                    if a.text is not None)
                   if match]

    meetings = []
    for (month_name, year, href) in page_links:
        doc = slurp(href)
        month_meetings = scrape_month_page(month_name, year, href, doc)
        if month_meetings:
            meetings.extend(month_meetings)

    return meetings


def save_meetings(meetings):
    meeting_records = []
    attendee_records = []

    for meeting in meetings:
        """
        The scraperwiki and sqlite storage model is far more efficient if you
        let it write all of the data in one call. It can fail if there's too
        much data, but this scraper is unlikely to hit those limits.
        """
        attendee_hash = hashlib.md5()
        for official in meeting['Officials']:
            attendee_hash.update(official['name'].encode('utf-8'))
        for visitor in meeting['Visitors']:
            attendee_hash.update(visitor['name'].encode('utf-8'))

        meeting_records.append({
            'MonthName': meeting['MonthName'],
            'Year': meeting['Year'],
            'Url': meeting['Url'],
            'Date': meeting['Date'],
            'Topics': meeting['Topics'],
            'AttendeeHash': attendee_hash.hexdigest()
        })

        for official in meeting['Officials']:
            attendee_records.append({
                'MonthName': meeting['MonthName'],
                'Year': meeting['Year'],
                'Date': meeting['Date'],
                'Topics': meeting['Topics'],
                'AttendeeHash': attendee_hash.hexdigest(),
                'Attendee': official['name'],
                'Org': official['org']
            })
            

        for visitor in meeting['Visitors']:
            attendee_records.append({
                'MonthName': meeting['MonthName'],
                'Year': meeting['Year'],
                'Date': meeting['Date'],
                'Topics': meeting['Topics'],
                'AttendeeHash': attendee_hash.hexdigest(),
                'Attendee': visitor['name'],
                'Org': visitor['org']
            })


    scraperwiki.sqlite.save(table_name="meetings",
                            unique_keys=['MonthName',
                                         'Year',
                                         'Date',
                                         'Topics',
                                         'AttendeeHash'],
                            data=meeting_records)

    scraperwiki.sqlite.save(table_name="attendees",
                            unique_keys=['MonthName',
                                         'Year',
                                         'Date',
                                         'Topics',
                                         'AttendeeHash',
                                         'Attendee',
                                         'Org'],
                            data=attendee_records)


def scrape_month_page(month_name, year, href, doc):
    print "Scraping {0}, {1}: {2}".format(month_name, year, href)

    asp_ctls_tables = [tbl for tbl in doc.cssselect('table')
                       if 'xmlns:ddwrt2' in tbl.attrib]
    assert len(asp_ctls_tables) in (1, 2), 'Unable to find table listing meetings for {0} {1} in {2}.'.format(month_name, year, href)

    
    if len(asp_ctls_tables) > 1:
        next_images = asp_ctls_tables[1].cssselect('img[src="/_layouts/1033/images/next.gif"]')
        prev_images = asp_ctls_tables[1].cssselect('img[src="/_layouts/1033/images/prev.gif"]')
        assert len(next_images) > 0 or len(prev_images) > 0, 'Meeting list page has a second ASP.NET control table but it doesn\'t contain a previous or next button. The page layout has probably changed.'


        if len(next_images) > 0:
            next_anchor = next_images[0].getparent()
            assert next_anchor.tag == 'a', 'Unable to find next page link.'
            next_onclick = next_anchor.attrib.get('onclick')
            next_href = next_anchor.attrib.get('href')
            assert next_onclick or next_href, 'No onclick or href attribute found on the next page link.'
        else:
            next_anchor = None
            next_onclick = None
            next_href = None


    rows = HtmlTableIterator(asp_ctls_tables[0])

    meetings = []
    for row in MeetingRowIterator(rows):
        (cell, text) = row['Treasury Official']
        officials = [{'name': name, 'org': 'Treasury'} 
                      for name in scrape_names(cell)]

        (cell, text) = row['Visitor and Affiliation']
        visitors = [parse_name_and_org(name)
                    for name in scrape_names(cell)]

        meetings.append({
            'MonthName': month_name,
            'Year': year,
            'Url': href,
            'Date': row['Date'][1],
            'Topics': row['Topics'][1].strip(),
            'Officials': officials,
            'Visitors': visitors
        })
    print "Found {0} meetings.".format(len(meetings))

    if len(asp_ctls_tables) > 1 and len(next_images) > 0:
        if next_onclick:
            next_meetings = mimic_onclick(month_name, year, next_onclick)
        elif next_href:
            next_meetings = mimic_page_refresh(month_name, year, href, doc, next_href)
        else:
            next_meetings = []

        meetings.extend(next_meetings)

    return meetings


def mimic_onclick(month_name, year, next_onclick):
    """
    Some pages use a RefreshPageTo JS function that updates the
    window.location property. This mimics that behavior by
    pulling the URL out of the JS function parameter.
    """
    next_url = ('http://www.treasury.gov' 
                + re.compile(r'.*"([^"]+)".*').match(next_onclick).group(1).replace('\\u0026', '&'))
    meetings = scrape_month_page(month_name, year, next_url, slurp(next_url))
    assert len(meetings) > 0, 'There was a second page of meetings for {0}, {1} but no meetings were found on that page.'.format(month_name, year)
    return meetings


def mimic_page_refresh(month_name, year, href, doc, next_href):
    """
    Some pages use a __doPostBack JS function that submits a form
    with specific form parameters. This branch mimics that form
    be pulling the JS function parameters out of the callback
    invocation.
    """
    match = re.compile(r'javascript: __doPostBack\("(.*?)","(.*?)"\)').match(next_href)
    assert match is not None, 'Unable to parse parameters from cal to __doPostBack'
    digest_value = [e.value
                    for e in doc.iterdescendants()
                    if hasattr(e, 'name')
                    and e.name == '__REQUESTDIGEST'][0]
    params = {
        '__EVENTTARGET': match.group(1),
        '__EVENTARGUMENT': match.group(2),
        '__REQUESTDIGEST': digest_value
    }
    doc = slurp(href, params, method='POST')
    meetings = scrape_month_page(month_name, year, href, doc)
    assert len(meetings) > 0, 'There was a second page of meetings for {0}, {1} but no meetings were found on that page.'.format(month_name, year)
    return meetings


def parse_name_and_org(name):
    name = re.compile(r', (Jr|Sr|I{2,3})', re.IGNORECASE).sub(r' \1', name)
    name = re.compile(r', (LLC|LLP|MLP|Corp|Corporation|Inc)[.]?', re.IGNORECASE).sub(r' \1', name)
    name = re.compile(r'& Co(mpany|\.)?', re.IGNORECASE).sub(r'', name)

    if ',' in name:
        """If there is a comma, it's trivial"""
        (name, org) = name.split(',', 1)
        return {
            'name': name.strip(),
            'org': org.strip()
        }
    else:
        """
        If there is no comma then the name is either the
        first two words or the first three in the case that
        the second ends with a period or is only 1 letter.
        """

        def without_periods(s):
            return re.compile(r'\.').sub('', s)

        words = name.strip().split(' ')
        if words[1].endswith('.') or len(without_periods(words[1])) == 1:
            return {
                'name': ' '.join(words[:3]),
                'org': ' '.join(words[3:])
            }
        else:
            return {
                'name': ' '.join(words[:2]),
                'org': ' '.join(words[2:])
            }


def scrape_names(cell):
    def gen_names():
        for elem in cell.iterdescendants():
            if elem.text:
                text = elem.text.strip()
                if text:
                    yield text
            if elem.tail:
                tail = elem.tail.strip()
                if tail:
                    yield tail

    return list(gen_names())


class MeetingRowIterator(object):
    """
    Iterates over a sequence of objects representing
    meetings. It filters out rows used for formatting
    by checking for required column names, correcting
    known errors.
    """

    def __init__(self, rows):
        self.rows = enumerate(iter(rows))

    def __iter__(self):
        return self

    def next(self):
        for (idx, row) in self.rows:

            """
            Some months list the Date field as DateType.
            """
            if 'Date' not in row and 'DateType' in row:
                row['Date'] = row['DateType']
                del row['DateType']


            """
            Formatting rows should have missing values for at
            least one of the required fields.
            """
            required_fields = ('Date', 
                               'Topics', 
                               'Treasury Official', 
                               'Visitor and Affiliation')
            missing_fields = [fld
                              for fld in required_fields
                              if row.get(fld) is None]
            if len(missing_fields) > 0:
                logging.debug('Row {0} lacks a value for these fields: {1}.'.format(idx, ', '.join(missing_fields)))
                continue

            return row
        raise StopIteration


class HtmlTableIterator(object):
    """
    Takes a lxml.html table element. It iterates over the
    rows in the table returning objects with keys that correspond
    to the text in header elements.
    """

    def __init__(self, dom):
        self.dom = dom
        self.rows = iter(dom.cssselect('tr'))
        self.headers = None

    def __iter__(self):
        return self

    def _set_headers(self, ths):
        self.headers = [th.text_content().strip() for th in ths]
        logging.debug('Headers found: {0}'.format(self.headers))

    def next(self):
        row = self.rows.next()

        ths = row.cssselect('th')
        if len(ths) > 0:
            self._set_headers(ths)
            return self.next()

        cells = row.cssselect('td')
        if not cells:
            return self.next()

        if not self.headers:
            return [(cell, cell.text_content().strip()) 
                    for cell in row.cssselect('td')]

        obj = dict(((hdr, None) for hdr in self.headers))
        obj.update(((self.headers[idx], (cell, cell.text_content()))
                    for (idx, cell) in enumerate(cells)))
        return obj


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    logging.basicConfig(level=logging.DEBUG)
    scrape_page_listing()

if __name__ == "scraper":
    scrape()
