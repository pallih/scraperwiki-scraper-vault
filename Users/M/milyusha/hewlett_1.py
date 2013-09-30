import scraperwiki
import urlparse
import lxml.html

for i in range(1288,13000): #USER: update range as necessary
    try:
        url = "http://www.hewlett.org/grants/%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        header=root.cssselect("h3") #this gets the project name
        tds = root.cssselect("td") #this is the tag that highlights where on the webpage we want to get the data from, it gets the rest of the data besides the project name
        data2 = {
            'project_name' : header[0].text_content(), 
            'amount' : tds[1].text_content(),
            'date_of_award' : tds[3].text_content(),
            'term_of_grant' : tds[5].text_content(),
            'program' : tds[7].text_content(),
            'region' : tds[9].text_content(),
            'grant_description' : tds[11].text_content(),
            'grantee_website' :  tds[13].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['project_name'], data=data2)


    except:
       print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
import scraperwiki
import urlparse
import lxml.html

for i in range(1288,13000): #USER: update range as necessary
    try:
        url = "http://www.hewlett.org/grants/%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        header=root.cssselect("h3") #this gets the project name
        tds = root.cssselect("td") #this is the tag that highlights where on the webpage we want to get the data from, it gets the rest of the data besides the project name
        data2 = {
            'project_name' : header[0].text_content(), 
            'amount' : tds[1].text_content(),
            'date_of_award' : tds[3].text_content(),
            'term_of_grant' : tds[5].text_content(),
            'program' : tds[7].text_content(),
            'region' : tds[9].text_content(),
            'grant_description' : tds[11].text_content(),
            'grantee_website' :  tds[13].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['project_name'], data=data2)


    except:
       print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
