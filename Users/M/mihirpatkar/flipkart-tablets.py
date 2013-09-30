import scraperwiki
import simplejson
from scrapemark import scrape

for page in range(0, 21):
    print page
    json = scraperwiki.scrape("http://www.flipkart.com/computers/laptops/all?response-type=json&inf-start=%i"%(page*20))
    
    html = simplejson.loads(json)["html"]
    
    
    scrape_data = scrape("""
    {*
    <a class="title tpadding5 fk-anchor-link" title="" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
    *}
    """, html=html);
    
    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

import scraperwiki
import simplejson
from scrapemark import scrape

for page in range(0, 21):
    print page
    json = scraperwiki.scrape("http://www.flipkart.com/computers/laptops/all?response-type=json&inf-start=%i"%(page*20))
    
    html = simplejson.loads(json)["html"]
    
    
    scrape_data = scrape("""
    {*
    <a class="title tpadding5 fk-anchor-link" title="" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
    *}
    """, html=html);
    
    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

