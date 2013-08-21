import scraperwiki
import lxml.html
import lxml.etree
import re
import urllib
import datetime
import dateutil

# Parse imdb
def parse_imdb(url, data):
    print "Parsing " + url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    img_td = root.cssselect("td[id='img_primary']")
    top_td = root.cssselect("td[id='overview-top']")
    btm_td = root.cssselect("td[id='overview-bottom']")
    if len(img_td) == 1 and len(top_td) == 1 and len(btm_td) == 1:
        data['imdb'] = url

        # Image
        elem_img = img_td[0].cssselect("div a img")
        if len(elem_img) > 0:
             data['img'] = elem_img[0].get("src")

        data['title'] = top_td[0].cssselect("h1[class='header'] span[itemprop='name']")[0].text_content()
        data['year']  = top_td[0].cssselect("h1[class='header'] span[class='nobr']")[0].text_content()
        
        # Genre
        data['genre'] = ""
        for sp in top_td[0].cssselect("div[class='infobar'] a span[itemprop='genre']"):
            data['genre'] = data['genre'] + " " + sp.text_content()
        
        # Rating
        elem_rating = top_td[0].cssselect("div[class='star-box giga-star'] div")[0].text_content()
        rating_match = re.search(r'\d+.\d*', elem_rating)
        if rating_match:
            data['rating'] = rating_match.group()
        
        # Description
        elem_descr = top_td[0].cssselect("p[itemprop='description']")
        if len(elem_descr) > 0:
            data['description'] = elem_descr[0].text_content()

        # Trailer
        elem_trailer = btm_td[0].cssselect("a[itemprop='trailer']")
        if len(elem_trailer) > 0:
            data['trailer'] = "http://www.imdb.com" + elem_trailer[0].get("href")
    return data

# Parse one nfo
def parse_nfo(url, data):
    print "Parsing " + url
    html = scraperwiki.scrape(url)
    imdb_match = re.search(r'imdb.com/title/tt[a-z0-9]+', html)
    if imdb_match > 0:
        parse_imdb("http://www." + imdb_match.group(), data)
    return data

def load_data(url):
    try:
        data_list = scraperwiki.sqlite.select("* from swdata where url = ?", url)
        if data_list:
            return data_list[0]
    except scraperwiki.sqlite.SqliteError, e:
        print str(e)

# Parse one rss item
def parse_rssitem(item):
    url = item.xpath("./enclosure")[0].get('url')
    pubdate = item.xpath("./pubDate")[0].text
    data = load_data(url)
    if not data:
        data = {'url': url, 
                'pubdate': pubdate, 
                'added': datetime.datetime.strptime(pubdate[:-6], "%a, %d %b %Y %H:%M:%S")}
        descr = item.xpath("./description")[0].text
        nfo_match = re.search(r'href=\"(.+?)\"', descr)
        if nfo_match:
            parse_nfo(nfo_match.group(1), data)
        if data.get('title'):
            print "Saving: " + data.get('title')
            scraperwiki.sqlite.save(unique_keys=['url'], data=data)

# Parse the rss feed
def parse_rssfeed(url):
    html = scraperwiki.scrape(url)
    parser = lxml.etree.XMLParser(strip_cdata=False)
    root = lxml.etree.fromstring(html, parser)
    for item in root.xpath('//rss/channel/item'):
        parse_rssitem(item)

# Main
parse_rssfeed("http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=10&links=preserve&exc=&submit=Create+Feed")
#parse_nfo("http://www.nzbindex.nl/nfo/85399855/TR-720p0070-Conviction.2010.720p.BluRay.TRsub.x264.DTS.ShareKiosk.nzb/?q=", {})
#data = {}
#parse_imdb("http://www.imdb.com/title/tt0882977/", data)
#print data

