import scraperwiki
import lxml.html
import cgi, os           

proprietary_name = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

html = scraperwiki.scrape("http://labels.fda.gov/getproprietaryname.cfm?searchfield=%s&OrderBy=MarketingCategory&numberperpage=10000&beginrow=1" % proprietary_name)


root = lxml.html.fromstring(html)

for tr in root.cssselect("span#user_provided tr"):
    tds = tr.cssselect("td")
    if len(tds)==6:
        data = {
            'proprietary_name' : tds[0].text_content().strip(),
            'ndc' : tds[1].text_content().strip(),
            'company_name' : tds[2].text_content().strip(),
            'application_number_or_regulatory_citation' : tds[3].text_content().strip(),
            'product_type' : tds[4].text_content().strip(),
            'marketing_category' : tds[5].text_content().strip(),
        }
        print data