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

def docs_links_from_html(url, root):
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



def scrape_and_find_next_link(url, seen=1):
    """
    Scrape the current list of posts, and then find and scrape
    the next link.
    """
    data = scraperwiki.scrape(url)
    docs = json.loads(data)
    pages = docs['response']['pages']
    results = docs['response']['results']
    for content in results:
        if 'body' in content['fields']:
            post_title = content['webTitle']
            docs_links_from_html(content['webUrl'],lxml.html.fromstring(content['fields']['body']))
        
    next_url = url.replace('page='+str(seen), 'page='+str(seen+1))
    if seen < pages:
        scrape_and_find_next_link(next_url, seen+1)

def reprocess_all_spreadsheets():
    """
    For each spreadsheet in the database, update the information
    via the Google Spreadsheets API.
    """
    data = scraperwiki.sqlite.select("url from spreadsheets")
    for row in data:
        process_google_spreadsheet(row["url"])

# Find any new posts.
scrape_and_find_next_link("http://content.guardianapis.com/search?tag=news%2Fdatablog%2C-type%2Finteractive&show-redistributable-only=body&page-size=50&format=json&show-fields=body&page=1&api-key=yr9duagkxh97kqp4x5evq5c4")

# Check all spreadsheets for updates.
reprocess_all_spreadsheets()

