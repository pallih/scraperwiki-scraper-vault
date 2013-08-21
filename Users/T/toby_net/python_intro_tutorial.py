# python intro tutorial 
# http://scraperwiki.com/docs/python/python_intro_tutorial/

# 1
print "Hello, coding in the cloud!"

# 2 
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

# 3
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
        'country': tds[0].text_content(),
        'years_in_school': int(tds[4].text_content())
    }
    print data
    # 4
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
