#A scrpaer for retrieving Top 100 scientists who shaped the worlds history
#Import the main namespace
import scraperwiki
#Assigning the URL to the scrpaer to retrieve all HTML data
html = scraperwiki.scrape('http://www.adherents.com/people/100_scientists.html')
#Test printing of HTML
print html
#This namespace can be used for converting the HTML data to XML format
import lxml.html
#root contains the XML formated dataof HTML
root = lxml.html.fromstring(html)
#Test printing of XML format
print root
#To count the 100 scientists
i=1
#root.cssselect("table[align='center'] tr") will give the table with rows
#means the line produces the complete table and rows
#looping for eacj row
for tr in root.cssselect("table[align='center'] tr"):
    #To end the loop with 100
    if i<=100:   
        #retrieving the TDs from the row TR
        tds = tr.cssselect("td")
        #Putting the data into an array "data"
        data = {
        'sno' : tds[0].text_content(),
        'name': tds[1].text_content(),
        'investigated' : tds[2].text_content()
          }
        #Sample printing
        print data
        #Increment i value after printing
        i=i+1
        #daving the data to magic SQLITE data base
        scraperwiki.sqlite.save(unique_keys=['sno'], data=data)

