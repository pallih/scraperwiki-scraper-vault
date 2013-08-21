# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# This is the webform that the FCC presents to users for querying the manufacturer database
target = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?btnSearch=true"

# Pull the webform from the FCC server
br = mechanize.Browser()
br.set_handle_robots(False) # This disables voluntary consideration of the robots.txt file
response = br.open(target)

# The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
# print "All forms:", [ form.name  for form in br.forms() ]

# This is the form to focus on
target_form = 'advancedSearchForm'

# Select the form from within the browser object
br.select_form(name=target_form)

# The following line was used during debug to identify the fields within the form we wish to utilize (bizName)
#print br.form

# This is the field within the form that we wish to set prior to POSTing the form
target_form_field = 'bizName'

# Set the form field to the business name we wish to search for
br[target_form_field] = 'samsung*'

# Submit the form and store the result in an object named "response"
response = br.submit()
#print response.read()

# Parse the result
response_page = lxml.html.fromstring(response)

# The data to be extracted from the response is (1) whether a next page exists and (2) the current page.
# We will iterate on the dataset by parsing the current page and then selecting a next page if one exists.

next_page_exists = 1 # Begin by assuming that a next page is present

#while (next_page_exists):
  # This loop does the following 3 things:
  # 1. Read the data table in the current page
  # 2. Determine if a "next page" exists
  # 3. Fetch the next page if it exists and loop back to process it else drop out of the 'while' loop

  # Read the table in the current page.
  # The table starts with <table id="srchResultsTable">

# Here is how to return an array of rows [1:end] from a table with cell padding=1 from the document object 'root':
# root.cssselect("table[cellpadding=1] tr")[1:]
# The table[cellpadding=1] identifies the portion of the document that is relevant and "tr" identifies the elements
# within that table that are relevant

#current_table = response_page.cssselect("table[id='srchResultsTable'] tr")

#for tr in current_table:
#  print tr + "\n"


  # Each dataset row is in the class <td id="resultDataCentered" class="resultTableData">. Therefore,
  # extract these rows.
  
  # Extract the table


  # Determine if a "next page" exists
  # A next page exists if the next page icon is valid.  A valid next page icon has the following form:
  #   <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page"></a>
  # Thus, if the <img> whose name is "nextPgIcon" has the src value of "images/icons/nextArrow-blue.gif",
  # a next page exists.

  #for tr in response_page.cssselect("

  # Fetch the next page if it exists




#for tr in root.cssselect("div[align='left'] tr"):
#  tds = tr.cssselect("td")
#  if len(tds)==12:
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    print data

    # To store data in the datastore, replace the "print data" line with the following line
    #scraperwiki.sqlite.save(unique_keys=['country'], data=data)

# To acquire data from the datastore, use this line
#select * from swdata order by years_in_school desc limit 10