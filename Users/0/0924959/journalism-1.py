import scraperwiki
html = scraperwiki.scrape('http://scraperwiki.com/hello_world.html')
print html

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object


def scrape_table(soup):
    #To define the name of the columns
    scraperwiki.metadata.save('data_columns',['Datablog post','Spreadsheet for the post','Title of blog post'])
    #To find table in html code
    table = soup.find("table",{"class": "in-article sortable"})
    #To find each row of the table
    rows = table.findAll("tr")
    for row in rows:
        record = {}
        #To find each cell of the table
        table_journalism = row.findAll("td")
        #Each row should include five cells
        if len(table_journalism) == 3:#check if it is correct
            record['Datablog post'] = table_journalism[0].text
            record['Spreadsheet for the post'] = table_journalism[1].text
            record['Title of blog post'] = table_journalism[2].text
            print record, "----------"
            #save one by one
            scraperwiki.datastore.save(["Datablog post"],record)

#Define the Website
website = "http://www.guardian.co.uk/news/datablog/2011/jan/27/data-store-office-for-national-statistics"
#put the all code in html variable
html = scraperwiki.scrape(website)
soup =  BeautifulSoup(html)
scrape_table(soup)


      
