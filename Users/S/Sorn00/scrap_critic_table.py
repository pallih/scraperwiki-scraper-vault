###############################################################################
# Scrape Critics and Urls Need to add test for ad display page
###############################################################################

import scraperwiki
import re






# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Critic Page Link', 'Critic'])

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use BeautifulSoup, which is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup



# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup,curCritic):
    data_table = soup.find("table", { "class" : "rt_table" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            print table_cells[0].span["class"]
            if "fresh" in table_cells[0].span["class"]:
                record['Rating'] = "Fresh"
            elif "rotten" in table_cells[0].span["class"]:
                record['Rating'] = "Rotten"
            else:
                record['Rating'] = " "
            record['title'] = table_cells[2].text
            record['movieId'] = table_cells[2].a["href"]
            record['Critic'] = curCritic
            
            
            
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["title"],record)



# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url,curCritic):
    print "in scrape and look"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup,curCritic)
    return soup
    #next_link = soup.find("a", { "class" : "next" })
    #print next_link
    #if next_link:
        #next_url = base_url + next_link['href']
        #print next_url
        #scrape_and_look_for_next_link(next_url)        
    


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
atoz = ["/critic/diana-abu-jaber/","/critic/marc-fennell/"]


for curCritic  in atoz:
    
    base_url = 'http://www.rottentomatoes.com' + curCritic + 'movies.php?cats=&genreid=&letter=&switches=&sortby=&limit=50&page='


    soup = scrape_and_look_for_next_link(base_url,curCritic)


    for x in range(2,1000):
                
               #if  soup.find('a', href = '/critics/authors.php?view=' + curView + '&page=' + str(x) ):
               #     /critic/marc-fennell/movies.php?cats=&genreid=&amp;letter=&switches=&sortby=&limit=50&page=2
               #if soup.find('a', href = '/critics/authors.php?view=&page=' + str(x) ):
               if  soup.find('a', href = '/critic/' + curCritic + '/movies.php?cats=&genreid=&letter=&switches=&sortby=&limit=50&page=' + str(x) ):
                   next_url = base_url + str(x)
                   print next_url
                   print x
                   soup = scrape_and_look_for_next_link(next_url,curCritic)
###############################################################################
# Scrape Critics and Urls Need to add test for ad display page
###############################################################################

import scraperwiki
import re






# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Critic Page Link', 'Critic'])

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use BeautifulSoup, which is a Python library especially for scraping.
# -----------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup



# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup,curCritic):
    data_table = soup.find("table", { "class" : "rt_table" })
    rows = data_table.findAll("tr")
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            print table_cells[0].span["class"]
            if "fresh" in table_cells[0].span["class"]:
                record['Rating'] = "Fresh"
            elif "rotten" in table_cells[0].span["class"]:
                record['Rating'] = "Rotten"
            else:
                record['Rating'] = " "
            record['title'] = table_cells[2].text
            record['movieId'] = table_cells[2].a["href"]
            record['Critic'] = curCritic
            
            
            
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["title"],record)



# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url,curCritic):
    print "in scrape and look"
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_table(soup,curCritic)
    return soup
    #next_link = soup.find("a", { "class" : "next" })
    #print next_link
    #if next_link:
        #next_url = base_url + next_link['href']
        #print next_url
        #scrape_and_look_for_next_link(next_url)        
    


# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
atoz = ["/critic/diana-abu-jaber/","/critic/marc-fennell/"]


for curCritic  in atoz:
    
    base_url = 'http://www.rottentomatoes.com' + curCritic + 'movies.php?cats=&genreid=&letter=&switches=&sortby=&limit=50&page='


    soup = scrape_and_look_for_next_link(base_url,curCritic)


    for x in range(2,1000):
                
               #if  soup.find('a', href = '/critics/authors.php?view=' + curView + '&page=' + str(x) ):
               #     /critic/marc-fennell/movies.php?cats=&genreid=&amp;letter=&switches=&sortby=&limit=50&page=2
               #if soup.find('a', href = '/critics/authors.php?view=&page=' + str(x) ):
               if  soup.find('a', href = '/critic/' + curCritic + '/movies.php?cats=&genreid=&letter=&switches=&sortby=&limit=50&page=' + str(x) ):
                   next_url = base_url + str(x)
                   print next_url
                   print x
                   soup = scrape_and_look_for_next_link(next_url,curCritic)
