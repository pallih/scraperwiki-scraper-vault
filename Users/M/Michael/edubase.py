import scraperwiki
import urlparse
import lxml.html

def scrape_table(root):
    rows = root.cssselect("table.search_results tbody tr")
    for row in rows:
        record = {}
        res = row.cssselect("td")
        if res:
            record['Name'] = res[0].text_content(),
            record['Local Authority'] = res[1].text_content(),
            record['Town'] = res[2].text_content(),
            record['Establishment Status'] = res[3].text_content(),
            record['Type of Establishment'] = res[4].text_content(),
            record['URN'] = res[5].text_content(),
            record['Establishment Number'] = res[6].text_content(),
            record['LA Number'] = res[7].text_content(),
            record['UKPRN'] = res[8].text_content(),
            record['Telephone number'] = res[9].text_content(),
            record['Postcode'] = res[10].text_content()
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["URN"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# Define starting url
base_url = 'http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml;jsessionid=0B3FF12869976A42558695404B30600D'
starting_url = urlparse.urljoin(base_url, '?page=1')
scrape_and_look_for_next_link(starting_url)import scraperwiki
import urlparse
import lxml.html

def scrape_table(root):
    rows = root.cssselect("table.search_results tbody tr")
    for row in rows:
        record = {}
        res = row.cssselect("td")
        if res:
            record['Name'] = res[0].text_content(),
            record['Local Authority'] = res[1].text_content(),
            record['Town'] = res[2].text_content(),
            record['Establishment Status'] = res[3].text_content(),
            record['Type of Establishment'] = res[4].text_content(),
            record['URN'] = res[5].text_content(),
            record['Establishment Number'] = res[6].text_content(),
            record['LA Number'] = res[7].text_content(),
            record['UKPRN'] = res[8].text_content(),
            record['Telephone number'] = res[9].text_content(),
            record['Postcode'] = res[10].text_content()
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["URN"], record)

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# Define starting url
base_url = 'http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml;jsessionid=0B3FF12869976A42558695404B30600D'
starting_url = urlparse.urljoin(base_url, '?page=1')
scrape_and_look_for_next_link(starting_url)