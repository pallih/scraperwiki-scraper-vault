import scraperwiki
import numpy
from scrapemark import scrape

for page in range(400,4150):
    Star = page*100 + 1
    End = Star + 100   
    print Star
    print End
    URL = "http://academic.research.microsoft.com/RankList?entitytype=2&topDomainID=16&subDomainID=0&last=0&start="+str(Star)+"&end="+str(End)
    print URL
    html = scraperwiki.scrape(URL)

    scrape_data = scrape("""
{*

<h3>
<a id="" href="{{ [mobile].[link] }}" >{{ [mobile].[title] }}</a>
</h3>





*}
""", html=html);

    data = [{'name':p['title'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

import scraperwiki
import numpy
from scrapemark import scrape

for page in range(400,4150):
    Star = page*100 + 1
    End = Star + 100   
    print Star
    print End
    URL = "http://academic.research.microsoft.com/RankList?entitytype=2&topDomainID=16&subDomainID=0&last=0&start="+str(Star)+"&end="+str(End)
    print URL
    html = scraperwiki.scrape(URL)

    scrape_data = scrape("""
{*

<h3>
<a id="" href="{{ [mobile].[link] }}" >{{ [mobile].[title] }}</a>
</h3>





*}
""", html=html);

    data = [{'name':p['title'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

