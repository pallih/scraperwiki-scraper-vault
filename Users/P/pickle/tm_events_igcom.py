import scraperwiki as sw
import lxml.html

urlTamil = "http://www.indiaglitz.com/channels/tamil/articles.asp"
urlHindi = "http://www.indiaglitz.com/channels/hindi/articles.asp"
urlTelugu = "http://www.indiaglitz.com/channels/telugu/articles.asp"
urlMalayalam = "http://www.indiaglitz.com/channels/malayalam/articles.asp"
source = "indiaglitz"

urls = [urlTamil, urlHindi, urlTelugu, urlMalayalam]
urlOrder = ['tamil', 'hindi', 'telugu', 'malayalam']

def main():
    for loop in range(0, len(urls)): 
        html = sw.scrape(urls[loop])
        root = lxml.html.fromstring(html)

        print urls[loop]
        print urlOrder[loop] + "NewsData"

        newsArticles =root.cssselect("td[class='black']")
          
        counter = 1  #counter for article looping
    
        for article in newsArticles:
            data = dataFromArticle(counter, article)
            if data == "skip":
                continue
            elif data:
                tblName = urlOrder[loop] + "NewsData"
                sw.sqlite.save(unique_keys=['index'], table_name=tblName, data=data)
                counter += 1
            else:
                break


#get data from individual article
def dataFromArticle(counter, article):
    root = lxml.html.fromstring(lxml.html.tostring(article))
        
    try:
        title = root.cssselect("h2 > a")[0].text
        articleUrl = root.cssselect("td > a")[0].attrib['href']
        date = root.cssselect("td > div[class='gray']")[0].text
        image = root.cssselect("td > a > img")[0].attrib['src']
        text =  root.cssselect("td > a")[0].text_content()
    
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
main()