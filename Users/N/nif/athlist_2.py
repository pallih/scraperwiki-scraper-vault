from string import ascii_lowercase
import urllib2
import scraperwiki
import lxml.html           
import urlparse


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'
    headers = {
        'User-Agent': user_agent,
        'Accept': '*/*',
    }
    request = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(request).read()

# scrape_athletes_list function: gets passed an individual page to scrape
def scrape_athletes_list(root):
    rows = root.cssselect("ul.athletesList li")  # selects all <li> blocks within <ul class="athletesList">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("span")
        if table_cells:
            record['Url'] = row.cssselect("div.athleteName a")[0].attrib.get('href')
            record['Name'] = row.cssselect("span.athletePassportName")[0].text
            record['Surname'] = row.cssselect("span.athletePassportSurname")[0].text
            record['Country'] = row.cssselect("div.country img")[0].attrib.get('alt')
            record['Noc'] = row.cssselect("span.noc")[0].text
            record['Sport'] = row.cssselect("div.disc a")[0].text

            # Finally, save the record to the datastore - 'Artist' is our unique key
            # scraperwiki.datastore.save(["Url"], record)
            scraperwiki.sqlite.save(unique_keys=["Url"], data=record)

base_url = "http://www.london2012.com"
def scrape_and_look_for_next_link(initial, page):
    url = urlparse.urljoin(base_url, '/athletes/initial=%s/index,page=%i.htmx' % (initial, page))
    print url
    html = get_html(url)
    root = lxml.html.fromstring(html)
    scrape_athletes_list(root)
    nores = root.cssselect("div.nores") # webmasters seem to have removed the link that was being selected by cssselect("div.nextLink a") before, so we have to brute force. :/
    if not nores:
        scrape_and_look_for_next_link(initial, page + 1)

for begin in ascii_lowercase:
    scrape_and_look_for_next_link(begin, 1)