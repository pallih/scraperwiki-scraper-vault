import scraperwiki
from scrapemark import scrape


for page in range(0,10):
    html = scraperwiki.scrape("http://www.homeshop18.com/laptops/categoryid:3291/search:*/start:*/listView:true/start:%d"%(page*24))

    scrape_data = scrape("""
{*
<div class="listView_title">
href="{{ [mobile].[link] }}" title="{{ [mobile].[name] }}">
</div>                
<div class="listView_price">
Price: 
<span class="our_price">{{ [mobile].[price] }}</span>
*}
""", html=html);

    data = [{'name':p['name'][0], 'url':p['link'][0],'price':p['price'][0] } for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

import scraperwiki
from scrapemark import scrape


for page in range(0,10):
    html = scraperwiki.scrape("http://www.homeshop18.com/laptops/categoryid:3291/search:*/start:*/listView:true/start:%d"%(page*24))

    scrape_data = scrape("""
{*
<div class="listView_title">
href="{{ [mobile].[link] }}" title="{{ [mobile].[name] }}">
</div>                
<div class="listView_price">
Price: 
<span class="our_price">{{ [mobile].[price] }}</span>
*}
""", html=html);

    data = [{'name':p['name'][0], 'url':p['link'][0],'price':p['price'][0] } for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

