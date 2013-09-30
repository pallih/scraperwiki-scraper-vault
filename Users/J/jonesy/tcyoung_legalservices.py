import scraperwiki
import re
from lxml import html
from lxml import etree

def get_content(url, title):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div#internalmiddleColumnservices")

    if len(article) > 0:
        
        h2 = article[0].cssselect('h2').pop()
        text = innerHTML(article[0])
        
        #print text

        data = {
            'title':title,
            'content': text,
            'url':url,
            'h2':h2.text
        }

        scraperwiki.sqlite.save(unique_keys=["title"], data=data)

def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.tcyoung.co.uk/Legal_Services/Adult_Incapacity_Law.aspx"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)


for link in doc.xpath('//*[@id="left"]/ul/li/a'):
    uri = link.cssselect('a').pop().get('href')
    split = uri.split('/')
    title = link.cssselect('a').pop().text_content()
    href = "http://www.tcyoung.co.uk/Legal_Services/"+split[-1]
    get_content(href, title )import scraperwiki
import re
from lxml import html
from lxml import etree

def get_content(url, title):
    doc_text = scraperwiki.scrape(url)
    doc = html.fromstring(doc_text)

    article = doc.cssselect("div#internalmiddleColumnservices")

    if len(article) > 0:
        
        h2 = article[0].cssselect('h2').pop()
        text = innerHTML(article[0])
        
        #print text

        data = {
            'title':title,
            'content': text,
            'url':url,
            'h2':h2.text
        }

        scraperwiki.sqlite.save(unique_keys=["title"], data=data)

def innerHTML(node): 
    buildString = ''
    for child in node:
        buildString += html.tostring(child)
    return buildString

url = "http://www.tcyoung.co.uk/Legal_Services/Adult_Incapacity_Law.aspx"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)


for link in doc.xpath('//*[@id="left"]/ul/li/a'):
    uri = link.cssselect('a').pop().get('href')
    split = uri.split('/')
    title = link.cssselect('a').pop().text_content()
    href = "http://www.tcyoung.co.uk/Legal_Services/"+split[-1]
    get_content(href, title )