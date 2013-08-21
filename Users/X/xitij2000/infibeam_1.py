import scraperwiki
from scrapemark import scrape


for page in range(23,23):
    html = scraperwiki.scrape("http://www.ncarry.com/category.php")

    scrape_data = scrape("""
<div class="smlLstng"> 
{*
<p>
<a href="{{ [mobile].[link] }}">
<strong>{{ [mobile].[name] }}</strong>
</a>
</p>
*}
</div>
""", html=html);

    data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["name"], data=data)

