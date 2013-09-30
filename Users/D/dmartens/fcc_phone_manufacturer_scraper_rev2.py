# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# ------------------------------------------------------------------------------------------------------

def parseResponseObject(response_object):
  # This function must consider three scenarios:
  # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
  # 2. a single page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">
  # 3. multiple pages of data were returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

  # Handle scenario 1 (empty table) first
  if ((response_object.cssselect("div[id='noMatch']")) == ""):
    print "No match found!"
    return

  # Must be either 2nd or 3rd case if we are still executing the function. Start with 2nd scenario

  # Extract each row within the result table by identifying the table with id=srchResultsTable
  rows = response_object.cssselect("table[id='srchResultsTable'] tr")

  #print the rows
  #for row in rows:
  #  print lxml.html.tostring(row) + "\n"

  # generate a string comprising only the rows
  rows_string = ""
  for row in rows:
    rows_string = rows_string + lxml.html.tostring(row)

  # Now extract the rows containing useful data, which have class='resultTableData'
  rows_only = lxml.html.fromstring(rows_string)
  rows_useful_odd = rows_only.cssselect("tr.resultBg1")
  rows_useful_even = rows_only.cssselect("tr.resultBg2")

  # combine odd and even rows into a single array of rows that can be processed
  rows_useful_combined = []
  for current_row in rows_useful_odd:
    rows_useful_combined.append(current_row)
  for current_row in rows_useful_even:
    rows_useful_combined.append(current_row)
  #print "%i rows of useful data found" % (len(rows_useful_combined))

  # Now parse the combined rows and store them
  for current_useful_row in rows_useful_combined:
    columns = current_useful_row.cssselect("td.resultTableData")
    frn = current_useful_row.cssselect("td.resultTableData a")[0]

    # the FRN will be the unique ID for each record
    scraperwiki.sqlite.save(unique_keys=["FRN"], data={"FRN":frn.text, "Registrant":columns[1].text, "Contact":columns[2].text, "Address":columns[3].text, "City":columns[4].text, "State":columns[5].text, "Zip":columns[6].text, "Country":columns[7].text, "RegDate":columns[8].text})

  # Now determine whether the current page is not the last page. If a next page exists, the following HTML will be present: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

  next_page_icon = response_object.cssselect("img[alt='Next Page']")

  if (next_page_icon):
    # Not null so must have found the next page icon
    print "Next page detected"
  else:
    print "No next page detected"
    return

  # must be third scenario - extract the next page link and parse its data
  # In this scenario, we want to mimic clicking on this link: <a href='/coresWeb/advancedSearch.do?next=true'>
  target_next_page = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?next=true"

  response_next_page = br.open(target_next_page) # The response object
  response_page_next = response_next_page.read()
  response_next_page_object = lxml.html.fromstring(response_page_next)

  # now parse it
  parseResponseObject(response_next_page_object)
  print "Current table processing completed."

# ------------------------------------------------------------------------------------------------------

# This is the webform that the FCC presents to users for querying the manufacturer database
target = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?btnSearch=true"

# Pull the initial webform from the FCC server
br = mechanize.Browser()
br.set_handle_robots(False) # This disables voluntary consideration of the robots.txt file

response = br.open(target) # The response object

# The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
# print "All forms:", [ form.name  for form in br.forms() ]

# This is the form to focus on within the page returned
target_form = 'advancedSearchForm'

# Select the form from within the browser object
br.select_form(name=target_form)

# This is the field within the form that we wish to set prior to POSTing the form
target_form_field = 'bizName'

# Set the form field to the business name we wish to search for
br[target_form_field] = 'samsung*'

# Submit the form, store the response to the submitted form in an object named "response", convert the response to a text page, and then convert the text page to an object
response = br.submit()
response_page = response.read()
response_object = lxml.html.fromstring(response_page)

parseResponseObject(response_object)

print "Processing completed."

# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# ------------------------------------------------------------------------------------------------------

def parseResponseObject(response_object):
  # This function must consider three scenarios:
  # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
  # 2. a single page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">
  # 3. multiple pages of data were returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

  # Handle scenario 1 (empty table) first
  if ((response_object.cssselect("div[id='noMatch']")) == ""):
    print "No match found!"
    return

  # Must be either 2nd or 3rd case if we are still executing the function. Start with 2nd scenario

  # Extract each row within the result table by identifying the table with id=srchResultsTable
  rows = response_object.cssselect("table[id='srchResultsTable'] tr")

  #print the rows
  #for row in rows:
  #  print lxml.html.tostring(row) + "\n"

  # generate a string comprising only the rows
  rows_string = ""
  for row in rows:
    rows_string = rows_string + lxml.html.tostring(row)

  # Now extract the rows containing useful data, which have class='resultTableData'
  rows_only = lxml.html.fromstring(rows_string)
  rows_useful_odd = rows_only.cssselect("tr.resultBg1")
  rows_useful_even = rows_only.cssselect("tr.resultBg2")

  # combine odd and even rows into a single array of rows that can be processed
  rows_useful_combined = []
  for current_row in rows_useful_odd:
    rows_useful_combined.append(current_row)
  for current_row in rows_useful_even:
    rows_useful_combined.append(current_row)
  #print "%i rows of useful data found" % (len(rows_useful_combined))

  # Now parse the combined rows and store them
  for current_useful_row in rows_useful_combined:
    columns = current_useful_row.cssselect("td.resultTableData")
    frn = current_useful_row.cssselect("td.resultTableData a")[0]

    # the FRN will be the unique ID for each record
    scraperwiki.sqlite.save(unique_keys=["FRN"], data={"FRN":frn.text, "Registrant":columns[1].text, "Contact":columns[2].text, "Address":columns[3].text, "City":columns[4].text, "State":columns[5].text, "Zip":columns[6].text, "Country":columns[7].text, "RegDate":columns[8].text})

  # Now determine whether the current page is not the last page. If a next page exists, the following HTML will be present: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

  next_page_icon = response_object.cssselect("img[alt='Next Page']")

  if (next_page_icon):
    # Not null so must have found the next page icon
    print "Next page detected"
  else:
    print "No next page detected"
    return

  # must be third scenario - extract the next page link and parse its data
  # In this scenario, we want to mimic clicking on this link: <a href='/coresWeb/advancedSearch.do?next=true'>
  target_next_page = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?next=true"

  response_next_page = br.open(target_next_page) # The response object
  response_page_next = response_next_page.read()
  response_next_page_object = lxml.html.fromstring(response_page_next)

  # now parse it
  parseResponseObject(response_next_page_object)
  print "Current table processing completed."

# ------------------------------------------------------------------------------------------------------

# This is the webform that the FCC presents to users for querying the manufacturer database
target = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?btnSearch=true"

# Pull the initial webform from the FCC server
br = mechanize.Browser()
br.set_handle_robots(False) # This disables voluntary consideration of the robots.txt file

response = br.open(target) # The response object

# The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
# print "All forms:", [ form.name  for form in br.forms() ]

# This is the form to focus on within the page returned
target_form = 'advancedSearchForm'

# Select the form from within the browser object
br.select_form(name=target_form)

# This is the field within the form that we wish to set prior to POSTing the form
target_form_field = 'bizName'

# Set the form field to the business name we wish to search for
br[target_form_field] = 'samsung*'

# Submit the form, store the response to the submitted form in an object named "response", convert the response to a text page, and then convert the text page to an object
response = br.submit()
response_page = response.read()
response_object = lxml.html.fromstring(response_page)

parseResponseObject(response_object)

print "Processing completed."

