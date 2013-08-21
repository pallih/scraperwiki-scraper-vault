import scraperwiki
html = scraperwiki.scrape("http://www.iwm.org.uk/collections/search?query=&filter[currentLocationDisplay][0]=%22Churchill%20War%20Rooms%22&items_per_page=10")
#print html

import lxml.html
root = lxml.html.fromstring(html)
for li in root.cssselect("ul.wrap li"):
    lis = li.cssselect("li a")
    data = {
      'title' : lis [0].text_content(),
      'href': lis [0].attrib['href']  
    }
    #scraperwiki.sqlite.save(unique_keys=['title'], data=data)
    secondhref = "http://www.iwm.org.uk" + lis[0].attrib['href']
    secondhtml = scraperwiki.scrape(secondhref)
    secondroot = lxml.html.fromstring(secondhtml)
    for secondli in secondroot.cssselect("div.object-info h1"):
        secondlis = secondli.cssselect("h1")
        data = {
          'title' : secondlis [0].text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

    for secondli in secondroot.cssselect("div.wrap dd"):
        secondlis = secondli.cssselect("dd")
        data = {
          'reference' : secondlis [0].text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=['reference'], data=data)


