import scraperwiki
import urlparse
import lxml.html

for i in range(1,1700): #USER: update range as necessary
    try:
        url = "http://212.27.125.205/Operations/PS_ProjectDetails.aspx?OP_INR=%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        tds = root.cssselect("span") #this is the tag that highlights where on the webpage we want to get the data from; <span id> tag here
        data = {
            'project_name' : tds[0].text_content(),
            'reference' : tds[2].text_content(),
            'sector' : tds[3].text_content(),
            'region' : tds[4].text_content(),
            'amount' : tds[5].text_content(),
            'approval_date' : tds[6].text_content(),
            'status' : tds[7].text_content(),
            'borrower' :  tds[8].text_content(),
            'loan_administrator' : tds[9].text_content(), 
            'executing_agency' : tds[10].text_content(),
            'co_financiers' : tds[11].text_content(), 
            'total_cost' : tds[12].text_content(),
            'description' : tds[13].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['project_name','reference'], data=data)

    except:
        print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
