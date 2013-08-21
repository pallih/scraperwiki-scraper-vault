import scraperwiki
import lxml.html

# Blank Python

html = scraperwiki.scrape('http://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number')

root = lxml.html.fromstring(html)
for tr in root.cssselect("div.mw-content-ltr tr"):
    tds = tr.cssselect("td")
    if len(tds)==5:
        data = {
            'n_id' : tds[1].text_content()[:-1],
            'name' : tds[3].text_content()[:-1],
            'primary_type' : tds[4].text_content()[:-1]
        }
        print data
    elif len(tds)==6:
        data = {
            'n_id' : tds[1].text_content()[:-1],
            'name' : tds[3].text_content()[:-1],
            'primary_type' : tds[4].text_content()[:-1],
            'secondary_type' : tds[5].text_content()[:-1]
        }
        scraperwiki.sqlite.save(unique_keys=['n_id'], data=data)