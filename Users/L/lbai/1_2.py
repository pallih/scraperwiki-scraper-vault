import scraperwiki
import lxml.html
import re

#script starts here
url = "http://lookbook.nu"
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
idre = re.compile('\D+(\d+)')
widthre = re.compile('width:(\d+)px')
heightre = re.compile('.*height:(\d+)px')

for div in root.cssselect("div.look_photo"):
    style = {}
    style['id'] = idre.match(div.get("id")).group(1)
    sizes = div.get("style")
    style['width'] = widthre.match(sizes).group(1)
    style['height'] = heightre.match(sizes).group(1)
    for row in div.cssselect("a"):
        style['link'] = row.get("href")
        style['content'] = row.get("title")

        #we scrape the product page
        product = scraperwiki.scrape(style['link'])
        
        proot = lxml.html.fromstring(product)

        #scrape the brands associated
        b = ""
        n = 1
        for row in proot.cssselect("ol li.linespaced"):
            #b += str(n) + "." + row.cssselect("h2")[0].text_content() + "," + row.cssselect("h3")[0].text_content() + "," + row.cssselect("a")[0].text_content() + "\n"
            #n = n + 1
            b += row.text_content()
        style["brands"] = b

        for meta in proot.cssselect("meta"):
            if meta.get("name") == "keywords":
                style['keywords'] = meta.get("content")

            #get meta data
            value = meta.get("property")
            if value == "og:description":
                style['description'] = meta.get("content")
            elif value == "og:image": #small version of image
                style['small_img'] = meta.get("content")
            

    for img in div.cssselect("img"):
        style['img'] = img.get("src")
        

    #save the record
    scraperwiki.sqlite.save(["id"], style)


