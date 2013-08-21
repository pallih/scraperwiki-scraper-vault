import scraperwiki
import requests
import lxml.html

# Functions

def getShotURLsFromURL(url):
    r = requests.get(url, verify=False)
    dom = lxml.html.fromstring(r.text)
    targetList = dom.cssselect('.dribbble-shot a.dribbble-link')
    links = []

    for result in targetList:
        link = {
            "url": result.get("href")
        }
        links.append(link)
    return links

def fetchAndSaveDataForUrl(url):
    r2 = requests.get(url, verify=False)
    dom = lxml.html.fromstring(r2.text)
    targetList = dom.cssselect('.color-chips li a')
    colors = []

    for result in targetList:
        color = {
            "color": result.text_content()
        }
        colors.append(color)

    targetList = dom.cssselect("#screenshot-title")

    shot = {
        "colors": colors,
        "title": targetList[0].text_content(),
        "url" : aLink["url"]
    }

    scraperwiki.sqlite.save(unique_keys=['url'], data=shot)


# Run

for i in range(1, 6):
    links = getShotURLsFromURL("http://dribbble.com/shots/popular?page=" + str(i))

    for aLink in links:
        fetchAndSaveDataForUrl("http://dribbble.com" + aLink["url"])





