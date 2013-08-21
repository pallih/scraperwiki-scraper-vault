import string
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

#now create a function called scrape_table which isn't run until the end... 
#this gets passed an individual page (soup) to scrape - look to see where it is created lower down
def scrape_table(soup,postcode):
    #find table class="reports"
    data_table = soup.find("table", { "summary" : "Childcare search results" })
    if data_table:
        #find each table row <tr>
        rows = data_table.findAll("tr")
        #for each row, loop through this
        for row in rows:
            #create a record to hold the data
            record = {}
            #find each cell <td>
            table_cells = row.findAll("td")
            #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
            if table_cells: 
                record['id'] = string.split(table_cells[1].h3.a.get('href'),'00by&')[1]
                record['postcode'] = postcode
                record['name'] = table_cells[1].h3.a.string
                record['link'] = table_cells[1].h3.a.get('href')
                record['type'] = table_cells[1].p.strong.string
                # Print out the data we've gathered
                print record, '------------'
                # Save the record to the datastore - 'id' is our unique key - 
                scraperwiki.sqlite.save(['id'], record)


#set the URL containing the form we need to open with mechanize
starting_url = 'http://fsd.liverpool.gov.uk/kb5/liverpool/fsd/category.page?category=2'
#start using mechanize to simulate a browser ('br')
br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
#open the URL previously defined as 'starting_url'

postcodes = ['L1','L2','L3','L4','L5','L6','L7','L8','L9','L10','L11','L12','L13','L14','L15','L16','L17','L18','L19','L20','L21','L23','L24','L25','L26','L27','L28','L29','L30','L31','L32','L33','L34','L35','L36','L37','L38','L39','L40','L67','L68','L69','L70','L71','L72','L73','L74','L75','L80']
br.open(starting_url)
for postcode in postcodes: 
    #br.select_form(nr=1)
    br['loc2']=postcode
    #submit the form and put the contents into 'response'
    response = br.submit()
    soup = BeautifulSoup(br.response().read())
    #need to do a loop through the "Next" buttons here
    page = 0
    scrape_table(soup,postcode)
    while soup.find("a", { "title" : "Next page" }):
        if page>0:
            response = br.follow_link(text_regex="Next")
            #create soup object by reading the contents of response and passing it through BeautifulSoup
            soup = BeautifulSoup(br.response().read())
            scrape_table(soup,postcode)
        page = page +1



