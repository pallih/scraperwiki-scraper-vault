# an empty search on the social care register brings up all 10,000 or so registrations
# first page is http://www.gscc.org.uk/registerSearch.php#results
# but that URL can't be linked to - instead use http://www.gscc.org.uk/registerSearch.php?o=1#results
# guessing that the 'o' after ? means an empty query? 
# and the =1 means what number the results page (of the first 10 results) starts from
# second page is http://www.gscc.org.uk/registerSearch.php?o=11#results
# 3rd page is http://www.gscc.org.uk/registerSearch.php?o=21#results
# links to each further page of results and the data in HTML in comments at bottom


import scraperwiki
import urlparse
import lxml.html

# This creates a function called scrape_table to scrape specific data from each page passed to it. 

# That data is in between <table> tags - there is only one table on each page so no need to be more specific
# Lower down you'll see it then splits the table into rows, and rows into cells
# It loops through the rows, assigning a record to each, and loops through cells too
# First, here's the creation of the function. 'root' in brackets is the page sent to it
 # - look for 'root' elsewhere in this page to see where it is created
def scrape_table(root):
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table>
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        # define table_cells as the contents of <td> - 
        table_cells = row.cssselect("td")
        # because there's more than one <td>, each one in turn is assigned to a different record
        # we have 7, which are identified by the index numbers [0] to [6] in turn: 
        if table_cells: 
            record['Title'] = table_cells[0].text
            record['Name'] = table_cells[1].text
            record['Town_of_employment_or_study'] = table_cells[2].text
            record['Registration_number'] = table_cells[3].text
            record['Part_of_the_register'] = table_cells[4].text
            record['Date_of_Registration'] = table_cells[5].text
            record['Info'] = table_cells[6].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Registration_number' is our unique key - 
# but when I scraped this with OutWit Hub there were multiple records of the same people
            scraperwiki.datastore.save(["Registration_number"], record)

# TO CHECK > "a.pageNext" should be class="pageNext" in HTML - guessing id="pageNext" would be a#pageNext
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.pageNext")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# establish the base URL... 
base_url = 'http://www.gscc.org.uk'

# ...and the extra parameters for the first page of search results
starting_url = urlparse.urljoin(base_url, '/registerSearch.php?o=1#results')

# call the function to start scraping the first page
scrape_and_look_for_next_link(starting_url)


# <div class="resultsNav"><a class="pageFirst disabled">&laquo; First</a><a class="pagePrev disabled">&lsaquo; Previous</a><span>Result <strong>1-10</strong> of <strong>111280</strong></span><a href="/registerSearch.php?o=11#results" class="pageNext" title="Click to view next page of results...">Next &rsaquo;</a><a href="/registerSearch.php?o=111271#results" class="pageLast" title="Click to view last page of results...">Last &raquo;</a></div> <div class="clear"></div>

# data to be scraped within HTML table as follows:
# <table>
         #   <tr>
          #      <th align="left">Title</th>
           #     <th align="left"><a href="?ord=surname&amp;dir=DESC#results" title="Search results are ordered by this column - click to reverse the order...">Name</a><img src="/SDimages/arrow_up.gif" width="15" height="15" alt="This column is in ascending order" title="This column is in ascending order" /></th>
            #    <th align="left"><a href="?ord=town#results" title="Click to reorder search results by this column...">Town of<br/>employment/study</a></th>
             #   <th align="left"><a href="?ord=gsccRef#results" title="Click to reorder search results by this column...">Registration<br/>no.</a></th>
              #  <th align="left">Part of the<br/>Register</th>
               # <th align="left"><a href="?ord=regDate#results" title="Click to reorder search results by this column...">Date of<br/>Registration</a></th>
                #<th align="left">Additional<br/>information</th>
#            </tr>
 #                   <tr class="row2"> 
                 #       <td align="left">Mrs</td>
                  #      <td align="left">Aalders, Sharon Jennifer</td>
                   #     <td align="left">IPSWICH</td>
                    #    <td align="left">E/1127351</td>
                     #   <td align="left">Registered Social Worker</td>
                      #  <td align="left">05/04/2009</td>
                       # <td align="left">N/A</td>
#                    </tr>
 #                   <tr class="row1"> 
  #                      <td align="left">Mr</td>
   #                     <td align="left">Aantjes, Arnoud</td>
    #                    <td align="left">Not Applicable</td>
     #                   <td align="left">E/2026594</td>
      #                  <td align="left">Registered Social Worker</td>
       #                 <td align="left">03/04/2009</td>
        #                <td align="left">N/A</td>
         #           </tr>
# And so on - the tr class formats alternate rows so they're easy to see.# an empty search on the social care register brings up all 10,000 or so registrations
# first page is http://www.gscc.org.uk/registerSearch.php#results
# but that URL can't be linked to - instead use http://www.gscc.org.uk/registerSearch.php?o=1#results
# guessing that the 'o' after ? means an empty query? 
# and the =1 means what number the results page (of the first 10 results) starts from
# second page is http://www.gscc.org.uk/registerSearch.php?o=11#results
# 3rd page is http://www.gscc.org.uk/registerSearch.php?o=21#results
# links to each further page of results and the data in HTML in comments at bottom


import scraperwiki
import urlparse
import lxml.html

# This creates a function called scrape_table to scrape specific data from each page passed to it. 

# That data is in between <table> tags - there is only one table on each page so no need to be more specific
# Lower down you'll see it then splits the table into rows, and rows into cells
# It loops through the rows, assigning a record to each, and loops through cells too
# First, here's the creation of the function. 'root' in brackets is the page sent to it
 # - look for 'root' elsewhere in this page to see where it is created
def scrape_table(root):
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table>
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        # define table_cells as the contents of <td> - 
        table_cells = row.cssselect("td")
        # because there's more than one <td>, each one in turn is assigned to a different record
        # we have 7, which are identified by the index numbers [0] to [6] in turn: 
        if table_cells: 
            record['Title'] = table_cells[0].text
            record['Name'] = table_cells[1].text
            record['Town_of_employment_or_study'] = table_cells[2].text
            record['Registration_number'] = table_cells[3].text
            record['Part_of_the_register'] = table_cells[4].text
            record['Date_of_Registration'] = table_cells[5].text
            record['Info'] = table_cells[6].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Registration_number' is our unique key - 
# but when I scraped this with OutWit Hub there were multiple records of the same people
            scraperwiki.datastore.save(["Registration_number"], record)

# TO CHECK > "a.pageNext" should be class="pageNext" in HTML - guessing id="pageNext" would be a#pageNext
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.pageNext")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# establish the base URL... 
base_url = 'http://www.gscc.org.uk'

# ...and the extra parameters for the first page of search results
starting_url = urlparse.urljoin(base_url, '/registerSearch.php?o=1#results')

# call the function to start scraping the first page
scrape_and_look_for_next_link(starting_url)


# <div class="resultsNav"><a class="pageFirst disabled">&laquo; First</a><a class="pagePrev disabled">&lsaquo; Previous</a><span>Result <strong>1-10</strong> of <strong>111280</strong></span><a href="/registerSearch.php?o=11#results" class="pageNext" title="Click to view next page of results...">Next &rsaquo;</a><a href="/registerSearch.php?o=111271#results" class="pageLast" title="Click to view last page of results...">Last &raquo;</a></div> <div class="clear"></div>

# data to be scraped within HTML table as follows:
# <table>
         #   <tr>
          #      <th align="left">Title</th>
           #     <th align="left"><a href="?ord=surname&amp;dir=DESC#results" title="Search results are ordered by this column - click to reverse the order...">Name</a><img src="/SDimages/arrow_up.gif" width="15" height="15" alt="This column is in ascending order" title="This column is in ascending order" /></th>
            #    <th align="left"><a href="?ord=town#results" title="Click to reorder search results by this column...">Town of<br/>employment/study</a></th>
             #   <th align="left"><a href="?ord=gsccRef#results" title="Click to reorder search results by this column...">Registration<br/>no.</a></th>
              #  <th align="left">Part of the<br/>Register</th>
               # <th align="left"><a href="?ord=regDate#results" title="Click to reorder search results by this column...">Date of<br/>Registration</a></th>
                #<th align="left">Additional<br/>information</th>
#            </tr>
 #                   <tr class="row2"> 
                 #       <td align="left">Mrs</td>
                  #      <td align="left">Aalders, Sharon Jennifer</td>
                   #     <td align="left">IPSWICH</td>
                    #    <td align="left">E/1127351</td>
                     #   <td align="left">Registered Social Worker</td>
                      #  <td align="left">05/04/2009</td>
                       # <td align="left">N/A</td>
#                    </tr>
 #                   <tr class="row1"> 
  #                      <td align="left">Mr</td>
   #                     <td align="left">Aantjes, Arnoud</td>
    #                    <td align="left">Not Applicable</td>
     #                   <td align="left">E/2026594</td>
      #                  <td align="left">Registered Social Worker</td>
       #                 <td align="left">03/04/2009</td>
        #                <td align="left">N/A</td>
         #           </tr>
# And so on - the tr class formats alternate rows so they're easy to see.# an empty search on the social care register brings up all 10,000 or so registrations
# first page is http://www.gscc.org.uk/registerSearch.php#results
# but that URL can't be linked to - instead use http://www.gscc.org.uk/registerSearch.php?o=1#results
# guessing that the 'o' after ? means an empty query? 
# and the =1 means what number the results page (of the first 10 results) starts from
# second page is http://www.gscc.org.uk/registerSearch.php?o=11#results
# 3rd page is http://www.gscc.org.uk/registerSearch.php?o=21#results
# links to each further page of results and the data in HTML in comments at bottom


import scraperwiki
import urlparse
import lxml.html

# This creates a function called scrape_table to scrape specific data from each page passed to it. 

# That data is in between <table> tags - there is only one table on each page so no need to be more specific
# Lower down you'll see it then splits the table into rows, and rows into cells
# It loops through the rows, assigning a record to each, and loops through cells too
# First, here's the creation of the function. 'root' in brackets is the page sent to it
 # - look for 'root' elsewhere in this page to see where it is created
def scrape_table(root):
    rows = root.cssselect("table tr")  # selects all <tr> blocks within <table>
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        # define table_cells as the contents of <td> - 
        table_cells = row.cssselect("td")
        # because there's more than one <td>, each one in turn is assigned to a different record
        # we have 7, which are identified by the index numbers [0] to [6] in turn: 
        if table_cells: 
            record['Title'] = table_cells[0].text
            record['Name'] = table_cells[1].text
            record['Town_of_employment_or_study'] = table_cells[2].text
            record['Registration_number'] = table_cells[3].text
            record['Part_of_the_register'] = table_cells[4].text
            record['Date_of_Registration'] = table_cells[5].text
            record['Info'] = table_cells[6].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Registration_number' is our unique key - 
# but when I scraped this with OutWit Hub there were multiple records of the same people
            scraperwiki.datastore.save(["Registration_number"], record)

# TO CHECK > "a.pageNext" should be class="pageNext" in HTML - guessing id="pageNext" would be a#pageNext
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    next_link = root.cssselect("a.pageNext")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# establish the base URL... 
base_url = 'http://www.gscc.org.uk'

# ...and the extra parameters for the first page of search results
starting_url = urlparse.urljoin(base_url, '/registerSearch.php?o=1#results')

# call the function to start scraping the first page
scrape_and_look_for_next_link(starting_url)


# <div class="resultsNav"><a class="pageFirst disabled">&laquo; First</a><a class="pagePrev disabled">&lsaquo; Previous</a><span>Result <strong>1-10</strong> of <strong>111280</strong></span><a href="/registerSearch.php?o=11#results" class="pageNext" title="Click to view next page of results...">Next &rsaquo;</a><a href="/registerSearch.php?o=111271#results" class="pageLast" title="Click to view last page of results...">Last &raquo;</a></div> <div class="clear"></div>

# data to be scraped within HTML table as follows:
# <table>
         #   <tr>
          #      <th align="left">Title</th>
           #     <th align="left"><a href="?ord=surname&amp;dir=DESC#results" title="Search results are ordered by this column - click to reverse the order...">Name</a><img src="/SDimages/arrow_up.gif" width="15" height="15" alt="This column is in ascending order" title="This column is in ascending order" /></th>
            #    <th align="left"><a href="?ord=town#results" title="Click to reorder search results by this column...">Town of<br/>employment/study</a></th>
             #   <th align="left"><a href="?ord=gsccRef#results" title="Click to reorder search results by this column...">Registration<br/>no.</a></th>
              #  <th align="left">Part of the<br/>Register</th>
               # <th align="left"><a href="?ord=regDate#results" title="Click to reorder search results by this column...">Date of<br/>Registration</a></th>
                #<th align="left">Additional<br/>information</th>
#            </tr>
 #                   <tr class="row2"> 
                 #       <td align="left">Mrs</td>
                  #      <td align="left">Aalders, Sharon Jennifer</td>
                   #     <td align="left">IPSWICH</td>
                    #    <td align="left">E/1127351</td>
                     #   <td align="left">Registered Social Worker</td>
                      #  <td align="left">05/04/2009</td>
                       # <td align="left">N/A</td>
#                    </tr>
 #                   <tr class="row1"> 
  #                      <td align="left">Mr</td>
   #                     <td align="left">Aantjes, Arnoud</td>
    #                    <td align="left">Not Applicable</td>
     #                   <td align="left">E/2026594</td>
      #                  <td align="left">Registered Social Worker</td>
       #                 <td align="left">03/04/2009</td>
        #                <td align="left">N/A</td>
         #           </tr>
# And so on - the tr class formats alternate rows so they're easy to see.