import scraperwiki
import lxml.html

# scrape pet policy from best western hotels

def parse_content(root):
    counter = 0
    for elem in root.cssselect("td:contains('Pet Policy:')"):
        counter += 1
        tag = elem.cssselect('strong')[0]
        if (tag.text_content() == 'Pet Policy:'):
            content = elem.text_content()
            print content[content.find('Pet Policy:') + 12:].strip()
    print counter

def get_url (url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    parse_content(root)

url = 'http://book.bestwestern.com/bestwestern/CA/QC/Quebec-City-hotels/BEST-WESTERN-PLUS-City-Centre-Centre-Ville/Hotel-Overview.do?propertyCode=67020'
url = 'http://book.bestwestern.com/bestwestern/US/OK/Bartlesville-hotels/BEST-WESTERN-Bartlesville-Inn/Hotel-Overview.do?propertyCode=37101'

get_url(url)

