import scraperwiki
import urlparse
import lxml.html

for i in range(1,1200): #USER: update range as necessary
    try:
        url = "http://www.badea.org/operation-details.htm?ProjectId=%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        spans = root.cssselect("td span")

        data = {
            'operation_id' : spans[10].text_content(), 
            'operation_name' : spans[12].text_content(),
            'operation_description' : spans[14].text_content(),
            'sector' : spans[16].text_content(),
            'amount' : spans[18].text_content()
        }

        scraperwiki.sqlite.save(unique_keys=['operation_id'], data=data)

    except:
       print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
import scraperwiki
import urlparse
import lxml.html

for i in range(1,1200): #USER: update range as necessary
    try:
        url = "http://www.badea.org/operation-details.htm?ProjectId=%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        spans = root.cssselect("td span")

        data = {
            'operation_id' : spans[10].text_content(), 
            'operation_name' : spans[12].text_content(),
            'operation_description' : spans[14].text_content(),
            'sector' : spans[16].text_content(),
            'amount' : spans[18].text_content()
        }

        scraperwiki.sqlite.save(unique_keys=['operation_id'], data=data)

    except:
       print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
