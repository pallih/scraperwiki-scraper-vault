import scraperwiki
import lxml.html
import re

index = 0
scraperwiki.sqlite.execute("delete from newsData");
for pageNo in range (1, 4):

    html = scraperwiki.scrape("http://www.sify.com/movies/moreheadlines/category/telugu/page/"+ str(pageNo) +".html")
    root = lxml.html.fromstring(html)

    bw_news_titles  = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-3) > a")
    bw_news_images  = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-1)")
    bw_news_details = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-1)")
    bw_news_dates   = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-2)[style='width:459px;float:left;font-family:Arial;font-size:12px;margin-top:7px;margin-bottom:10px;']")


    for i in range(0, len(bw_news_titles)):
        if bw_news_details[i].text_content() != "":

            index = index + 1
        
            root2   = lxml.html.fromstring(lxml.html.tostring(bw_news_images[i]))  
            n_image = root2.cssselect("div > a > img")
            
            image = ""
            if n_image:
                image =  n_image[0].attrib['src']       
            
            data = {
            "index" : index,
            "title" : bw_news_titles[i].text_content(),
            "detail": bw_news_details[i].text_content(),
            "image" : image,
            "site"  : bw_news_titles[i].attrib['href'],
            "date"  : bw_news_dates[i].text_content(),
            "source" : "Sify Movies"
            }         

            scraperwiki.sqlite.save(unique_keys=['index'], table_name="newsData", data=data)

import scraperwiki
import lxml.html
import re

index = 0
scraperwiki.sqlite.execute("delete from newsData");
for pageNo in range (1, 4):

    html = scraperwiki.scrape("http://www.sify.com/movies/moreheadlines/category/telugu/page/"+ str(pageNo) +".html")
    root = lxml.html.fromstring(html)

    bw_news_titles  = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-3) > a")
    bw_news_images  = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-1)")
    bw_news_details = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-1)")
    bw_news_dates   = root.cssselect("div[style='width:484px;float:left;background-color:#FFFFFF;'] > div > div:nth-child(4n-2)[style='width:459px;float:left;font-family:Arial;font-size:12px;margin-top:7px;margin-bottom:10px;']")


    for i in range(0, len(bw_news_titles)):
        if bw_news_details[i].text_content() != "":

            index = index + 1
        
            root2   = lxml.html.fromstring(lxml.html.tostring(bw_news_images[i]))  
            n_image = root2.cssselect("div > a > img")
            
            image = ""
            if n_image:
                image =  n_image[0].attrib['src']       
            
            data = {
            "index" : index,
            "title" : bw_news_titles[i].text_content(),
            "detail": bw_news_details[i].text_content(),
            "image" : image,
            "site"  : bw_news_titles[i].attrib['href'],
            "date"  : bw_news_dates[i].text_content(),
            "source" : "Sify Movies"
            }         

            scraperwiki.sqlite.save(unique_keys=['index'], table_name="newsData", data=data)

