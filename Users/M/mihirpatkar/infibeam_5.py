import scraperwiki
from scrapemark import scrape


for page in range(1,11):
    html = scraperwiki.scrape("http://www.infibeam.com/Laptop_Computers_Accessories/Search_ajax.action?category=Laptop&store=Computers_Accessories&page=%i"%page)

    scrape_data = scrape("""
<ul class="srch_result" >
{*
<li>
<a href="{{ [mobile].[link] }}">
<span class="title">{{ [mobile].[name] }}</span>
</a>
</li>
*}
</ul>
""", html=html);

    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

import scraperwiki
from scrapemark import scrape


for page in range(1,11):
    html = scraperwiki.scrape("http://www.infibeam.com/Laptop_Computers_Accessories/Search_ajax.action?category=Laptop&store=Computers_Accessories&page=%i"%page)

    scrape_data = scrape("""
<ul class="srch_result" >
{*
<li>
<a href="{{ [mobile].[link] }}">
<span class="title">{{ [mobile].[name] }}</span>
</a>
</li>
*}
</ul>
""", html=html);

    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

