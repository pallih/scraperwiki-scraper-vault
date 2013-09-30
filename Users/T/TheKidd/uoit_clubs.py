import scraperwiki
import lxml.html

html = scraperwiki.scrape("https://connect.uoit.ca/uoit/campus_community/studentclubs.ezc")
root = lxml.html.fromstring(html)
clubs = root.cssselect("div#Page-Content-Inner p span")[4:]

for pos, club in enumerate(clubs):
    
    data = {'id': pos}
    data['name'] = club.text_content().strip()
    url = club.cssselect("a")
    if len(url) > 0:
        data['url'] = url[0].get('href').strip()
    else:
        data['url'] = ""
    print data
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
import scraperwiki
import lxml.html

html = scraperwiki.scrape("https://connect.uoit.ca/uoit/campus_community/studentclubs.ezc")
root = lxml.html.fromstring(html)
clubs = root.cssselect("div#Page-Content-Inner p span")[4:]

for pos, club in enumerate(clubs):
    
    data = {'id': pos}
    data['name'] = club.text_content().strip()
    url = club.cssselect("a")
    if len(url) > 0:
        data['url'] = url[0].get('href').strip()
    else:
        data['url'] = ""
    print data
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
