import scraperwiki

# Blank Python
import urlparse
import scraperwiki
import lxml.html


def scrape_table(root):
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div[class='listing-body'] tr"):
        tds = tr.cssselect("td")
        data = {
                'Recipe Name' : tds[0].text_content(), 'Skill level' : tds[1].text_content() , 'Ingredients' : tds[4].text_content()
                }
        scraperwiki.sqlite.save(unique_keys=['item'], data=data)


url="http://www.gw2db.com/recipes?page=%d"
for page in range(1,2):
   html=scraperwiki.scrape(url % page)
   scrape_table(html)
