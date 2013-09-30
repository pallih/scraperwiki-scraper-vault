import scraperwiki
import urlparse
import lxml.html

#get the extension info from its page
def scrape_extension(url):
    html = scraperwiki.scrape( urlparse.urljoin('http://www.fileinfo.com/',url))
    root = lxml.html.fromstring(html)
    scrape_table(root)
    

    rows = root.cssselect("table.programs tr")
    applications = {}
    junction = {}

    for row in rows:
        system = row[0].text_content()
        if system=="Windows":
            rows_apps = row.cssselect("table.apps tr");
            for row_app in rows_apps:
                #application_short_name application_name application_url application_image

                applications['application_name'] = row_app.cssselect("td.program")[0].text_content();
                applications['application_short_name'] = applications['application_name'].replace(' ', '').lower()
                        
                # get the url
                url_download = row_app.cssselect("td.program")[0].cssselect('a')
                if url_download:
                    applications['application_url'] = url_download[0].get('href');
                    
                        
                # get the image
                img_icon = row_app.cssselect("td.appicon")[0].cssselect('img')
                if img_icon:
                    applications['application_image'] = img_icon[0].get('src');
                    

                #junction - extension = split url + application short name
                junction['extension_name'] = url.replace("/extension/", "").replace(".","");
                
                junction['application_short_name'] = applications['application_short_name']
                
                
                
                
                scraperwiki.sqlite.save(unique_keys=["extension_name","application_short_name"], data=junction, table_name="junction")
                scraperwiki.sqlite.save(unique_keys=["application_name"], data=applications, table_name="applications")  
    



# scrape_table function: gets the table of extensions from pages
def scrape_table(root):
    rows = root.cssselect("table.list tr")  # selects all <tr> blocks within <table class="list">
    for row in rows:
        
        link = row.cssselect("a")
        
        if link:            
            extension_page = link[0].get('href')            
                        
            scrape_extension(extension_page)
            
            
            # Finally, save the record to the database
            #scraperwiki.sqlite.save(unique_keys=["extension_name"], data=record)           

    


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

urls = ['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']

scrape_urls(starting_url, urls)

import scraperwiki
import urlparse
import lxml.html

#get the extension info from its page
def scrape_extension(url):
    html = scraperwiki.scrape( urlparse.urljoin('http://www.fileinfo.com/',url))
    root = lxml.html.fromstring(html)
    scrape_table(root)
    

    rows = root.cssselect("table.programs tr")
    applications = {}
    junction = {}

    for row in rows:
        system = row[0].text_content()
        if system=="Windows":
            rows_apps = row.cssselect("table.apps tr");
            for row_app in rows_apps:
                #application_short_name application_name application_url application_image

                applications['application_name'] = row_app.cssselect("td.program")[0].text_content();
                applications['application_short_name'] = applications['application_name'].replace(' ', '').lower()
                        
                # get the url
                url_download = row_app.cssselect("td.program")[0].cssselect('a')
                if url_download:
                    applications['application_url'] = url_download[0].get('href');
                    
                        
                # get the image
                img_icon = row_app.cssselect("td.appicon")[0].cssselect('img')
                if img_icon:
                    applications['application_image'] = img_icon[0].get('src');
                    

                #junction - extension = split url + application short name
                junction['extension_name'] = url.replace("/extension/", "").replace(".","");
                
                junction['application_short_name'] = applications['application_short_name']
                
                
                
                
                scraperwiki.sqlite.save(unique_keys=["extension_name","application_short_name"], data=junction, table_name="junction")
                scraperwiki.sqlite.save(unique_keys=["application_name"], data=applications, table_name="applications")  
    



# scrape_table function: gets the table of extensions from pages
def scrape_table(root):
    rows = root.cssselect("table.list tr")  # selects all <tr> blocks within <table class="list">
    for row in rows:
        
        link = row.cssselect("a")
        
        if link:            
            extension_page = link[0].get('href')            
                        
            scrape_extension(extension_page)
            
            
            # Finally, save the record to the database
            #scraperwiki.sqlite.save(unique_keys=["extension_name"], data=record)           

    


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

urls = ['s', 't', 'u', 'v', 'w', 'x', 'y', 'z']

scrape_urls(starting_url, urls)

