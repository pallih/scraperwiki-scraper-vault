import scraperwiki
from scrapemark import scrape


for page in range(1,3):
 html =scraperwiki.scrape ('http://www.snapdeal.com/products/computers-laptops')
#html = scraperwiki.scrape("http://compareindia.in.com/products/digital-cameras/62-%i"%(page))
 print html
 scrape_data = scrape("""
{*
<a href="{{[mobile].[url] }}"  v="p" categoryId="57" class="hit-ss-logger">
*}
""",html=html);

#title="{{ [mobile].[title] }}" "

 data = [{'url':p['url'][0]} for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["url"], data=data)

