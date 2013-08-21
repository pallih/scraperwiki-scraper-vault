import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://news.ycombinator.com/item?id=4596379")
root = lxml.html.fromstring(html)
hiring = []
looking = []
for comment in root.find_class("comment"):
    print comment.text_content()
    break;

