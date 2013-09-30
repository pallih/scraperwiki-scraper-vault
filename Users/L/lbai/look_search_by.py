import scraperwiki
import lxml.html
import re

#like look_search, but filters by value

baseurl = "http://lookbook.nu/"
link = baseurl + "looks?q="

search_topics = [
"chic",
"classic",
"vintage",
"edgy",
"hipster"
]

idre = re.compile('\D+(\d+)')
widthre = re.compile('width:(\d+)px')
heightre = re.compile('.*height:(\d+)px')

for look in search_topics:
    url = link + "/" + str(look) + "/"
    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)

    #for each minilook on the page, pull the page
    for minilook in root.cssselect("li.minilook"):
        style = {}
        style['id'] = minilook.get("lookid")
        style['link'] = baseurl + "look/" + style['id']

        #we scrape the product page
        product = scraperwiki.scrape(style['link'])
        proot = lxml.html.fromstring(product)
        
        style['content'] = proot.cssselect("title")[0].text_content()
        sizes = proot.cssselect("div.look_photo")[0].get("style")
        style['width'] = widthre.match(sizes).group(1)
        style['height'] = heightre.match(sizes).group(1)

        style['img'] = proot.cssselect("img")[1].get("src")
        
        #scrape the brands associated
        b = ""
        for row in proot.cssselect("ol li.linespaced"):
            b += row.text_content()
        style["brands"] = b
    
        #get additional meta data
        for meta in proot.cssselect("meta"):
            if meta.get("name") == "keywords":
                style['keywords'] = meta.get("content")
    
            value = meta.get("property")
            if value == "og:description":
                style['description'] = meta.get("content")
            elif value == "og:image": #small version of image
                style['small_img'] = meta.get("content")   
        
        style['look'] = look

        #save the record
        scraperwiki.sqlite.save(["id"], style)
    
import scraperwiki
import lxml.html
import re

#like look_search, but filters by value

baseurl = "http://lookbook.nu/"
link = baseurl + "looks?q="

search_topics = [
"chic",
"classic",
"vintage",
"edgy",
"hipster"
]

idre = re.compile('\D+(\d+)')
widthre = re.compile('width:(\d+)px')
heightre = re.compile('.*height:(\d+)px')

for look in search_topics:
    url = link + "/" + str(look) + "/"
    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)

    #for each minilook on the page, pull the page
    for minilook in root.cssselect("li.minilook"):
        style = {}
        style['id'] = minilook.get("lookid")
        style['link'] = baseurl + "look/" + style['id']

        #we scrape the product page
        product = scraperwiki.scrape(style['link'])
        proot = lxml.html.fromstring(product)
        
        style['content'] = proot.cssselect("title")[0].text_content()
        sizes = proot.cssselect("div.look_photo")[0].get("style")
        style['width'] = widthre.match(sizes).group(1)
        style['height'] = heightre.match(sizes).group(1)

        style['img'] = proot.cssselect("img")[1].get("src")
        
        #scrape the brands associated
        b = ""
        for row in proot.cssselect("ol li.linespaced"):
            b += row.text_content()
        style["brands"] = b
    
        #get additional meta data
        for meta in proot.cssselect("meta"):
            if meta.get("name") == "keywords":
                style['keywords'] = meta.get("content")
    
            value = meta.get("property")
            if value == "og:description":
                style['description'] = meta.get("content")
            elif value == "og:image": #small version of image
                style['small_img'] = meta.get("content")   
        
        style['look'] = look

        #save the record
        scraperwiki.sqlite.save(["id"], style)
    
