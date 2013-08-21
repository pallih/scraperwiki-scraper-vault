import scraperwiki
import lxml.html
from lxml import etree
import re
import hashlib
import time
# Blank Python


def md5(txt):
    m = hashlib.md5(txt)
    return str(m.hexdigest())

def removeHtmlTags(html):
    return re.sub("</?(.*?)>","",html, flags=re.DOTALL | re.IGNORECASE)

def getHtmlContent(root):
    return etree.tostring(root)


time_ = str(long(time.time()))

def parseDiv(div, table_name="swdata"):
    lis = div.cssselect("li[class='jav-has-layout']")
    for li in lis:
        a = li.cssselect("h4 a")[0]
        link =  a.attrib['href']
        title = a.text_content()
        votes = int(removeHtmlTags(getHtmlContent(li.cssselect("p[class='votes']")[0])).strip())
        cat, content = parseFikraPage("http://www.fikra.ma"+link)
        data = {'title':title, 'link':link, 'category':cat, 'content':content, 'votes' : votes, 'time' :time_}
        scraperwiki.sqlite.save(unique_keys=['title'], data=data, table_name=table_name)
        scraperwiki.sqlite.execute("update "+table_name+" SET votes= ? WHERE link = ?",[votes, link])




def parseFikraPage(link):
    html = scraperwiki.scrape(link)
    root  = lxml.html.fromstring(html)
    divcontent = root.cssselect("div[class='jav-item-details-content']")[0]
    cat = divcontent.cssselect("span")[0].text_content()
    pcontent = divcontent.cssselect("div p")

    if len(pcontent) > 0:
        content = pcontent[0].text_content()
    else:
        content = "empty"
    
    return cat, content


"""
html2 = scraperwiki.scrape("http://www.fikra.ma/index.php?option=com_javoice&view=items&layout=item&cid=3015&type=4&Itemid=53")

hata = {"id":1, "html":html}
scraperwiki.sqlite.save(unique_keys=['id'], data=hata, table_name="html")
hata = {"id":2, "html":html2}
scraperwiki.sqlite.save(unique_keys=['id'], data=hata, table_name="html")
"""

#html = scraperwiki.sqlite.select("* from html WHERE id = 1")[0]['html']
#print html

html = scraperwiki.scrape("http://www.fikra.ma/")
root  = lxml.html.fromstring(html)

#print parseFikraPage(root)

div = root.cssselect("div[class='moduletable']")

parseDiv(div[0],"new")
parseDiv(div[1],"hot")
"""
ul = root.cssselect("ul[class='overview'] li")


for li in ul:
    text = etree.tostring(li)
    td, typee = findTd(li)
    title = td.text_content()
    content = (re.sub("</?(.*?)>", "", text, flags= re.DOTALL | re.IGNORECASE)).strip()
    hash = md5(content)
    data = {"hash":hash, "time":time_, "title":title, "content":content, "type":typee}
    scraperwiki.sqlite.save(unique_keys=['hash'], data=data, table_name="promo") """
