# Blank Python
#A scrpaer for retrieving NGX data
#Import the main namespace
import scraperwiki
#Assigning the URL to the scrpaer to retrieve all HTML data
html = scraperwiki.scrape('http://www.ngx.com/marketdata/settlements/IASETTLE.html')
#Test printing of HTML
print html
#This namespace can be used for converting the HTML data to XML format
import lxml.html
#root contains the XML formated dataof HTML
root = lxml.html.fromstring(html)
#Test printing of XML format
print root
#To count the 120 rows
i=1
#root.cssselect("table[align='left'] tr") will give the table with rows
#means the line produces the complete table and rows
#looping for eacj row
for tr in root.cssselect("table[align='left'] tr"):
    #To end the loop with 120
    if i<=120:  
        #retrieving the TDs from the row TR
        tds = tr.cssselect("td")
        #Putting the data into an array "data"
        data = {
        'Begin' : tds[0].text_content(),
        'End': tds[1].text_content(),
        'Instrument' : tds[2].text_content(),
        'Settlement' : tds[3].text_content(),
          }
        #Sample printing
        print data
        #Increment i value after printing
        i=i+1
        #daving the data to magic SQLITE data base
        scraperwiki.sqlite.save(data=data)
