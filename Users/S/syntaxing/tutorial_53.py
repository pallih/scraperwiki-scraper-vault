import scraperwiki
import lxml.html

  
url = "http://www.techbargains.com/recentnews.cfm"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
    
    

for main in root.cssselect("div.CBoxTDealStyling"):

    #scraperwiki.sqlite.save(unique_keys=["title"], data={"title":main.text, "link": main.attrib['href']})   
    title =  main.cssselect('div.upperrightSort a')
    orig_price = main.cssselect("div.strikedtext")
    cheap_price = main.cssselect("div.redboldtext") 


    try:
        scraperwiki.sqlite.save(unique_keys=["title"], data={"title":title[0].text, "original price":orig_price[0].text,"discounted price":cheap_price[0].text})
    except IndexError:
        pass


