import scraperwiki
import lxml.html

# Blank Python

html = scraperwiki.scrape("http://www.dragonboat.org.uk/league_stuff/leaguetablemod.php")
print html

           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[cellpadding=0] tr") [1:]:
    tds = tr.cssselect("td")
    if len(tds) > 0:
       data = { 'Club' : tds[0].text_content(),
            'Events' : tds[1].text_content() ,
            'Points' : tds[2].text_content()
       }
    scraperwiki.sqlite.save(unique_keys=['Club'], data=data)



import scraperwiki
import lxml.html

# Blank Python

html = scraperwiki.scrape("http://www.dragonboat.org.uk/league_stuff/leaguetablemod.php")
print html

           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[cellpadding=0] tr") [1:]:
    tds = tr.cssselect("td")
    if len(tds) > 0:
       data = { 'Club' : tds[0].text_content(),
            'Events' : tds[1].text_content() ,
            'Points' : tds[2].text_content()
       }
    scraperwiki.sqlite.save(unique_keys=['Club'], data=data)



