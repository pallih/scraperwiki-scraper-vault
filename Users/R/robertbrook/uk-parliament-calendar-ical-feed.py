import scraperwiki
from BeautifulSoup import BeautifulStoneSoup

starting_url = 'http://services.parliament.uk/calendar/all.rss'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)

items = soup.findAll('item') 
for item in items:
    categories = []
    for category in item.findAll("category"):
        categories.append(category.text)
    record = { "guid" : item.guid.text, 
               "title" : item.title.text,
               "link" : item.link.text,
               "author" : item.author.text,
               "starttime" : (item.find('parlycal:starttime').text if item.find('parlycal:starttime') else ""),
               "categories" : categories,
               "description" : item.description.text,
               "id" : item.find('parlycal:event')['id'],
               "house" : item.find('parlycal:house').text,
               "chamber" : item.find('parlycal:chamber').text,
               "date" : item.find('parlycal:date').text,
               "committee" : item.find('parlycal:comittee').text,
               "inquiry" : item.find('parlycal:inquiry').text,
               "witnesses" : item.find('parlycal:witnesses').text,
               "location" : item.find('parlycal:location').text,
               "subject" : item.find('parlycal:subject').text
            }
    scraperwiki.sqlite.save(["id"], record) 
    