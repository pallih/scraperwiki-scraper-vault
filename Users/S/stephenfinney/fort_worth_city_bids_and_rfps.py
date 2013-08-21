import scraperwiki
import dateutil.parser
import sys
from BeautifulSoup import BeautifulSoup


def create_table():
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Bid ID' str, 'Title' str, 'Status' str, 'Issue Date' datetime, 'Close Date' datetime, 'Required Date' date, 'Department' str, 'Contact Name' str, 'Contact Info' str, 'Details Link' str)")
    scraperwiki.sqlite.commit()


def record_data():
    print "Getting links to data..."
    html = scraperwiki.scrape("http://www.fortworthtexas.gov/purchasing")
    root = BeautifulSoup(html)

    main = root.find('div', {"id" : "main"})
    headers = main.findAll('h3')
    record = {}
    index = 0
    strongs = root.findAll('strong')
    dates = root.findAll('p')

    for header in headers:
        if ":" in header.text:
            record['Bid ID'] = header.text[:header.text.find(":")]
        else: 
            record['Bid ID'] = "N/A"

        if header.find('a',href=True):
            record['Details Link'] = header.find('a',href=True)
        else: 
            record['Details Link'] = "N/A"

        record['Title'] = header.text

        if "Status:" in strongs[index]:
            record['Close Date'] = (dates[index])[(dates[index]).find('Closes ')]:]
        print record['Close Date']
        

    #for header in headers:
    #    if header and header.find('a',href=True):
    #        links.append("http://fortworthtexas.gov" + header.find('a',href=True)['href'])
    #    else:
    #        print "Link not found! At: " + header.text


    #for link in links:
    #    html = scraperwiki.scrape(link)
    #    root = BeautifulSoup(html)

    

create_table()
record_data()
