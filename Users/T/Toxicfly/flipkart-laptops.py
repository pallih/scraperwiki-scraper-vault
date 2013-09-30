import scraperwiki
import simplejson
from scrapemark import scrape

for page in range(0, 50):
    print page
    json = scraperwiki.scrape("http://www.flipkart.com/laptops/all?response-type=json&inf-start=%i"%(page*20))
    
    html = simplejson.loads(json)["html"]
    print html
    
    scrape_data = scrape("""
    {*
    <a class="title tpadding5 fk-anchor-link" title="" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
    <div class='fk-price line n-dis'><span class="price final-price">{{ [mobile].[price] }}</</span></div>                        

    *}
    """, html=html);
    
    data = [{'name':p['name'][0], 'url':p['link'][0],'Price':p['price'][0]} for p in scrape_data['mobile']]
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

import scraperwiki
import simplejson
from scrapemark import scrape

for page in range(0, 50):
    print page
    json = scraperwiki.scrape("http://www.flipkart.com/laptops/all?response-type=json&inf-start=%i"%(page*20))
    
    html = simplejson.loads(json)["html"]
    print html
    
    scrape_data = scrape("""
    {*
    <a class="title tpadding5 fk-anchor-link" title="" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
    <div class='fk-price line n-dis'><span class="price final-price">{{ [mobile].[price] }}</</span></div>                        

    *}
    """, html=html);
    
    data = [{'name':p['name'][0], 'url':p['link'][0],'Price':p['price'][0]} for p in scrape_data['mobile']]
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

