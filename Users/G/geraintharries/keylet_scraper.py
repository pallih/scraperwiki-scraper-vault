import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re
import MySQLdb

count = 0
start = 2049
limit = 4000

for i in range(start, limit):
   myString = str(i)
   webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P"+myString).read()

   regexFindPostcode = re.compile('Postcode: (.*)</span></li>')
   regexFindTitle = re.compile('class="open">(.*)</a></h1>')
   regexFindRooms = re.compile('Bedrooms: (.*)</span></li><li title="Number of reception rooms"><span>')
   regexFindPrice = re.compile('Price: £(.*)</span></li><li title="Available"><span>')
   regexFindDescription = re.compile('<div class="fulldetails"><p>(.*)</div><h2>')

   #print ref
   post = re.findall(regexFindPostcode, webpage)
   title = re.findall(regexFindTitle, webpage)
   rooms = re.findall(regexFindRooms, webpage)
   price = re.findall(regexFindPrice, webpage)
   description = re.findall(regexFindDescription, webpage)
   link = re.findall(regexFindDescription, webpage)

   #print post + title + rooms + price + description


    
    

    
   #print post

   if len(post) == 0:
     print myString + ":Empty Page"
   else:
     
     db = MySQLdb.connect("localhost.blockbe.net","blokcben","TwX62!Em1","blockben_hackteam")
     cursor = db.cursor()
     query = "INSERT INTO defaces VALUES ('%s')" % (post)
     try:
       cursor.execute(query)
       db.commit()
     except Exception, e:
       db.rollback()
     print e
     db.close()



     print post + title + rooms + price + description
     count += 1
     print count