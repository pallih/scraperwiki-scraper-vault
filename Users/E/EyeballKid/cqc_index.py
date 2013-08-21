# scrape the UK Care Quality Commision registered services directory.
# They are replacing this with a new care services directory at:
# http://caredirectory.cqc.org.uk/caredirectory/searchthecaredirectory.cfm
# Not sure if the new directory will have all the same information or not,
# so grabbing this set while we can...

import scraperwiki
import lxml.html
import re
import urlparse

from pprint import pprint
import csv

# search starting page:
# http://www.cqc.org.uk/registeredservicesdirectory/rsquicksearch.asp


def walk_pages():
    # there are 1806 pages
    page_num = 1

    while 1:
        page_url = 'http://www.cqc.org.uk/registeredservicesdirectory/rssearchresults.asp?Action=SearchByPostNew&cPage=' + str(page_num) + '&TurnPage=Y&seltype=CRH&seltypename=Care%20homes&ServiceName=&servCats=1,2,3&userCats=&CareType=&Regions=&SelRegion=&SelArea=&Postcode=&Distance=5%20&StarRatings=%20&NR=0&Suspended=0&Capacity=&CapacityOver=&OwnershipTypeCode=&sort=&SearchKey='

        print "fetch page %d %s" % (page_num,page_url)
        html = scraperwiki.scrape(page_url)
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(page_url)

        scan_results_page(doc)

        # look for "Next page" links
        if not doc.cssselect('a.next'):
            break
        page_num += 1



# eg "Tel: 01732838876 - total capacity 5 places"
tel_places_pat = re.compile(r'Tel:\s*(.*?)\s*-\s*total\s+capacity\s+(\d+)\s+places', re.DOTALL|re.UNICODE|re.IGNORECASE )

provider_type_pat = re.compile(r'Provider\s+type:\s*(.*?)\s*$',re.UNICODE|re.IGNORECASE|re.DOTALL)

# extract id from url
id_pat = re.compile(r'\bid=(\d+)',re.IGNORECASE)

def scan_results_page(doc):
    """ scan a page of search results and store care home entries in db """

    def tidy(s):
        """ replace non-breaking spaces and trim whitespace """
        s = s.replace(u'\u00a0',u' ')
        s = s.strip()
        return s

    results = doc.cssselect('div.content .yellowrows, div.content .whiterows')
    for entry in results:
        row = {}
        p = entry.cssselect('p')



        # p[0] is rating
        # "Good" "Excellent" etc...
        readable_rating = tidy(unicode(p[0].text_content()))
        if 'not yet rated' in readable_rating.lower():
            row['rating'] = None
        else:
            star_icon = p[0].xpath('.//img/@src')[0]
            m = re.compile('/(\d)stars.gif$').search(star_icon)
            row['rating'] = int(m.group(1))


        # name and link to details on cqc site
        a = p[1].find('a')
        row['name'] = tidy(unicode(a.text_content()))
        row['cqc_url'] = a.get('href')

        # address
        row['address'] = tidy(unicode(p[2].text_content()))

        # "Tel: 01732838876 - total capacity 5 places"
        foo = unicode(p[3].text_content())
        m = tel_places_pat.search(foo)
        row['tel'] = m.group(1)
        row['places'] = int(m.group(2))

        # "Care home only ( dementia + mental health, excluding learning disability or dementia + old age, not falling within any other category )"
        row['care_type'] = tidy(unicode(p[4].text_content()))

        m = provider_type_pat.match(p[5].text_content())
        row['provider_type'] = unicode(m.group(1)).lower()

        # grab unique (hopefully!) id from url
        row['id'] = int(id_pat.search(row['cqc_url']).group(1))

#        pprint(row)
        scraperwiki.sqlite.save(unique_keys=["id"], data=row)

def main():
    walk_pages()


main()



