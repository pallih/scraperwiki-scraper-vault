import scraperwiki
import lxml.html
import re

index = 0
scraperwiki.sqlite.execute("delete from newsData");
html = scraperwiki.scrape("http://www.behindwoods.com/features/News/News23/index.html")
root = lxml.html.fromstring(html)

bw_newsList = root.cssselect("a[class='tamil-movies-news-b']")

for movie in bw_newsList:
    bw_news_url = "http://www.behindwoods.com" + movie.attrib['href']   

    html2 = scraperwiki.scrape(bw_news_url)
    root2 = lxml.html.fromstring(html2)


    bw_news_date = root2.cssselect("table > tr:nth-child(3) > td[class = 'tamil-movies-news-head-t']")
    bw_news_detail = root2.cssselect("td[class = 'tamil-movies-content']")
    bw_news_image = root2.cssselect("div[class = 'c4'] > table > tr > td > img")

    bw_image_url = ""    
    if bw_news_image[0].attrib['src']:
        bw_image_url = "http://www.behindwoods.com" + bw_news_image[0].attrib['src']

    #format data
    newsTitle  =  movie.text #re.sub("(([\s]{2,})|([\n]))", "", movie.text)
    newsDetail = bw_news_detail[0].text_content() #re.sub("(([\s]{2,})|([\n]))", "", bw_news_detail[0].text_content())
    newsDate   = bw_news_date[0].text_content() #re.sub("(([\s]{2,})|([\n]))", "", bw_news_date[0].text_content())

    index = index + 1

    data = {
            "index" : index,
            "title" : newsTitle,
            "detail": newsDetail,
            "image" : bw_image_url,
            "site"  : bw_news_url,
            "date"  : newsDate,
            "source": "Behind Woods"
            }   

    print scraperwiki.sqlite.save(unique_keys=['index'], table_name="newsData", data=data)import scraperwiki
import lxml.html
import re

index = 0
scraperwiki.sqlite.execute("delete from newsData");
html = scraperwiki.scrape("http://www.behindwoods.com/features/News/News23/index.html")
root = lxml.html.fromstring(html)

bw_newsList = root.cssselect("a[class='tamil-movies-news-b']")

for movie in bw_newsList:
    bw_news_url = "http://www.behindwoods.com" + movie.attrib['href']   

    html2 = scraperwiki.scrape(bw_news_url)
    root2 = lxml.html.fromstring(html2)


    bw_news_date = root2.cssselect("table > tr:nth-child(3) > td[class = 'tamil-movies-news-head-t']")
    bw_news_detail = root2.cssselect("td[class = 'tamil-movies-content']")
    bw_news_image = root2.cssselect("div[class = 'c4'] > table > tr > td > img")

    bw_image_url = ""    
    if bw_news_image[0].attrib['src']:
        bw_image_url = "http://www.behindwoods.com" + bw_news_image[0].attrib['src']

    #format data
    newsTitle  =  movie.text #re.sub("(([\s]{2,})|([\n]))", "", movie.text)
    newsDetail = bw_news_detail[0].text_content() #re.sub("(([\s]{2,})|([\n]))", "", bw_news_detail[0].text_content())
    newsDate   = bw_news_date[0].text_content() #re.sub("(([\s]{2,})|([\n]))", "", bw_news_date[0].text_content())

    index = index + 1

    data = {
            "index" : index,
            "title" : newsTitle,
            "detail": newsDetail,
            "image" : bw_image_url,
            "site"  : bw_news_url,
            "date"  : newsDate,
            "source": "Behind Woods"
            }   

    print scraperwiki.sqlite.save(unique_keys=['index'], table_name="newsData", data=data)