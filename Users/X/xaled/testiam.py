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



time_ = str(long(time.time()))
td_types = ["lilisteFix","lilisteInternet","lilisteMobile","lilisteMobileVM","lilisteFixVM","lilisteInternetVM"]


def findTd(li):
    for t in td_types:
        td = li.cssselect("td[class='"+t+"']")
        if len(td)>0:
            return td[0],t
    return None, None

html = scraperwiki.scrape("http://www.iam.ma/PROMO/Pages/promo.aspx")

#hata = {"id":1, "html":html}
#scraperwiki.sqlite.save(unique_keys=['id'], data=hata, table_name="html")

#html = scraperwiki.sqlite.select("* from html WHERE id = 1")[0]['html']
#print html

root  = lxml.html.fromstring(html)



ul = root.cssselect("ul[class='overview'] li")


for li in ul:
    text = etree.tostring(li)
    td, typee = findTd(li)
    title = td.text_content()
    content = (re.sub("</?(.*?)>", "", text, flags= re.DOTALL | re.IGNORECASE)).strip()
    hash = md5(content)
    data = {"hash":hash, "time":time_, "title":title, "content":content, "type":typee}
    scraperwiki.sqlite.save(unique_keys=['hash'], data=data, table_name="promo")
    
