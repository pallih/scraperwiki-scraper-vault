import scraperwiki
import lxml.html

# Blank Python

list="http://open-data.europa.eu/open-data/data/dataset?page=%s"
base="http://open-data.europa.eu"

def get_num():
    html=scraperwiki.scrape(list%1)
    root=lxml.html.fromstring(html)
    pn=root.cssselect(".pagination > ul > li a")[3]
    return int(pn.text_content())

pages=range(101,get_num()+1)

def get_list_from_page(num):
    root=lxml.html.fromstring(scraperwiki.scrape(list%num))
    return [i.get("href") for i in root.cssselect(".datasets .title a")]

def get_text(root,sel,sep=" "):
    return sep.join((i.text_content().strip().rstrip() for i in root.cssselect(sel)))

def get_metadata(url):
    root=lxml.html.fromstring(scraperwiki.scrape("%s%s"%(base,url)))
    metadata={"dataset_url":url}
    metadata["title"]=get_text(root,"h1.page_heading")
    metadata["description"]=get_text(root,"#notes-extract")
    metadata["license"]=get_text(root,"#dataset-license a")
    metadata["formats"]=get_text(root,"span.format-box",",")
    for (k,v) in zip([i for i in root.cssselect(".dataset-label")],[i for i in root.cssselect(".dataset-details")]):
        metadata[str(k.text_content())]=v.text_content()
    
    return metadata

for page in pages:
    for u in get_list_from_page(page):
        scraperwiki.sqlite.save(unique_keys=["dataset_url"],data=get_metadata(u))
import scraperwiki
import lxml.html

# Blank Python

list="http://open-data.europa.eu/open-data/data/dataset?page=%s"
base="http://open-data.europa.eu"

def get_num():
    html=scraperwiki.scrape(list%1)
    root=lxml.html.fromstring(html)
    pn=root.cssselect(".pagination > ul > li a")[3]
    return int(pn.text_content())

pages=range(101,get_num()+1)

def get_list_from_page(num):
    root=lxml.html.fromstring(scraperwiki.scrape(list%num))
    return [i.get("href") for i in root.cssselect(".datasets .title a")]

def get_text(root,sel,sep=" "):
    return sep.join((i.text_content().strip().rstrip() for i in root.cssselect(sel)))

def get_metadata(url):
    root=lxml.html.fromstring(scraperwiki.scrape("%s%s"%(base,url)))
    metadata={"dataset_url":url}
    metadata["title"]=get_text(root,"h1.page_heading")
    metadata["description"]=get_text(root,"#notes-extract")
    metadata["license"]=get_text(root,"#dataset-license a")
    metadata["formats"]=get_text(root,"span.format-box",",")
    for (k,v) in zip([i for i in root.cssselect(".dataset-label")],[i for i in root.cssselect(".dataset-details")]):
        metadata[str(k.text_content())]=v.text_content()
    
    return metadata

for page in pages:
    for u in get_list_from_page(page):
        scraperwiki.sqlite.save(unique_keys=["dataset_url"],data=get_metadata(u))
