import scraperwiki
import simplejson
from scrapemark import scrape

json = scraperwiki.scrape("http://www.adexmart.com/modules/coremanager/modules/filtersearch/filtersearch.json.php?act=filter&ident=15&page=1&perpage=666&orderby=newest&orderway=desc")

html = simplejson.loads(json)["products"]

print html

scrape_data = scrape("""
{*
<li>
<h3><a title="" href="{{ [mobile].[link] }}">{{ [mobile].[name] }}</a></h3>
</li>
*}
""", html=html);

data = [{'name':p['name'][0], 'url':p['link'][0]} for p in scrape_data['mobile']]

scraperwiki.sqlite.save(unique_keys=["name"], data=data)

