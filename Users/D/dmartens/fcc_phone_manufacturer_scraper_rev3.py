# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# ------------------------------------------------------------------------------------------------------

class Scraper:
  # This class comprises the main object for the FCC phone scraper. This class will initialize itself
  # upon instantiation and provides member functions for performing traditional actions.

  self.BrowserObject = "" # this common variable will store a pointer to a mechanize.Browser instance
  self.IgnoreRobots = 1 # Scrapers, by their nature, seek automated retrieval of data

  self.FormObjects = {}
  self.PageObjects = {}

  def __init__(self):
    # This is the constructor for the Scraper class. This class shares a Browser instance for
    # each instance of the class but also contains separate variable data for instances of the
    # class reflecting pages or forms.

    self.BrowserObject = mechanize.Browser()

  def SetRobots(self,tempRobotFlag):
    # This method will set or clear the flag that determines whether the robots.txt file is considered

    self.IgnoreRobots = tempRobotFlag
    return

  def DefineForm(self,tempFormName,tempURL):
    # This method creates a ScraperForm object that is referenced within the Scraper class by name FormName
    tempFormObject = ScraperForm(self.GetBrowserObject(),tempURL)
    self.SetForm(tempFormName,tempFormObject)
    return

  def GetForm(self,tempFormName):
    # This method retrieves a previously defined form identifed as tempFormName
    if (!self.FormObject.has_key(tempFormName)):
      print "Error: seeking form with name %s but it doesn't exist.\n" % (tempFormName)
      return(NULL)

    return(self.FormObjects[tempFormName])

  def SetForm(self,tempFormName,tempFormObject):
    # This method stores a form object by name
    self.FormObject[tempFormName] = tempFormObject
    return

  def GetBrowserObject(self):
    # This method merely returns a pointer to a BrowserObject - Form and Page classes call this function
    return(self.BrowserObject)

  def SetBrowserObject(self,tempBrowserObject):
    self.BrowserObject = tempBrowserObject

  def CreateBrowserObject(self):
    self.SetBrowserObject(mechanize.Browser())

Class ScraperForm:
  # This class comprises an object for storing data concerning a specific web form.

  def __init__(self,tempScraperObject):

    self.SetURL("")
    self.SetScraperObject(tempBrowserObject)

  def __init__(self,tempScraperObject,tempURL):

    self.SetURL(tempURL)
    self.SetScraperObject(tempScraperObject)

  def SetScraperObject(self,tempScraperObject):
    self.ScraperObject = tempScraperObject

  def GetScraperObject(self):
    return(self.ScraperObject)

  def SetFormResponseObject(self,tempFormResponseObject):
    self.FormResponseObject = tempFormResponseObject

  def GetFormResponseObject(self):
    return(self.FormResponseObject)

  def SetFormClass(self,tempFormClass):
    self.FormClass = tempFormClass

  def GetFormClass(self):
    return(self.FormClass)

  def SetURL(self,tempURL):
    self.URL = tempURL

  def GetURL(self):
    return(self.URL)

  def SetFormObject(self, tempFormObject):
    # This member function simply stores the form object returned from the Internet
    self.FormObject = tempFormObject

  def GetFormObject(self):
    return(self.FormObject)

  def SetFormObjectFiltered(self, tempFormObjectFiltered):
    # This member function stores the form object representing just the form itself rather than the full page
    self.FormObjectFiltered = tempFormObjectFiltered

  def GetFormObjectFiltered(self):
    return(self.FormObjectFiltered)

  def RetrieveForm(self):
    tempBrowserObject = self.GetScraperObject().GetBrowserObject()
    tempURL = self.GetURL()
    tempFormClass = self.GetFormClass()

    # Pull the form from the Internet
    SetFormObject(self.tempBrowserObject.open(tempURL))

    # Extract the identified form class from the returned page
    self.SetFormObjectFiltered(tempBrowserObject.select_form(name=tempFormClass))

  def SetFieldValue(self,tempFieldName, tempFieldValue):
    self.GetScraperObject().GetBrowserObject()[tempFieldName] = tempFieldValue

  def SubmitForm(self):
    # Submit the form and store the response
    self.SetFormResponseObject(lxml.html.fromstring(self.GetScraperObject().GetBrowserObject().submit().read()))
    
  def ParseFormResponse(self):
    # This member function will get overloaded by an implementing subclass

    # This function must consider three scenarios:
    # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
    # 2. one page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">
    # 3. multiple pages of data was returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">

    # Handle scenario 1 first
    if (self.GetFormResponseObject().cssselect("div[id='noMatch']")) == ""):
      print "No match found!"
      return

    # Must be either the 2nd or 3rd scenario.
    # Evaluating the 2nd scenario

    tempRows = self.GetFormResponseObject().cssselect("table[id='srchResultsTable'] tr")

    # Generate a string comprising only the rows
    tempRowsString = ""
    for tempCurrentRow in tempRows:
      tempRowsString = tempRowsString + lxml.html.tostring(tempCurrentRow)

    # Now extract the rows containing useful data, which have class 'resultTableData'
    tempRowsOnlyString = lxml.html.fromstring(tempRowsString)
    tempRowsUsefulOdd = tempRowsOnlyString.cssselect("tr.resultBg1")
    tempRowsUsefulEven = tempRowsOnlyString.cssselect("tr.resultBg2")

    # Combine even and odd rows into a single array of rows that can be processed
    tempRowsUsefulCombined = []
    for tempCurrentRow in tempRowsUsefulOdd:
      tempRowsUsefulCombined.append(tempCurrentRow)
    for tempCurrentRow in tempRowsUsefulEven:
      tempRowsUsefulCombined.append(tempCurrentRow)

    # Now parse the combined rows and store them
    for tempCurrentRow in tempRowsUsefulCombined:
      tempColumns = tempCurrentRow.cssselect("td.resultTableData")
      tempFRN = tempCurrentRow.cssselect("td.resultTableData a")[0]

    # the FRN will be the unique ID for each record
    scraperwiki.sqlite.save(unique_keys=["FRN"], data={"FRN":tempFRN.text, "Registrant":tempColumns[1].text, "Contact":tempColumns[2].text, "Address":tempColumns[3].text, "City":tempColumns[4].text, "State":tempColumns[5].text, "Zip":tempColumns[6].text, "Country":tempColumns[7].text, "RegDate":tempColumns[8].text})

    # Now determine whether the current page is not the last page. If a next page exists, the following HTML will be present: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

    tempNextPageIcon = self.GetFormResponseObject().cssselect("img[alt='Next Page']")

    if (tempNextPageIcon):
      # Not null so must have found the next page icon
      print "Next page detected"
    else:
      print "No next page detected"
      return

    # must be third scenario - extract the next page link and parse its data
    # In this scenario, we want to mimic clicking on this link: <a href='/coresWeb/advancedSearch.do?next=true'>
    tempNextPageTarget = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?next=true"

    #tempNextPageResponse = br.open(tempNextPageTarget) # The response object
    #response_page_next = response_next_page.read()
    #response_next_page_object = lxml.html.fromstring(response_page_next)

    # Generate a form object by retrieving the next form page from the Internet
    self.SetFormResponseObject(lxml.html.fromstring(self.GetBrowserObject().open(tempNextPageTarget).read()))

    # now parse it
    #parseResponseObject(response_next_page_object)
    self.ParseFormResponse()
    print "Current table processing completed."
    return

Class ScraperPage:
  # This class comprises an object for storing data concerning a specific web page.
  
  def __init__(self):

    self.URL = ""

  def __init__(self,URL):

    self.URL = URL

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

# This string is used for iterating on search characters
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Pull the initial webform from the FCC server
##br = mechanize.Browser()
##br.set_handle_robots(False) # This disables voluntary consideration of the robots.txt file

Scraper = Scraper() # Create a Scraper object

# Set a name to refer to the form
TargetFormName = "FCC third-party identifier form"

# Create a form object with the name and target specified
ScraperForm = Scraper.DefineForm(TargetFormName,target)

for current_first_letter in "a":
  #print "processing first letter %s" % (current_first_letter)
  for current_second_letter in "a":
    #print "processing second letter %s" % (current_second_letter)

    # 
    #response = br.open(target) # The response object
    
    # Get the form from the Internet and store results internal to ScraperForm
    ScraperForm.RetrieveForm()

    # The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
    # print "All forms:", [ form.name  for form in br.forms() ]

    # This is the form to focus on within the page returned
    target_form = 'advancedSearchForm'

    # store the form class sought
    ScraperForm.SetFormClass(target_form)

    # Select the form from within the browser object
    #br.select_form(name=target_form)    

    # This is the field within the form that we wish to set prior to POSTing the form
    target_form_field = 'bizName'

    # Set the form field to the business name we wish to search for
    #br[target_form_field] = 'samsung*'
    #current_search_string = current_first_letter + current_second_letter + "*"
    current_search_string = "samsung*"
    print "current_search_string is %s" % (current_search_string)

    #br[target_form_field] = current_search_string
    # Identify form field to be modified and value of modified field
    ScraperForm.SetFieldValue(target_form_field,current_search_string)

    # Submit the form, store the response to the submitted form in an object named "response", convert the response to a text page, and then convert the text page to an object
    #response = br.submit()
    #response_page = response.read()
    #response_object = lxml.html.fromstring(response_page)
    #parseResponseObject(response_object)
    ScraperForm.SubmitForm()
    ScraperForm.ParseFormResponse()

    print "second letter %s has been processed" % (current_second_letter)
  print "first letter %s has been processed" % (current_first_letter)

print "Processing completed."

# ------------------------------------------------------------------------------------------------------

# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# ------------------------------------------------------------------------------------------------------

class Scraper:
  # This class comprises the main object for the FCC phone scraper. This class will initialize itself
  # upon instantiation and provides member functions for performing traditional actions.

  self.BrowserObject = "" # this common variable will store a pointer to a mechanize.Browser instance
  self.IgnoreRobots = 1 # Scrapers, by their nature, seek automated retrieval of data

  self.FormObjects = {}
  self.PageObjects = {}

  def __init__(self):
    # This is the constructor for the Scraper class. This class shares a Browser instance for
    # each instance of the class but also contains separate variable data for instances of the
    # class reflecting pages or forms.

    self.BrowserObject = mechanize.Browser()

  def SetRobots(self,tempRobotFlag):
    # This method will set or clear the flag that determines whether the robots.txt file is considered

    self.IgnoreRobots = tempRobotFlag
    return

  def DefineForm(self,tempFormName,tempURL):
    # This method creates a ScraperForm object that is referenced within the Scraper class by name FormName
    tempFormObject = ScraperForm(self.GetBrowserObject(),tempURL)
    self.SetForm(tempFormName,tempFormObject)
    return

  def GetForm(self,tempFormName):
    # This method retrieves a previously defined form identifed as tempFormName
    if (!self.FormObject.has_key(tempFormName)):
      print "Error: seeking form with name %s but it doesn't exist.\n" % (tempFormName)
      return(NULL)

    return(self.FormObjects[tempFormName])

  def SetForm(self,tempFormName,tempFormObject):
    # This method stores a form object by name
    self.FormObject[tempFormName] = tempFormObject
    return

  def GetBrowserObject(self):
    # This method merely returns a pointer to a BrowserObject - Form and Page classes call this function
    return(self.BrowserObject)

  def SetBrowserObject(self,tempBrowserObject):
    self.BrowserObject = tempBrowserObject

  def CreateBrowserObject(self):
    self.SetBrowserObject(mechanize.Browser())

Class ScraperForm:
  # This class comprises an object for storing data concerning a specific web form.

  def __init__(self,tempScraperObject):

    self.SetURL("")
    self.SetScraperObject(tempBrowserObject)

  def __init__(self,tempScraperObject,tempURL):

    self.SetURL(tempURL)
    self.SetScraperObject(tempScraperObject)

  def SetScraperObject(self,tempScraperObject):
    self.ScraperObject = tempScraperObject

  def GetScraperObject(self):
    return(self.ScraperObject)

  def SetFormResponseObject(self,tempFormResponseObject):
    self.FormResponseObject = tempFormResponseObject

  def GetFormResponseObject(self):
    return(self.FormResponseObject)

  def SetFormClass(self,tempFormClass):
    self.FormClass = tempFormClass

  def GetFormClass(self):
    return(self.FormClass)

  def SetURL(self,tempURL):
    self.URL = tempURL

  def GetURL(self):
    return(self.URL)

  def SetFormObject(self, tempFormObject):
    # This member function simply stores the form object returned from the Internet
    self.FormObject = tempFormObject

  def GetFormObject(self):
    return(self.FormObject)

  def SetFormObjectFiltered(self, tempFormObjectFiltered):
    # This member function stores the form object representing just the form itself rather than the full page
    self.FormObjectFiltered = tempFormObjectFiltered

  def GetFormObjectFiltered(self):
    return(self.FormObjectFiltered)

  def RetrieveForm(self):
    tempBrowserObject = self.GetScraperObject().GetBrowserObject()
    tempURL = self.GetURL()
    tempFormClass = self.GetFormClass()

    # Pull the form from the Internet
    SetFormObject(self.tempBrowserObject.open(tempURL))

    # Extract the identified form class from the returned page
    self.SetFormObjectFiltered(tempBrowserObject.select_form(name=tempFormClass))

  def SetFieldValue(self,tempFieldName, tempFieldValue):
    self.GetScraperObject().GetBrowserObject()[tempFieldName] = tempFieldValue

  def SubmitForm(self):
    # Submit the form and store the response
    self.SetFormResponseObject(lxml.html.fromstring(self.GetScraperObject().GetBrowserObject().submit().read()))
    
  def ParseFormResponse(self):
    # This member function will get overloaded by an implementing subclass

    # This function must consider three scenarios:
    # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
    # 2. one page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">
    # 3. multiple pages of data was returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">

    # Handle scenario 1 first
    if (self.GetFormResponseObject().cssselect("div[id='noMatch']")) == ""):
      print "No match found!"
      return

    # Must be either the 2nd or 3rd scenario.
    # Evaluating the 2nd scenario

    tempRows = self.GetFormResponseObject().cssselect("table[id='srchResultsTable'] tr")

    # Generate a string comprising only the rows
    tempRowsString = ""
    for tempCurrentRow in tempRows:
      tempRowsString = tempRowsString + lxml.html.tostring(tempCurrentRow)

    # Now extract the rows containing useful data, which have class 'resultTableData'
    tempRowsOnlyString = lxml.html.fromstring(tempRowsString)
    tempRowsUsefulOdd = tempRowsOnlyString.cssselect("tr.resultBg1")
    tempRowsUsefulEven = tempRowsOnlyString.cssselect("tr.resultBg2")

    # Combine even and odd rows into a single array of rows that can be processed
    tempRowsUsefulCombined = []
    for tempCurrentRow in tempRowsUsefulOdd:
      tempRowsUsefulCombined.append(tempCurrentRow)
    for tempCurrentRow in tempRowsUsefulEven:
      tempRowsUsefulCombined.append(tempCurrentRow)

    # Now parse the combined rows and store them
    for tempCurrentRow in tempRowsUsefulCombined:
      tempColumns = tempCurrentRow.cssselect("td.resultTableData")
      tempFRN = tempCurrentRow.cssselect("td.resultTableData a")[0]

    # the FRN will be the unique ID for each record
    scraperwiki.sqlite.save(unique_keys=["FRN"], data={"FRN":tempFRN.text, "Registrant":tempColumns[1].text, "Contact":tempColumns[2].text, "Address":tempColumns[3].text, "City":tempColumns[4].text, "State":tempColumns[5].text, "Zip":tempColumns[6].text, "Country":tempColumns[7].text, "RegDate":tempColumns[8].text})

    # Now determine whether the current page is not the last page. If a next page exists, the following HTML will be present: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

    tempNextPageIcon = self.GetFormResponseObject().cssselect("img[alt='Next Page']")

    if (tempNextPageIcon):
      # Not null so must have found the next page icon
      print "Next page detected"
    else:
      print "No next page detected"
      return

    # must be third scenario - extract the next page link and parse its data
    # In this scenario, we want to mimic clicking on this link: <a href='/coresWeb/advancedSearch.do?next=true'>
    tempNextPageTarget = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?next=true"

    #tempNextPageResponse = br.open(tempNextPageTarget) # The response object
    #response_page_next = response_next_page.read()
    #response_next_page_object = lxml.html.fromstring(response_page_next)

    # Generate a form object by retrieving the next form page from the Internet
    self.SetFormResponseObject(lxml.html.fromstring(self.GetBrowserObject().open(tempNextPageTarget).read()))

    # now parse it
    #parseResponseObject(response_next_page_object)
    self.ParseFormResponse()
    print "Current table processing completed."
    return

Class ScraperPage:
  # This class comprises an object for storing data concerning a specific web page.
  
  def __init__(self):

    self.URL = ""

  def __init__(self,URL):

    self.URL = URL

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

# This string is used for iterating on search characters
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Pull the initial webform from the FCC server
##br = mechanize.Browser()
##br.set_handle_robots(False) # This disables voluntary consideration of the robots.txt file

Scraper = Scraper() # Create a Scraper object

# Set a name to refer to the form
TargetFormName = "FCC third-party identifier form"

# Create a form object with the name and target specified
ScraperForm = Scraper.DefineForm(TargetFormName,target)

for current_first_letter in "a":
  #print "processing first letter %s" % (current_first_letter)
  for current_second_letter in "a":
    #print "processing second letter %s" % (current_second_letter)

    # 
    #response = br.open(target) # The response object
    
    # Get the form from the Internet and store results internal to ScraperForm
    ScraperForm.RetrieveForm()

    # The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
    # print "All forms:", [ form.name  for form in br.forms() ]

    # This is the form to focus on within the page returned
    target_form = 'advancedSearchForm'

    # store the form class sought
    ScraperForm.SetFormClass(target_form)

    # Select the form from within the browser object
    #br.select_form(name=target_form)    

    # This is the field within the form that we wish to set prior to POSTing the form
    target_form_field = 'bizName'

    # Set the form field to the business name we wish to search for
    #br[target_form_field] = 'samsung*'
    #current_search_string = current_first_letter + current_second_letter + "*"
    current_search_string = "samsung*"
    print "current_search_string is %s" % (current_search_string)

    #br[target_form_field] = current_search_string
    # Identify form field to be modified and value of modified field
    ScraperForm.SetFieldValue(target_form_field,current_search_string)

    # Submit the form, store the response to the submitted form in an object named "response", convert the response to a text page, and then convert the text page to an object
    #response = br.submit()
    #response_page = response.read()
    #response_object = lxml.html.fromstring(response_page)
    #parseResponseObject(response_object)
    ScraperForm.SubmitForm()
    ScraperForm.ParseFormResponse()

    print "second letter %s has been processed" % (current_second_letter)
  print "first letter %s has been processed" % (current_first_letter)

print "Processing completed."

# ------------------------------------------------------------------------------------------------------

