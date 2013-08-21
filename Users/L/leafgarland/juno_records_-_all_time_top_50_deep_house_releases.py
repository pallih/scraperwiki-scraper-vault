import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.juno.co.uk/deep-house/charts/bestsellers/all/")
root = lxml.html.fromstring(html)

# div#main table.product_list tr.row1
# div#main table.product_list span.artist_search_highlight a
rank = 0
for el in root.cssselect("div#main table.product_list tr"):
    classa = el.attrib["class"]
    if classa == "row1" or classa == "row2":
        artist = el.cssselect("span.artist_search_highlight a")[0].text
        title = el.cssselect("span.title_search_highlight")[0].text
        data = {'artist': artist, 'title': title, 'rank': rank }
        scraperwiki.sqlite.save(unique_keys=['artist', 'title'], data=data)
        rank = rank + 1



