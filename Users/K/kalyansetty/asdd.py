import scraperwiki
import httplib2,time,re
from BeautifulSoup import BeautifulSoup
#SCRAPING_CONN = httplib2.Http(".cache")
SCRAPING_DOMAIN_RE = re.compile("\w+:/*(?P<domain>[a-zA-Z0-9.]*)/")
SCRAPING_DOMAINS = {}
SCRAPING_CACHE_FOR = 60 * 15 # cache for 15 minutes
SCRAPING_REQUEST_STAGGER = 1100 # in milliseconds
SCRAPING_CACHE = {}

def fetch(url,method="GET"):
    key = (url,method)
    now = time.time()
    if SCRAPING_CACHE.has_key(key):
        data,cached_at = SCRAPING_CACHE[key]
        if now - cached_at < SCRAPING_CACHE_FOR:
            return data
    domain = SCRAPING_DOMAIN_RE.findall(url)[0]
    if SCRAPING_DOMAINS.has_key(domain):
        last_scraped = SCRAPING_DOMAINS[domain]
        elapsed = now - last_scraped
    if elapsed < SCRAPING_REQUEST_STAGGER:
        wait_period = (SCRAPING_REQUEST_STAGGER - elapsed) / 1000
        time.sleep(wait_period)
    SCRAPING_DOMAINS[domain] = time.time()
    data = SCRAPING_CONN.request(url,method)
    SCRAPING_CACHE[key] = (data,now)
    return data

def extract_story(s):
    d = {}
    d['link'] = s[0].findChildren()[0]['href']
    d['title'] = s[0].findChildren()[0].string
    d['score'] = s[1].findChildren()[0].string
    d['poster'] = s[1].findChildren()[1].string
    try:
        d['num_comments'] = int(s[1].findChildren()[2].string.split(" ")[0])
    except ValueError:
        d['num_comments'] = 0
    d['time'] = " ".join(s[1].contents[-2].strip().split(" ")[:2])
    return d

def fetch_stories():
    page = fetch("http://news.google.co.uk/news/section?pz=1&cf=all&ned=uk&topic=w&ict=ln","GET")
    soup = BeautifulSoup(page[1])
    titles = [x for x in soup.findAll('td','title') if x.findChildren()][:-1]
    subtexts = soup.findAll('td','subtext')
    stories = [extract_story(s) for s in zip(titles,subtexts)]
    return stories

while True:
    stories = fetch_stories()
    stories.sort(lambda a,b: cmp(a['num_comments'],b['num_comments']))
    stories.reverse()
    for s in stories:
        print u"[%s cmnts] %s (%s) by %s, %s ago." % (s['num_comments'],s['title'],s['link'],s['poster'],s['time'])
    print u"\n\n\n"
    time.sleep(60 * 5)
