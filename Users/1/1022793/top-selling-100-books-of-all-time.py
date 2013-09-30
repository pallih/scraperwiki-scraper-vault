import scraperwiki
from BeautifulSoup import BeautifulSoup
def books(soup):
    #describing each columns:
    scraperwiki.metadata.save('data_columns',[ 'Pos', 'Title', 'Author' , 'Imprint','Volume','Value$'])
    #describing the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #describing the rows of the table:
    rows = soup.findAll("tr")
    for row in rows:
        record = {}
        #describing the cells
        tablecolm = row.findAll("td")
        if len(tablecolm) ==6:
             record['Pos'] = tablecolm[0].text
             record['Title'] = tablecolm[1].text
             record['Author'] = tablecolm[2].text
             record['Imprint'] = tablecolm[3].text
             record['Volume'] = tablecolm[4].text
             record['Value$'] = tablecolm[5].text
             print record,
             print "-------------"
            #saving the data:
             scraperwiki.datastore.save(["Pos"], record)
#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jan/01/top-100-books-of-all-time"
html = scraperwiki.scrape(website)#installing the weblink 
soup = BeautifulSoup(html)
books(soup)import scraperwiki
from BeautifulSoup import BeautifulSoup
def books(soup):
    #describing each columns:
    scraperwiki.metadata.save('data_columns',[ 'Pos', 'Title', 'Author' , 'Imprint','Volume','Value$'])
    #describing the tables in HTML code:
    table = soup.find("table", {"class": "in-article sortable"})
    #describing the rows of the table:
    rows = soup.findAll("tr")
    for row in rows:
        record = {}
        #describing the cells
        tablecolm = row.findAll("td")
        if len(tablecolm) ==6:
             record['Pos'] = tablecolm[0].text
             record['Title'] = tablecolm[1].text
             record['Author'] = tablecolm[2].text
             record['Imprint'] = tablecolm[3].text
             record['Volume'] = tablecolm[4].text
             record['Value$'] = tablecolm[5].text
             print record,
             print "-------------"
            #saving the data:
             scraperwiki.datastore.save(["Pos"], record)
#Inserting the URL of the web page, from where the data was taken:
website = "http://www.guardian.co.uk/news/datablog/2011/jan/01/top-100-books-of-all-time"
html = scraperwiki.scrape(website)#installing the weblink 
soup = BeautifulSoup(html)
books(soup)