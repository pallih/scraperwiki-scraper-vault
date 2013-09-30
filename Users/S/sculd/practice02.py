import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
print(html)
root = lxml.html.fromstring(html)

for el in root.cssselect("div.tags a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']

el = root.cssselect("div#customers strong")[0]
print el
print el.text
print el.tail

eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>')
print eg.text_content() # 'A thing goes boom up on the tree'
import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://scraperwiki.com/")
print(html)
root = lxml.html.fromstring(html)

for el in root.cssselect("div.tags a"):
    print el
    print lxml.html.tostring(el)
    print el.attrib['href']

el = root.cssselect("div#customers strong")[0]
print el
print el.text
print el.tail

eg = lxml.html.fromstring('<h2>A thing <b>goes boom</b> up <i>on <em>the tree</em></i></h2>')
print eg.text_content() # 'A thing goes boom up on the tree'
