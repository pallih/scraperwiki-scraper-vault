import scraperwiki
import re
from lxml import html
from lxml import etree

def get_content(uri, url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div.article")

    if len(article) > 0:
        
        h1 = article[0].cssselect('h1').pop()

        text = innerHTML(article[0])
        
        text = re.sub(r'/images/stories/(?:\w+/)*([\w%\s-]+\.(?:jpg|png|gif|jpeg))', r'{{media url="wysiwyg/\1"}}', text)

        print text

        data = {
            'product':product,
            'content': text,
            'url':url,
            'uri':uri,
            'h1':h1.text
        }

        scraperwiki.sqlite.save(unique_keys=["product"], data=data)

def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.xpath('//*[@id="menu"]/div/ul[1]/li[4]/div/div[2]/div/div/ul/li'):
    uri = link.cssselect('a').pop().get('href')
    product = link.cssselect('span').pop().text_content()
    href = url+uri
    get_content(uri, href, product)

    import scraperwiki
import re
from lxml import html
from lxml import etree

def get_content(uri, url, product):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div.article")

    if len(article) > 0:
        
        h1 = article[0].cssselect('h1').pop()

        text = innerHTML(article[0])
        
        text = re.sub(r'/images/stories/(?:\w+/)*([\w%\s-]+\.(?:jpg|png|gif|jpeg))', r'{{media url="wysiwyg/\1"}}', text)

        print text

        data = {
            'product':product,
            'content': text,
            'url':url,
            'uri':uri,
            'h1':h1.text
        }

        scraperwiki.sqlite.save(unique_keys=["product"], data=data)

def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.water-for-health.co.uk"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for link in doc.xpath('//*[@id="menu"]/div/ul[1]/li[4]/div/div[2]/div/div/ul/li'):
    uri = link.cssselect('a').pop().get('href')
    product = link.cssselect('span').pop().text_content()
    href = url+uri
    get_content(uri, href, product)

    