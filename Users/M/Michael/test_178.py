import scraperwiki
import urlparse
import lxml.html

def scrape_table(root):
    rows = root.cssselect("div.vcard")
    for row in rows:
        record = {}
        td = row.cssselect("span")
        if td:
            record['Name'] = td[0].text,
            record['Address'] = td[1].text,
            record['Post-code'] = td[5].text,
            record['Tel'] = td[7].text
            print record
            # I think post-code is always unique so I've used this as the key
            scraperwiki.sqlite.save(["Post-code"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    get_link = root.cssselect("#bottomPageNumbers a")
# Struggling to figure out how to select this html element. I think I need to iterate through the
# get_link tuple, see if any element matches 'Next' and, if so, assign it to next_link. But how?
    for i, v in enumerate(get_link):
        print i, v.text
        if v[i].text == 'Next':
            next_link = get_link[i] 
            print next_link
            if next_link:
                next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
                print next_url
                scrape_and_look_for_next_link(next_url)

# Define starting url
base_url = 'http://www.yell.com'
starting_url = urlparse.urljoin(base_url, '/ucs/UcsSearchAction.do?startAt=10&keywords=fast+food&location=birmingham&scrambleSeed=78966600&showOoa=10&ppcStartAt=0&pageNum=1')
scrape_and_look_for_next_link(starting_url)