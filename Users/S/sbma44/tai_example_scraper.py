import scraperwiki
import lxml.html

html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)

for el in root.cssselect("div.tags li a"):
    print el.text, el.attrib['href']    

    html_for_tag_page = scraperwiki.scrape("https://scraperwiki.com" + el.attrib['href'] )
    root_for_tag_page = lxml.html.fromstring(html_for_tag_page)

    matching_python_scrapers = 0
    for tag_el in root.cssselect("table.code_about tr.python"):
        matching_python_scrapers = matching_python_scrapers + 1

    scraperwiki.sqlite.save(unique_keys=['url'], data={'title': el.text, 'url': el.attrib['href'], 'num_python_scrapers': matching_python_scrapers})


