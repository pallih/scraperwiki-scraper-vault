from datetime import datetime, timedelta
import scraperwiki
import requests
import lxml.html
from lxml.cssselect import CSSSelector as CSS
import dateutil.parser
import dateutil.tz


TARGET = "http://vultus.stblogs.org/archives.html"
HEADERS = {
    'User-agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
}
ROW_KEY = ['year', 'month', 'slug']
ROW_SCHEMA = ROW_KEY + ['title', 'text', 'author', 'date', 'tags']
EDIT_WINDOW = timedelta(days=10)

sel_item = CSS("div.archive-individual li")
sel_anchor = CSS("a")
sel_asset = CSS("#alpha-inner")
sel_author = CSS("div.asset-header span.byline address.author a")
sel_date = CSS("div.asset-header span.byline abbr.published")
sel_text = CSS("div.asset-content")
sel_tags = CSS("div.asset-footer li.entry-category a")

def scrape(url):
    return lxml.html.fromstring(requests.get(url, headers=HEADERS).text)

def Row(**kwargs):
    row = dict((field, None) for field in ROW_SCHEMA)
    row.update(kwargs)
    return row

store = scraperwiki.sqlite.save
parsedate = dateutil.parser.parse
tzlocal = dateutil.tz.tzlocal

# If the scraper has run once successfully, subsequent runs should
# only scrape new pages and pages that are less than ten days old (to
# allow for edits by the author)
historic_latest = scraperwiki.sqlite.get_var('latest')
if historic_latest:
    historic_latest = parsedate(historic_latest)
    print("Begin scraping archive ten days prior to: %s" % historic_latest.strftime("%Y.%m.%d"))

latest = datetime(year=2000, month=12, day=31, tzinfo=tzlocal())
latest_timestamp = None

# the scraping loop below swallows errors, but the error may have been
# due to a request timeout or similar, so we want to retry those pages
# that don't exist in the database
try:
    archive = set(
        (d['year'], d['month'], d['slug']) for d in scraperwiki.sqlite.select("year, month, slug FROM pages")
    )
except:
    archive = set([])
print "PAGE COUNT: %s" % len(archive)

# begin scrape - first the archive index page to get all individual page urls
index = scrape(TARGET)

# go through the list of page links and scrape each one
for li in sel_item(index):
    date = li.text.rstrip().rstrip(':').strip()
    a = sel_anchor(li)[0]
    href = a.get('href')
    if href:
        year, month, day = map(int, date.split('.'))
        slug = href.split('/')[5].partition('.')[0]
        if (year, month, slug) in archive and historic_latest:
            # don't re-scrape anything outside the ten day edit window
            if datetime(year=year, month=month, day=day, tzinfo=tzlocal()) < historic_latest-EDIT_WINDOW:
                # you could break here because the list is date-ordered
                continue
        print("%s - %s - %s" % (date, slug, href))
        page = scrape(href)
        try:
            content = sel_asset(page)[0]
            timestamp = sel_date(content)[0].get('title')
            date = parsedate(timestamp)
            if date > latest:
                # there's a new 'latest' timestamp - saved as a variable below
                latest = date
                latest_timestamp = timestamp
            row = Row(year=year, month=month, title=a.text_content(), slug=slug)
            row['date'] = date
            row['author'] = sel_author(content)[0].text_content()
            row['tags'] = ','.join(a.text_content() for a in sel_tags(content))
            row['text'] = lxml.html.tostring(sel_text(content)[0])
        except Exception, e:
            print("Skipping " + href)
            print("    ERROR: %s" % e)
            continue
        #print row
        store(unique_keys=ROW_KEY, data=row, table_name="pages")

if latest_timestamp:
    scraperwiki.sqlite.save_var('latest', latest_timestamp)



