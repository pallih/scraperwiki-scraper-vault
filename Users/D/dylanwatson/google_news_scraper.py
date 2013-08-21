import scraperwiki
import BeautifulSoup
import HTMLParser

parser = HTMLParser.HTMLParser()

def getRSSFeed(url):
    html = scraperwiki.scrape("http://api.geonames.org/rssToGeoRSS?feedUrl=" + url + "&username=demo")
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("item")
    pubdate = None

    for d in news:
        try:
            title = parser.unescape(d.find("title").getText())
            link = ''
            try:
                link = d.find("link").getText()
            except Exception as e:
                 link = d.getText().split("url=")[1].split("tag:")[0]
            description = parser.unescape(d.find("description").getText())
            try:
                pubdate = d.find("pubdate").getText()
            except Exception as e:
                pubdate = soup.findAll("pubDate").first()
            latitude = ''
            longitude = ''
            try:
                latitude = d.find("geo:lat").getText()
            except Exception as e:
                latitude = ''

            try:
                longitude = d.find("geo:long").getText()
            except Exception as e:
                longitude = ''
            data = {
                    "title":title,
                    "description":description,
                    "link":link,
                    "pubdate":pubdate,
                    "source":url,
                    "latitude" : latitude,
                    "longitude" : longitude
                }
            scraperwiki.sqlite.save(unique_keys=['title', 'link'],data=data)
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (url, e)

def getDefenceFeed(url):
    html = scraperwiki.scrape("http://api.geonames.org/rssToGeoRSS?feedUrl=" + url + "&username=demo")
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("item")
    pubdate = soup.findAll("pubdate")[0].getText()

    for d in news:
        try:
            title = parser.unescape(d.find("title").getText())
            link = d.find("link").getText()
            description = parser.unescape(d.find("description").getText())
            latitude = ''
            longitude = ''
            try:
                latitude = d.find("geo:lat").getText()
            except Exception as e:
                latitude = ''

            try:
                longitude = d.find("geo:long").getText()
            except Exception as e:
                longitude = ''
            data = {
                    "title":title,
                    "description":description,
                    "link":link,
                    "pubdate":pubdate,
                    "source":url,
                    "latitude" : latitude,
                    "longitude" : longitude
                }
            scraperwiki.sqlite.save(unique_keys=['title', 'link'],data=data)
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (url, e)

def getGoogleKeywordFeed(countryCode, keyword):
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&q=" + keyword + "&um=1&ie=UTF-8&output=rss")

def getCountryGoogleFeeds(countryCode):
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&output=rss") # Country
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=n&output=rss") # National
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=tc&output=rss") # Technology
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=snc&output=rss") # Science
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=w&output=rss") # International
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=b&output=rss") # Business
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=s&output=rss") # Sports
    #getGoogleKeywordFeed(countryCode, "parliament")

def scrapeFeeds():
    getCountryGoogleFeeds("au") #Australia
    getCountryGoogleFeeds("uk") #UK
    getCountryGoogleFeeds("us") #US
    getCountryGoogleFeeds("nz") #New Zealand
    getCountryGoogleFeeds("ca") #Canada
    
    getRSSFeed("http://blogs.defensenews.com/rss-feed/?sitename=Def-Regions") #Defence News
    getRSSFeed("http://blogs.defensenews.com/rss-feed/?sitename=C4ISR")
    getRSSFeed("http://www.defensenews.com/rss/europe")
    getRSSFeed("http://www.defensenews.com/rss/americas")
    getRSSFeed("http://www.defensenews.com/rss/asia-pacific-rim")
    getRSSFeed("http://www.defensenews.com/rss/middle-east-africa")
    getRSSFeed("http://www.defensenews.com/rss/air-warfare")
    getRSSFeed("http://www.defensenews.com/rss/land-warfare")
    getRSSFeed("http://www.defensenews.com/rss/naval-warfare")
    getRSSFeed("http://www.defensenews.com/rss/policy")
    getRSSFeed("http://www.defensenews.com/rss/budget")
    getRSSFeed("http://www.defensenews.com/rss/business-watch")
    getRSSFeed("http://www.defensenews.com/rss/commentary")
    getRSSFeed("http://www.defensenews.com/rss/logistics")
    getRSSFeed("http://www.defensenews.com/rss/c4isr-features")

    getRSSFeed('http://feeds.feedburner.com/newscomaunationalbreakingnewsndm')
    getRSSFeed('http://feeds.feedburner.com/newscomauworldnewsndm')
    getRSSFeed('http://feeds.feedburner.com/newscomauthenationndm')

    getRSSFeed('http://feeds.bbci.co.uk/news/rss.xml')
    getRSSFeed('http://rss.cnn.com/rss/edition.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_world.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_americas.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_meast.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_asia.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_europe.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_us.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_connecttheworld.rss')
    getRSSFeed('http://rss.cnn.com/rss/cnn_latest.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_space.rss')

    getRSSFeed('http://www.cbsnews.com/feeds/rss/main.rss')
    getRSSFeed('http://www.cbsnews.com/feeds/rss/national.rss')
    getRSSFeed('http://www.cbsnews.com/feeds/rss/world.rss')
    
    getRSSFeed('http://feeds.abcnews.com/abcnews/mostreadstories')
    getRSSFeed('http://feeds.abcnews.com/abcnews/thisweekheadlines')
    getRSSFeed('http://feeds.abcnews.com/abcnews/2020headlines')
    getRSSFeed('http://feeds.abcnews.com/abcnews/topstories')
    getRSSFeed('http://feeds.abcnews.com/abcnews/internationalheadlines')
    getRSSFeed('http://feeds.abcnews.com/abcnews/usheadlines')
    
    getRSSFeed('http://feeds.reuters.com/reuters/MostRead')
    
    getRSSFeed('http://feeds.bbci.co.uk/news/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/world/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/world/middle_east/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/england/rss.xml')
    
    getRSSFeed('http://www.abc.net.au/news/feed/51120/rss.xml')
    getRSSFeed('http://www.abc.net.au/news/feed/45910/rss.xml')
    getRSSFeed('http://www.abc.net.au/news/feed/52278/rss.xml')
    getRSSFeed('http://www.abc.net.au/news/feed/46182/rss.xml')

    getRSSFeed('http://news.yahoo.com/rss/topstories')
    getRSSFeed('http://news.yahoo.com/rss/')
    getRSSFeed('http://news.yahoo.com/rss/world')

#scrapeFeeds()
getRSSFeed("http://blogs.defensenews.com/rss-feed/?sitename=Def-Regions") #Defence News
import scraperwiki
import BeautifulSoup
import HTMLParser

parser = HTMLParser.HTMLParser()

def getRSSFeed(url):
    html = scraperwiki.scrape("http://api.geonames.org/rssToGeoRSS?feedUrl=" + url + "&username=demo")
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("item")
    pubdate = None

    for d in news:
        try:
            title = parser.unescape(d.find("title").getText())
            link = ''
            try:
                link = d.find("link").getText()
            except Exception as e:
                 link = d.getText().split("url=")[1].split("tag:")[0]
            description = parser.unescape(d.find("description").getText())
            try:
                pubdate = d.find("pubdate").getText()
            except Exception as e:
                pubdate = soup.findAll("pubDate").first()
            latitude = ''
            longitude = ''
            try:
                latitude = d.find("geo:lat").getText()
            except Exception as e:
                latitude = ''

            try:
                longitude = d.find("geo:long").getText()
            except Exception as e:
                longitude = ''
            data = {
                    "title":title,
                    "description":description,
                    "link":link,
                    "pubdate":pubdate,
                    "source":url,
                    "latitude" : latitude,
                    "longitude" : longitude
                }
            scraperwiki.sqlite.save(unique_keys=['title', 'link'],data=data)
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (url, e)

def getDefenceFeed(url):
    html = scraperwiki.scrape("http://api.geonames.org/rssToGeoRSS?feedUrl=" + url + "&username=demo")
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("item")
    pubdate = soup.findAll("pubdate")[0].getText()

    for d in news:
        try:
            title = parser.unescape(d.find("title").getText())
            link = d.find("link").getText()
            description = parser.unescape(d.find("description").getText())
            latitude = ''
            longitude = ''
            try:
                latitude = d.find("geo:lat").getText()
            except Exception as e:
                latitude = ''

            try:
                longitude = d.find("geo:long").getText()
            except Exception as e:
                longitude = ''
            data = {
                    "title":title,
                    "description":description,
                    "link":link,
                    "pubdate":pubdate,
                    "source":url,
                    "latitude" : latitude,
                    "longitude" : longitude
                }
            scraperwiki.sqlite.save(unique_keys=['title', 'link'],data=data)
        except Exception as e:
            print 'Oh dear, failed to scrape %s due to %s' % (url, e)

def getGoogleKeywordFeed(countryCode, keyword):
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&q=" + keyword + "&um=1&ie=UTF-8&output=rss")

def getCountryGoogleFeeds(countryCode):
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&output=rss") # Country
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=n&output=rss") # National
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=tc&output=rss") # Technology
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=snc&output=rss") # Science
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=w&output=rss") # International
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=b&output=rss") # Business
    getRSSFeed("https://news.google.com/news/feeds?hl=en&ned=" + countryCode + "&topic=s&output=rss") # Sports
    #getGoogleKeywordFeed(countryCode, "parliament")

def scrapeFeeds():
    getCountryGoogleFeeds("au") #Australia
    getCountryGoogleFeeds("uk") #UK
    getCountryGoogleFeeds("us") #US
    getCountryGoogleFeeds("nz") #New Zealand
    getCountryGoogleFeeds("ca") #Canada
    
    getRSSFeed("http://blogs.defensenews.com/rss-feed/?sitename=Def-Regions") #Defence News
    getRSSFeed("http://blogs.defensenews.com/rss-feed/?sitename=C4ISR")
    getRSSFeed("http://www.defensenews.com/rss/europe")
    getRSSFeed("http://www.defensenews.com/rss/americas")
    getRSSFeed("http://www.defensenews.com/rss/asia-pacific-rim")
    getRSSFeed("http://www.defensenews.com/rss/middle-east-africa")
    getRSSFeed("http://www.defensenews.com/rss/air-warfare")
    getRSSFeed("http://www.defensenews.com/rss/land-warfare")
    getRSSFeed("http://www.defensenews.com/rss/naval-warfare")
    getRSSFeed("http://www.defensenews.com/rss/policy")
    getRSSFeed("http://www.defensenews.com/rss/budget")
    getRSSFeed("http://www.defensenews.com/rss/business-watch")
    getRSSFeed("http://www.defensenews.com/rss/commentary")
    getRSSFeed("http://www.defensenews.com/rss/logistics")
    getRSSFeed("http://www.defensenews.com/rss/c4isr-features")

    getRSSFeed('http://feeds.feedburner.com/newscomaunationalbreakingnewsndm')
    getRSSFeed('http://feeds.feedburner.com/newscomauworldnewsndm')
    getRSSFeed('http://feeds.feedburner.com/newscomauthenationndm')

    getRSSFeed('http://feeds.bbci.co.uk/news/rss.xml')
    getRSSFeed('http://rss.cnn.com/rss/edition.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_world.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_americas.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_meast.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_asia.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_europe.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_us.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_connecttheworld.rss')
    getRSSFeed('http://rss.cnn.com/rss/cnn_latest.rss')
    getRSSFeed('http://rss.cnn.com/rss/edition_space.rss')

    getRSSFeed('http://www.cbsnews.com/feeds/rss/main.rss')
    getRSSFeed('http://www.cbsnews.com/feeds/rss/national.rss')
    getRSSFeed('http://www.cbsnews.com/feeds/rss/world.rss')
    
    getRSSFeed('http://feeds.abcnews.com/abcnews/mostreadstories')
    getRSSFeed('http://feeds.abcnews.com/abcnews/thisweekheadlines')
    getRSSFeed('http://feeds.abcnews.com/abcnews/2020headlines')
    getRSSFeed('http://feeds.abcnews.com/abcnews/topstories')
    getRSSFeed('http://feeds.abcnews.com/abcnews/internationalheadlines')
    getRSSFeed('http://feeds.abcnews.com/abcnews/usheadlines')
    
    getRSSFeed('http://feeds.reuters.com/reuters/MostRead')
    
    getRSSFeed('http://feeds.bbci.co.uk/news/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/world/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/world/middle_east/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml')
    getRSSFeed('http://feeds.bbci.co.uk/news/england/rss.xml')
    
    getRSSFeed('http://www.abc.net.au/news/feed/51120/rss.xml')
    getRSSFeed('http://www.abc.net.au/news/feed/45910/rss.xml')
    getRSSFeed('http://www.abc.net.au/news/feed/52278/rss.xml')
    getRSSFeed('http://www.abc.net.au/news/feed/46182/rss.xml')

    getRSSFeed('http://news.yahoo.com/rss/topstories')
    getRSSFeed('http://news.yahoo.com/rss/')
    getRSSFeed('http://news.yahoo.com/rss/world')

#scrapeFeeds()
getRSSFeed("http://blogs.defensenews.com/rss-feed/?sitename=Def-Regions") #Defence News
