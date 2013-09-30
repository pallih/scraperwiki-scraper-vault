import scraperwiki
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object


def scrape_table(soup):
    #To define the name of the columns
    scraperwiki.metadata.save('data_columns',['Name','Area','Title','Warned by Police/came forward','When warned/came forward,if known, year','Details'])
    #To find table in html code
    table = soup.find("table",{"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_hack = row.findAll("td")
        #Each row should include five cells
        if len(table_hack) == 6:#check if it is correct
            record['Name'] = table_hack[0].text
            record['Area'] = table_hack[1].text
            record['Title'] = table_hack[2].text
            record['Warned by Police/came forward'] = table_hack[3].text
            record['When warned/came forward,if known, year'] = table_hack[4].txt
            record['Details'] = table_hack[5].text
            print record
            print "------------" 
            #save one by one
            scraperwiki.datastore.save(["Name"],record)

#Define the Website
website = "http://www.guardian.co.uk/news/datablog/2010/sep/10/phone-hacking-victims-list"
#put the all code in html variable
html = scraperwiki.scrape(website)
soup =  BeautifulSoup(html)
scrape_table(soup)


                            import scraperwiki
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object


def scrape_table(soup):
    #To define the name of the columns
    scraperwiki.metadata.save('data_columns',['Name','Area','Title','Warned by Police/came forward','When warned/came forward,if known, year','Details'])
    #To find table in html code
    table = soup.find("table",{"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_hack = row.findAll("td")
        #Each row should include five cells
        if len(table_hack) == 6:#check if it is correct
            record['Name'] = table_hack[0].text
            record['Area'] = table_hack[1].text
            record['Title'] = table_hack[2].text
            record['Warned by Police/came forward'] = table_hack[3].text
            record['When warned/came forward,if known, year'] = table_hack[4].txt
            record['Details'] = table_hack[5].text
            print record
            print "------------" 
            #save one by one
            scraperwiki.datastore.save(["Name"],record)

#Define the Website
website = "http://www.guardian.co.uk/news/datablog/2010/sep/10/phone-hacking-victims-list"
#put the all code in html variable
html = scraperwiki.scrape(website)
soup =  BeautifulSoup(html)
scrape_table(soup)


                            