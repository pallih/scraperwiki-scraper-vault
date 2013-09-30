import scraperwiki as sw
import lxml.html
import urllib
import re

#todo : delete old data before update

urlTamil = "http://tamil.way2movies.com/news_tamil.html?cat=3&page=1"
urlHindi = "http://hindi.way2movies.com/news_hindi.html?cat=4&page=1"
urlTelugu = "http://telugu.way2movies.com/news_telugu.html?cat=4&page=1"

source = "way2movies"

urls = [urlTamil, urlHindi, urlTelugu]
urlOrder = ['tamil', 'hindi', 'telugu']

def main():
    for loop in range(0, len(urls)): 
        html = sw.scrape(urls[loop])
        root = lxml.html.fromstring(html)

        print urls[loop]
        print urlOrder[loop] + "NewsData"

        newsArticles =root.cssselect("div[class='newslist'] > div[class='news-box']")
          
        counter = 1  #counter for article looping
    
        for article in newsArticles:
            data = dataFromArticle(counter, article)
            if data == "skip":
                continue
            elif data:
                tblName = urlOrder[loop] + "NewsData"
                #print data
                sw.sqlite.save(unique_keys=['index'], table_name=tblName, data=data)
                counter += 1
            else:
                break


#get data from individual article
def dataFromArticle(counter, article):
    root = lxml.html.fromstring(lxml.html.tostring(article))
    try:
        title = root.cssselect("div[class='news-box'] > div[class='flt discp'] > a > h3 , div[class='news-box'] > div[class='flt discp'] > h3 > a")[0].text.strip(' \t\n\r')
        articleUrl = root.cssselect("div[class='news-box'] > div[class='flt img'] > a")[0].attrib['href'].strip(' \t\n\r')
        date = root.cssselect("div[class='news-box'] > div[class='flt discp'] > div[class='post-date']")[0].text_content().strip(' \t\n\r')
        image = root.cssselect("div[class='news-box'] > div[class='flt img'] > a > img")[0].attrib['src'].strip(' \t\n\r')
        text =  root.cssselect("div[class='news-box'] > div[class='flt discp'] > p")[0].text_content().strip(' \t\n\r')

        title = re.sub("[^\w\s,-:&.]+" , "", title.encode('utf-8'))
        text = re.sub("[^\w\s,-:&.]+" , "", text.encode('utf-8'))
        date = str.split(date, "|")[1].strip(' \t\n\r')      

        if title == None:
            return "skip"

        data = {
            "index" : counter,
            "title" : title,
            "detail": text,
            "image" : image,
            "site"  : articleUrl,
            "date"  : date,
            "source" : source
            }      

        return data

    except IndexError:
        print "try to access outside range : title not present"
        return

    

#call main function
main()\import scraperwiki as sw
import lxml.html
import urllib
import re

#todo : delete old data before update

urlTamil = "http://tamil.way2movies.com/news_tamil.html?cat=3&page=1"
urlHindi = "http://hindi.way2movies.com/news_hindi.html?cat=4&page=1"
urlTelugu = "http://telugu.way2movies.com/news_telugu.html?cat=4&page=1"

source = "way2movies"

urls = [urlTamil, urlHindi, urlTelugu]
urlOrder = ['tamil', 'hindi', 'telugu']

def main():
    for loop in range(0, len(urls)): 
        html = sw.scrape(urls[loop])
        root = lxml.html.fromstring(html)

        print urls[loop]
        print urlOrder[loop] + "NewsData"

        newsArticles =root.cssselect("div[class='newslist'] > div[class='news-box']")
          
        counter = 1  #counter for article looping
    
        for article in newsArticles:
            data = dataFromArticle(counter, article)
            if data == "skip":
                continue
            elif data:
                tblName = urlOrder[loop] + "NewsData"
                #print data
                sw.sqlite.save(unique_keys=['index'], table_name=tblName, data=data)
                counter += 1
            else:
                break


#get data from individual article
def dataFromArticle(counter, article):
    root = lxml.html.fromstring(lxml.html.tostring(article))
    try:
        title = root.cssselect("div[class='news-box'] > div[class='flt discp'] > a > h3 , div[class='news-box'] > div[class='flt discp'] > h3 > a")[0].text.strip(' \t\n\r')
        articleUrl = root.cssselect("div[class='news-box'] > div[class='flt img'] > a")[0].attrib['href'].strip(' \t\n\r')
        date = root.cssselect("div[class='news-box'] > div[class='flt discp'] > div[class='post-date']")[0].text_content().strip(' \t\n\r')
        image = root.cssselect("div[class='news-box'] > div[class='flt img'] > a > img")[0].attrib['src'].strip(' \t\n\r')
        text =  root.cssselect("div[class='news-box'] > div[class='flt discp'] > p")[0].text_content().strip(' \t\n\r')

        title = re.sub("[^\w\s,-:&.]+" , "", title.encode('utf-8'))
        text = re.sub("[^\w\s,-:&.]+" , "", text.encode('utf-8'))
        date = str.split(date, "|")[1].strip(' \t\n\r')      

        if title == None:
            return "skip"

        data = {
            "index" : counter,
            "title" : title,
            "detail": text,
            "image" : image,
            "site"  : articleUrl,
            "date"  : date,
            "source" : source
            }      

        return data

    except IndexError:
        print "try to access outside range : title not present"
        return

    

#call main function
main()\