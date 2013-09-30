import scraperwiki

# Blank Python
print "Hey, these are physics conferences!"

#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)


import scraperwiki
html = scraperwiki.scrape("http://www.iop.org/events/scientific/conferences/rss.xml")
print html


import lxml.html 
root = lxml.html.fromstring(html)
eventlist = root.cssselect('item')


for event in eventlist:
      confname_css = event.cssselect('title')[0]
      confname = confname_css.text_content()

      url_css = event.cssselect('link')[0]
      url = url_css.text_content()
    

      description_css = event.cssselect('description')[0]
      description = description_css.text_content()
    
      scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url,'description':description})

import requestsimport scraperwiki

# Blank Python
print "Hey, these are physics conferences!"

#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)


import scraperwiki
html = scraperwiki.scrape("http://www.iop.org/events/scientific/conferences/rss.xml")
print html


import lxml.html 
root = lxml.html.fromstring(html)
eventlist = root.cssselect('item')


for event in eventlist:
      confname_css = event.cssselect('title')[0]
      confname = confname_css.text_content()

      url_css = event.cssselect('link')[0]
      url = url_css.text_content()
    

      description_css = event.cssselect('description')[0]
      description = description_css.text_content()
    
      scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url,'description':description})

import requests