from itertools import count, imap
from lxml import html
from re import search
from scraperwiki import scrape
from scraperwiki.sqlite import save

def cleanup(text):
    return ' '.join(text.split()) #cleanup nbsp or some junk

class DistrictServices(object):
    BASE_URI = 'http://www.sanfrancisco.com/social-services/business-directory/san-francisco'
    PAGINATION_RE = '(\d+) to (\d+) of (\d+)'

    def __iter__(self):
        for page in imap(self.page, count(1)):
            page_links = list(page.cssselect("div#listingPagination > *"))
            #print page_links
            page_text = cleanup(page_links[len(page_links)-1].tail)
            #print page_text
            (start, end, total) = search(self.PAGINATION_RE, page_text).groups()

            for row in page.cssselect("table#list tr"):
                if len(row.cssselect("td.line")) or len(row.cssselect("td#adSenseFeatured")):
                    continue # Skipping adsense or spacing nonsense
                titlefree = row.cssselect("td.name > div.titlefree")[0]
                yield {
                    'district' : cleanup(row.cssselect("td.name > div.cat > a")[0].text_content()),
                    'link' : titlefree.cssselect("a")[0].attrib['href'],
                    'name' : cleanup(titlefree.cssselect("a")[0].text_content()),
                    'address' : cleanup(titlefree.tail[:-2]), # Pull off last two chars (space and left paren)
                    'phone' : cleanup(row.cssselect("td.phone")[0].text_content())
                }
            if int(end) == int(total): break

    def page(self, pn):
        return html.fromstring(scrape('/'.join([self.BASE_URI, str(pn)])))

for service in DistrictServices():
    #print service
    save(unique_keys=['link'], data=service)
from itertools import count, imap
from lxml import html
from re import search
from scraperwiki import scrape
from scraperwiki.sqlite import save

def cleanup(text):
    return ' '.join(text.split()) #cleanup nbsp or some junk

class DistrictServices(object):
    BASE_URI = 'http://www.sanfrancisco.com/social-services/business-directory/san-francisco'
    PAGINATION_RE = '(\d+) to (\d+) of (\d+)'

    def __iter__(self):
        for page in imap(self.page, count(1)):
            page_links = list(page.cssselect("div#listingPagination > *"))
            #print page_links
            page_text = cleanup(page_links[len(page_links)-1].tail)
            #print page_text
            (start, end, total) = search(self.PAGINATION_RE, page_text).groups()

            for row in page.cssselect("table#list tr"):
                if len(row.cssselect("td.line")) or len(row.cssselect("td#adSenseFeatured")):
                    continue # Skipping adsense or spacing nonsense
                titlefree = row.cssselect("td.name > div.titlefree")[0]
                yield {
                    'district' : cleanup(row.cssselect("td.name > div.cat > a")[0].text_content()),
                    'link' : titlefree.cssselect("a")[0].attrib['href'],
                    'name' : cleanup(titlefree.cssselect("a")[0].text_content()),
                    'address' : cleanup(titlefree.tail[:-2]), # Pull off last two chars (space and left paren)
                    'phone' : cleanup(row.cssselect("td.phone")[0].text_content())
                }
            if int(end) == int(total): break

    def page(self, pn):
        return html.fromstring(scrape('/'.join([self.BASE_URI, str(pn)])))

for service in DistrictServices():
    #print service
    save(unique_keys=['link'], data=service)
