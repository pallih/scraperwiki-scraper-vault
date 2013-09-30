import scraperwiki,re
import lxml.html


url='http://itc.conversationsnetwork.org/series/technation.html'
html=scraperwiki.scrape(url)

root = lxml.html.fromstring(html)

def scrapePage(id):
    #url='http://itc.conversationsnetwork.org/shows/detail3514.html'
    url='http://itc.conversationsnetwork.org/shows/detail'+id+'.html'
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    if page.cssselect("div[id='amazonDiv']"):
        key=re.search('http://itc.conversationsnetwork.org/shows/(.*)$',url).group(1)
        title=page.cssselect('title')[0].text_content()
        desc=page.cssselect("meta[name='description']")[0].attrib['content']
        print title,desc,
        download=page.cssselect('div[id="controlPanel1"] ul li')[1].cssselect('a')[0].attrib['href']
        print download

        ad=page.cssselect("div[id='amazonDiv']")[0].getnext()
        m=re.search("asin:'(.*)'",ad.text_content())
        isbn=m.group(1)
        print key,isbn#,ad.text_content()
        author=title.split('|')[0].strip()
        scraperwiki.sqlite.save(unique_keys=["id"], data={"id":key, "title":title,'desc':desc,'isbn':isbn,'author':author,'audioURL':download})

def parseResultsPage(pageUrl):
    #pageUrl='http://itc.conversationsnetwork.org/series/technation.html'
    html=scraperwiki.scrape(pageUrl)
    root = lxml.html.fromstring(html)
    for episode in root.cssselect("div[class='centerColumnFeature episodeFullSummary']"):
        print episode.attrib['id'],
        id=re.search("episode-(.*)",episode.attrib['id']).group(1)
        print id
        scrapePage(id)
        #<div id='episode-4938' class='centerColumnFeature episodeFullSummary'> 

parseResultsPage(url)
pageLinks=root.cssselect("div[class='seriesPagePager']")
pages=[]
for page in pageLinks[0].cssselect("a"):
    if page not in pages:
        pages.append(page)
        print page.attrib['href']
        offset=page.attrib['href'].split('offset=')[1]
        if int(offset)<11:
            purl='http://itc.conversationsnetwork.org'+page.attrib['href']
            print purl
            parseResultsPage(purl)
#for page in 
#<div class='seriesPagePager'>

#<meta name="description" content

#scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name,'addr':address,'postcode':postcode,'rating':rating,'ratingval':ratingval,'typ':typ})import scraperwiki,re
import lxml.html


url='http://itc.conversationsnetwork.org/series/technation.html'
html=scraperwiki.scrape(url)

root = lxml.html.fromstring(html)

def scrapePage(id):
    #url='http://itc.conversationsnetwork.org/shows/detail3514.html'
    url='http://itc.conversationsnetwork.org/shows/detail'+id+'.html'
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    if page.cssselect("div[id='amazonDiv']"):
        key=re.search('http://itc.conversationsnetwork.org/shows/(.*)$',url).group(1)
        title=page.cssselect('title')[0].text_content()
        desc=page.cssselect("meta[name='description']")[0].attrib['content']
        print title,desc,
        download=page.cssselect('div[id="controlPanel1"] ul li')[1].cssselect('a')[0].attrib['href']
        print download

        ad=page.cssselect("div[id='amazonDiv']")[0].getnext()
        m=re.search("asin:'(.*)'",ad.text_content())
        isbn=m.group(1)
        print key,isbn#,ad.text_content()
        author=title.split('|')[0].strip()
        scraperwiki.sqlite.save(unique_keys=["id"], data={"id":key, "title":title,'desc':desc,'isbn':isbn,'author':author,'audioURL':download})

def parseResultsPage(pageUrl):
    #pageUrl='http://itc.conversationsnetwork.org/series/technation.html'
    html=scraperwiki.scrape(pageUrl)
    root = lxml.html.fromstring(html)
    for episode in root.cssselect("div[class='centerColumnFeature episodeFullSummary']"):
        print episode.attrib['id'],
        id=re.search("episode-(.*)",episode.attrib['id']).group(1)
        print id
        scrapePage(id)
        #<div id='episode-4938' class='centerColumnFeature episodeFullSummary'> 

parseResultsPage(url)
pageLinks=root.cssselect("div[class='seriesPagePager']")
pages=[]
for page in pageLinks[0].cssselect("a"):
    if page not in pages:
        pages.append(page)
        print page.attrib['href']
        offset=page.attrib['href'].split('offset=')[1]
        if int(offset)<11:
            purl='http://itc.conversationsnetwork.org'+page.attrib['href']
            print purl
            parseResultsPage(purl)
#for page in 
#<div class='seriesPagePager'>

#<meta name="description" content

#scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name,'addr':address,'postcode':postcode,'rating':rating,'ratingval':ratingval,'typ':typ})