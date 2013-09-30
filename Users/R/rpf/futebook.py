import scraperwiki
import lxml.html

order = 0

def extractdata(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for el in root.cssselect("div.post"):
        id = ""
        href = ""
        title = ""
        src = ""

        global order
        order = order + 1

        id = el.attrib["id"]

        for post in root.cssselect("div#" + el.attrib["id"] + " h2.entry-title a"):
            href = post.attrib['href']
            title = post.text_content()

        for img in root.cssselect("div#" + el.attrib["id"] + " div.entry-content img"):
            src = img.attrib["src"]

        print "ID -> " + id + " HREF -> " + href + " TITLE -> " + title + " SRC -> " + src

        data = {
            'id' : id,
            'href' : href,
            'title' : title.strip(),
            'src' : src,
            'order': order
        }
    
        scraperwiki.sqlite.save(unique_keys = ["id"], data = data)

    for pagenumber in root.cssselect("ul.page-numbers li a.next"):
        return pagenumber.attrib["href"]

    return ""

url = "http://futebooks.com/"

while url <> "":
    url = extractdata(url)

import scraperwiki
import lxml.html

order = 0

def extractdata(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for el in root.cssselect("div.post"):
        id = ""
        href = ""
        title = ""
        src = ""

        global order
        order = order + 1

        id = el.attrib["id"]

        for post in root.cssselect("div#" + el.attrib["id"] + " h2.entry-title a"):
            href = post.attrib['href']
            title = post.text_content()

        for img in root.cssselect("div#" + el.attrib["id"] + " div.entry-content img"):
            src = img.attrib["src"]

        print "ID -> " + id + " HREF -> " + href + " TITLE -> " + title + " SRC -> " + src

        data = {
            'id' : id,
            'href' : href,
            'title' : title.strip(),
            'src' : src,
            'order': order
        }
    
        scraperwiki.sqlite.save(unique_keys = ["id"], data = data)

    for pagenumber in root.cssselect("ul.page-numbers li a.next"):
        return pagenumber.attrib["href"]

    return ""

url = "http://futebooks.com/"

while url <> "":
    url = extractdata(url)

