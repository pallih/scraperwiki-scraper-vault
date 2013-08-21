import scraperwiki
import lxml.html
# Blank Python

html = scraperwiki.scrape("http://velocityconf.com/velocityeu/public/schedule/full")
root = lxml.html.fromstring(html)
for link in root.cssselect(".summary .url"):
    title = link.text
    newhtml = scraperwiki.scrape("http://velocityconf.com"+link.attrib['href'])
    newroot = lxml.html.fromstring(newhtml)
    for item in newroot.cssselect(".en_grade_average_detail"):
        data = {
            "title": title,
            "score": item.text_content()[1:4]
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
#        print data["title"],data["score"]
