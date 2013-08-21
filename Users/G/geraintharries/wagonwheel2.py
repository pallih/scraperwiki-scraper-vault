import scraperwiki
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re
#import MySQLdb

fields = ['id VARCHAR UNIQUE PRIMARY KEY', 'aaa VARCHAR' ]
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS test (%s)" % ", ".join(fields))


count = 0
start = 2000
limit = 4000
id = 0

ids = [4693, 3391, 4715, 1229, 1355, 2839, 3308, 1759, 3593, 1084, 782, 4578, 4343, 4465, 8153, 2905, 3629, 4601, 4000, 4122, 1906, 4178, 8270, 3028, 2170, 2427, 1045, 2743, 2207, 2699, 3602, 1237, 1377, 4464, 1160, 1168, 2262, 2028, 1996, 3266, 4313, 4314, 2354, 3032, 4501, 2243, 2831, 4321, 3417, 986, 2195, 8152, 4574, 2934, 8374, 4511, 4504, 4718, 2419, 4426, 3306, 4496, 2346, 8336, 1578, 933, 2690, 1977, 3250, 2200, 1281, 3440, 2984, 4339, 4258, 3674, 3793, 3934, 3524, 4069, 3483, 4024, 1297, 4643, 1294, 982, 990, 8250, 3510, 1064, 1015, 2296, 1699, 3461, 3552, 2672, 1412, 1040, 4249, 1032, 872, 4408, 3109, 932, 3739, 4463, 1033, 1191, 1895, 2053, 1130, 1823, 3997, 1024, 3688, 4449]
out = []
for i in ids:
    myString = str(i)
    webpage = urlopen("http://www.cpshomes.co.uk/lettings/properties/property_details.aspx?reference=P"+myString).read()

    regexFindPostcode = re.compile('Postcode: (.*)</span></li>')
    regexFindTitle = re.compile('class="open">(.*)</a></h1>')
    regexFindRooms = re.compile('Bedrooms: (.*)</span></li><li title="Number of reception rooms"><span>')
    regexFindPrice = re.compile('Price: (.*)</span></li><li title="Available"><span>')
    regexFindDescription = re.compile('<div class="fulldetails"><p>(.*)</div><h2>')

    post = re.findall(regexFindPostcode, webpage)
    title = re.findall(regexFindTitle, webpage)
    rooms = re.findall(regexFindRooms, webpage)
    price = re.findall(regexFindPrice, webpage)
    description = re.findall(regexFindDescription, webpage)
    link = re.findall(regexFindDescription, webpage)

    if len(post) == 0:
        print myString + ":Empty Page"
    else:
        print post + title + rooms + price + description
        #out.append(post + title + rooms + price + description)
#    print "1"
#    db = MySQLdb.connect("localhost.blockbe.net","blockbe","XXXXXXXXXX","blockben_hackteam") 
#    print "2"    
#    cursor = db.cursor()
#    print "3"    
#    query = "INSERT INTO property ('%i, %s, %s, %s, %s, %s, %s') VALUES" % (id, title, post, link, rooms, price, description)
#    print "4"
#    db.close()
#scraperwiki.sqlite.save(['id'], out, table_name='test')