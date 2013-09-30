import urllib2
from BeautifulSoup import BeautifulSoup
url=urllib2.urlopen("http://www.guardian.co.uk/football/premierleague")
soup = BeautifulSoup(url)
table = soup.find('table' ,attrs={'class':'full'})
for row in table.findAll('tr') : # for all TR items (table rows)
    for td in row.findAll('td') : # for TD items in row
        text = td.renderContents().strip()
        text = int(text)
   
print (text)
#print text) / 4
print('-----') import urllib2
from BeautifulSoup import BeautifulSoup
url=urllib2.urlopen("http://www.guardian.co.uk/football/premierleague")
soup = BeautifulSoup(url)
table = soup.find('table' ,attrs={'class':'full'})
for row in table.findAll('tr') : # for all TR items (table rows)
    for td in row.findAll('td') : # for TD items in row
        text = td.renderContents().strip()
        text = int(text)
   
print (text)
#print text) / 4
print('-----') 