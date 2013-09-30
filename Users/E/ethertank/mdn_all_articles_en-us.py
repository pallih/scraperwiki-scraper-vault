# Blank Python
import scraperwiki
import lxml.html

r = range(103)

for z in r:

    html = scraperwiki.scrape("https://developer.mozilla.org/en-US/docs/all?page=" + str(r[z] + 1)) 
    root = lxml.html.fromstring(html)

    URL = root.cssselect("#document-list li small")

    for x in URL:
        data = {
            'URL' : "https://developer.mozilla.org" + x.text_content()
        }
    
        scraperwiki.sqlite.save(unique_keys = ['URL'], data = data)

# Blank Python
import scraperwiki
import lxml.html

r = range(103)

for z in r:

    html = scraperwiki.scrape("https://developer.mozilla.org/en-US/docs/all?page=" + str(r[z] + 1)) 
    root = lxml.html.fromstring(html)

    URL = root.cssselect("#document-list li small")

    for x in URL:
        data = {
            'URL' : "https://developer.mozilla.org" + x.text_content()
        }
    
        scraperwiki.sqlite.save(unique_keys = ['URL'], data = data)

