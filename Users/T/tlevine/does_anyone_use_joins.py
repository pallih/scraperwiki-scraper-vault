from scraperwiki.sqlite import attach,select,save,execute,commit, show_tables
from json import loads
from urllib2 import urlopen
from lxml.html import fromstring,tostring

def copyUrlsDb():
    attach('scraperwiki_scraper_urls')
    save(['url'],select('url,0 as "scraped" from scraper_urls'),'urls')

def getUrls():
    urls=select('url from urls where `scraped`=0;')
    return [row['url'] for row in urls]

def getScraperSlug(url):
    if url[0:7]=="/views/":
        return url[7:-1]
    elif url[0:10]=="/scrapers/":
        return url[10:-1]
    else:
        raise ValueError

def getCode(slug):
    codeinfo = loads(urlopen("https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=%s&version=-1" % slug).read())[0]
    if "error" in codeinfo:
        return None, None
    else:
        try:
            return codeinfo['code'], codeinfo["userroles"]["owner"][0]
        except:
            return codeinfo['code'], None

def main():
    if "urls" not in show_tables():
        copyUrlsDb()
    for url in getUrls():
        slug = getScraperSlug(url)
        code, user = getCode(slug)
        if code != None:
            c = code.lower()
            save(['url'], {
                "code":code, "user": user, "url": url,
                "has_join": " join " in c,
                "has_attach": "attach" in c,
                "has_twitter": "twitter" in c,
            })
        execute('UPDATE `urls` SET `scraped`=1 WHERE `url` = ?', url)
        commit()

    d = select('`user`, count(*) AS "attach-and-join-count" from `swdata` WHERE (`has_join` = 1 and `has_attach` = 1) GROUP BY `user`')
    save(['user'], d, 'results')

main()