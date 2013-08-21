import scraperwiki
import requests
import lxml.html

html = requests.get("http://blog.ups.com").content
dom = lxml.html.fromstring(html)

for entry in dom.cssselect('.theentry'):
    post = {
        'title': entry.cssselect('.entry-title')[0].text_content(),
        'author': entry.cssselect('.the-meta a')[0].text_content(),
        'url': entry.cssselect('a')[0].get('href'),
        'comments': int( entry.cssselect('.comment-number')[0].text_content() ),
        'category': entry.cssselect('table a')[0].text_content()
    }
    print post
    
    scraperwiki.sqlite.save(['url'], post)