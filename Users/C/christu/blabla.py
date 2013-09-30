import scraperwiki

# Blank Python
html = scraperwiki.scrape('http://odlinfo.bfs.de/laenderliste.php')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
           

 
#import lxml.html
#root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#tds = root.cssselect('td') # get all the <td> tags
#for td in tds:
#    print lxml.html.tostring(td) # the full HTML tag
#    print td.text  

#def run():
 #   html = scraperwiki.scrape('http://odlinfo.bfs.de/laenderliste.php')
  #  html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
   # table = html.findAll('table')[4];
    #rows = table.findAll('tr');   
    #for i in range(1,len(rows)):
     #      row = rows[i]
      #     cols = row.findAll('td')
       #    href = cols[0].find('a')['href']
        #   state = cols[1].text
# print td.text

for td in tds:
    record = { "td" : td.text } # column name and value
    scraperwiki.sqlite.save(["td"], record) # save the records one by one

import scraperwiki

# Blank Python
html = scraperwiki.scrape('http://odlinfo.bfs.de/laenderliste.php')

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
           

 
#import lxml.html
#root = lxml.html.fromstring(html) # turn our HTML into an lxml object
#tds = root.cssselect('td') # get all the <td> tags
#for td in tds:
#    print lxml.html.tostring(td) # the full HTML tag
#    print td.text  

#def run():
 #   html = scraperwiki.scrape('http://odlinfo.bfs.de/laenderliste.php')
  #  html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
   # table = html.findAll('table')[4];
    #rows = table.findAll('tr');   
    #for i in range(1,len(rows)):
     #      row = rows[i]
      #     cols = row.findAll('td')
       #    href = cols[0].find('a')['href']
        #   state = cols[1].text
# print td.text

for td in tds:
    record = { "td" : td.text } # column name and value
    scraperwiki.sqlite.save(["td"], record) # save the records one by one

