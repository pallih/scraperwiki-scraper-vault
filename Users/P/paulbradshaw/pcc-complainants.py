import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
#scraperwiki.metadata.save('data_columns', ['complainant', 'case', 'date', 'link'])

# creates scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    # create data_table variable & using find function on soup object to pass ul to that
    complainant_list = soup.find("ul")

    # finds all li in data_table object and passes result to rows
    rows = complainant_list.findAll("li")

    # create an empty dictionary
    record = {}

    # Loops through rows object and performs actions below.
    for row in rows:

        # Set up our data record - we'll need it later.
        # populates that dictionary with names, each of which contains the text of the row created above
            record['name'] = row.text

        #if ("Council" in record['name']) or ("council" in record['name']) or ("Councillor" in record['name']):
        # Print out the data we've gathered.

        # Finally, save the record to the datastore - 'complainant' is our unique key.

        # Finds the <a> section of the row, and the href attribute within that.
        # And assigns that to complaints object 
            complaints = row.find("a")['href']
            print complaints

        # Records the (full) complaints URL in the record dictionary
            complaints_link = base_url + complaints
            record['complaints_link'] = complaints_link

        # Below takes contents of each complaints link and counts number of li's
            html = scraperwiki.scrape(complaints_link)
            soup = BeautifulSoup(html)
            complaints_list = soup.find("ul")
            complaints = complaints_list.findAll("li")
            print len(complaints)

        # This stores the count (len) - length of list - in record
            record['number_of_complaints'] = len(complaints)
            print record
            scraperwiki.datastore.save(["name"], record)
        # NOW need to go to the complaints page and store contents in a new object
        
        
       
# scrape_and_look_for_next_link function: 
# calls the scrape_table function above
# then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):

# this line takes the url value above - which has in turn been taken from starting_url below, 
# and scrapes it using scraperwiki's scrape command
# then assigns the results to the html variable
    html = scraperwiki.scrape(url)
# this line passes the results of that in turn through BeautifulSoup into a variable 'soup'
    soup = BeautifulSoup(html)
# now we pass 'soup' to the scrape_table function, which has been created above
    scrape_page(soup)

    #this looks for <a class="next" ...> and creates next_link variable for that; 
    # sees <a> as a dictionary with keys (attributes) and values - hence {}
    next_link = soup.find("a", {"class" : "next"})
    if next_link:
        # if there is a link there, then add the href attribute of it and adding it to the base url variable
        next_url = base_url + '/complainants' + next_link['href']
        
        # Final line reruns the same function.
        scrape_and_look_for_next_link(next_url)

# These lines specify the webpage where the scraping starts.

base_url = 'http://complaints.pccwatch.co.uk'
# this line provides the format for each of the pages that follows, so the next one will be ?page=2
starting_url = base_url + '/complainants?page=1'

# this line passes the 'starting_url' variable to the scrape_and_... function - starting_url is basically the base_url plus a little extra
scrape_and_look_for_next_link(starting_url)
import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
#scraperwiki.metadata.save('data_columns', ['complainant', 'case', 'date', 'link'])

# creates scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    # create data_table variable & using find function on soup object to pass ul to that
    complainant_list = soup.find("ul")

    # finds all li in data_table object and passes result to rows
    rows = complainant_list.findAll("li")

    # create an empty dictionary
    record = {}

    # Loops through rows object and performs actions below.
    for row in rows:

        # Set up our data record - we'll need it later.
        # populates that dictionary with names, each of which contains the text of the row created above
            record['name'] = row.text

        #if ("Council" in record['name']) or ("council" in record['name']) or ("Councillor" in record['name']):
        # Print out the data we've gathered.

        # Finally, save the record to the datastore - 'complainant' is our unique key.

        # Finds the <a> section of the row, and the href attribute within that.
        # And assigns that to complaints object 
            complaints = row.find("a")['href']
            print complaints

        # Records the (full) complaints URL in the record dictionary
            complaints_link = base_url + complaints
            record['complaints_link'] = complaints_link

        # Below takes contents of each complaints link and counts number of li's
            html = scraperwiki.scrape(complaints_link)
            soup = BeautifulSoup(html)
            complaints_list = soup.find("ul")
            complaints = complaints_list.findAll("li")
            print len(complaints)

        # This stores the count (len) - length of list - in record
            record['number_of_complaints'] = len(complaints)
            print record
            scraperwiki.datastore.save(["name"], record)
        # NOW need to go to the complaints page and store contents in a new object
        
        
       
# scrape_and_look_for_next_link function: 
# calls the scrape_table function above
# then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):

# this line takes the url value above - which has in turn been taken from starting_url below, 
# and scrapes it using scraperwiki's scrape command
# then assigns the results to the html variable
    html = scraperwiki.scrape(url)
# this line passes the results of that in turn through BeautifulSoup into a variable 'soup'
    soup = BeautifulSoup(html)
# now we pass 'soup' to the scrape_table function, which has been created above
    scrape_page(soup)

    #this looks for <a class="next" ...> and creates next_link variable for that; 
    # sees <a> as a dictionary with keys (attributes) and values - hence {}
    next_link = soup.find("a", {"class" : "next"})
    if next_link:
        # if there is a link there, then add the href attribute of it and adding it to the base url variable
        next_url = base_url + '/complainants' + next_link['href']
        
        # Final line reruns the same function.
        scrape_and_look_for_next_link(next_url)

# These lines specify the webpage where the scraping starts.

base_url = 'http://complaints.pccwatch.co.uk'
# this line provides the format for each of the pages that follows, so the next one will be ?page=2
starting_url = base_url + '/complainants?page=1'

# this line passes the 'starting_url' variable to the scrape_and_... function - starting_url is basically the base_url plus a little extra
scrape_and_look_for_next_link(starting_url)
import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
#scraperwiki.metadata.save('data_columns', ['complainant', 'case', 'date', 'link'])

# creates scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    # create data_table variable & using find function on soup object to pass ul to that
    complainant_list = soup.find("ul")

    # finds all li in data_table object and passes result to rows
    rows = complainant_list.findAll("li")

    # create an empty dictionary
    record = {}

    # Loops through rows object and performs actions below.
    for row in rows:

        # Set up our data record - we'll need it later.
        # populates that dictionary with names, each of which contains the text of the row created above
            record['name'] = row.text

        #if ("Council" in record['name']) or ("council" in record['name']) or ("Councillor" in record['name']):
        # Print out the data we've gathered.

        # Finally, save the record to the datastore - 'complainant' is our unique key.

        # Finds the <a> section of the row, and the href attribute within that.
        # And assigns that to complaints object 
            complaints = row.find("a")['href']
            print complaints

        # Records the (full) complaints URL in the record dictionary
            complaints_link = base_url + complaints
            record['complaints_link'] = complaints_link

        # Below takes contents of each complaints link and counts number of li's
            html = scraperwiki.scrape(complaints_link)
            soup = BeautifulSoup(html)
            complaints_list = soup.find("ul")
            complaints = complaints_list.findAll("li")
            print len(complaints)

        # This stores the count (len) - length of list - in record
            record['number_of_complaints'] = len(complaints)
            print record
            scraperwiki.datastore.save(["name"], record)
        # NOW need to go to the complaints page and store contents in a new object
        
        
       
# scrape_and_look_for_next_link function: 
# calls the scrape_table function above
# then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):

# this line takes the url value above - which has in turn been taken from starting_url below, 
# and scrapes it using scraperwiki's scrape command
# then assigns the results to the html variable
    html = scraperwiki.scrape(url)
# this line passes the results of that in turn through BeautifulSoup into a variable 'soup'
    soup = BeautifulSoup(html)
# now we pass 'soup' to the scrape_table function, which has been created above
    scrape_page(soup)

    #this looks for <a class="next" ...> and creates next_link variable for that; 
    # sees <a> as a dictionary with keys (attributes) and values - hence {}
    next_link = soup.find("a", {"class" : "next"})
    if next_link:
        # if there is a link there, then add the href attribute of it and adding it to the base url variable
        next_url = base_url + '/complainants' + next_link['href']
        
        # Final line reruns the same function.
        scrape_and_look_for_next_link(next_url)

# These lines specify the webpage where the scraping starts.

base_url = 'http://complaints.pccwatch.co.uk'
# this line provides the format for each of the pages that follows, so the next one will be ?page=2
starting_url = base_url + '/complainants?page=1'

# this line passes the 'starting_url' variable to the scrape_and_... function - starting_url is basically the base_url plus a little extra
scrape_and_look_for_next_link(starting_url)
import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
#scraperwiki.metadata.save('data_columns', ['complainant', 'case', 'date', 'link'])

# creates scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    # create data_table variable & using find function on soup object to pass ul to that
    complainant_list = soup.find("ul")

    # finds all li in data_table object and passes result to rows
    rows = complainant_list.findAll("li")

    # create an empty dictionary
    record = {}

    # Loops through rows object and performs actions below.
    for row in rows:

        # Set up our data record - we'll need it later.
        # populates that dictionary with names, each of which contains the text of the row created above
            record['name'] = row.text

        #if ("Council" in record['name']) or ("council" in record['name']) or ("Councillor" in record['name']):
        # Print out the data we've gathered.

        # Finally, save the record to the datastore - 'complainant' is our unique key.

        # Finds the <a> section of the row, and the href attribute within that.
        # And assigns that to complaints object 
            complaints = row.find("a")['href']
            print complaints

        # Records the (full) complaints URL in the record dictionary
            complaints_link = base_url + complaints
            record['complaints_link'] = complaints_link

        # Below takes contents of each complaints link and counts number of li's
            html = scraperwiki.scrape(complaints_link)
            soup = BeautifulSoup(html)
            complaints_list = soup.find("ul")
            complaints = complaints_list.findAll("li")
            print len(complaints)

        # This stores the count (len) - length of list - in record
            record['number_of_complaints'] = len(complaints)
            print record
            scraperwiki.datastore.save(["name"], record)
        # NOW need to go to the complaints page and store contents in a new object
        
        
       
# scrape_and_look_for_next_link function: 
# calls the scrape_table function above
# then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):

# this line takes the url value above - which has in turn been taken from starting_url below, 
# and scrapes it using scraperwiki's scrape command
# then assigns the results to the html variable
    html = scraperwiki.scrape(url)
# this line passes the results of that in turn through BeautifulSoup into a variable 'soup'
    soup = BeautifulSoup(html)
# now we pass 'soup' to the scrape_table function, which has been created above
    scrape_page(soup)

    #this looks for <a class="next" ...> and creates next_link variable for that; 
    # sees <a> as a dictionary with keys (attributes) and values - hence {}
    next_link = soup.find("a", {"class" : "next"})
    if next_link:
        # if there is a link there, then add the href attribute of it and adding it to the base url variable
        next_url = base_url + '/complainants' + next_link['href']
        
        # Final line reruns the same function.
        scrape_and_look_for_next_link(next_url)

# These lines specify the webpage where the scraping starts.

base_url = 'http://complaints.pccwatch.co.uk'
# this line provides the format for each of the pages that follows, so the next one will be ?page=2
starting_url = base_url + '/complainants?page=1'

# this line passes the 'starting_url' variable to the scrape_and_... function - starting_url is basically the base_url plus a little extra
scrape_and_look_for_next_link(starting_url)
import scraperwiki
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
#scraperwiki.metadata.save('data_columns', ['complainant', 'case', 'date', 'link'])

# creates scrape_table function: gets passed an individual page to scrape
def scrape_page(soup):
    # create data_table variable & using find function on soup object to pass ul to that
    complainant_list = soup.find("ul")

    # finds all li in data_table object and passes result to rows
    rows = complainant_list.findAll("li")

    # create an empty dictionary
    record = {}

    # Loops through rows object and performs actions below.
    for row in rows:

        # Set up our data record - we'll need it later.
        # populates that dictionary with names, each of which contains the text of the row created above
            record['name'] = row.text

        #if ("Council" in record['name']) or ("council" in record['name']) or ("Councillor" in record['name']):
        # Print out the data we've gathered.

        # Finally, save the record to the datastore - 'complainant' is our unique key.

        # Finds the <a> section of the row, and the href attribute within that.
        # And assigns that to complaints object 
            complaints = row.find("a")['href']
            print complaints

        # Records the (full) complaints URL in the record dictionary
            complaints_link = base_url + complaints
            record['complaints_link'] = complaints_link

        # Below takes contents of each complaints link and counts number of li's
            html = scraperwiki.scrape(complaints_link)
            soup = BeautifulSoup(html)
            complaints_list = soup.find("ul")
            complaints = complaints_list.findAll("li")
            print len(complaints)

        # This stores the count (len) - length of list - in record
            record['number_of_complaints'] = len(complaints)
            print record
            scraperwiki.datastore.save(["name"], record)
        # NOW need to go to the complaints page and store contents in a new object
        
        
       
# scrape_and_look_for_next_link function: 
# calls the scrape_table function above
# then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):

# this line takes the url value above - which has in turn been taken from starting_url below, 
# and scrapes it using scraperwiki's scrape command
# then assigns the results to the html variable
    html = scraperwiki.scrape(url)
# this line passes the results of that in turn through BeautifulSoup into a variable 'soup'
    soup = BeautifulSoup(html)
# now we pass 'soup' to the scrape_table function, which has been created above
    scrape_page(soup)

    #this looks for <a class="next" ...> and creates next_link variable for that; 
    # sees <a> as a dictionary with keys (attributes) and values - hence {}
    next_link = soup.find("a", {"class" : "next"})
    if next_link:
        # if there is a link there, then add the href attribute of it and adding it to the base url variable
        next_url = base_url + '/complainants' + next_link['href']
        
        # Final line reruns the same function.
        scrape_and_look_for_next_link(next_url)

# These lines specify the webpage where the scraping starts.

base_url = 'http://complaints.pccwatch.co.uk'
# this line provides the format for each of the pages that follows, so the next one will be ?page=2
starting_url = base_url + '/complainants?page=1'

# this line passes the 'starting_url' variable to the scrape_and_... function - starting_url is basically the base_url plus a little extra
scrape_and_look_for_next_link(starting_url)
