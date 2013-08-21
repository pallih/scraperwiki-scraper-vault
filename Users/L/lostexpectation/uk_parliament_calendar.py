import scraperwiki
from BeautifulSoup import BeautifulStoneSoup

starting_url = 'http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)

items = soup.findAll('item') 
for item in items:
    titles = []
    for title in item.findAll("title"):
        titles.append(title.text)
    record = { "guid" : item.guid.text, 
               "title" : item.title.text,
               "link" : item.link.text,
#article['pubdate'] 
#  "pubdate"    : dateutil.parser.item.pubdate.text,
# "pubdate" : item.pubdate.text,
            #   "author" : item.author.text,
                "descriptionol" : item.ol.text,
           #    "description" : item.description.text,
               "id" : item.find('pi:activity').text, #['id'],
  "livedate" : item.find('pi:livedate').text,
#  "activity" : item.find('pi:activity').text,
          #     "alltags" : item.find('pi:tags').text,
#for alltag in alltags:
 # "tag" = item.find('pi:tag').text,
 #  "alltags" : tag .",",

#item['tags'].append(tag)

#"alltags" : item.find('pi:tags').text,
#record['alltags'] = item.find('pi:tags').text,
#alltags = item.findAll('pi:tags').text
#print alltags
alltags = item..find('pi:tags').text
      #  record['alltags'] = []
        for alltag in alltags:
            tag = {}
#tag['text'] = alltag.string
         "tag" = item.find('pi:tag').text,
            record['tags'].append(tag)
     "tags" : append(", ",tag)
               "agenda" : item.find('pi:agenda').text,
               "screenshot" : item.find('pi:screenshot').text,
     "access_tags" : item.find('pi:access_tags').text
}
    scraperwiki.sqlite.save(["id"], record) 
    import scraperwiki
from BeautifulSoup import BeautifulStoneSoup

starting_url = 'http://www.fingalcoco.public-i.tv/core/data/2704/archived/1/future/1/agenda/1.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)

items = soup.findAll('item') 
for item in items:
    titles = []
    for title in item.findAll("title"):
        titles.append(title.text)
    record = { "guid" : item.guid.text, 
               "title" : item.title.text,
               "link" : item.link.text,
#article['pubdate'] 
#  "pubdate"    : dateutil.parser.item.pubdate.text,
# "pubdate" : item.pubdate.text,
            #   "author" : item.author.text,
                "descriptionol" : item.ol.text,
           #    "description" : item.description.text,
               "id" : item.find('pi:activity').text, #['id'],
  "livedate" : item.find('pi:livedate').text,
#  "activity" : item.find('pi:activity').text,
          #     "alltags" : item.find('pi:tags').text,
#for alltag in alltags:
 # "tag" = item.find('pi:tag').text,
 #  "alltags" : tag .",",

#item['tags'].append(tag)

#"alltags" : item.find('pi:tags').text,
#record['alltags'] = item.find('pi:tags').text,
#alltags = item.findAll('pi:tags').text
#print alltags
alltags = item..find('pi:tags').text
      #  record['alltags'] = []
        for alltag in alltags:
            tag = {}
#tag['text'] = alltag.string
         "tag" = item.find('pi:tag').text,
            record['tags'].append(tag)
     "tags" : append(", ",tag)
               "agenda" : item.find('pi:agenda').text,
               "screenshot" : item.find('pi:screenshot').text,
     "access_tags" : item.find('pi:access_tags').text
}
    scraperwiki.sqlite.save(["id"], record) 
    