import scraperwiki           
html = scraperwiki.scrape("http://www.indeed.com.ph/jobs?q=engineer&l=")
#print html

import lxml.html           
root = lxml.html.fromstring(html)
for div in root.cssselect("td[id='resultsCol'] div"):
    a = div.cssselect("h2[class='jobtitle'] a")
    if len(a)==1:
        data = {
            'title' : a[0].text_content()}
        print data
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)