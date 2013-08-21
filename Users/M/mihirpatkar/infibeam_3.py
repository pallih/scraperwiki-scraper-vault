import scraperwiki
import simplejson
from scrapemark import scrape

for page in range(0, 9):
    print page
    json = scraperwiki.scrape("http://www.infibeam.com/Cameras/Search_ajax.action?subCategory=Point_and_Shoot&store=Cameras&page=%i"%(page+1))
    
    html = simplejson.loads(json)["html"]
    
    
    scrape_data = scrape("""
    {*
    <a class="title tpadding5 fk-anchor-link" title="" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a>
    *}
    """, html=html);
    
    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

