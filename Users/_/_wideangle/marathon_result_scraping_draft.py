import scraperwiki
           
html = scraperwiki.scrape("http://www.marathontulokset.com/ilmo2/results_show.php?serie=HCR_0_130&hcmyear=2011&hcmid=2&base=results_hcr2008")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("tr td")
    if len(tds)>4:
        data = {
          'eka' : tds[0].text_content(),
          'number' : tds[1].text_content(),
          'Last name' : tds[2].text_content(),
          'First name' : tds[3].text_content()
        }
print data

#scraperwiki.sqlite.save(['eka'],data=data)

import scraperwiki
           
html = scraperwiki.scrape("http://www.marathontulokset.com/ilmo2/results_show.php?serie=HCR_0_130&hcmyear=2011&hcmid=2&base=results_hcr2008")

import lxml.html           
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("tr td")
    if len(tds)>4:
        data = {
          'eka' : tds[0].text_content(),
          'number' : tds[1].text_content(),
          'Last name' : tds[2].text_content(),
          'First name' : tds[3].text_content()
        }
print data

#scraperwiki.sqlite.save(['eka'],data=data)

