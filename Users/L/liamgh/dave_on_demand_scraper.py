# Experimental DAVE TV video page scraper
import scraperwiki
import lxml.html
import re

baseUrl = "http://video.uktv.co.uk"

def processSeriesInfo(seriesInfo):
    results = re.search('Series (?P<series>\d*), Episode (?P<episode>\d*) \| (?P<longleft>[A-Za-z0-9 ]*)', seriesInfo)
    # TODO time left
    return {
        "seriesNumber": results.group("series"), 
        "episodeNumber": results.group("episode")
    }

def getEpisodeTitle(title, seriesInfo):
    if title != "":
        return title
    else: 
        return "Series " + seriesInfo["seriesNumber"] + " Episode " + seriesInfo["episodeNumber"]

def scrapeEpisode(episodeListingEle, genreUrl, brandUrl):
    episodeDetailEle = episodeListingEle.cssselect("div.episode-detail")[0]
    episodeImageEle = episodeListingEle.cssselect("div.episode-image")[0]
    # If no title given use the episode and series no instead
    title = episodeDetailEle.cssselect("p.title")[0].text_content()
    description = episodeDetailEle.cssselect("div.synopsis")[0].text_content()
    uri = baseUrl + episodeImageEle.cssselect("a")[0].attrib.get('href').strip()
    image = episodeImageEle.cssselect("img")[0].attrib.get('src').strip()
    seriesInfo = processSeriesInfo(episodeDetailEle.cssselect("p.series-info a")[0].text_content())
    data = {
       'type': 'episode',
       'title': getEpisodeTitle(title, seriesInfo),
       'description': description,
       'image': image,
       'uri': uri,
       'location': uri,
       'genre': genreUrl,
       'container': brandUrl,
       'episode_number': seriesInfo["episodeNumber"],
       'series_number': seriesInfo["seriesNumber"]
    }
    scraperwiki.sqlite.save(unique_keys=['uri'], data=data)


def scrapeBrandPage(genreUrl, brandUrl):
    html = scraperwiki.scrape(brandUrl)
    root = lxml.html.fromstring(html)
    programmeDetailsEle = root.cssselect("div#programme-details")[0]
    title = programmeDetailsEle.cssselect("div.title h1")[0].text_content()
    description = programmeDetailsEle.cssselect("div.synopsis p")[0].text_content().strip()
    image = root.cssselect("div.programme-image img")[0].attrib.get('src').strip()
   
    data = {
        "type": 'brand',
        "title": title,
        "genre": genreUrl,
        "description": description,
        "image": image,
        "uri": brandUrl,
    }
    scraperwiki.sqlite.save(unique_keys=['uri'], data=data)
    
    # Get the series that have not been loaded
    seriesLinks = root.cssselect("li.tab-season")
    firstSeriesLink=True
    for seriesLink in seriesLinks:
        if firstSeriesLink:
            firstSeriesLink=False
        else:
            processOtherSeries(seriesLink.attrib.get('id'), genreUrl, brandUrl)

    episodeListingEles = root.cssselect("ul.episode-list-container li")
    for episodeListingEle in episodeListingEles:
        scrapeEpisode(episodeListingEle, genreUrl, brandUrl)
    
def processOtherSeries(tabId, genreUrl, brandUrl):
    seriesUrl = tabId.replace("-","/").replace("tab/", baseUrl + "/dave/connect/ajax_requester/load_programme_detail/")
    rawJson = scraperwiki.scrape(seriesUrl)
    rawJson = re.sub("\r|\n|\t","",rawJson)
    rawJson = rawJson.decode("string-escape")
    start = rawJson.index("\"html\": \"") + 9
    end = rawJson.index("\", \"script\"")
    root = lxml.html.fromstring(rawJson[start:end])
    episodeListingEles = root.cssselect("li")
    for episodeListingEle in episodeListingEles:
        scrapeEpisode(episodeListingEle, genreUrl, brandUrl)

def scrapeGenrePage(genre_url):
    html = scraperwiki.scrape(genre_url)
    root = lxml.html.fromstring(html)
    progs = root.cssselect("div#content-genres li div.promo a.imagecache-connected_listing_linked")
    for prog in progs:
        scrapeBrandPage(genre_url, baseUrl + prog.attrib.get('href'))
    

startUrl = baseUrl + "/dave/programmes/by-genre/show-all"
html = scraperwiki.scrape(startUrl)
root = lxml.html.fromstring(html)
genresEle = root.cssselect("div#genre-list")[0]
for a in genresEle.cssselect("li a"):
    url = a.attrib.get('href')
    if (url != startUrl):
        scrapeGenrePage(url)


