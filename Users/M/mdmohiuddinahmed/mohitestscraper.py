import scraperwiki

html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
#print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    #if len(tds) == 12:
    try:
        for i in range(0,11):
            try:
                print(' | '+tds[i].text_content()), 
            except:
                pass
    except:
        pass
    print('\n')
# data = { 
        #    'country' : tds[0].text_content(),
        #    'years_in_school' : int(tds[4].text_content())
      #  }
        # scraperwiki.sqlite.save(unique_keys=['country'], data=data)



