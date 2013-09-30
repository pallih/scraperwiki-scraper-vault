# Experimental Koldcast TV video page scraper
import scraperwiki
import lxml.html

baseUrl = "http://www.koldcast.tv"

def writeEpisodes(episodesLink, genre):
    html = scraperwiki.scrape(baseUrl + episodesLink)
    root = lxml.html.fromstring(html)

    for li in root.cssselect(".ContentBox_li"):
        brandEle = li.cssselect("h6")
        titleEle = li.cssselect("a h5")
        descriptionEle = li.cssselect("p")
        imageEle = li.cssselect("a span img")
        locationEle = li.cssselect("a")
        brandBlank = brandEle[0].text_content() + " - "
    
        data = {
            'type': 'episode',
            'title': titleEle[0].text_content().replace(brandBlank, "").strip(),
            'description': descriptionEle[0].text_content().strip(),
            'image': baseUrl + imageEle[0].attrib.get('src').strip(),
            'uri': baseUrl + locationEle[0].attrib.get('href').strip(),
            'location': baseUrl + locationEle[0].attrib.get('href').strip(),
            'genre': genre,
            'container': uri
        }
        scraperwiki.sqlite.save(unique_keys=['uri'], data=data)
    

def processShow(uri):
    html = scraperwiki.scrape(uri)
    # Get Brand info
    root = lxml.html.fromstring(html)
    showPageFeatureEle = root.cssselect("div#ShowPageFeature")[0]
    title = showPageFeatureEle.cssselect("h3.content")[0].text_content().strip()
    genre = showPageFeatureEle.cssselect("span.subtitle")[0].text_content().strip()
    description = showPageFeatureEle.cssselect(".descriptor .expandable p")[0].text_content().strip()
    image = showPageFeatureEle.cssselect("div.showBanner img")[0].attrib.get('src').strip()

    data = {
        "type": 'brand',
        "title": title,
        "genre": genre,
        "description": description,
        "image": image,
        "uri": uri,
    }
    scraperwiki.sqlite.save(unique_keys=['uri'], data=data)

    # Episodes
    episodesLink = root.cssselect(".watchNow")[0].attrib.get('href').strip()
    writeEpisodes(episodesLink, genre)


#uris = ["http://www.koldcast.tv/show/bloody-mary-show", "http://www.koldcast.tv/show/chatndish","http://www.koldcast.tv/show/devanity","http://www.koldcast.tv/show/thurston","http://www.koldcast.tv/show/nasa-tv"]
uris = ["http://www.koldcast.tv/show/hipsterhood"]
for uri in uris:
    processShow(uri)# Experimental Koldcast TV video page scraper
import scraperwiki
import lxml.html

baseUrl = "http://www.koldcast.tv"

def writeEpisodes(episodesLink, genre):
    html = scraperwiki.scrape(baseUrl + episodesLink)
    root = lxml.html.fromstring(html)

    for li in root.cssselect(".ContentBox_li"):
        brandEle = li.cssselect("h6")
        titleEle = li.cssselect("a h5")
        descriptionEle = li.cssselect("p")
        imageEle = li.cssselect("a span img")
        locationEle = li.cssselect("a")
        brandBlank = brandEle[0].text_content() + " - "
    
        data = {
            'type': 'episode',
            'title': titleEle[0].text_content().replace(brandBlank, "").strip(),
            'description': descriptionEle[0].text_content().strip(),
            'image': baseUrl + imageEle[0].attrib.get('src').strip(),
            'uri': baseUrl + locationEle[0].attrib.get('href').strip(),
            'location': baseUrl + locationEle[0].attrib.get('href').strip(),
            'genre': genre,
            'container': uri
        }
        scraperwiki.sqlite.save(unique_keys=['uri'], data=data)
    

def processShow(uri):
    html = scraperwiki.scrape(uri)
    # Get Brand info
    root = lxml.html.fromstring(html)
    showPageFeatureEle = root.cssselect("div#ShowPageFeature")[0]
    title = showPageFeatureEle.cssselect("h3.content")[0].text_content().strip()
    genre = showPageFeatureEle.cssselect("span.subtitle")[0].text_content().strip()
    description = showPageFeatureEle.cssselect(".descriptor .expandable p")[0].text_content().strip()
    image = showPageFeatureEle.cssselect("div.showBanner img")[0].attrib.get('src').strip()

    data = {
        "type": 'brand',
        "title": title,
        "genre": genre,
        "description": description,
        "image": image,
        "uri": uri,
    }
    scraperwiki.sqlite.save(unique_keys=['uri'], data=data)

    # Episodes
    episodesLink = root.cssselect(".watchNow")[0].attrib.get('href').strip()
    writeEpisodes(episodesLink, genre)


#uris = ["http://www.koldcast.tv/show/bloody-mary-show", "http://www.koldcast.tv/show/chatndish","http://www.koldcast.tv/show/devanity","http://www.koldcast.tv/show/thurston","http://www.koldcast.tv/show/nasa-tv"]
uris = ["http://www.koldcast.tv/show/hipsterhood"]
for uri in uris:
    processShow(uri)