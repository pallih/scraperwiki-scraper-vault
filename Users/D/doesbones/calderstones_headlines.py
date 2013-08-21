import scraperwiki           
html = scraperwiki.scrape("http://calderstones.co.uk/parents.html")
print html

import lxml.html           
root = lxml.html.fromstring(html)
for myheading in root.cssselect("div[align='center'] h3"):

        data = {
            'heading' : myheading.text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['heading'], data=data)

