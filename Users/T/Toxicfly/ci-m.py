import scraperwiki
from scrapemark import scrape


for page in range(1,164):
    html = scraperwiki.scrape("http://compareindia.in.com/products/mobile-phones/23-%i"%(page))

    scrape_data = scrape("""
{*
<div class="feat_rt">
<h2><a class="b_18" href="{{ [mobile].[link] }}" >< >


*}
""", html=html);

#title="{{ [mobile].[title] }}" "

    data = [{'url':p['link'][0] } for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

import scraperwiki
from scrapemark import scrape


for page in range(1,164):
    html = scraperwiki.scrape("http://compareindia.in.com/products/mobile-phones/23-%i"%(page))

    scrape_data = scrape("""
{*
<div class="feat_rt">
<h2><a class="b_18" href="{{ [mobile].[link] }}" >< >


*}
""", html=html);

#title="{{ [mobile].[title] }}" "

    data = [{'url':p['link'][0] } for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

