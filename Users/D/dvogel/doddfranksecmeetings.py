import re
import sys
import hashlib
from pprint import pprint

import lxml.html
import requests
from dateutil.parser import parse as dateparse

try:
    import scraperwiki
except ImportError:
    pass


BaseUrl = 'http://sec.gov'


def get_homepage():
    url = 'http://sec.gov/spotlight/regreformcomments.shtml'
    return requests.get(url).content


def get_comment_urls(page):
    return [BaseUrl + x for x in re.findall(r'<a href="(.*?)">are available', page)]


def scrape():
    page = get_homepage()
    comment_urls = get_comment_urls(page)

    meetings = []

    for url in comment_urls:
        for data in parse_comment_page(url):
            meetings.append(data)

    return meetings


def get_category(page):
    try:
        category = lxml.html.fromstring(page).cssselect('h1')[0].text_content().split('\n')[1].strip()
    except IndexError:
        try:
            category = lxml.html.fromstring(page).cssselect('h1')[0].text_content().split(':')[1].strip()
        except IndexError:
            category = re.search(r'Comments on (.*)$', lxml.html.fromstring(page).cssselect('h1')[0].text_content()).groups()[0]
    return category


def parse_comment_page(url):
    page = requests.get(url).content
    category = get_category(page)
    meeting_section = re.search(r'<a name="meetings" id="meetings">.*', page, re.S)
    if not meeting_section:
        return

    doc = lxml.html.fromstring(meeting_section.group())
    rows = doc.cssselect('tr')
    for row in rows:
        cells = row.cssselect('td')
        try:
            date = dateparse(cells[0].text_content())
        except ValueError:
            continue

        meeting = cells[1].cssselect('a')[0]
        pdf_url = BaseUrl +  meeting.attrib['href']
        meeting_title = meeting.text_content()
        meeting = parse_meeting_description(meeting_title)
        if meeting is None:
            continue
        meeting.update({'url': pdf_url,
                        'pdf_url': pdf_url,
                        'meeting_time': date.isoformat(),
                        'category': category, })
        yield meeting


def parse_meeting_description(text):
    regex = re.compile(r'''^Memorandum from (?:the )?(?P<from>.*?)(?:[Rr]egarding|re:) (?:an? )?(?P<meeting_time>(?:January|February|March|April|May|June|July|August|September|October|November|December) \d\d?, \d{4})?,? ?(?P<type>.+)(?:with )(?:representatives (?:of|from) )?(?P<remainder>.*)''')
    m = regex.search(text)
    if not m:
        print "Skipping meeting because the description could not be parsed: {0}".format(text)
        return None
    data = m.groupdict()
    data['description'] = text
    #data['visitors'] = re.sub(r'(r|R)epresentatives? (of|from) ', '', data['attendees'])
    data['organizations'] = parse_attendees(data['remainder'])
    return data


def parse_attendees(descr):
    company_suffixes = re.compile(r", (Inc|LLC|LLP)[.]?")
    separators = re.compile(r",(?: (?:and )?the)? ", re.IGNORECASE)
    return separators.split(company_suffixes.sub(r" \1", descr))


def dict_hash(d, hashfunc=hashlib.md5):
    if isinstance(d, dict) == False:
        import ipdb; ipdb.set_trace()

    d_hash = hashfunc()
    for (k, v) in sorted(d.items()):
        d_hash.update(k.encode('utf-8', 'replace'))
        if v:
            d_hash.update(v.encode('utf-8', 'replace'))
    return d_hash.hexdigest()


class DictSlicer(object):
    def __init__(self, *ks):
        self.ks = ks

    def __call__(self, d):
        return dict(((k, v) for (k, v) in d.iteritems() if k in self.ks))


def save_meetings(meetings):
    # The same meetings are listed on multiple pages. The important info comes 
    # the description so we just make a dict keyed by the description.
    slicer = DictSlicer('category', 'meeting_time', 'from', 'url', 'pdf_url', 'type')
    meetings_index = dict(((dict_hash(slicer(m)), m) for m in meetings))
    meetings = meetings_index.values()

    all_keys = ['category',
                'description',
                'from',
                'meeting_time',
                'pdf_url',
                'type',
                'url',
                'visitors']
    meeting_records = []
    organization_records = []
    for m in meetings:
        r = dict.fromkeys(all_keys, '')
        for key in all_keys:
            r[key] = m.get(key, '')
        meeting_records.append(r)

        for org_name in m['organizations']:
            if not org_name:
                print org_name
                sys.exit(1)
            organization_records.append({
                'category': m['category'],
                'meeting_time': m['meeting_time'],
                'from': m['from'],
                'url': m['url'],
                'pdf_url': m['pdf_url'],
                'type': m['type'],
                'org_name': org_name
            })

    scraperwiki.sqlite.save(table_name='meetings',
                            unique_keys=['category',
                                         'meeting_time',
                                         'from',
                                         'url',
                                         'pdf_url',
                                         'type'],
                            data=meeting_records)

    scraperwiki.sqlite.save(table_name='organizations',
                            unique_keys=['category',
                                         'meeting_time',
                                         'from',
                                         'url',
                                         'pdf_url',
                                         'type',
                                         'org_name'],
                            data=organization_records)


if __name__ == '__main__':
    meetings = scrape()
    save_meetings(meetings)
    pprint(meetings, indent=4, width=8, stream=sys.stdout)

if __name__ == 'scraper':
    meetings = scrape()
    save_meetings(meetings)

