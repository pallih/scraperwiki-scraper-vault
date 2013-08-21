import scraperwiki
import urlparse
import lxml.html

#get the extension info from its page
def scrape_extension(url, record):
    html = scraperwiki.scrape( urlparse.urljoin('http://www.fileinfo.com/',url))
    root = lxml.html.fromstring(html)
    scrape_table(root)
    rows = root.cssselect("td.description")
     
    # get the info about the file
    record['extension_info'] = str()
    for row in rows:
        record['extension_info'] += row.text_content()
        
    #get the image for the url <img src="/images/icons/files/128/generic.png" class="fileicon"
    image = root.cssselect("img.fileicon")
    #create record and remove unessary ../ characters
    record['extension_image'] = urlparse.urljoin('http://www.fileinfo.com/', image[0].get('src').replace("../", ""))
    
    return record



# scrape_table function: gets the table of extensions from pages
def scrape_table(root):
    rows = root.cssselect("table.list tr")  # selects all <tr> blocks within <table class="list">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        link = row.cssselect("a")
        
        if table_cells: 
            record['extension_name'] = link[0].text.replace(".", "")
            extension_page = link[0].get('href')
            #slit the string and get the first word in lowercase
            record['category_short_name'] = table_cells[1].text.split(' ')[0].lower()
            record['extension_description'] = table_cells[2].text
                        
            record = scrape_extension(extension_page ,record)
            
            
            # Finally, save the record to the database
            scraperwiki.sqlite.save(unique_keys=["extension_name"], data=record)           

    


# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_urls(url, urls):
    for page in urls:
        html = scraperwiki.scrape( urlparse.urljoin(base_url,page))
        
        root = lxml.html.fromstring(html)
        scrape_table(root)
        
    
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.fileinfo.com/list/'
starting_url = urlparse.urljoin(base_url, '1')

urls = ['i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

scrape_urls(starting_url, urls)

