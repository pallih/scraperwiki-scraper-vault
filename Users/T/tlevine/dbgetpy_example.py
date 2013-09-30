from scraperwiki.utils import swimport
dbget=swimport('dbgetpy')

#Save
urls=["https://scraperwiki.com/scrapers/dbgetpy","https://scraperwiki.com"]
for url in urls:
  dbget.save_page(url)

#Retrieve
html=dbget.get_page("https://scraperwiki.com/scrapers/dbgetpy")
print htmlfrom scraperwiki.utils import swimport
dbget=swimport('dbgetpy')

#Save
urls=["https://scraperwiki.com/scrapers/dbgetpy","https://scraperwiki.com"]
for url in urls:
  dbget.save_page(url)

#Retrieve
html=dbget.get_page("https://scraperwiki.com/scrapers/dbgetpy")
print html