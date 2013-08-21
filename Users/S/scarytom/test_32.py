import scraperwiki
import lxml.html

for i in range(24):

    html = scraperwiki.scrape("http://sourceforge.net/directory/?page=" + str(i + 1))
    root = lxml.html.fromstring(html)

    for el in root.cssselect("div.project_info header a"):
        data = { 'title' : el.text_content(), 'url' : 'http://sourceforge.net' + el.attrib['href'] }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
