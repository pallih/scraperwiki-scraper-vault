import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup



def scrape_table(soup):
    #find table class="reports"
    parent_div = soup.find("div", { "id" : "posts" })
    if parent_div:
        #find each table row <tr>
        divs = parent_div.findAll("div",{"class" : "page"})
        #for each row, loop through this
        for div in divs:
            #create a record to hold the data
            record = {}
            #find each cell <td>
            postbody = div.find("div",{"class" : "postbody"})
            bikeImg = postbody.find("img")
            #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            if bikeImg: 
                if bikeImg.get('src') != 'http://static.lfgss.com/images/londonfgss/buttons_lite/viewpost.gif':
                    record['image'] = bikeImg.get('src')
                    print(record)
                    # Save the record to the datastore - 'id' is our unique key - 
                    scraperwiki.sqlite.save(['image'], record)


startingpage = 1006

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.lfgss.com/thread29-'+str(startingpage)+'.html' #Getbike porn thread

#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
br.set_debug_responses(True)
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'
response = br.open(starting_url)

soup = BeautifulSoup(response.read())
#need to do a loop through the "Next" buttons here
page = startingpage
scrape_table(soup)
while soup.find("a", { "href" : "http://www.lfgss.com/thread29-"+ str(page+1)+".html" }):
    print ("page : "+str(page))
    if page>startingpage:
        response = br.open("http://www.lfgss.com/thread29-"+ str(page+1)+".html")
        #create soup object by reading the contents of response and passing it through BeautifulSoup
        soup = BeautifulSoup(br.response().read())
        scrape_table(soup)
    page = page +1


import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup



def scrape_table(soup):
    #find table class="reports"
    parent_div = soup.find("div", { "id" : "posts" })
    if parent_div:
        #find each table row <tr>
        divs = parent_div.findAll("div",{"class" : "page"})
        #for each row, loop through this
        for div in divs:
            #create a record to hold the data
            record = {}
            #find each cell <td>
            postbody = div.find("div",{"class" : "postbody"})
            bikeImg = postbody.find("img")
            #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            if bikeImg: 
                if bikeImg.get('src') != 'http://static.lfgss.com/images/londonfgss/buttons_lite/viewpost.gif':
                    record['image'] = bikeImg.get('src')
                    print(record)
                    # Save the record to the datastore - 'id' is our unique key - 
                    scraperwiki.sqlite.save(['image'], record)


startingpage = 1006

#set the URL containing the form we need to open with mechanize
starting_url = 'http://www.lfgss.com/thread29-'+str(startingpage)+'.html' #Getbike porn thread

#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
br.set_debug_responses(True)
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'
response = br.open(starting_url)

soup = BeautifulSoup(response.read())
#need to do a loop through the "Next" buttons here
page = startingpage
scrape_table(soup)
while soup.find("a", { "href" : "http://www.lfgss.com/thread29-"+ str(page+1)+".html" }):
    print ("page : "+str(page))
    if page>startingpage:
        response = br.open("http://www.lfgss.com/thread29-"+ str(page+1)+".html")
        #create soup object by reading the contents of response and passing it through BeautifulSoup
        soup = BeautifulSoup(br.response().read())
        scrape_table(soup)
    page = page +1


