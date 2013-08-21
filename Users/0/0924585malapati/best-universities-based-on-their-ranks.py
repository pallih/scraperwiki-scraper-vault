import scraperwiki     #Namespace for Scrapper wiki web site
from BeautifulSoup import BeautifulSoup   #Import the namespace to read web pages

print "TOP 10 countries in currency "

Page = scraperwiki.scrape('http://www.xe.com/')
Source = BeautifulSoup(Page)
scraperwiki.metadata.save('columns', ['country name  ', 'currency name', 'worldrank','highest denomination till date' ,'year of currency eastablishment','trading','mobile currency site'])
MainTable = Source.findall ("table", { "trading" : "1":"10" })
RowDetails = MainTable.findAll("tr")
print "****Scrapping Started*****"
for row in RowDetails:
        Dicrecord = {}  #Create Dictionary to store top currency Details
        Columns = row.findAll("td")
        if Columns:
            Dicrecord['country name'] = Columns[0].text
            Dicrecord['currency name'] = Columns[1].text
            Dicrecord['highest denomination till date'] = Columns[2].text
            Dicrecord['year of currency eastablishment'] = Columns[3].text
            Dicrecord['trading'] = Columns[5].text
            Dicrecord['mobile currency site'] = Columns[8].text   
            scraperwiki.datastore.save(["top 10 currency"], Dicrecord)
            print Dicrecord
print "****Scrapping Complted*****"
