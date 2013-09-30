import scraperwiki
import urlparse
import lxml.html

html = scraperwiki.scrape("http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml;jsessionid=0B3FF12869976A42558695404B30600D?page=4")
print html

root = lxml.html.fromstring(html)
for tr in root.cssselect("table.search_results tbody tr"):
    # Get the headers
    # hdrs = tr.cssselect("thead tr th")
    # Get the results
    res = tr.cssselect("td")
    data = {
        'Establishment name' : res[0].text,
        'Local Authority' : res[1].text,
        'Town' : res[2].text,
        'Establishment Status' : res[3].text,
        'Type of Establishment' : res[4].text,
        'Establishment Number' : res[6].text,
        'LA Number' : res[7].text,
        'UKPRN' : res[8].text,
        'Telephone number' : res[9].text,
        'Postcode' : res[10].text
    }
    print data

    ## Replace 'print data' with this to import to datastore
    # scraperwiki.sqlite.save(unique_keys=['name'], data=data)
import scraperwiki
import urlparse
import lxml.html

html = scraperwiki.scrape("http://www.education.gov.uk/edubase/public/quickSearchResult.xhtml;jsessionid=0B3FF12869976A42558695404B30600D?page=4")
print html

root = lxml.html.fromstring(html)
for tr in root.cssselect("table.search_results tbody tr"):
    # Get the headers
    # hdrs = tr.cssselect("thead tr th")
    # Get the results
    res = tr.cssselect("td")
    data = {
        'Establishment name' : res[0].text,
        'Local Authority' : res[1].text,
        'Town' : res[2].text,
        'Establishment Status' : res[3].text,
        'Type of Establishment' : res[4].text,
        'Establishment Number' : res[6].text,
        'LA Number' : res[7].text,
        'UKPRN' : res[8].text,
        'Telephone number' : res[9].text,
        'Postcode' : res[10].text
    }
    print data

    ## Replace 'print data' with this to import to datastore
    # scraperwiki.sqlite.save(unique_keys=['name'], data=data)
