import scraperwiki
import lxml.html
import re
import urllib
import pprint

# Reads list of bills from
# http://mn.gov/governor/resources/legislation/

root_url = 'http://mn.gov/governor/resources/legislation/'

# Attach topic/category scraper
scraperwiki.sqlite.attach('mn-topic-bill-counts', 'topics')
topic_query = "topic FROM topics.swdata WHERE bills_upper LIKE '%%%s%%' OR bills_upper LIKE '%%%s%%' OR bills_lower LIKE '%%%s%%' OR bills_lower LIKE '%%%s%%'"


# Get list of pages to scrape
def get_next(root):
    found = False

    for a in root.cssselect('#content_leftblock_nav_705 a'):
        if a.text_content() == 'Next':
            found = root_url + a.attrib['href']

    return found


# Get votes
def get_votes(data):
    vote_action_re = re.compile('(passed)(.*)(vote)(.*[^0-9])([0-9]+\-[0-9]+)', re.I | re.M | re.S)
    url = 'https://www.revisor.mn.gov/bills/bill.php?b=' + urllib.quote_plus(data['chamber']) + '&f=' + urllib.quote_plus(data['bill']) + '&ssn=0&y=2013'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    # House votes
    for tr in root.cssselect('.house table.actions tr'):
        if vote_action_re.search(tr[1].text_content()):
            data['house_vote'] = vote_action_re.search(tr[1].text_content()).groups()[4]

    # Senate votes
    for tr in root.cssselect('.senate table.actions tr'):
        if vote_action_re.search(tr[1].text_content()):
            data['senate_vote'] = vote_action_re.search(tr[1].text_content()).groups()[4]

    scraperwiki.sqlite.save(unique_keys=['bill'], data=data)


# Columns:
# Chapter    House File    Senate File    Description    Presented    Signed    Vetoed    Filed w/o Signature
def scrape_governor_page(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    next_found = get_next(root)

    for tr in root.cssselect('table.table_legislation tbody tr'):
        # Look for house or senate
        if tr[1].text_content():
            bill = 'HF ' + tr[1].text_content()
            chamber = 'house'
        else:
            bill = 'SF ' + tr[2].text_content()
            chamber = 'senate'

        # For some reason, data is missing or wrong
        if tr[0].text_content().strip() == '18' and tr[4].text_content().strip() == '4/19/13':
            bill = 'HF 75'
            chamber = 'house'
        if bill == 'HF 340':
            bill = 'SF 340'
            chamber = 'senate'
        bill = bill.rstrip('AaBbCcDdEeFf')

        # Check if veto has link
        veto_link = ''
        for a in tr[6].cssselect('a'):
            veto_link = root_url + a.attrib['href']

        # Get categories
        output_topics = []
        topics = scraperwiki.sqlite.select(topic_query % (bill, bill.replace(' ', ''), bill, bill.replace(' ', '')))
        for t in topics:
            output_topics.append(t['topic'])

        print('||'.join(output_topics))
            
        data = {
            'chapter': tr[0].text_content().strip(),
            'chamber': chamber,
            'bill': bill,
            'description': tr[3].text_content().strip(),
            'presented': tr[4].text_content().strip(),
            'signed': bool(tr[5].text_content().strip() != '-' or not tr[6].text_content().strip()),
            'vetoed': bool(tr[6].text_content().strip() != '-' or not tr[6].text_content().strip()),
            'signed_no_signature': bool(tr[7].text_content().strip() != '-' or not tr[7].text_content().strip()),
            'veto_link': veto_link,
            'topics': '||'.join(output_topics)
        }

        get_votes(data)

    return next_found
        

current = root_url
while (current):
    print 'Scraping: ' + current
    current = scrape_governor_page(current)
import scraperwiki
import lxml.html
import re
import urllib
import pprint

# Reads list of bills from
# http://mn.gov/governor/resources/legislation/

root_url = 'http://mn.gov/governor/resources/legislation/'

# Attach topic/category scraper
scraperwiki.sqlite.attach('mn-topic-bill-counts', 'topics')
topic_query = "topic FROM topics.swdata WHERE bills_upper LIKE '%%%s%%' OR bills_upper LIKE '%%%s%%' OR bills_lower LIKE '%%%s%%' OR bills_lower LIKE '%%%s%%'"


# Get list of pages to scrape
def get_next(root):
    found = False

    for a in root.cssselect('#content_leftblock_nav_705 a'):
        if a.text_content() == 'Next':
            found = root_url + a.attrib['href']

    return found


# Get votes
def get_votes(data):
    vote_action_re = re.compile('(passed)(.*)(vote)(.*[^0-9])([0-9]+\-[0-9]+)', re.I | re.M | re.S)
    url = 'https://www.revisor.mn.gov/bills/bill.php?b=' + urllib.quote_plus(data['chamber']) + '&f=' + urllib.quote_plus(data['bill']) + '&ssn=0&y=2013'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    # House votes
    for tr in root.cssselect('.house table.actions tr'):
        if vote_action_re.search(tr[1].text_content()):
            data['house_vote'] = vote_action_re.search(tr[1].text_content()).groups()[4]

    # Senate votes
    for tr in root.cssselect('.senate table.actions tr'):
        if vote_action_re.search(tr[1].text_content()):
            data['senate_vote'] = vote_action_re.search(tr[1].text_content()).groups()[4]

    scraperwiki.sqlite.save(unique_keys=['bill'], data=data)


# Columns:
# Chapter    House File    Senate File    Description    Presented    Signed    Vetoed    Filed w/o Signature
def scrape_governor_page(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    next_found = get_next(root)

    for tr in root.cssselect('table.table_legislation tbody tr'):
        # Look for house or senate
        if tr[1].text_content():
            bill = 'HF ' + tr[1].text_content()
            chamber = 'house'
        else:
            bill = 'SF ' + tr[2].text_content()
            chamber = 'senate'

        # For some reason, data is missing or wrong
        if tr[0].text_content().strip() == '18' and tr[4].text_content().strip() == '4/19/13':
            bill = 'HF 75'
            chamber = 'house'
        if bill == 'HF 340':
            bill = 'SF 340'
            chamber = 'senate'
        bill = bill.rstrip('AaBbCcDdEeFf')

        # Check if veto has link
        veto_link = ''
        for a in tr[6].cssselect('a'):
            veto_link = root_url + a.attrib['href']

        # Get categories
        output_topics = []
        topics = scraperwiki.sqlite.select(topic_query % (bill, bill.replace(' ', ''), bill, bill.replace(' ', '')))
        for t in topics:
            output_topics.append(t['topic'])

        print('||'.join(output_topics))
            
        data = {
            'chapter': tr[0].text_content().strip(),
            'chamber': chamber,
            'bill': bill,
            'description': tr[3].text_content().strip(),
            'presented': tr[4].text_content().strip(),
            'signed': bool(tr[5].text_content().strip() != '-' or not tr[6].text_content().strip()),
            'vetoed': bool(tr[6].text_content().strip() != '-' or not tr[6].text_content().strip()),
            'signed_no_signature': bool(tr[7].text_content().strip() != '-' or not tr[7].text_content().strip()),
            'veto_link': veto_link,
            'topics': '||'.join(output_topics)
        }

        get_votes(data)

    return next_found
        

current = root_url
while (current):
    print 'Scraping: ' + current
    current = scrape_governor_page(current)
