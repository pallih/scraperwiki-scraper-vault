import scraperwiki    
import re
import mechanize
import datetime
from BeautifulSoup import BeautifulSoup

# by default, scrape incidents from today and yesterday
# (today will be incomplete until tomorrow)
START_DAYS_AGO = 0
NUM_DAYS = 6

starting_page = 'http://p2c.chpd.us/Summary_Disclaimer.aspx'
page_count_id = 'mainContent_lblPageCount'
date_from_id = 'MasterPage$mainContent$txtDateFrom2'
date_to_id = 'MasterPage$mainContent$txtDateTo2'
event_target_initial = 'MasterPage$mainContent$cmdSubmit2'
event_target_perpage = 'MasterPage$mainContent$gvSummary'

def parse_page_count(html):
    """
    Returns the total page count from the given HTML.
    """
    soup = BeautifulSoup(html)
    page_count = soup.find('span', attrs={'id': page_count_id})
    if not page_count:
        print html
        # Generally this means "no results" for the day, which can often happen for current day
        # Might want to check for that specifically at some point, but it works equally well to
        # just set page_count to 0 if we cannot find the page count span.
        page_count = 0
    else:
        page_count = ''.join(page_count.findAll(text=True))
        page_count = int(re.findall('Page \d+ of (\d+)', page_count)[0])
    return page_count


def parse_results(html):
    """
    Returns a list of dictionaries that describe the incidents in the given HTML.
    """
    soup = BeautifulSoup(html)
    get_text = lambda elem: ''.join([d.strip() for d in elem.findAll(text=True)])
    incidents = []
    for r in soup.findAll('tr', attrs={'class': 'EventSearchGridRow'}):
        _, date, inc_type, details_raw, location, _ = r.findAll('td')
        details = re.findall(r'<strong>(.+?):?</strong> ?(.+)', str(details_raw))
        details = dict((k.strip(), v.strip()) for k, v in details)
        case_num = details.pop('Case #', '')
        case_num = case_num and int(case_num) or None
        incident = {
            'date': datetime.datetime.strptime(get_text(date), '%m/%d/%Y %H:%M'),
            'incident_type': get_text(inc_type),
            'location': get_text(location),
            'case_num': case_num,
            'arrestee': details.pop('Arrestee', ''),
            'charge': details.pop('Charge', ''),
            'primary_offense': details.pop('Primary Offense', ''),
        }
        if details:
            raise ValueError("Didn't remove all details: %s" % details)
        incidents.append(incident)
    return incidents


def get_pages(day):
    """
    Returns the HTML of all pages of results for the given day.
    """
    br = mechanize.Browser()
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6')]
    # agree to the disclaimer
    br.open(starting_page)
    br.select_form(nr=0)
    r = br.submit()
    # initiate the search for the given day
    print 'Retrieving page 1'
    br.select_form(nr=0)    
    br.form.set_all_readonly(False)
    day = day.strftime('%m/%d/%Y')
    br[date_from_id] = day
    br[date_to_id] = day
    br['__EVENTTARGET'] = event_target_initial
    response = br.submit()
    pages = [response.read()]
    # parse the page count and retrieve subsequent pages
    for p in range(2, parse_page_count(pages[0]) + 1):
        print 'Retrieving page %s' % p
        br.select_form(nr=0)
        br.form.set_all_readonly(False)
        br['__EVENTTARGET'] = event_target_perpage
        br['__EVENTARGUMENT'] = 'Page$%s' % p
        # remove the "Search" (type=submit) input from the form, otherwise we get the first page of results over and over
        br.form.controls = [ctl for ctl in br.form.controls if not ctl.type.startswith("submit")]
        response = br.submit()
        pages.append(response.read())
    return pages

for x in range(START_DAYS_AGO, START_DAYS_AGO + NUM_DAYS):
    day = datetime.datetime.today() - datetime.timedelta(days=x)
    print 'Retrieving results for %s' % day.strftime('%Y-%m-%d')
    pages = get_pages(day)
    
    print 'Parsing %s pages of results' % len(pages)
    results = []
    for page in pages:
        results.extend(parse_results(page))
    
    print 'Found %s results, saving in scraperwiki' % len(results)
    scraperwiki.sqlite.save(['date', 'location'], results)