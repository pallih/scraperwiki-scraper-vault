import scraperwiki
import urlparse
import lxml.html
import re
  
urls = """

http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works
http://scholar.google.com/citations?user=HwXwfLkAAAAJ&hl=en

""".strip()

urls = urls.splitlines()
loop = True
for url in urls:
    # this will be use for next links in urlparse.urljoin
    base_url = url
    
    # initialize for the first loop iteration
    next_url = url
    while True:

        print "Scraping next academic", next_url 
        html = scraperwiki.scrape(next_url)
        root = lxml.html.fromstring(html)

        # within the table with class "cit-table"
        # select the rows after the first TR (tr+tr, i.e. tr preceeded by another tr)
        for tr in root.cssselect("table.cit-table tr + tr"):
            tds = tr.cssselect("td")
            #  for td in root.cssselect("td"):
            #      brs = td.cssselect("br")
            if len(tds)==4:
                data = {
                'Title' : tds[0].find("a").text_content(),
                'Authors' : tds[0].find('span[@class="cit-gray"]').text_content(),
                'Citations' : tds[1].text_content(),
                'Year' : tds[3].text_content(),
                }
                #print data
                scraperwiki.sqlite.save(unique_keys = ('Title', 'Year'), data= data)

        # --------------------
        # look for a next page
        # Next or Previous links are of class "cit-dark-link"
        # use XPath starts-with() to test link text
        # see for example http://stackoverflow.com/questions/147486/xpath-query-searching-for-an-element-with-specific-text
        # you may need starts-with(normalize-space(.), 'Test') is there is leading whitespace
        # in our case it's sufficient
        nextlinks = root.xpath('//a[@class="cit-dark-link" and starts-with(., "Next")]')
        if loop and nextlinks:
            next_url = urlparse.urljoin(base_url, nextlinks[0].get('href'))
        else:
            break
import scraperwiki
import urlparse
import lxml.html
import re
  
urls = """

http://scholar.google.com/citations?hl=en&user=D8lvl64AAAAJ&view_op=list_works
http://scholar.google.com/citations?user=HwXwfLkAAAAJ&hl=en

""".strip()

urls = urls.splitlines()
loop = True
for url in urls:
    # this will be use for next links in urlparse.urljoin
    base_url = url
    
    # initialize for the first loop iteration
    next_url = url
    while True:

        print "Scraping next academic", next_url 
        html = scraperwiki.scrape(next_url)
        root = lxml.html.fromstring(html)

        # within the table with class "cit-table"
        # select the rows after the first TR (tr+tr, i.e. tr preceeded by another tr)
        for tr in root.cssselect("table.cit-table tr + tr"):
            tds = tr.cssselect("td")
            #  for td in root.cssselect("td"):
            #      brs = td.cssselect("br")
            if len(tds)==4:
                data = {
                'Title' : tds[0].find("a").text_content(),
                'Authors' : tds[0].find('span[@class="cit-gray"]').text_content(),
                'Citations' : tds[1].text_content(),
                'Year' : tds[3].text_content(),
                }
                #print data
                scraperwiki.sqlite.save(unique_keys = ('Title', 'Year'), data= data)

        # --------------------
        # look for a next page
        # Next or Previous links are of class "cit-dark-link"
        # use XPath starts-with() to test link text
        # see for example http://stackoverflow.com/questions/147486/xpath-query-searching-for-an-element-with-specific-text
        # you may need starts-with(normalize-space(.), 'Test') is there is leading whitespace
        # in our case it's sufficient
        nextlinks = root.xpath('//a[@class="cit-dark-link" and starts-with(., "Next")]')
        if loop and nextlinks:
            next_url = urlparse.urljoin(base_url, nextlinks[0].get('href'))
        else:
            break
