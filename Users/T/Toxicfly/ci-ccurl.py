import scraperwiki
from scrapemark import scrape


for page in range(1,50):
    html = scraperwiki.scrape("http://bus.gov.ru/public/register/search.html?d-442831-p=%i"%(page))
    print html
    scrape_data = scrape("""
{*
<td class="tableBgLeft">{{ [mobile].[id] }}</td>
<td>{{ [mobile].[name] }}</td>
*}
""", html=html);

#title="{{ [mobile].[title] }}" "

    data = [{'id':p['id'][0],'Name':p['name'][0] } for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["id"], data=data)

import scraperwiki
from scrapemark import scrape


for page in range(1,50):
    html = scraperwiki.scrape("http://bus.gov.ru/public/register/search.html?d-442831-p=%i"%(page))
    print html
    scrape_data = scrape("""
{*
<td class="tableBgLeft">{{ [mobile].[id] }}</td>
<td>{{ [mobile].[name] }}</td>
*}
""", html=html);

#title="{{ [mobile].[title] }}" "

    data = [{'id':p['id'][0],'Name':p['name'][0] } for p in scrape_data['mobile']]

    scraperwiki.sqlite.save(unique_keys=["id"], data=data)

