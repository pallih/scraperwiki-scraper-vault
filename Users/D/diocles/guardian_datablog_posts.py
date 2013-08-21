import scraperwiki
import lxml.html
import json
from urlparse import urlparse, parse_qs

def process_google_spreadsheet(url):
    """
    Given a link to a Google Spreadsheet, parse the key, look up
    the title and last modified date, and store these in a table.
    """
    parsed = urlparse(url)
    key_list = parse_qs(parsed.query).get("key")
    if key_list == None:
        return None

    key = key_list[0]

    json_url = "https://spreadsheets.google.com/feeds/worksheets/" + key + "/public/basic?alt=json"
    try:
        data = scraperwiki.scrape(json_url)
        spreadsheet = json.loads(data)
        title = spreadsheet["feed"]["title"]["$t"]
        date  = spreadsheet["feed"]["updated"]["$t"]
    except:
        title = ""
        date = ""

    standard_url = "http://spreadsheets.google.com/ccc?key=" + key

    record = {
        "url": standard_url,
        "key": key,
        "title": title,
        "updated": date,
    }

    scraperwiki.sqlite.save(unique_keys=["key"], data=record, table_name="spreadsheets")

    return key

def scrape_post(url, title):
    """
    Given the URL and title of a particular post, scrape
    the publication date and any mentioned spreadsheets.
    """
    # Never re-scrape posts.
    try:
        present = []
        present = scraperwiki.sqlite.select("1 from posts where url = ?", url)
    except:
        pass
    else:
        if present:
            return 1

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    pubdate = ""
    times = root.cssselect("time")
    for time in times:
        if time.attrib.get("pubdate") != None:
            pubdate = time.attrib.get("datetime")
            break

    # FIXME This won't be perfect.
    spreadsheet = ""
    links = root.cssselect("a")
    for link in links:
        link_url = link.attrib.get("href")
        if link_url == None:
            continue

        if link_url.find("spreadsheets.google.com") >= 0:
            key = process_google_spreadsheet(link_url)
            if key == None:
                continue

            scraperwiki.sqlite.save(unique_keys=["post_url", "spreadsheet_key"],
                                    data={"post_url": url, "spreadsheet_key": key},
                                    table_name="p_s")

    record = {
        "pubdate": pubdate,
        "url": url,
        "title": title,
    }

    scraperwiki.sqlite.save(unique_keys=["url"], data=record, table_name="posts")
    return 0

def scrape_and_find_next_link(url):
    """
    Scrape the current list of posts, and then find and scrape
    the next link.
    """
    seen = 0
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    posts = root.cssselect("#blog-posts-excerpts h3 a")
    for post in posts:
        post_title = post.text_content()
        post_url = post.attrib.get("href")
        seen += scrape_post(post_url, post_title)

    # Return without traversing the next links if we've reached posts we've seen.
    if seen:
        return

    next_link = root.cssselect(".pagination .last a")
    if next_link:
        next_url = next_link[0].attrib.get("href")
        scrape_and_find_next_link(next_url)

def reprocess_all_spreadsheets():
    """
    For each spreadsheet in the database, update the information
    via the Google Spreadsheets API.
    """
    data = scraperwiki.sqlite.select("url from spreadsheets")
    for row in data:
        process_google_spreadsheet(row["url"])

# Find any new posts.
scrape_and_find_next_link("http://www.guardian.co.uk/news/datablog")

# Check all spreadsheets for updates.
reprocess_all_spreadsheets()

