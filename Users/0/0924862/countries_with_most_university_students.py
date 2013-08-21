# # Blank Python

#print "Hello, coding in the cloud!"
import scraperwiki
webpage = 'http://www.aneki.com/students.html'
html = scraperwiki.scrape(webpage)
#print html
import lxml.etree
import lxml.html

#print help(lxml.html.parse)

base_url = 'http://www.aneki.com/students.html'

root = lxml.html.parse(base_url).getroot()

#print lxml.etree.tostring(root)


print 'number of tables', len(root.cssselect("table border=0 cellspacing=0 cellpadding=0 width=100% tr.tcont"))

for tr in root.cssselect("table border=0 cellspacing=0 cellpadding=0 width=100% tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'top 10 countries' : tds[0].text_content(),
      'students_in_universities' : int(tds[4].text_content())
    }
    print data

    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

