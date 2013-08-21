import scraperwiki, lxml.html

# Blank Python

print "hello, cloud coding!"

def scrapePage(page='0'):
    html = scraperwiki.scrape("http://opendataphilly.org/opendata/?sort=name&filter=data&page="+str(page))
    root = lxml.html.fromstring(html)
    lxml.html.resolve_base_href(root) #not doing anything

    for res in root.cssselect("#results_list li.resource"):
        title = res.cssselect("#resource_title")
        desc = res.cssselect("#resource_desc")
        for link in title[0].iterlinks():
            # scrape each item i.e. http://opendataphilly.org/opendata/resource/11/topographic-contours-2ft/
            itemUrl = "http://opendataphilly.org"+str(link[2])

        itemHtml = scraperwiki.scrape(itemUrl)
        item = lxml.html.fromstring(itemHtml)

        data = {
          'title' : title[0].text_content(),
          'desc' : desc[0].text_content(),
          'itemUrl' : itemUrl
          #'itemHtml' : itemHtml
        }

        tab_data = item.cssselect("#tab_data")[0]
        for counter,info in enumerate(tab_data.cssselect("div")):
            if (counter == 0 or counter % 2):
                 key = str(info.text_content()) 
            else: 
                 data[key] = str(info.text_content())
            
        print data
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

for i in range(1,29):
    scrapePage(i)