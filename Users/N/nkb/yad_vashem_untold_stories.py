import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

for page in range(1, 38):
    # Adress to scrape
    url = 'http://istinomer.rs/izjave/istinitost/page/'+ str(page) +'/'
    # Sets up the automatic browser
    br = mechanize.Browser()
    # Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    # opens the URL
    br.open(url)
    # Extracts the HTML
    soup = BeautifulSoup(br.response().read())
    # Finds all the article snippets in the HTML
    declarations = soup.findAll("article")
    # Loop through all the articles
    for declaration in declarations:
        # Initialize the record variable where we'll store the data
        record = {}
        # Finds the name of the target and the date of the statement
        date_name = declaration.find("div", { "class" : "entry-meta" })
        # Stores the text only
        record['date_name'] = date_name.text
        # Repeat operation for the gauge
        merac = declaration.find("div", { "class" : "merac" })
        # Extract the image URL
        image_url = merac.img['src']
        # Stores the image url in our Record variable
        record['merac'] = image_url
    
        # Finally, save the record to the datastore 
        scraperwiki.sqlite.save(["date_name"], record)