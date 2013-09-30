from urllib import urlopen
import urllib
from BeautifulSoup import BeautifulSoup
import re

count = 0
start = 2049
limit = 4000

f = urllib.urlopen("http://www.cpshomes.co.uk/sales/properties/property_list_rss.aspx")


from xml.dom.minidom import parse, parseString
dom1 = parse(f)   # parse an XML file
dom2 = parseString( "<myxml>Some data <empty/> some more data</myxml>" )
print dom1.toxml()
print dom2.toxml()


#######################################################
#
#Data base portion of program
#
#######################################################



db = MySQLdb.connect("dburl","user","password","dbname")
    
cursor = db.cursor()
    
query = "INSERT INTO defaces VALUES ('%s')" % (xml)
    
#query.format(id, url, country, ip, notifier, webserver, system, date, time)
    
db.close()


#######################################################
#
#Regexes and parsing code
#
#######################################################

#from xml.dom.minidom import parse, parseString
#doc= minidom.parse(http://www.cpshomes.co.uk/sales/properties/property_list_rss.aspx)

#parent= doc.documentElement
#children= [child for child in parent.childNodes if child.nodeType==1]
#content= ' '.join([child.firstChild.nodeValue for child in children])

#fp= open(outputFilename, 'wb')
#fp.write(content)
#fp.close()

#webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_list_rss.aspx").read()
#print webpage

#print dom3

#regexFindReference = re.compile('<title xml:space="preserve">(.*)</title><link>')


#ref = re.findall(regexFindReference, webpage)


#print ref
    #post = re.findall(regexFindPostcode, webpage)
    #title = re.findall(regexFindTitle, webpage)
    #rooms = re.findall(regexFindRooms, webpage)
    #price = re.findall(regexFindPrice, webpage)
    #description = re.findall(regexFindDescription, webpage)
    #link = re.findall(regexFindDescription, webpage)

    #print post + title + rooms + price + description

#for i in range(start, limit):
    #myString = str(i)
   # webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P"+myString).read()
    
    #regexFindPostcode = re.compile('Postcode: (.*)</span></li>')
    #regexFindTitle = re.compile('class="open">(.*)</a></h1>')
    #regexFindRooms = re.compile('Bedrooms: (.*)</span></li><li title="Number of reception rooms"><span>')
    #regexFindPrice = re.compile('Price: £(.*)</span></li><li title="Available"><span>')
    #regexFindDescription = re.compile('<div class="fulldetails"><p>(.*)</div><h2>')

    
    #print post

    #if len(post) == 0:
      #  print myString + ":Empty Page"
   # else:
       # print post + title + rooms + price + description
       # count += 1
       # print countfrom urllib import urlopen
import urllib
from BeautifulSoup import BeautifulSoup
import re

count = 0
start = 2049
limit = 4000

f = urllib.urlopen("http://www.cpshomes.co.uk/sales/properties/property_list_rss.aspx")


from xml.dom.minidom import parse, parseString
dom1 = parse(f)   # parse an XML file
dom2 = parseString( "<myxml>Some data <empty/> some more data</myxml>" )
print dom1.toxml()
print dom2.toxml()


#######################################################
#
#Data base portion of program
#
#######################################################



db = MySQLdb.connect("dburl","user","password","dbname")
    
cursor = db.cursor()
    
query = "INSERT INTO defaces VALUES ('%s')" % (xml)
    
#query.format(id, url, country, ip, notifier, webserver, system, date, time)
    
db.close()


#######################################################
#
#Regexes and parsing code
#
#######################################################

#from xml.dom.minidom import parse, parseString
#doc= minidom.parse(http://www.cpshomes.co.uk/sales/properties/property_list_rss.aspx)

#parent= doc.documentElement
#children= [child for child in parent.childNodes if child.nodeType==1]
#content= ' '.join([child.firstChild.nodeValue for child in children])

#fp= open(outputFilename, 'wb')
#fp.write(content)
#fp.close()

#webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_list_rss.aspx").read()
#print webpage

#print dom3

#regexFindReference = re.compile('<title xml:space="preserve">(.*)</title><link>')


#ref = re.findall(regexFindReference, webpage)


#print ref
    #post = re.findall(regexFindPostcode, webpage)
    #title = re.findall(regexFindTitle, webpage)
    #rooms = re.findall(regexFindRooms, webpage)
    #price = re.findall(regexFindPrice, webpage)
    #description = re.findall(regexFindDescription, webpage)
    #link = re.findall(regexFindDescription, webpage)

    #print post + title + rooms + price + description

#for i in range(start, limit):
    #myString = str(i)
   # webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P"+myString).read()
    
    #regexFindPostcode = re.compile('Postcode: (.*)</span></li>')
    #regexFindTitle = re.compile('class="open">(.*)</a></h1>')
    #regexFindRooms = re.compile('Bedrooms: (.*)</span></li><li title="Number of reception rooms"><span>')
    #regexFindPrice = re.compile('Price: £(.*)</span></li><li title="Available"><span>')
    #regexFindDescription = re.compile('<div class="fulldetails"><p>(.*)</div><h2>')

    
    #print post

    #if len(post) == 0:
      #  print myString + ":Empty Page"
   # else:
       # print post + title + rooms + price + description
       # count += 1
       # print count