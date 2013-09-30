import scraperwiki
html = scraperwiki.scrape("http://espn.go.com/wnba/standings")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr[align=right]"):
    tds = tr.cssselect("td")
    data = {
      'Name' : tds[0].text_content(),
      'W' : tds[1].text_content(),
      'L' : tds[2].text_content(),
      'PCT' : tds[3].text_content(),
      'GB' : tds[4].text_content(),
      'HOME' : tds[5].text_content(),
      'ROAD' : tds[6].text_content(),
      'PF' : tds[7].text_content(),
      'PA' : tds[8].text_content(),
      'STREAK' : tds[9].text_content(),
      'L 10' : tds[10].text_content()
    }
    print data
    
#scraperwiki.sqlite.save(unique_keys=['Name', 'W', 'L', 'PCT', 'GB', 'HOME', 'ROAD', 'PF', 'PA', 'STREAK', 'L 10'], data=data)import scraperwiki
html = scraperwiki.scrape("http://espn.go.com/wnba/standings")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr[align=right]"):
    tds = tr.cssselect("td")
    data = {
      'Name' : tds[0].text_content(),
      'W' : tds[1].text_content(),
      'L' : tds[2].text_content(),
      'PCT' : tds[3].text_content(),
      'GB' : tds[4].text_content(),
      'HOME' : tds[5].text_content(),
      'ROAD' : tds[6].text_content(),
      'PF' : tds[7].text_content(),
      'PA' : tds[8].text_content(),
      'STREAK' : tds[9].text_content(),
      'L 10' : tds[10].text_content()
    }
    print data
    
#scraperwiki.sqlite.save(unique_keys=['Name', 'W', 'L', 'PCT', 'GB', 'HOME', 'ROAD', 'PF', 'PA', 'STREAK', 'L 10'], data=data)