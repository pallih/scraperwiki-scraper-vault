import lxml.html
import lxml.etree

url = 'http://onethingwell.org/'
root = lxml.html.parse(url).getroot()

link_articles = root.cssselect("article.link")
regular_articles = root.cssselect("article.regular")
photo_articles = root.cssselect("article.photo") 

for article in link_articles:
    print lxml.etree.tostring(article)

for article in regular_articles:
    print lxml.etree.tostring(article)

for article in photo_articles:
    print lxml.etree.tostring(article)

import lxml.html
import lxml.etree

url = 'http://onethingwell.org/'
root = lxml.html.parse(url).getroot()

link_articles = root.cssselect("article.link")
regular_articles = root.cssselect("article.regular")
photo_articles = root.cssselect("article.photo") 

for article in link_articles:
    print lxml.etree.tostring(article)

for article in regular_articles:
    print lxml.etree.tostring(article)

for article in photo_articles:
    print lxml.etree.tostring(article)

