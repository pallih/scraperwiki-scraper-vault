import scraperwiki
from scrapemark import scrape

for page in range(1, 7):
    print page
    html = scraperwiki.scrape(("http://www.phonearena.com/phones/manufacturers/Zen-Mobile/%i")%page)
    
    print html  
    scrape_data = scrape("""
    {*                        <h3><a href="{{ [mobile].[link] }}" >{{ [mobile].[name] }}</a></h3><div class="s_short_specs" style="display: none"><ul class="s_list_1 red_2 s_mb_5"><li>

    *}
    """, html=html);
    
    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]
    
    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

