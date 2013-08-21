import scraperwiki
import lxml.html

# Blank Python

print 'hello, coding in the cloud'
html =  scraperwiki.scrape("https://play.google.com/store/apps/details?id=com.webmd.android&feature=search_result#?t=W251bGwsMSwxLDEsImNvbS53ZWJtZC5hbmRyb2lkIl0.")

#print html

root = lxml.html.fromstring(html)

for tds in root.cssselect("p.review-text"):

  
    
        data={
            'review': tds.text_content()
        }



        scraperwiki.sqlite.save(unique_keys=['review'], data=data)
#print root.cssselect("a.next")
