import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import scraperwiki
html = scraperwiki.scrape("http://oceaninfosoft.com/wordpress_table/result.php")
print html


import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table['entry-content'] tr.tcont"): 
    tds = tr.cssselect("td")
    data = {
      'Post Title' : tds[0].text_content(),
'Post ID' : tds[1].text_content(),

'Author' : tds[3].text_content(),

'Latest Comment' : tds[7].text_content(),

'Date' : tds[9].text_content(),
      'date' : int(tds[4].text_content())
    }
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)






