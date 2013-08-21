import scraperwiki
import urlparse
import lxml.html

for i in range(1288,12000):
    try:
        url = "http://www.hewlett.org/grants/%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        tds = root.cssselect("td") #this is the tag that highlights where on the webpage we want to get the data from
        header = root.cssselect("h3")
        data = {
        'project_name' : header[0].text_content(), #this isn't right
        'amount' : tds[1].text_content(),
        'date_of_award' : tds[3].text_content(),
        'term_of_grant' : tds[5].text_content(),
        'program' : tds[7].text_content(),
        'region' : tds[9].text_content(),
        'grant_description' : tds[11].text_content(),
        'grantee_website' :  tds[13].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['project_name'], data=data)

    except:
        print i


