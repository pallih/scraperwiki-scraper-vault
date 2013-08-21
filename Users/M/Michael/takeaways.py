import scraperwiki
import urlparse
import lxml.html

def scrape_table(root):
    rows = root.cssselect("div.search-result")
    for row in rows:
        record = {}
        td1 = row.cssselect("h3")
        td2 = row.cssselect("p.address")
        td3 = row.cssselect("p.tel")
        if td:
            record['Name'] = td1.text,
            record['Address'] = td2.text,
            record['Tel'] = td3.text
            print record
            scraperwiki.sqlite.save(["Tel"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.nextLink")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# Define starting url
base_url = 'http://www.localmole.co.uk'
starting_url = urlparse.urljoin(base_url, '/find-business/Birmingham/Takeaways/')
scrape_and_look_for_next_link(starting_url)