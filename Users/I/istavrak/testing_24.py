import scraperwiki,re
from bs4 import BeautifulSoup

starting_url = 'http://www.tripadvisor.com/Hotel_Review-g190445-d235610-Reviews-Hilton_Innsbruck-Innsbruck_Tirol_Austrian_Alps.html'
start_review_url = 'http://www.tripadvisor.com/Hotel_Review-g190445-d235610-Reviews-or'
end_review_url= '-Hilton_Innsbruck-Innsbruck_Tirol_Austrian_Alps.html'


hotelDetails = {}
record = {}
responseTable = {}

html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

#Retrieve the hotel name
hNameNode =soup.find("h1", { "property" : "v:name" })
if not (hNameNode is None):
    hNameNode = hNameNode.prettify().split('</span>')
    print hNameNode
    hName = hNameNode[1][1:-7]
    hotelDetails['Hotel']=hName
    print hName

#Retrieve the hotel stars
hStarsNode =soup.find("div", { "class" : "stars" })
if not (hStarsNode is None):
    hStarsNode = hStarsNode.prettify().split('content="')
    print hStarsNode
    hStars = hStarsNode[1][0:3]
    hotelDetails['Stars']= hStars
    print hStars

#Retrieve the reviewing chart
for levels in soup.find_all("ul", { "class" : "barChart" }):
    #levels =soup.find("ul", { "class" : "barChart" })
    print levels
    if not (levels is None):
        levels = levels.prettify().split('<div class="wrap row">')
        for level in levels:
            #print level
            levelHtml=BeautifulSoup(level)
            levelText = levelHtml.find("span", { "class" : "text" })
            if not (levelText is None):
                levelText = levelText.prettify().split('>')
                PerformanceTitle=levelText[1][1:-7]
                record['Performance']=levelText[1][1:-7]
    
            
            levelText = levelHtml.find("span", { "class" : "compositeCount" })
            if not (levelText is None):
                        levelText = levelText.prettify().split('>')
                        record['Reviewers']=levelText[1][1:-7]
                        record['Hotelkey']=hName+PerformanceTitle
                        scraperwiki.sqlite.save(['Hotelkey'],record)

#Retrieve the reviews and check if the hotelier has replied to any
NReviewsHtml = soup.find("h3", {"class" : "reviews_header"})
if not (NReviewsHtml is None):
    NReviewsHtml = NReviewsHtml.prettify().split('>')
    number = NReviewsHtml[1].split(' reviews')
    NReviews = int(number[0])
    hotelDetails['Reviews']=NReviews
    scraperwiki.sqlite.save(['Hotel'], hotelDetails)
    for x in range(0, (NReviews+10)/10):
        review_url = start_review_url+str(x*10)+end_review_url
        #print review_url
        htmlR = scraperwiki.scrape(review_url)
        soupR = BeautifulSoup(htmlR)
        #print soupR
        
        
        reviews =soupR.find_all("div", { "class" : "reviewSelector" })
        if not (reviews is None):
            counter1=0
            counter2=0
            counter3=0
            counter4=0
            counter5=0
            TotalCounter=0
            
            for a_review in reviews:
                #Retrieve the rating
                #ratingHtml=BeautifulSoup(a_review)
                response=a_review.find_all("div", { "class" : "mgrRspnInline" })
                for a_response in response:
                    ratingNode =a_review.find("img", { "class" : "sprite-ratings" })
                    if not (ratingNode is None):
                        ratingNode= ratingNode.prettify().split('content="')
                        print ratingNode
                        rating= float(ratingNode[1][0:3])
                        if rating>=1 and rating<2:
                            counter1=counter1+1 
                        elif rating>=2 and rating<3:
                            counter2=counter2+1
                        elif rating>=3 and rating<4:
                            counter3=counter3+1
                        elif rating>=4 and rating<5:
                            counter4=counter4+1
                        elif rating>=5:
                            counter5=counter5+1            
                        print rating
                        TotalCounter=counter1+counter2+counter3+counter4+counter5


            
            if TotalCounter>0:
                responseTable['Times']=TotalCounter
                responseTable['Times1']=counter1
                responseTable['Times2']=counter2
                responseTable['Times3']=counter3
                responseTable['Times4']=counter4
                responseTable['Times5']=counter5
                responseTable['reviewSpan']= x*10
                responseTable['url']= review_url
                scraperwiki.sqlite.save(['url'], responseTable)
