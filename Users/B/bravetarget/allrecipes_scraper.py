import scraperwiki
import lxml.html 

pageNum = 2171
recID = 42606

while pageNum < 2210:
    pageNum += 1
    html = scraperwiki.scrape("http://allrecipes.com/recipes/ViewAll.aspx?Page=" + str(pageNum))
    root = lxml.html.fromstring(html)

    for el in root.cssselect("table.rectable div.rectitlediv h3 a"):
        try:
            detailURL = el.attrib['href']
            recHtml = scraperwiki.scrape(detailURL)
            recRoot = lxml.html.fromstring(recHtml)
            ingrStr = ""
            ingrAmtStr = ""
            dirStr = ""
            cookStr = ""
            imgURL = ""
            popularity = 0
            for recEl in recRoot.cssselect("span.ingredient-amount"):
                ingrAmtStr += " | " + recEl.text
            for recEl in recRoot.cssselect("span.ingredient-name"):
                ingrStr += " | " + recEl.text
            for recEl in recRoot.cssselect("span.plaincharacterwrap"):
                dirStr += " | " + recEl.text
        
            try:
                timeEl = recRoot.cssselect("time#timeTotal")[0]
                cookStr = timeEl.attrib['datetime']
            except:
                cookStr = "PT1HR30M"

            try: 
                popEl = recRoot.cssselect("meta#metaReviewCount")[0]
                popularity = int(popEl.attrib['content'])
            except:
                popularity = 0
    
            try: 
                imgEl = recRoot.cssselect("meta#metaOpenGraphImage")[0]
                imgURL = imgEl.attrib['content']
            except:
                imgURL = "X"

        except:
            print "detail scrape failed"
            
        try:
            scraperwiki.sqlite.save(unique_keys=["recipe_id"], data={"recipe_id":recID, "recipe_title":el.text, "ingredients":ingrStr, "ingr_amount":ingrAmtStr, "directions":dirStr, "cook_time":cookStr, "popularity":popularity, "img_url":imgURL})
            recID += 1
        except:
            print "db locked"
            
        
    # print el.text
    # print el.attrib['href']



# Blank Python

