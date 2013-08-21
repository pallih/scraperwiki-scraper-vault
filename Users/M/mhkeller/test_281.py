import scraperwiki
import urllib2
#from bs4 import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup




#Create/open a file called wunder.txt (csv)
f = open('poll-data.txt', 'w')

state2 = "az"
state = state2 + "/arizona_romney_vs_obama-1757"
url = "http://www.realclearpolitics.com/epolls/2012/president/" + state + ".html"
page = urllib2.urlopen(url)
print 'Opened URL'

#Get Different polls from page
soup = BeautifulSoup(page)

RCPAverage_Date = soup.findAll('table')[4].findAll('tr')[1].findAll('td')[1].string
RCPAverage_R = soup.findAll('table')[4].findAll('tr')[1].findAll('td')[3].string
RCPAverage_O = soup.findAll('table')[4].findAll('tr')[1].findAll('td')[4].string

print RCPAverage_Date
print RCPAverage_R
print RCPAverage_O

poll_table = soup.findAll('table')[4]


for row in poll_table:
    print 'hey'

# meanTemp = soup.findAll(attrs={"class":"nobr"})[3].span.string
# print 'Opened meanTemp'
# rainFall = soup.findAll(attrs={"class":"nobr"})[12].span.string
# print 'Opened rainFall'
# snowFall = soup.findAll(attrs={"class":"nobr"})[15].span.string
# print 'Opened snowFall'

# #Format month for timestamp
# if len(str(m)) < 2:
# mStamp = '0' + str(m)
# else: 
# mStamp = str(m)

# #Format day for timestamp

# if len(str(d)) < 2:
# dStamp = "0" + str(d)
# else:
# dStamp = str(d)

# #Build timestamp
# timestamp = '2011_' + str(m) + "_" + str(d)

# f.write(timestamp + ',' + meanTemp + ',' + str(rainFall) + ',' + str(snowFall) + '\n')