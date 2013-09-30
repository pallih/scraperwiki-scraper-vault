from asynchat import fifo as FIFOQueue
from urllib2 import Request, urlopen, HTTPError
from time import sleep

from lxml import html
from scrapemark import scrape
from scraperwiki import sqlite

url = 'http://www.swiftcodesinfo.com/search-swift.php?country=%s' % 'AFGHANISTAN'

BASE_URL= 'http://www.swiftcodesinfo.com'
SWIFT_URL = 'http://www.swiftcodesinfo.com/swift-code/index.php'

COUNTRY_PATTERN = """{* <td style="width:20%"><a href='{{ [countries].link|abs }}' title="Swift Code of{{ [countries].name }}" class="s"></a></td> *}"""


SWIFT_CODE_PATTERN = """<th>Bank Name</th>
{*
<td>{{ [banks].name }}</td>
<td><b>{{ [banks].swift_code }}</b>
Swift code breakdown:<table>
<tr><td>{{ [banks].code_bank }}:</td><td>Bank code</td></tr>
<tr><td>{{ [banks].code_country }}:</td><td>Country Code</td></tr>
<tr><td>{{ [banks].code_location }}:</td><td>Location Code</td></tr>
<tr><td>{{ [banks].code_branch }}:</td><td>Branch Code</td></tr>
</table>
</td><td>{{ [banks].address|html }}</td>
*}
"""
PAGINATION_PATTERN= """{* <a href="/swift-code/search-swift-complete.php?{{ [] }}"></a>*}"""

HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Encoding': '',
 'Accept-Language': 'en-US,en;q=0.8',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Host': 'www.swiftcodesinfo.com',
 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.32 (KHTML, like Gecko) Ubuntu/10.10 Chromium/13.0.751.0 Chrome/13.0.751.0 Safari/534.32'}
DONE = set([completed['url'] for completed in sqlite.select('url FROM _done')])

Q = FIFOQueue()

def GET(url, headers=HEADERS, attempts_made=0):
    req = Request(url, headers=HEADERS)
    attempts_made = attempts_made
    try:
        sleep(5 * attempts_made)
        res = urlopen(req)
    except HTTPError as e:
        if attempts_made < 6:
            res = GET(url=url, headers=headers, attempts_made=attempts_made+1)
        else:
            raise
    return res.read()

def cleanup_address(address):
    """
    >>> cleanup_address('NEW YORK BRANCH                    , 520 MADISON AVENUE, 25TH FLOOR     ,<br>NEW YORK<br>UNITED STATES'
    """
    return '\n'.join([portion.replace('<br>', '\n') for portion in [a.strip() for a in address.split(',')]])


def get_country_html(url, attempts=0):
    res = GET(url)
    if 'Query execution was interrupted' in res:
        if attemps < 5:
            res = get_country_html(url, attempts=attempts+1)
        else:
            res = ''
    return res

def parse_swift_code_page(url, country_name, queue=Q):
    if url in DONE:
        return None
    print 'downloading', country_name 
    raw=get_country_html(url)
        
    banks = scrape(SWIFT_CODE_PATTERN, html=raw)['banks']
    for bank in banks:
        bank['address'] = cleanup_address(bank['address'])
        bank['country_name'] = country_name
        bank['source'] = url
    sqlite.save(['swift_code'], data=banks, table_name='swift_codes')
    
    if 'page=' not in url:
        try:
            n_pages = max(int(link.split('=')[-1]) for link in scrape(PAGINATION_PATTERN, html=raw))
            pages = [BASE_URL + '/swift-code/search-swift-complete.php?country=%s&page=%d' % (country_name.replace(' ', '%20'), n)  for n in xrange(n_pages)]
        except ValueError: #no more pages
            pages = []
        for newurl in pages:
            queue.push((parse_swift_code_page, newurl, country_name))
    DONE.add(url)
    sqlite.save(['url'], table_name='_done', data=dict(url=url))

def swift_codes(queue=Q):
    print 'Getting countries'
    raw = GET(SWIFT_URL)
    print raw
    countries = scrape(COUNTRY_PATTERN, html=raw, headers=HEADERS)['countries']
    print countries
    for country in countries:
        print country
        country['link'] = BASE_URL + country['link']
        queue.push((parse_swift_code_page, country['link'], country['name']))

def main(queue=Q):
    swift_codes()
    while not queue.is_empty():
        job = queue.pop()
        if job[0]:
            print job[1]
            apply(job[1][0], job[1][1:])
main()
from asynchat import fifo as FIFOQueue
from urllib2 import Request, urlopen, HTTPError
from time import sleep

from lxml import html
from scrapemark import scrape
from scraperwiki import sqlite

url = 'http://www.swiftcodesinfo.com/search-swift.php?country=%s' % 'AFGHANISTAN'

BASE_URL= 'http://www.swiftcodesinfo.com'
SWIFT_URL = 'http://www.swiftcodesinfo.com/swift-code/index.php'

COUNTRY_PATTERN = """{* <td style="width:20%"><a href='{{ [countries].link|abs }}' title="Swift Code of{{ [countries].name }}" class="s"></a></td> *}"""


SWIFT_CODE_PATTERN = """<th>Bank Name</th>
{*
<td>{{ [banks].name }}</td>
<td><b>{{ [banks].swift_code }}</b>
Swift code breakdown:<table>
<tr><td>{{ [banks].code_bank }}:</td><td>Bank code</td></tr>
<tr><td>{{ [banks].code_country }}:</td><td>Country Code</td></tr>
<tr><td>{{ [banks].code_location }}:</td><td>Location Code</td></tr>
<tr><td>{{ [banks].code_branch }}:</td><td>Branch Code</td></tr>
</table>
</td><td>{{ [banks].address|html }}</td>
*}
"""
PAGINATION_PATTERN= """{* <a href="/swift-code/search-swift-complete.php?{{ [] }}"></a>*}"""

HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Encoding': '',
 'Accept-Language': 'en-US,en;q=0.8',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Host': 'www.swiftcodesinfo.com',
 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.32 (KHTML, like Gecko) Ubuntu/10.10 Chromium/13.0.751.0 Chrome/13.0.751.0 Safari/534.32'}
DONE = set([completed['url'] for completed in sqlite.select('url FROM _done')])

Q = FIFOQueue()

def GET(url, headers=HEADERS, attempts_made=0):
    req = Request(url, headers=HEADERS)
    attempts_made = attempts_made
    try:
        sleep(5 * attempts_made)
        res = urlopen(req)
    except HTTPError as e:
        if attempts_made < 6:
            res = GET(url=url, headers=headers, attempts_made=attempts_made+1)
        else:
            raise
    return res.read()

def cleanup_address(address):
    """
    >>> cleanup_address('NEW YORK BRANCH                    , 520 MADISON AVENUE, 25TH FLOOR     ,<br>NEW YORK<br>UNITED STATES'
    """
    return '\n'.join([portion.replace('<br>', '\n') for portion in [a.strip() for a in address.split(',')]])


def get_country_html(url, attempts=0):
    res = GET(url)
    if 'Query execution was interrupted' in res:
        if attemps < 5:
            res = get_country_html(url, attempts=attempts+1)
        else:
            res = ''
    return res

def parse_swift_code_page(url, country_name, queue=Q):
    if url in DONE:
        return None
    print 'downloading', country_name 
    raw=get_country_html(url)
        
    banks = scrape(SWIFT_CODE_PATTERN, html=raw)['banks']
    for bank in banks:
        bank['address'] = cleanup_address(bank['address'])
        bank['country_name'] = country_name
        bank['source'] = url
    sqlite.save(['swift_code'], data=banks, table_name='swift_codes')
    
    if 'page=' not in url:
        try:
            n_pages = max(int(link.split('=')[-1]) for link in scrape(PAGINATION_PATTERN, html=raw))
            pages = [BASE_URL + '/swift-code/search-swift-complete.php?country=%s&page=%d' % (country_name.replace(' ', '%20'), n)  for n in xrange(n_pages)]
        except ValueError: #no more pages
            pages = []
        for newurl in pages:
            queue.push((parse_swift_code_page, newurl, country_name))
    DONE.add(url)
    sqlite.save(['url'], table_name='_done', data=dict(url=url))

def swift_codes(queue=Q):
    print 'Getting countries'
    raw = GET(SWIFT_URL)
    print raw
    countries = scrape(COUNTRY_PATTERN, html=raw, headers=HEADERS)['countries']
    print countries
    for country in countries:
        print country
        country['link'] = BASE_URL + country['link']
        queue.push((parse_swift_code_page, country['link'], country['name']))

def main(queue=Q):
    swift_codes()
    while not queue.is_empty():
        job = queue.pop()
        if job[0]:
            print job[1]
            apply(job[1][0], job[1][1:])
main()
