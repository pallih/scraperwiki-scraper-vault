import scraperwiki
import lxml.html 

html = scraperwiki.scrape("https://www.patientopinion.org.uk/feed/opinions?format=atom&phrase=jargon&numitems=30")     
root = lxml.html.fromstring(html)
for tr in root.cssselect("title"):
       
    try:
        website = tr.text
        print website
    except:
        website = "parser issue :("
  
    data = {
        'title' : 'title',
        'text': website
        }
    scraperwiki.sqlite.save(unique_keys=['text'], data=data)
import scraperwiki
import lxml.html 

html = scraperwiki.scrape("https://www.patientopinion.org.uk/feed/opinions?format=atom&phrase=jargon&numitems=30")     
root = lxml.html.fromstring(html)
for tr in root.cssselect("title"):
       
    try:
        website = tr.text
        print website
    except:
        website = "parser issue :("
  
    data = {
        'title' : 'title',
        'text': website
        }
    scraperwiki.sqlite.save(unique_keys=['text'], data=data)
