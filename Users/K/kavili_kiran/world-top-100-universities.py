import scraperwiki
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
print html


from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
tds = soup.findAll('td') # get all the <td> tags
for td in tds:
    print td # the full HTML tag
    print td.text # just the text inside the HTML tag



for td in tds:
     record = { "td" : td.text } # column name and value
     scraperwiki.datastore.save(["td"], record) # save the records one by one


def scrape_table(soup):
    #To define the name of the columns
    scraperwiki.metadata.save('data_columns',['2010Rank','UniversityName','Country','2009Rank','2008Rank',])
    #To find table in html code
    table = soup.find("table",{"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_td = row.findAll("td")
        #Each row should include five cells
        if len(table_td) == 5:#check if it is correct
            record['2010Rank'] = table_td[0].text
            record['UniversityName'] = table_td[1].text
            record['Country'] = table_td[2].text
            record['2009Rank'] = table_td[3].text
                        print record
            print "-" * 100
            #save one by one
            scraperwiki.datastore.save(["2010Rank"],record)
            

#Define the Website
website = "http://www.guardian.co.uk/news/datablog/2010/sep/08/worlds-top-100-universities-2010"
#put the all code in html variable
html = scraperwiki.scrape(website)
soup =  BeautifulSoup(html)
scrape_table(soup)

