import scraperwiki
import lxml.html

ListadePosts = 'http://http://blogueirasfeministas.com/'
keywords = ["vitima", "violencia", "mulher", "saude"]

def pegar_root_da_url(url):
    doc = lxml.html.parse(url)
    return doc.getroot()



