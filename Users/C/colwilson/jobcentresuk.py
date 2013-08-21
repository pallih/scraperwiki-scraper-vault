import scraperwiki
import scrapemark
from bs4 import BeautifulSoup
 
url = "http://www.jobcentreplus.info/Jobcentre-Information-Maps/index.html"
html = scraperwiki.scrape(url=url)
soup = BeautifulSoup(html)

content = soup.find_all(id="content")
print type(html)


data = scrapemark.scrape("""
        {*
                <b><a title="{{[offices].office_code}}">{{[offices].name}}</a></b>
                <br>
                <b>{{[offices].postcode}}</b><b>{{[offices].phone}}</b>
                <br>
                <b></b>{{[offices].district}}<b></b>{{[offices].region}}<hr>
        *}
        """,
        url=url)

#scraperwiki.sqlite.save(unique_keys=["office_code"], data=data['offices'])


