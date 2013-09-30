import scraperwiki
import lxml.html
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape("http://www.lespros.co.jp/artists/yui_aragaki/archive.html")

soup = BeautifulSoup(html)

news = soup.find('div',{'class':'news_item_content'})

for i in news.findAll('h3'):
    print i.a.img.get('alt')
    i.a.img.extract()
    print i.a.contents[0]
    print i.nextSibling.nextSibling.renderContents()

    import scraperwiki
import lxml.html
from BeautifulSoup import BeautifulSoup

html = scraperwiki.scrape("http://www.lespros.co.jp/artists/yui_aragaki/archive.html")

soup = BeautifulSoup(html)

news = soup.find('div',{'class':'news_item_content'})

for i in news.findAll('h3'):
    print i.a.img.get('alt')
    i.a.img.extract()
    print i.a.contents[0]
    print i.nextSibling.nextSibling.renderContents()

    