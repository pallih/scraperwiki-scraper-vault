# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# --------------------------------------------------------------------------------------

# "Scraper" is the main class for this program. Scraper instantiates one or more "ScraperForm"
# or "ScraperPage" instances, each of which handle interfacing with a web form. Therefore, a proper 
# procedure would be to instantiate Scraper and then have Scraper generate a ScraperForm or
# ScraperPage.

# Defined debug levels: (from 1 [lowest] to 4 [highest]) - higher levels print more
CONST_DEBUGLEVEL_ERROR = 1 # 1 - print error conditions
CONST_DEBUGLEVEL_RESULTS = 2 # 2 - also print functional results such as parsing results or steps taken
CONST_DEBUGLEVEL_OBJECTCREATION = 3 # 3 - also print object creation results
CONST_DEBUGLEVEL_FUNCTIONS = 4 # 4 - also print function entry and exit messages

# The next two constants are used for range checks
CONST_DEBUGLEVEL_MINIMUM = CONST_DEBUGLEVEL_ERROR
CONST_DEBUGLEVEL_MAXIMUM = CONST_DEBUGLEVEL_FUNCTIONS

CONST_BOOLEAN_TRUE = 1
CONST_BOOLEAN_FALSE = 0
CONST_BOOLEAN_ERROR = -1 # Return code for functions that return boolean values and experience errors

CONST_NEWLINE = "\n"
CONST_EMPTYSTRING = ""
CONST_COMMA = ","

#CONST_ERRORSTRING_DEBUGLEVEL_NOTSET = "ERROR: ScraperDebug() was called with its DebugLevel parameter not set as an integer"
CONST_ERRORSTRING_DEBUGLEVEL_OUTOFRANGE = "ERROR: ScraperDebug() was called with a message level of (%i), which is outside its allowable range of (%i) to (%i)"

CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONE = "ERROR: ScraperDebug() was called with its tempDebugMessage parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONSTRING = "ERROR: ScraperDebug() received ARG tempDebugMessage as non-string"
CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONE = "ERROR: ScraperDebug() was called with its tempDebugLevel parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONINTEGER = "ERROR: ScraperDebug() received ARG tempDebugLevel as non-integer"

CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPFUNCTIONNAME_NONE = "ERROR: ScraperDebugFunctionEntry() was called with its tempFunctionName parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPFUNCTIONNAME_NONSTRING = "ERROR: ScraperDebugFunctionEntry() received ARG tempFunctionName as non-string"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONE = "ERROR: ScraperDebugFunctionEntry() was called with its tempMessageArray parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONARRAY = "ERROR: ScraperDebugFunctionEntry() received ARG tempMessageArray as non-array"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_STRING = "string(%s)"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_INTEGER = "int(%i)"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_UNKNOWN = "(unknown)"
CONST_OKSTRING_SCRAPERDEBUGFUNCTIONENTRY_MESSAGE = "Entering function (%s()) with ARGV(%s)"

CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONE = "ERROR: ScraperDebugFunctionExit() was called with its tempFunctionName parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONSTRING = "ERROR: ScraperDebugFunctionExit() received ARG tempFunctionName as non-string"
CONST_OKSTRING_SCRAPERDEBUGFUNCTIONEXIT_MESSAGE = "Exiting function (%s())"

CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONE = "ERROR: ScraperDebugObjectCreation() was called with its tempObjectName parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONSTRING = "ERROR: ScraperDebugObjectCreation() received ARG tempObjectName as non-string"
CONST_OKSTRING_SCRAPERDEBUGOBJECTCREATION_MESSAGE = "Object (%s) was created"

CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONE = "ERROR: ScraperDebugFunctionalMessage() was called with its tempFunctionalMessage parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONSTRING = "ERROR: ScraperDebugFunctionalMessage() received ARG tempFunctionalMessage as non-string"
CONST_OKSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_MESSAGE = "(%s)"

CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONE = "ERROR: ScraperDebugErrorMessage() was called with its tempErrorMessage parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONSTRING = "ERROR: ScraperDebugErrorMessage() received ARG tempErrorMessage as non-string"
CONST_OKSTRING_SCRAPERDEBUGERRORMESSAGE_MESSAGE = "Error: %s"

CONST_FUNCTION_MAIN = "main"

CONST_CLASSNAME_SCRAPER = "Scraper"
CONST_CLASSNAME_SCRAPERFORM = "ScraperForm"

CONST_FUNCTION_SCRAPER_INIT_NAME = "Scraper.__init__"

CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_NAME = "Scraper.SetRobotsIgnore"
CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_FUNCTIONALMESSAGE = "Set RobotsIgnore to TRUE"

CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_NAME = "Scraper.SetRobotsRespect"
CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_FUNCTIONALMESSAGE = "Set RobotsIgnore to FALSE"

CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME = "Scraper.GetRobotsIgnoreFlag"
CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONE = "ERROR: ScraperForm.GetRobotsIgnoreFlag() was called but ScraperForm.IgnoreRobots is None"
CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONINTEGER = "ERROR: ScraperForm.GetRobotsIgnoreFlag() found that ScraperObject.IgnoreRobots did not refer to an integer"
CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONBOOLEAN = "ERROR: ScraperForm.GetRobotsIgnoreFlag() found that ScraperObject.IgnoreRobots did not contain a boolean value (0 or 1)"

CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME = "Scraper.DefineForm"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONE = "ERROR: Scraper.DefineForm() was called with its tempFormName parameter as NONE"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONSTRING = "ERROR: Scraper.DefineForm() received ARG tempFormName as non-string"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONE = "ERROR: Scraper.DefineForm() was called with its tempURL parameter as NONE"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONSTRING = "ERROR: Scraper.DefineForm() received ARG tempURL as non-string"
#CONST_ERRORSTRING_SCRAPER_DEFINEFORM_SCRAPERFORM_ALLOCATIONERROR = "ERROR: Scraper.DefineForm() failed to allocate a ScraperForm object"

CONST_FUNCTION_SCRAPER_GETFORM_NAME = "Scraper.GetForm"
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONE = "ERROR: Scraper.GetForm() was called with its tempFormName parameter as NONE"
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONSTRING = "ERROR: Scraper.GetForm() received ARG tempFormName as non-string"
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONEXISTENT = "ERROR: Scraper.GetForm() sought a form with name (%s) but it doesn't exist."
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_VALUE_NONE = "ERROR: Scraper.GetForm() sought a form with name (%s) but the stored form with that name was None"
CONST_FUNCTION_SCRAPER_GETFORM_FUNCTIONALMESSAGE = "Retrieved form object"

CONST_FUNCTION_SCRAPER_SETFORM_NAME = "Scraper.SetForm"
CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONE = "ERROR: Scraper.SetForm() was called with its tempFormName parameter as NONE"
CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONSTRING = "ERROR: Scraper.SetForm() received ARG tempFormName as non-string"
CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMOBJECT_NONE = "ERROR: Scraper.SetForm() was called with its tempFormObject parameter as NONE"
CONST_FUNCTION_SCRAPER_SETFORM_FUNCTIONALMESSAGE = "Stored form object"

CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME = "Scraper.GetBrowserObject"
CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_FUNCTIONALMESSAGE = "Retrieved browser object"

CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME = "Scraper.SetBrowserObject"
CONST_ERRORSTRING_SCRAPER_SETBROWSEROBJECT_TEMPBROWSEROBJECT_NONE = "ERROR: Scraper.SetBrowserObject() was called with its tempBrowserObject parameter as NONE"
CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_FUNCTIONALMESSAGE = "Stored browser object"

CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_NAME = "Scraper.CreateBrowserObject"
CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_OBJECTCREATED = "mechanize.Browser"

CONST_FUNCTION_SCRAPERFORM_INIT_NAME = "ScraperForm.__init__"
CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPSCRAPEROBJECT_NONE = "ERROR: ScraperForm.__init__() was called with its tempScraperObject parameter as NONE"
CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL = "ERROR: ScraperForm.__init__() was called with its tempURL parameter as NONE"
CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL_NONSTRING = "ERROR: ScraperForm.__init__() received ARG tempURL as non-string"

CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME = "ScraperForm.SetScraperObject"
CONST_ERRORSTRING_SCRAPERFORM_SETSCRAPEROBJECT_TEMPSCRAPEROBJECT_NONE = "ERROR: ScraperForm.SetScraperObject() was called with its tempScraperObject parameter as NONE"
CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_FUNCTIONALMESSAGE = "Stored scraper object"

CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME = "ScraperForm.GetScraperObject"
CONST_ERRORSTRING_SCRAPERFORM_GETSCRAPEROBJECT_SCRAPERFORMSCRAPEROBJECT_NONE = "ERROR: ScraperForm.GetScraperObject() was called but ScraperForm.ScraperObject is NONE"

CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME = "ScraperForm.SetFormResponseObject"
CONST_ERRORSTRING_SCRAPERFORM_SETFORMRESPONSEOBJECT_TEMPFORMRESPONSEOBJECT_NONE = "ERROR: ScraperForm.SetFormResponseObject() was called with its tempFormResponseObject parameter as NONE"
CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_FUNCTIONALMESSAGE = "Stored form response object"

CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME = "ScraperForm.GetFormResponseObject"
CONST_ERRORSTRING_SCRAPERFORM_GETFORMRESPONSEOBJECT_SCRAPERFORMFORMRESPONSEOBJECT_NONE = "ERROR: ScraperForm.GetFormResponseObject() was called but ScraperForm.FormResponseObject is NONE"

CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME = "ScraperForm.SetFormClass"
CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONE = "ERROR: ScraperForm.SetFormClass() was called with its tempFormClass parameter as NONE"
CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONSTRING = "ERROR: ScraperForm.SetFormClass() received ARG tempFormClass as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_FUNCTIONALMESSAGE = "Stored form class as (%s)"

CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME = "ScraperForm.GetFormClass"
CONST_ERRORSTRING_SCRAPERFORM_GETFORMCLASS_FORMRESPONSEOBJECT_NONE = "ERROR: ScraperForm.GetFormClass() was called but ScraperForm.FormResponseObject is NONE"

CONST_FUNCTION_SCRAPERFORM_SETURL_NAME = "ScraperForm.SetURL"
CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONE = "ERROR: ScraperForm.setURL() received ARG tempURL as None"
CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONSTRING = "ERROR: ScraperForm.setURL() received ARG tempURL as non-string"
CONST_FUNCTION_SCRAPERFORM_SETURL_FUNCTIONALMESSAGE = "Stored ScraperForm.URL as (%s)"

CONST_FUNCTION_SCRAPERFORM_GETURL_NAME = "ScraperForm.GetURL"
CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONE = "ERROR: ScraperForm.getURL() was called with self.URL as None"
CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONSTRING = "ERROR: ScraperForm.getURL() was called with self.URL as non-string"
CONST_FUNCTION_SCRAPERFORM_GETURL_FUNCTIONALMESSAGE = "Read ScraperForm.URL as (%s)"

CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME = "ScraperForm.SetFormObject"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_TEMPFORMOBJECT_NONE = "ERROR: ScraperForm.SetFormObject() received ARG tempFormObject as None"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_FUNCTIONALMESSAGE = "Set form object"

CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME = "ScraperForm.GetFormObject"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FORMOBJCET_NONE = "ERROR: ScraperForm.GetFormObject() was called with self.FormObject as None"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FUNCTIONALMESSAGE = "Retrieved form object"

CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME = "ScraperForm.SetFormObjectFiltered"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_TEMPFORMOBJECTFILTERED_NONE = "ERROR: ScraperForm.SetFormObjectFiltered() received ARG tempFormObjectFiltered as None"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_FUNCTIONALMESSAGE = "Stored filtered form object"

CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME = "ScraperForm.GetFormObjectFiltered"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FORMOBJECTFILTERED_NONE = "ERROR: ScraperForm.GetFormObjectFiltered() was called with self.FormObjectFiltered as None"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FUNCTIONALMESSAGE = "Retrieved filtered form object"

CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME = "ScraperForm.RetrieveForm"
CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_TEMPFORMOBJECT_NONE = "ScraperForm.RetrieveForm attempted to open URL (%s) but received None as a response."
CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_FUNCTIONALMESSAGE = "Retrieved form from the Internet at (%s) and stored it"

CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME = "ScraperForm.SetFieldValue"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONE = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldName as None"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONSTRING = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldName as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONE = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldValue as None"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONSTRING = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldValue as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONE = "ERROR: ScraperForm.SetFieldValue() retrieved tempFieldName (%s) from form as None"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONSTRING = "ERROR: ScraperForm.SetFieldValue() retrieved tempFieldName (%s) from form as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_FUNCTIONALMESSAGE = "Set field named (%s) as (%s)"

CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME = "ScraperForm.SubmitForm"
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_RESPONSE_NONE = "Error: ScraperForm.SubmitForm() submitted a form but received None in response."
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSE_NONE = "Error: ScraperForm.SubmitForm() read a responsive form but found None."
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSEOBJECT_NONE = "Error: ScraperForm.SubmitForm() parsed the result from a submitted form but found None."
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMSUBMITTED = "Form submitted"
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMREADSTORED = "Form response read and stored"

CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME = "ScraperForm.ParseFormCSS"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONE = "Error: ScraperForm.ParseFormCSS() received ARG tempCSS as None"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONSTRING = "ERROR: ScraperForm.ParseFormCSS() received ARG tempCSS as non-string"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMATCH = "ScraperForm.ParseFormCSS searched for CSS text (%s) and found it."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMISS = "ScraperForm.ParseFormCSS searched for CSS text (%s) but DID NOT find it."

CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME = "ScraperForm.ParseCSS"
CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONE = "Error: ScraperForm.ParseCSS() received ARG tempCSS as None"
CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONSTRING = "ERROR: ScraperForm.ParseCSS() received ARG tempCSS as non-string"
CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMATCH = "ScraperForm.ParseCSS searched for CSS text (%s) and found it."
CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMISS = "ScraperForm.ParseCSS searched for CSS text (%s) but DID NOT find it."

CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_NAME = "ScraperForm.GetFormNameList"
CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_STRING = "(%s)"

CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_NAME = "ScraperForm.ParseformResponse"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO1 = "ScraperForm.ParseFormResponse() determined that 'no match' was returned by the server."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO1 = "div[id='noMatch']"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_RESULTTABLE = "table[id='srchResultsTable'] tr"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_ODDROW = "tr.resultBg1"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_EVENROW = "tr.resultBg2"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_COLUMNS = "td.resultTableData"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_TEMPFRN = "td.resultTableData a"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_FRN = "FRN"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_FRN = 0
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGISTRANT = "Registrant"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGISTRANT = 1
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CONTACT = "Contact"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CONTACT = 2
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ADDRESS = "Address"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ADDRESS = 3
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CITY = "City"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CITY = 4
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_STATE = "State"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_STATE = 5
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ZIP = "Zip"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ZIP = 6
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_COUNTRY = "Country"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_COUNTRY = 7
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGDATE = "RegDate"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGDATE = 8
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_UNIQUEKEYS = CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_FRN
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_NEXTPAGE = "img[alt='Next Page']"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGEFOUND = "Next page detected - parse it."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGENOTFOUND = "Next page NOT detected - second scenario is complete."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO3_TARGETURL = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?next=true"

# This is the lowest level of debug a default setting and reflects minimal debugging info
DebugLevel = CONST_DEBUGLEVEL_ERROR 

def ScraperDebug(tempDebugMessage,tempDebugLevel):
  # The DebugLevel variable reflects what level the system debug is set to and
  # the tempDebugLevel variable reflects the debug level that is required for
  # the present debug message to be printed

  # This function will print a debug  message if the DebugLevel >= tempDebugLevel
  # (i.e., if the global debug level is >= to debug level needed to print 

  if (tempDebugMessage is None):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONE
    return

  if not(isinstance(tempDebugMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONSTRING
    return

  if (tempDebugLevel is None):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONE
    return

  if not(isinstance(tempDebugLevel, int)):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONINTEGER
    return

  if ((tempDebugLevel > CONST_DEBUGLEVEL_MAXIMUM) or (tempDebugLevel < CONST_DEBUGLEVEL_MINIMUM)):
    print CONST_ERRORSTRING_DEBUGLEVEL_OUTOFRANGE % (tempDebugLevel, CONST_DEBUGLEVEL_MINIMUM, CONST_DEBUGLEVEL_MAXIMUM)
    return

  # ARGVs were apparently OK - proceed with debug message if global debug level is >= debug level for current message
  if (DebugLevel >= tempDebugLevel):
    print tempDebugMessage + CONST_NEWLINE

  return

def ScraperDebugFunctionEntry(tempFunctionName,tempMessageArray):

  tempDebugString = CONST_EMPTYSTRING # This string reflects the entire debug message as it is constructed
  tempArgvString  = CONST_EMPTYSTRING # This string is used to construct an ARGV string
  tempFirstElementFlag = CONST_BOOLEAN_TRUE # used for managing the comma in ARGV string generation

  # ARGV error checking
  if (tempFunctionName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPFUNCTIONNAME_NONE
    return

  if not(isinstance(tempFunctionName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPDEBUGMESSAGE_NONSTRING
    return

  if (tempMessageArray is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONE
    return

  if not(isinstance(tempMessageArray, list)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONARRAY
    return

  for tempCurrentArrayElement in tempMessageArray:
    if not(tempFirstElementFlag):
      # Add a comma to the working string before adding the next ARGV component
      tempDebugString = tempDebugString + CONST_COMMA

    if (isinstance(tempCurrentArrayElement,str)):
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_STRING % tempCurrentArrayElement
    elif (isinstance(tempCurrentArrayElement,int)):
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_INTEGER % tempCurrentArrayElement
    else:
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_UNKNOWN

    tempDebugString = tempDebugString + tempArgvString
    tempFirstElementFlag = CONST_BOOLEAN_FALSE # Commas should be added before each subsequent ARGV string

  ScraperDebug(CONST_OKSTRING_SCRAPERDEBUGFUNCTIONENTRY_MESSAGE % (tempFunctionName,tempDebugString),CONST_DEBUGLEVEL_FUNCTIONS)
  return

def ScraperDebugFunctionExit(tempFunctionName):

  # ARGV error checking
  if (tempFunctionName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONE
    return

  if not(isinstance(tempFunctionName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGFUNCTIONEXIT_MESSAGE % (tempFunctionName)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_FUNCTIONS)
  return

def ScraperDebugObjectCreation(tempObjectName):

  # ARGV error checking
  if (tempObjectName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONE
    return

  if not(isinstance(tempObjectName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGOBJECTCREATION_MESSAGE % (tempObjectName)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_OBJECTCREATION)
  return

def ScraperDebugFunctionalMessage(tempFunctionalMessage):

  # ARGV error checking
  if (tempFunctionalMessage is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONE
    return

  if not(isinstance(tempFunctionalMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_MESSAGE % (tempFunctionalMessage)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_RESULTS)
  return

def ScraperDebugErrorMessage(tempErrorMessage):

  # ARGV error checking
  if (tempErrorMessage is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONE
    return

  if not(isinstance(tempErrorMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGERRORMESSAGE_MESSAGE % (tempErrorMessage)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_ERROR)
  return

class Scraper:
  # This class comprises the main object for the FCC phone scraper. This class will 
  # initialize itself upon instantiation and provides member functions for performing 
  # traditional actions.

  # this common variable will store a pointer to a mechanize.Browser instance

  def __init__(self):
    # This is the constructor for the Scraper class. This class shares a Browser instance for
    # each instance of the class but also contains separate variable data for instances of the
    # class reflecting pages or forms.

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_INIT_NAME,[])

    self.BrowserObject = CONST_EMPTYSTRING 

    self.FormObject = {}

    self.SetRobotsIgnore() # Scrapers, by their nature, seek automated retrieval of data

    self.CreateBrowserObject() # Create a browser object and store it for later use

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_INIT_NAME)

  def SetRobotsIgnore(self):
    # This method will set the flag that determines whether the robots.txt file is considered

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_NAME,[])

    self.IgnoreRobots = CONST_BOOLEAN_TRUE
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_NAME)
    return

  def SetRobotsRespect(self):
    # This method will set the flag that determines whether the robots.txt file is considered

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_NAME,[])

    self.IgnoreRobots = CONST_BOOLEAN_FALSE
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_NAME)
    return

  def GetRobotsIgnoreFlag(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME,[])

    # Do error checking to ensure that the robots flag had previously been set
    if (self.IgnoreRobots is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)
      return(CONST_BOOLEAN_ERROR)

    if not(isinstance(self.IgnoreRobots, int)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONINTEGER)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)
      return(CONST_BOOLEAN_ERROR)

    if ((self.IgnoreRobots != CONST_BOOLEAN_TRUE) and (self.IgnoreRobots != CONST_BOOLEAN_FALSE)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONBOOLEAN)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)
      return(CONST_BOOLEAN_ERROR)
      
    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)

    return(self.IgnoreRobots)

  def DefineForm(self,tempFormName,tempURL):
    # This method creates a ScraperForm object that is referenced within the Scraper class by name FormName

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME,[tempFormName,tempURL])

    # ARGV error checking
    if (tempFormName is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if not(isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if not(isinstance(tempURL, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)      
      return(CONST_BOOLEAN_ERROR)

    tempBrowserObject = self.GetBrowserObject()

    tempFormObject = ScraperForm(self,tempURL)
    ScraperDebugObjectCreation(CONST_CLASSNAME_SCRAPERFORM)

    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_SCRAPERFORM_ALLOCATIONERROR)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    self.SetForm(tempFormName,tempFormObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
    return(CONST_BOOLEAN_TRUE)

  def GetForm(self,tempFormName):
    # This method retrieves a previously defined form identifed as tempFormName

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_GETFORM_NAME,[tempFormName])

    # ARGV error checking
    if (tempFormName is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)
      return(None)

    if not(isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)
      return(None)

    if not(self.FormObject.has_key(tempFormName)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONEXISTENT % (tempFormName))
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  
      return(None)

    tempFormObject = self.FormObject[tempFormName]
    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_VALUE_NONE % (tempFormName))
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  
      return(None)

    # AR: confirm that a FormObject was stored and retrieved

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_GETFORM_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  

    return(tempFormObject)

  def SetForm(self,tempFormName,tempFormObject):
    # This method stores a form object by name
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETFORM_NAME,[tempFormName,tempFormObject])

    # ARGV error checking
    if (tempFormName is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)
      return

    if not(isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)
      return

    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)
      return

    # AR: add an error checking routine to ensure that a FormObject was received
    #if (!isinstance(tempFormName, str)):
    #  ScraperDebugErrorMessage("ERROR: Scraper.SetForm() received ARG tempFormName as non-string")
    #  ScraperDebugFunctionExit("Scraper.SetForm")
    #  return

    self.FormObject[tempFormName] = tempFormObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETFORM_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)

  def GetBrowserObject(self):
    # This method merely returns a pointer to a BrowserObject - Form and Page classes call this function
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME,[])

    tempBrowserObject = self.BrowserObject
    if (tempBrowserObject is None):
      ScraperDebugErrorMessage("ERROR: Scraper.GetBrowserObject() read self.BrowserObject but found that it was None.")
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME,[])

    # AR: add check to ensure that self.BrowserObject is a Browser object

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME)

    return(self.BrowserObject)

  def SetBrowserObject(self,tempBrowserObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME,[tempBrowserObject])

    # ARGV error checking
    if (tempBrowserObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETBROWSEROBJECT_TEMPBROWSEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME)
      return

    # AR: add an error checking routine to ensure that a BrowserObject was received
    #if (!isinstance(tempBrowserObject, str)):
    #  ScraperDebugErrorMessage("ERROR: Scraper.SetBrowserObject() received ARG tempBrowserObject as non-string")
    #  ScraperDebugFunctionExit("Scraper.SetBrowserObject")
    #  return

    self.BrowserObject = tempBrowserObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME)

  def CreateBrowserObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_NAME,[])

    tempBrowserObject = mechanize.Browser()
    # AR: insert error checking code ensuring that a Browser object was returned

    ScraperDebugObjectCreation(CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_OBJECTCREATED)

    self.SetBrowserObject(tempBrowserObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_NAME)

class ScraperForm:
  # This class comprises an object for storing data concerning a specific web form.

  def __init__(self,tempScraperObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_INIT_NAME,[tempScraperObject])

    # ARGV error checking
    if (tempScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.__init__() received ARG tempScraperObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.__init__")
    #  return

    self.SetURL(CONST_EMPTYSTRING)
    self.SetScraperObject(tempScraperObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)

  def __init__(self,tempScraperObject,tempURL):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_INIT_NAME,[tempScraperObject,tempURL])

    # ARGV error checking
    if (tempScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.__init__() received ARG tempScraperObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.__init__")
    #  return

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    if not(isinstance(tempURL, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    self.SetURL(tempURL)
    self.SetScraperObject(tempScraperObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)

  def SetScraperObject(self,tempScraperObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME,[tempScraperObject])

    # ARGV error checking
    if (tempScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETSCRAPEROBJECT_TEMPSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetScraperObject() received ARG tempScraperObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.SetScraperObject")
    #  return

    self.ScraperObject = tempScraperObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME)
    return

  def GetScraperObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME,[])

    # Do error checking to ensure that the scraper object had previously been set
    if (self.ScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETSCRAPEROBJECT_SCRAPERFORMSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME)
      return(None)

    # AR: add an error check to ensure that self.ScraperObject refers to a scraper object
    #if (!isinstance(self.ScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetScraperObject() found that ScraperObject.ScraperObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit("ScraperForm.GetScraperObject")
    #  return(None)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME)

    return(self.ScraperObject)

  def SetFormResponseObject(self,tempFormResponseObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME,[tempFormResponseObject])

    # ARGV error checking
    if (tempFormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMRESPONSEOBJECT_TEMPFORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempFormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetFormResponseObject() received ARG tempFormResponseObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.SetFormResponseObject")
    #  return

    self.FormResponseObject = tempFormResponseObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME)

  def GetFormResponseObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME,[])

    # Do error checking to ensure that the form response object had previously been set
    if (self.FormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETFORMRESPONSEOBJECT_SCRAPERFORMFORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME)
      return(None)

    # AR: add an error check to ensure that self.ScraperObject refers to a scraper object
    #if (!isinstance(self.FormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetFormResponseObject() found that ScraperObject.FormResponseObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit("ScraperForm.GetFormResponseObject")
    #  return(None)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME)

    return(self.FormResponseObject)

  def SetFormClass(self,tempFormClass):
    # This function receives a form class and selects that form within the current page
    # returned by the browser
    
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME,[tempFormClass])

    # ARGV error checking
    if (tempFormClass is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)
      return

    if not(isinstance(tempFormClass, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)
      return

    self.FormClass = tempFormClass
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_FUNCTIONALMESSAGE % tempFormClass)

    # Now select the form within the Browser object using the equivalent of this code: br.select_form(name=target_form)
    self.GetScraperObject().GetBrowserObject().select_form(name=tempFormClass)
    
    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)

  def GetFormClass(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME,[])

    # Do error checking to ensure that the form class had previously been set
    if (self.FormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETFORMCLASS_FORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)
      return(None)

    # AR: add an error check to ensure that self.FormResponseObject refers to a form object
    #if (!isinstance(self.FormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetFormClass() found that ScraperObject.FormResponseObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)
    #  return(None)


    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)

    return(self.FormClass)

  def SetURL(self,tempURL):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME,[tempURL])

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    if not(isinstance(tempURL,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    self.URL = tempURL

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETURL_FUNCTIONALMESSAGE % tempURL)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    return

  def GetURL(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME,[])

    if (self.URL is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME)

    if not(isinstance(self.URL,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_GETURL_FUNCTIONALMESSAGE % self.URL)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME)

    return(self.URL)

  def SetFormObject(self, tempFormObject):
    # This member function simply stores the form object returned from the Internet

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME,[tempFormObject])

    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_TEMPFORMOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)
      return(None)

    # AR: test whether tempFormObject is a form object
    #if (!isinstance(tempFormObject,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetFormObject() received ARG tempFormObject as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    self.FormObject = tempFormObject

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME)

    return(tempFormObject)

  def GetFormObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME,[])

    if (self.FormObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FORMOBJCET_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    # AR: check whether self.FormObject is a form object
    #if (!isinstance(self.URL,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.getURL() was called with self.URL as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    return(self.FormObject)

  def SetFormObjectFiltered(self, tempFormObjectFiltered):
    # This member function stores the form object representing just the form itself rather than the full page

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME,[tempFormObjectFiltered])

    if (tempFormObjectFiltered is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_TEMPFORMOBJECTFILTERED_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME)

    # AR: test whether tempFormObjectFiltered is a form object
    #if (!isinstance(tempFormObject,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetFormObject() received ARG tempFormObject as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    self.FormObjectFiltered = tempFormObjectFiltered

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME)
    return

  def GetFormObjectFiltered(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME,[])

    if (self.FormObjectFiltered is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FORMOBJECTFILTERED_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    # AR: check whether self.FormObjectFiltered is a form object
    #if (!isinstance(self.URL,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.getURL() was called with self.URL as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME)

    return(self.FormObjectFiltered)

  def RetrieveForm(self):
    # This function reads a URL stored in this object and reads a form at that URL
    
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME,[])

    tempBrowserObject = self.GetScraperObject().GetBrowserObject()
    tempURL = self.GetURL()
    #tempFormClass = self.GetFormClass()

    # Set Robots flag accordingly
    if self.GetScraperObject().GetRobotsIgnoreFlag == CONST_BOOLEAN_TRUE:
      tempRobotsFlag = True
    else:
      tempRobotsFlag = False

    self.GetScraperObject().GetBrowserObject().set_handle_robots(tempRobotsFlag)

    # Pull the form from the Internet
    tempFormObject = tempBrowserObject.open(tempURL)
    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_TEMPFORMOBJECT_NONE % tempURL)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME)
      return(None)

    self.SetFormObject(tempFormObject)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_FUNCTIONALMESSAGE % tempURL)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME)

    return

  def SetFieldValue(self,tempFieldName, tempFieldValue):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME,[tempFieldName,tempFieldValue])

    if (tempFieldName is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if not(isinstance(tempFieldName,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if (tempFieldValue is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if not(isinstance(tempFieldValue,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if (self.GetScraperObject().GetBrowserObject()[tempFieldName] is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONE % tempFieldName)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if not(isinstance(tempFieldName,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONSTRING % tempFieldName)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    self.GetScraperObject().GetBrowserObject()[tempFieldName] = tempFieldValue

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_FUNCTIONALMESSAGE % (tempFieldName,tempFieldValue))

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

  def SubmitForm(self):
    # Submit the form and store the response

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME,[])

    # Submit the form and store result
    tempResponse = self.GetScraperObject().GetBrowserObject().submit()
    if (tempResponse is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_RESPONSE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
      return(None)
    
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMSUBMITTED)

    # Read the response in
    tempFormResponse = tempResponse.read()
    if (tempFormResponse is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
      return(None)
    
    # Parse response into form
    tempFormResponseObject = lxml.html.fromstring(tempFormResponse)
    if (tempFormResponseObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
      return(None)
    
    self.SetFormResponseObject(tempFormResponseObject)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMREADSTORED)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)

  def ParseCSS(self,tempTargetCSS,tempDataToParse):
    # This function receives a string with which to parse a received form and then extracts the portion
    # of the returned form with that CSS and returns a reference to that extracted result

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME,[tempTargetCSS])

    if (tempDataToParse is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPDATATOPARSE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    # AR: add a checking routine to ensure that tempDataToParse is an object of the proper type
    #if (!isinstance(tempDataToParse,str):
    #  ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPDATATOPARSE_NONSTRING)
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    if (tempTargetCSS is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    if not(isinstance(tempTargetCSS,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    tempParsedCSS = tempDataToParse.cssselect(tempTargetCSS)
    
    ScraperDebugFunctionalMessage("ScraperForm.ParseCSS found (%s)" % tempParsedCSS)

    if (not tempParsedCSS):
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMISS % tempTargetCSS)
      return(None)
      
    # Must not have been a MISS so is a MATCH
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMATCH % tempTargetCSS)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    return(tempParsedCSS)
    
  def ParseFormCSS(self,tempTargetCSS):
    # This function receives a string with which to seek within a received form and then extracts the portion
    # of the returned form with that CSS and returns a reference to that extracted result

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME,[tempTargetCSS])

    if (tempTargetCSS is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME)

    if not(isinstance(tempTargetCSS,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME)

    tempFormResponseObject = self.GetFormResponseObject()
    tempParsedCSS = self.ParseCSS(tempTargetCSS,tempFormResponseObject) # returns an array of HTML elements
    
    if (tempParsedCSS is None): # if array is empty must not have found it (so abort)
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMISS % tempTargetCSS)
      return(None)
      
    # Must not have been a MISS so is a MATCH
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMATCH % tempTargetCSS)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME)

    return(tempParsedCSS)

  def GetFormNameList(self):
    # This function creates a list of form names returned from a URL

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_NAME,[])

    tempFormString = CONST_EMPTYSTRING
    for tempForm in self.GetScraperObject().GetBrowserObject().forms():
      tempFormString = tempFormString + CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_STRING % tempForm.name

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_NAME)

    return(tempFormString)

  def ParseFormResponse(self):
    # This member function will get overloaded by an implementing subclass

    # This function must consider three scenarios:
    # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
    # 2. one page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">
    # 3. multiple pages of data was returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_NAME,[])

    # Handle scenario 1 first - check received form for CSS ID that reflects "no match"
    tempParsedFormCSS = self.ParseFormCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO1)
    if (tempParsedFormCSS):
      # Found the CSS class that reflects "no match"
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO1)
      return
      
    # Must be either the 2nd or 3rd scenario.
    # Evaluating the 2nd scenario

    tempRows = self.ParseFormCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_RESULTTABLE)

    # Generate a string comprising only the rows
    tempRowsString = CONST_EMPTYSTRING
    for tempCurrentRow in tempRows:
      tempRowsString = tempRowsString + lxml.html.tostring(tempCurrentRow)

    # Now extract the rows containing useful data, which have class 'resultTableData'
    tempRowsOnlyString = lxml.html.fromstring(tempRowsString)
    tempRowsUsefulOdd = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_ODDROW,tempRowsOnlyString)
    tempRowsUsefulEven = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_EVENROW,tempRowsOnlyString)

    # Combine even and odd rows into a single array of rows that can be processed
    tempRowsUsefulCombined = []
    for tempCurrentRow in tempRowsUsefulOdd:
      tempRowsUsefulCombined.append(tempCurrentRow)
    for tempCurrentRow in tempRowsUsefulEven:
      tempRowsUsefulCombined.append(tempCurrentRow)

    #print "The length of tempRowsUsefulCombined is %i" % len(tempRowsUsefulCombined)

    # Now parse the combined rows and store them
    for tempCurrentRow in tempRowsUsefulCombined:
      tempColumns = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_COLUMNS,tempCurrentRow)
      #print "The number of columns found is %i" % len(tempColumns)

      tempFRN = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_TEMPFRN,tempCurrentRow)[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_FRN]
      #tempColumns = tempCurrentRow.cssselect(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_COLUMNS)
      #tempFRN = tempCurrentRow.cssselect(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_TEMPFRN)[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_FRN]
      #print "Found tempFRN of %s" % tempFRN

    # the FRN will be the unique ID for each record
      scraperwiki.sqlite.save(unique_keys=[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_UNIQUEKEYS], 
        data={CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_FRN:tempFRN.text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGISTRANT:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGISTRANT].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CONTACT:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CONTACT].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ADDRESS:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ADDRESS].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CITY:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CITY].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_STATE:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_STATE].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ZIP:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ZIP].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_COUNTRY:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_COUNTRY].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGDATE:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGDATE].text})

    # Now determine whether the current page is not the last page. If a next page exists, the following HTML will be present: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

    tempNextPageIcon = self.ParseFormCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_NEXTPAGE)

    if (tempNextPageIcon):
      # Not null so must have found the next page icon
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGEFOUND)
    else:
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGENOTFOUND)
      return # return because no 'next page' to process - we are done with the second scenario

    # must be third scenario - extract the next page link and parse its data
    # In this scenario, we want to mimic clicking on this link: <a href='/coresWeb/advancedSearch.do?next=true'>

    #tempNextPageResponse = br.open(tempNextPageTarget) # The response object
    #response_page_next = response_next_page.read()
    #response_next_page_object = lxml.html.fromstring(response_page_next)

    # Generate a form object by retrieving the next form page from the Internet
    #self.SetURL(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO3_TARGETURL)
    #tempFormObject = self.RetrieveForm()
    
    self.SetFormResponseObject(lxml.html.fromstring(self.GetScraperObject().GetBrowserObject().open(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO3_TARGETURL).read()))

    # now parse it
    #parseResponseObject(response_next_page_object)
    self.ParseFormResponse()

    #print "Current table processing completed."

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_NAME)
    return


# ------------------------------------------------------------------------------------------------------

ScraperDebugFunctionEntry(CONST_FUNCTION_MAIN,[])

DebugLevel = 1 # turn results and errors on (only)

# This is the webform that the FCC presents to users for querying the manufacturer database
tempTarget = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?btnSearch=true"

# This string is used for iterating on search characters
alphabet = "bcdefghijklmnopqrstuvwxyz"

# Create a form object with the name and target specified
# Processing proceeds as follows: 
# 1. Retrieve one or more forms at the URL provided (and store those forms)
# 2. Within the retrieved URL, select the form we want
# 3. Modify the selected form to reflect data settings for that form
# 4. Submit the modified form
# 5. Interpret the result received after submitting the modified form
# 6. Act on the interpreted result, which may lead to recursive processing


for tempFirstLetter in alphabet:
  ScraperDebugFunctionalMessage("Processing first letter (%s)" % tempFirstLetter )
  for tempSecondLetter in alphabet:
    ScraperDebugFunctionalMessage("Processing second letter (%s)" % tempSecondLetter )
    
    tempScraper = Scraper() # Create a Scraper object

    if (tempScraper is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_MAIN_FAILEDTOALLOCATESCRAPER)
      ScraperDebugFunctionExit(CONST_FUNCTION_MAIN,[])

    ScraperDebugFunctionalMessage("A Scraper object has been created.")
    # AR: check that Scraper is of a Scraper() class

    # Set a name to refer to the form
    tempTargetFormName = "FCC third-party identifier form"

    tempScraper.DefineForm(tempTargetFormName,tempTarget)

    tempScraperForm = tempScraper.GetForm(tempTargetFormName)

    ScraperDebugFunctionalMessage("A ScraperForm object has been defined with the name (%s)" % tempTargetFormName)


    # Get the form from the Internet and store results internal to ScraperForm
    tempScraperForm.RetrieveForm()

    # The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
    #print "These are the forms that were retrieved from the Internet:",[ form.name  for form in Scraper.GetBrowserObject().forms() ]
    tempFormString = tempScraperForm.GetFormNameList()
    ScraperDebugFunctionalMessage("Found the following forms: %s" % tempFormString)

    # This is the form to focus on within the page returned
    tempTargetForm = 'advancedSearchForm'

    # store the form class sought and then select the form with that class from within the URL retrieved
    tempScraperForm.SetFormClass(tempTargetForm)

    # This is the field within the selected form that we wish to set prior to POSTing the form
    tempTargetFormField = 'bizName'

    # Set the form field to the business name we wish to search for
    #br[tempTargetFormField] = 'samsung*'
    #tempCurrentSearchString = current_first_letter + current_second_letter + "*"
    #tempCurrentSearchString = "samsung*"
    tempCurrentSearchString = tempFirstLetter + tempSecondLetter + "*"
    ScraperDebugFunctionalMessage("Current business name search string is: %s" % tempCurrentSearchString)

    #br[tempTargetFormField] = tempCurrentSearchString
    # Identify form field to be modified and value of modified field
    tempScraperForm.SetFieldValue(tempTargetFormField,tempCurrentSearchString)

    # Submit the form, store the response to the submitted form in an object named "response", convert the response to a text page, and then convert the text page to an object
    #response = br.submit()
    #response_page = response.read()
    #response_object = lxml.html.fromstring(response_page)
    #parseResponseObject(response_object)
    
    # Submit the form so we can parse the results
    tempScraperForm.SubmitForm()
    
    # Parse the results
    tempScraperForm.ParseFormResponse()

    ScraperDebugFunctionalMessage("Processing complete for second letter (%s)" % tempSecondLetter )

    #print "second letter %s has been processed" % (current_second_letter)

    ScraperDebugFunctionalMessage("Processing complete for first letter (%s)" % tempFirstLetter )
    #print "first letter %s has been processed" % (current_first_letter)

    #ScraperForm = Scraper.GetForm(tempTargetFormName) # refetch the input form so we can provide another search string

ScraperDebugFunctionalMessage("All processing complete.")

ScraperDebugFunctionExit(CONST_FUNCTION_MAIN)

# ------------------------------------------------------------------------------------------------------

# This scraper generates a table of cell phone manufacturers that have submitted to the 
# FCC requests for authorization to market an identified cell phone within the US. Once
# the list of manufacturers is developed, a list of submitted cell phones can also be
# ascertained. This script performs the first part (manufacturer identification).

# Import needed libraries
import scraperwiki
import mechanize 
import lxml.html

# --------------------------------------------------------------------------------------

# "Scraper" is the main class for this program. Scraper instantiates one or more "ScraperForm"
# or "ScraperPage" instances, each of which handle interfacing with a web form. Therefore, a proper 
# procedure would be to instantiate Scraper and then have Scraper generate a ScraperForm or
# ScraperPage.

# Defined debug levels: (from 1 [lowest] to 4 [highest]) - higher levels print more
CONST_DEBUGLEVEL_ERROR = 1 # 1 - print error conditions
CONST_DEBUGLEVEL_RESULTS = 2 # 2 - also print functional results such as parsing results or steps taken
CONST_DEBUGLEVEL_OBJECTCREATION = 3 # 3 - also print object creation results
CONST_DEBUGLEVEL_FUNCTIONS = 4 # 4 - also print function entry and exit messages

# The next two constants are used for range checks
CONST_DEBUGLEVEL_MINIMUM = CONST_DEBUGLEVEL_ERROR
CONST_DEBUGLEVEL_MAXIMUM = CONST_DEBUGLEVEL_FUNCTIONS

CONST_BOOLEAN_TRUE = 1
CONST_BOOLEAN_FALSE = 0
CONST_BOOLEAN_ERROR = -1 # Return code for functions that return boolean values and experience errors

CONST_NEWLINE = "\n"
CONST_EMPTYSTRING = ""
CONST_COMMA = ","

#CONST_ERRORSTRING_DEBUGLEVEL_NOTSET = "ERROR: ScraperDebug() was called with its DebugLevel parameter not set as an integer"
CONST_ERRORSTRING_DEBUGLEVEL_OUTOFRANGE = "ERROR: ScraperDebug() was called with a message level of (%i), which is outside its allowable range of (%i) to (%i)"

CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONE = "ERROR: ScraperDebug() was called with its tempDebugMessage parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONSTRING = "ERROR: ScraperDebug() received ARG tempDebugMessage as non-string"
CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONE = "ERROR: ScraperDebug() was called with its tempDebugLevel parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONINTEGER = "ERROR: ScraperDebug() received ARG tempDebugLevel as non-integer"

CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPFUNCTIONNAME_NONE = "ERROR: ScraperDebugFunctionEntry() was called with its tempFunctionName parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPFUNCTIONNAME_NONSTRING = "ERROR: ScraperDebugFunctionEntry() received ARG tempFunctionName as non-string"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONE = "ERROR: ScraperDebugFunctionEntry() was called with its tempMessageArray parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONARRAY = "ERROR: ScraperDebugFunctionEntry() received ARG tempMessageArray as non-array"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_STRING = "string(%s)"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_INTEGER = "int(%i)"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_UNKNOWN = "(unknown)"
CONST_OKSTRING_SCRAPERDEBUGFUNCTIONENTRY_MESSAGE = "Entering function (%s()) with ARGV(%s)"

CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONE = "ERROR: ScraperDebugFunctionExit() was called with its tempFunctionName parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONSTRING = "ERROR: ScraperDebugFunctionExit() received ARG tempFunctionName as non-string"
CONST_OKSTRING_SCRAPERDEBUGFUNCTIONEXIT_MESSAGE = "Exiting function (%s())"

CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONE = "ERROR: ScraperDebugObjectCreation() was called with its tempObjectName parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONSTRING = "ERROR: ScraperDebugObjectCreation() received ARG tempObjectName as non-string"
CONST_OKSTRING_SCRAPERDEBUGOBJECTCREATION_MESSAGE = "Object (%s) was created"

CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONE = "ERROR: ScraperDebugFunctionalMessage() was called with its tempFunctionalMessage parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONSTRING = "ERROR: ScraperDebugFunctionalMessage() received ARG tempFunctionalMessage as non-string"
CONST_OKSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_MESSAGE = "(%s)"

CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONE = "ERROR: ScraperDebugErrorMessage() was called with its tempErrorMessage parameter as NONE"
CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONSTRING = "ERROR: ScraperDebugErrorMessage() received ARG tempErrorMessage as non-string"
CONST_OKSTRING_SCRAPERDEBUGERRORMESSAGE_MESSAGE = "Error: %s"

CONST_FUNCTION_MAIN = "main"

CONST_CLASSNAME_SCRAPER = "Scraper"
CONST_CLASSNAME_SCRAPERFORM = "ScraperForm"

CONST_FUNCTION_SCRAPER_INIT_NAME = "Scraper.__init__"

CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_NAME = "Scraper.SetRobotsIgnore"
CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_FUNCTIONALMESSAGE = "Set RobotsIgnore to TRUE"

CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_NAME = "Scraper.SetRobotsRespect"
CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_FUNCTIONALMESSAGE = "Set RobotsIgnore to FALSE"

CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME = "Scraper.GetRobotsIgnoreFlag"
CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONE = "ERROR: ScraperForm.GetRobotsIgnoreFlag() was called but ScraperForm.IgnoreRobots is None"
CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONINTEGER = "ERROR: ScraperForm.GetRobotsIgnoreFlag() found that ScraperObject.IgnoreRobots did not refer to an integer"
CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONBOOLEAN = "ERROR: ScraperForm.GetRobotsIgnoreFlag() found that ScraperObject.IgnoreRobots did not contain a boolean value (0 or 1)"

CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME = "Scraper.DefineForm"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONE = "ERROR: Scraper.DefineForm() was called with its tempFormName parameter as NONE"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONSTRING = "ERROR: Scraper.DefineForm() received ARG tempFormName as non-string"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONE = "ERROR: Scraper.DefineForm() was called with its tempURL parameter as NONE"
CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONSTRING = "ERROR: Scraper.DefineForm() received ARG tempURL as non-string"
#CONST_ERRORSTRING_SCRAPER_DEFINEFORM_SCRAPERFORM_ALLOCATIONERROR = "ERROR: Scraper.DefineForm() failed to allocate a ScraperForm object"

CONST_FUNCTION_SCRAPER_GETFORM_NAME = "Scraper.GetForm"
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONE = "ERROR: Scraper.GetForm() was called with its tempFormName parameter as NONE"
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONSTRING = "ERROR: Scraper.GetForm() received ARG tempFormName as non-string"
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONEXISTENT = "ERROR: Scraper.GetForm() sought a form with name (%s) but it doesn't exist."
CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_VALUE_NONE = "ERROR: Scraper.GetForm() sought a form with name (%s) but the stored form with that name was None"
CONST_FUNCTION_SCRAPER_GETFORM_FUNCTIONALMESSAGE = "Retrieved form object"

CONST_FUNCTION_SCRAPER_SETFORM_NAME = "Scraper.SetForm"
CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONE = "ERROR: Scraper.SetForm() was called with its tempFormName parameter as NONE"
CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONSTRING = "ERROR: Scraper.SetForm() received ARG tempFormName as non-string"
CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMOBJECT_NONE = "ERROR: Scraper.SetForm() was called with its tempFormObject parameter as NONE"
CONST_FUNCTION_SCRAPER_SETFORM_FUNCTIONALMESSAGE = "Stored form object"

CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME = "Scraper.GetBrowserObject"
CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_FUNCTIONALMESSAGE = "Retrieved browser object"

CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME = "Scraper.SetBrowserObject"
CONST_ERRORSTRING_SCRAPER_SETBROWSEROBJECT_TEMPBROWSEROBJECT_NONE = "ERROR: Scraper.SetBrowserObject() was called with its tempBrowserObject parameter as NONE"
CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_FUNCTIONALMESSAGE = "Stored browser object"

CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_NAME = "Scraper.CreateBrowserObject"
CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_OBJECTCREATED = "mechanize.Browser"

CONST_FUNCTION_SCRAPERFORM_INIT_NAME = "ScraperForm.__init__"
CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPSCRAPEROBJECT_NONE = "ERROR: ScraperForm.__init__() was called with its tempScraperObject parameter as NONE"
CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL = "ERROR: ScraperForm.__init__() was called with its tempURL parameter as NONE"
CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL_NONSTRING = "ERROR: ScraperForm.__init__() received ARG tempURL as non-string"

CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME = "ScraperForm.SetScraperObject"
CONST_ERRORSTRING_SCRAPERFORM_SETSCRAPEROBJECT_TEMPSCRAPEROBJECT_NONE = "ERROR: ScraperForm.SetScraperObject() was called with its tempScraperObject parameter as NONE"
CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_FUNCTIONALMESSAGE = "Stored scraper object"

CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME = "ScraperForm.GetScraperObject"
CONST_ERRORSTRING_SCRAPERFORM_GETSCRAPEROBJECT_SCRAPERFORMSCRAPEROBJECT_NONE = "ERROR: ScraperForm.GetScraperObject() was called but ScraperForm.ScraperObject is NONE"

CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME = "ScraperForm.SetFormResponseObject"
CONST_ERRORSTRING_SCRAPERFORM_SETFORMRESPONSEOBJECT_TEMPFORMRESPONSEOBJECT_NONE = "ERROR: ScraperForm.SetFormResponseObject() was called with its tempFormResponseObject parameter as NONE"
CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_FUNCTIONALMESSAGE = "Stored form response object"

CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME = "ScraperForm.GetFormResponseObject"
CONST_ERRORSTRING_SCRAPERFORM_GETFORMRESPONSEOBJECT_SCRAPERFORMFORMRESPONSEOBJECT_NONE = "ERROR: ScraperForm.GetFormResponseObject() was called but ScraperForm.FormResponseObject is NONE"

CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME = "ScraperForm.SetFormClass"
CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONE = "ERROR: ScraperForm.SetFormClass() was called with its tempFormClass parameter as NONE"
CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONSTRING = "ERROR: ScraperForm.SetFormClass() received ARG tempFormClass as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_FUNCTIONALMESSAGE = "Stored form class as (%s)"

CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME = "ScraperForm.GetFormClass"
CONST_ERRORSTRING_SCRAPERFORM_GETFORMCLASS_FORMRESPONSEOBJECT_NONE = "ERROR: ScraperForm.GetFormClass() was called but ScraperForm.FormResponseObject is NONE"

CONST_FUNCTION_SCRAPERFORM_SETURL_NAME = "ScraperForm.SetURL"
CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONE = "ERROR: ScraperForm.setURL() received ARG tempURL as None"
CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONSTRING = "ERROR: ScraperForm.setURL() received ARG tempURL as non-string"
CONST_FUNCTION_SCRAPERFORM_SETURL_FUNCTIONALMESSAGE = "Stored ScraperForm.URL as (%s)"

CONST_FUNCTION_SCRAPERFORM_GETURL_NAME = "ScraperForm.GetURL"
CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONE = "ERROR: ScraperForm.getURL() was called with self.URL as None"
CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONSTRING = "ERROR: ScraperForm.getURL() was called with self.URL as non-string"
CONST_FUNCTION_SCRAPERFORM_GETURL_FUNCTIONALMESSAGE = "Read ScraperForm.URL as (%s)"

CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME = "ScraperForm.SetFormObject"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_TEMPFORMOBJECT_NONE = "ERROR: ScraperForm.SetFormObject() received ARG tempFormObject as None"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_FUNCTIONALMESSAGE = "Set form object"

CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME = "ScraperForm.GetFormObject"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FORMOBJCET_NONE = "ERROR: ScraperForm.GetFormObject() was called with self.FormObject as None"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FUNCTIONALMESSAGE = "Retrieved form object"

CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME = "ScraperForm.SetFormObjectFiltered"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_TEMPFORMOBJECTFILTERED_NONE = "ERROR: ScraperForm.SetFormObjectFiltered() received ARG tempFormObjectFiltered as None"
CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_FUNCTIONALMESSAGE = "Stored filtered form object"

CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME = "ScraperForm.GetFormObjectFiltered"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FORMOBJECTFILTERED_NONE = "ERROR: ScraperForm.GetFormObjectFiltered() was called with self.FormObjectFiltered as None"
CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FUNCTIONALMESSAGE = "Retrieved filtered form object"

CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME = "ScraperForm.RetrieveForm"
CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_TEMPFORMOBJECT_NONE = "ScraperForm.RetrieveForm attempted to open URL (%s) but received None as a response."
CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_FUNCTIONALMESSAGE = "Retrieved form from the Internet at (%s) and stored it"

CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME = "ScraperForm.SetFieldValue"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONE = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldName as None"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONSTRING = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldName as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONE = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldValue as None"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONSTRING = "ERROR: ScraperForm.SetFieldValue() received ARG tempFieldValue as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONE = "ERROR: ScraperForm.SetFieldValue() retrieved tempFieldName (%s) from form as None"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONSTRING = "ERROR: ScraperForm.SetFieldValue() retrieved tempFieldName (%s) from form as non-string"
CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_FUNCTIONALMESSAGE = "Set field named (%s) as (%s)"

CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME = "ScraperForm.SubmitForm"
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_RESPONSE_NONE = "Error: ScraperForm.SubmitForm() submitted a form but received None in response."
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSE_NONE = "Error: ScraperForm.SubmitForm() read a responsive form but found None."
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSEOBJECT_NONE = "Error: ScraperForm.SubmitForm() parsed the result from a submitted form but found None."
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMSUBMITTED = "Form submitted"
CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMREADSTORED = "Form response read and stored"

CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME = "ScraperForm.ParseFormCSS"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONE = "Error: ScraperForm.ParseFormCSS() received ARG tempCSS as None"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONSTRING = "ERROR: ScraperForm.ParseFormCSS() received ARG tempCSS as non-string"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMATCH = "ScraperForm.ParseFormCSS searched for CSS text (%s) and found it."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMISS = "ScraperForm.ParseFormCSS searched for CSS text (%s) but DID NOT find it."

CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME = "ScraperForm.ParseCSS"
CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONE = "Error: ScraperForm.ParseCSS() received ARG tempCSS as None"
CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONSTRING = "ERROR: ScraperForm.ParseCSS() received ARG tempCSS as non-string"
CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMATCH = "ScraperForm.ParseCSS searched for CSS text (%s) and found it."
CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMISS = "ScraperForm.ParseCSS searched for CSS text (%s) but DID NOT find it."

CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_NAME = "ScraperForm.GetFormNameList"
CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_STRING = "(%s)"

CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_NAME = "ScraperForm.ParseformResponse"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO1 = "ScraperForm.ParseFormResponse() determined that 'no match' was returned by the server."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO1 = "div[id='noMatch']"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_RESULTTABLE = "table[id='srchResultsTable'] tr"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_ODDROW = "tr.resultBg1"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_EVENROW = "tr.resultBg2"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_COLUMNS = "td.resultTableData"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_TEMPFRN = "td.resultTableData a"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_FRN = "FRN"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_FRN = 0
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGISTRANT = "Registrant"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGISTRANT = 1
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CONTACT = "Contact"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CONTACT = 2
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ADDRESS = "Address"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ADDRESS = 3
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CITY = "City"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CITY = 4
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_STATE = "State"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_STATE = 5
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ZIP = "Zip"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ZIP = 6
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_COUNTRY = "Country"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_COUNTRY = 7
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGDATE = "RegDate"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGDATE = 8
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_UNIQUEKEYS = CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_FRN
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_NEXTPAGE = "img[alt='Next Page']"
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGEFOUND = "Next page detected - parse it."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGENOTFOUND = "Next page NOT detected - second scenario is complete."
CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO3_TARGETURL = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?next=true"

# This is the lowest level of debug a default setting and reflects minimal debugging info
DebugLevel = CONST_DEBUGLEVEL_ERROR 

def ScraperDebug(tempDebugMessage,tempDebugLevel):
  # The DebugLevel variable reflects what level the system debug is set to and
  # the tempDebugLevel variable reflects the debug level that is required for
  # the present debug message to be printed

  # This function will print a debug  message if the DebugLevel >= tempDebugLevel
  # (i.e., if the global debug level is >= to debug level needed to print 

  if (tempDebugMessage is None):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONE
    return

  if not(isinstance(tempDebugMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONSTRING
    return

  if (tempDebugLevel is None):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONE
    return

  if not(isinstance(tempDebugLevel, int)):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONINTEGER
    return

  if ((tempDebugLevel > CONST_DEBUGLEVEL_MAXIMUM) or (tempDebugLevel < CONST_DEBUGLEVEL_MINIMUM)):
    print CONST_ERRORSTRING_DEBUGLEVEL_OUTOFRANGE % (tempDebugLevel, CONST_DEBUGLEVEL_MINIMUM, CONST_DEBUGLEVEL_MAXIMUM)
    return

  # ARGVs were apparently OK - proceed with debug message if global debug level is >= debug level for current message
  if (DebugLevel >= tempDebugLevel):
    print tempDebugMessage + CONST_NEWLINE

  return

def ScraperDebugFunctionEntry(tempFunctionName,tempMessageArray):

  tempDebugString = CONST_EMPTYSTRING # This string reflects the entire debug message as it is constructed
  tempArgvString  = CONST_EMPTYSTRING # This string is used to construct an ARGV string
  tempFirstElementFlag = CONST_BOOLEAN_TRUE # used for managing the comma in ARGV string generation

  # ARGV error checking
  if (tempFunctionName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPFUNCTIONNAME_NONE
    return

  if not(isinstance(tempFunctionName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPDEBUGMESSAGE_NONSTRING
    return

  if (tempMessageArray is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONE
    return

  if not(isinstance(tempMessageArray, list)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONARRAY
    return

  for tempCurrentArrayElement in tempMessageArray:
    if not(tempFirstElementFlag):
      # Add a comma to the working string before adding the next ARGV component
      tempDebugString = tempDebugString + CONST_COMMA

    if (isinstance(tempCurrentArrayElement,str)):
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_STRING % tempCurrentArrayElement
    elif (isinstance(tempCurrentArrayElement,int)):
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_INTEGER % tempCurrentArrayElement
    else:
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_UNKNOWN

    tempDebugString = tempDebugString + tempArgvString
    tempFirstElementFlag = CONST_BOOLEAN_FALSE # Commas should be added before each subsequent ARGV string

  ScraperDebug(CONST_OKSTRING_SCRAPERDEBUGFUNCTIONENTRY_MESSAGE % (tempFunctionName,tempDebugString),CONST_DEBUGLEVEL_FUNCTIONS)
  return

def ScraperDebugFunctionExit(tempFunctionName):

  # ARGV error checking
  if (tempFunctionName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONE
    return

  if not(isinstance(tempFunctionName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGFUNCTIONEXIT_MESSAGE % (tempFunctionName)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_FUNCTIONS)
  return

def ScraperDebugObjectCreation(tempObjectName):

  # ARGV error checking
  if (tempObjectName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONE
    return

  if not(isinstance(tempObjectName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGOBJECTCREATION_TEMPOBJECTNAME_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGOBJECTCREATION_MESSAGE % (tempObjectName)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_OBJECTCREATION)
  return

def ScraperDebugFunctionalMessage(tempFunctionalMessage):

  # ARGV error checking
  if (tempFunctionalMessage is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONE
    return

  if not(isinstance(tempFunctionalMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_TEMPFUNCTIONALMESSAGE_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGFUNCTIONALMESSAGE_MESSAGE % (tempFunctionalMessage)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_RESULTS)
  return

def ScraperDebugErrorMessage(tempErrorMessage):

  # ARGV error checking
  if (tempErrorMessage is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONE
    return

  if not(isinstance(tempErrorMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGERRORMESSAGE_TEMPERRORMESSAGE_NONSTRING
    return

  tempDebugString = CONST_OKSTRING_SCRAPERDEBUGERRORMESSAGE_MESSAGE % (tempErrorMessage)
  ScraperDebug(tempDebugString,CONST_DEBUGLEVEL_ERROR)
  return

class Scraper:
  # This class comprises the main object for the FCC phone scraper. This class will 
  # initialize itself upon instantiation and provides member functions for performing 
  # traditional actions.

  # this common variable will store a pointer to a mechanize.Browser instance

  def __init__(self):
    # This is the constructor for the Scraper class. This class shares a Browser instance for
    # each instance of the class but also contains separate variable data for instances of the
    # class reflecting pages or forms.

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_INIT_NAME,[])

    self.BrowserObject = CONST_EMPTYSTRING 

    self.FormObject = {}

    self.SetRobotsIgnore() # Scrapers, by their nature, seek automated retrieval of data

    self.CreateBrowserObject() # Create a browser object and store it for later use

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_INIT_NAME)

  def SetRobotsIgnore(self):
    # This method will set the flag that determines whether the robots.txt file is considered

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_NAME,[])

    self.IgnoreRobots = CONST_BOOLEAN_TRUE
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETROBOTSIGNORE_NAME)
    return

  def SetRobotsRespect(self):
    # This method will set the flag that determines whether the robots.txt file is considered

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_NAME,[])

    self.IgnoreRobots = CONST_BOOLEAN_FALSE
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETROBOTSRESPECT_NAME)
    return

  def GetRobotsIgnoreFlag(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME,[])

    # Do error checking to ensure that the robots flag had previously been set
    if (self.IgnoreRobots is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)
      return(CONST_BOOLEAN_ERROR)

    if not(isinstance(self.IgnoreRobots, int)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONINTEGER)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)
      return(CONST_BOOLEAN_ERROR)

    if ((self.IgnoreRobots != CONST_BOOLEAN_TRUE) and (self.IgnoreRobots != CONST_BOOLEAN_FALSE)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETROBOTSIGNOREFLAG_IGNOREROBOTS_NONBOOLEAN)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)
      return(CONST_BOOLEAN_ERROR)
      
    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETROBOTSIGNOREFLAG_NAME)

    return(self.IgnoreRobots)

  def DefineForm(self,tempFormName,tempURL):
    # This method creates a ScraperForm object that is referenced within the Scraper class by name FormName

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME,[tempFormName,tempURL])

    # ARGV error checking
    if (tempFormName is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if not(isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if not(isinstance(tempURL, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)      
      return(CONST_BOOLEAN_ERROR)

    tempBrowserObject = self.GetBrowserObject()

    tempFormObject = ScraperForm(self,tempURL)
    ScraperDebugObjectCreation(CONST_CLASSNAME_SCRAPERFORM)

    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_SCRAPERFORM_ALLOCATIONERROR)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    self.SetForm(tempFormName,tempFormObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
    return(CONST_BOOLEAN_TRUE)

  def GetForm(self,tempFormName):
    # This method retrieves a previously defined form identifed as tempFormName

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_GETFORM_NAME,[tempFormName])

    # ARGV error checking
    if (tempFormName is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)
      return(None)

    if not(isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)
      return(None)

    if not(self.FormObject.has_key(tempFormName)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONEXISTENT % (tempFormName))
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  
      return(None)

    tempFormObject = self.FormObject[tempFormName]
    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_VALUE_NONE % (tempFormName))
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  
      return(None)

    # AR: confirm that a FormObject was stored and retrieved

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_GETFORM_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  

    return(tempFormObject)

  def SetForm(self,tempFormName,tempFormObject):
    # This method stores a form object by name
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETFORM_NAME,[tempFormName,tempFormObject])

    # ARGV error checking
    if (tempFormName is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)
      return

    if not(isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)
      return

    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETFORM_TEMPFORMOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)
      return

    # AR: add an error checking routine to ensure that a FormObject was received
    #if (!isinstance(tempFormName, str)):
    #  ScraperDebugErrorMessage("ERROR: Scraper.SetForm() received ARG tempFormName as non-string")
    #  ScraperDebugFunctionExit("Scraper.SetForm")
    #  return

    self.FormObject[tempFormName] = tempFormObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETFORM_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETFORM_NAME)

  def GetBrowserObject(self):
    # This method merely returns a pointer to a BrowserObject - Form and Page classes call this function
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME,[])

    tempBrowserObject = self.BrowserObject
    if (tempBrowserObject is None):
      ScraperDebugErrorMessage("ERROR: Scraper.GetBrowserObject() read self.BrowserObject but found that it was None.")
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME,[])

    # AR: add check to ensure that self.BrowserObject is a Browser object

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETBROWSEROBJECT_NAME)

    return(self.BrowserObject)

  def SetBrowserObject(self,tempBrowserObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME,[tempBrowserObject])

    # ARGV error checking
    if (tempBrowserObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_SETBROWSEROBJECT_TEMPBROWSEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME)
      return

    # AR: add an error checking routine to ensure that a BrowserObject was received
    #if (!isinstance(tempBrowserObject, str)):
    #  ScraperDebugErrorMessage("ERROR: Scraper.SetBrowserObject() received ARG tempBrowserObject as non-string")
    #  ScraperDebugFunctionExit("Scraper.SetBrowserObject")
    #  return

    self.BrowserObject = tempBrowserObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_SETBROWSEROBJECT_NAME)

  def CreateBrowserObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_NAME,[])

    tempBrowserObject = mechanize.Browser()
    # AR: insert error checking code ensuring that a Browser object was returned

    ScraperDebugObjectCreation(CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_OBJECTCREATED)

    self.SetBrowserObject(tempBrowserObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_CREATEBROWSEROBJECT_NAME)

class ScraperForm:
  # This class comprises an object for storing data concerning a specific web form.

  def __init__(self,tempScraperObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_INIT_NAME,[tempScraperObject])

    # ARGV error checking
    if (tempScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.__init__() received ARG tempScraperObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.__init__")
    #  return

    self.SetURL(CONST_EMPTYSTRING)
    self.SetScraperObject(tempScraperObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)

  def __init__(self,tempScraperObject,tempURL):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_INIT_NAME,[tempScraperObject,tempURL])

    # ARGV error checking
    if (tempScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.__init__() received ARG tempScraperObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.__init__")
    #  return

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    if not(isinstance(tempURL, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_INIT_TEMPURL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)
      return

    self.SetURL(tempURL)
    self.SetScraperObject(tempScraperObject)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_INIT_NAME)

  def SetScraperObject(self,tempScraperObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME,[tempScraperObject])

    # ARGV error checking
    if (tempScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETSCRAPEROBJECT_TEMPSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetScraperObject() received ARG tempScraperObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.SetScraperObject")
    #  return

    self.ScraperObject = tempScraperObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETSCRAPEROBJECT_NAME)
    return

  def GetScraperObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME,[])

    # Do error checking to ensure that the scraper object had previously been set
    if (self.ScraperObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETSCRAPEROBJECT_SCRAPERFORMSCRAPEROBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME)
      return(None)

    # AR: add an error check to ensure that self.ScraperObject refers to a scraper object
    #if (!isinstance(self.ScraperObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetScraperObject() found that ScraperObject.ScraperObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit("ScraperForm.GetScraperObject")
    #  return(None)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETSCRAPEROBJECT_NAME)

    return(self.ScraperObject)

  def SetFormResponseObject(self,tempFormResponseObject):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME,[tempFormResponseObject])

    # ARGV error checking
    if (tempFormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMRESPONSEOBJECT_TEMPFORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME)
      return

    # AR: add an error checking routine to ensure that a tempScraperObject was received
    #if (!isinstance(tempFormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetFormResponseObject() received ARG tempFormResponseObject as non-string")
    #  ScraperDebugFunctionExit("ScraperForm.SetFormResponseObject")
    #  return

    self.FormResponseObject = tempFormResponseObject
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMRESPONSEOBJECT_NAME)

  def GetFormResponseObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME,[])

    # Do error checking to ensure that the form response object had previously been set
    if (self.FormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETFORMRESPONSEOBJECT_SCRAPERFORMFORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME)
      return(None)

    # AR: add an error check to ensure that self.ScraperObject refers to a scraper object
    #if (!isinstance(self.FormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetFormResponseObject() found that ScraperObject.FormResponseObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit("ScraperForm.GetFormResponseObject")
    #  return(None)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMRESPONSEOBJECT_NAME)

    return(self.FormResponseObject)

  def SetFormClass(self,tempFormClass):
    # This function receives a form class and selects that form within the current page
    # returned by the browser
    
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME,[tempFormClass])

    # ARGV error checking
    if (tempFormClass is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)
      return

    if not(isinstance(tempFormClass, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)
      return

    self.FormClass = tempFormClass
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_FUNCTIONALMESSAGE % tempFormClass)

    # Now select the form within the Browser object using the equivalent of this code: br.select_form(name=target_form)
    self.GetScraperObject().GetBrowserObject().select_form(name=tempFormClass)
    
    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)

  def GetFormClass(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME,[])

    # Do error checking to ensure that the form class had previously been set
    if (self.FormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETFORMCLASS_FORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)
      return(None)

    # AR: add an error check to ensure that self.FormResponseObject refers to a form object
    #if (!isinstance(self.FormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetFormClass() found that ScraperObject.FormResponseObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)
    #  return(None)


    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)

    return(self.FormClass)

  def SetURL(self,tempURL):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME,[tempURL])

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    if not(isinstance(tempURL,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETURL_TEMPURL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    self.URL = tempURL

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETURL_FUNCTIONALMESSAGE % tempURL)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    return

  def GetURL(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME,[])

    if (self.URL is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME)

    if not(isinstance(self.URL,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETURL_URL_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_GETURL_FUNCTIONALMESSAGE % self.URL)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME)

    return(self.URL)

  def SetFormObject(self, tempFormObject):
    # This member function simply stores the form object returned from the Internet

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME,[tempFormObject])

    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_TEMPFORMOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)
      return(None)

    # AR: test whether tempFormObject is a form object
    #if (!isinstance(tempFormObject,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetFormObject() received ARG tempFormObject as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    self.FormObject = tempFormObject

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME)

    return(tempFormObject)

  def GetFormObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME,[])

    if (self.FormObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FORMOBJCET_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    # AR: check whether self.FormObject is a form object
    #if (!isinstance(self.URL,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.getURL() was called with self.URL as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    return(self.FormObject)

  def SetFormObjectFiltered(self, tempFormObjectFiltered):
    # This member function stores the form object representing just the form itself rather than the full page

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME,[tempFormObjectFiltered])

    if (tempFormObjectFiltered is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_TEMPFORMOBJECTFILTERED_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME)

    # AR: test whether tempFormObjectFiltered is a form object
    #if (!isinstance(tempFormObject,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.SetFormObject() received ARG tempFormObject as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

    self.FormObjectFiltered = tempFormObjectFiltered

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME)
    return

  def GetFormObjectFiltered(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME,[])

    if (self.FormObjectFiltered is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FORMOBJECTFILTERED_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    # AR: check whether self.FormObjectFiltered is a form object
    #if (!isinstance(self.URL,str):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.getURL() was called with self.URL as non-string")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_FUNCTIONALMESSAGE)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME)

    return(self.FormObjectFiltered)

  def RetrieveForm(self):
    # This function reads a URL stored in this object and reads a form at that URL
    
    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME,[])

    tempBrowserObject = self.GetScraperObject().GetBrowserObject()
    tempURL = self.GetURL()
    #tempFormClass = self.GetFormClass()

    # Set Robots flag accordingly
    if self.GetScraperObject().GetRobotsIgnoreFlag == CONST_BOOLEAN_TRUE:
      tempRobotsFlag = True
    else:
      tempRobotsFlag = False

    self.GetScraperObject().GetBrowserObject().set_handle_robots(tempRobotsFlag)

    # Pull the form from the Internet
    tempFormObject = tempBrowserObject.open(tempURL)
    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_TEMPFORMOBJECT_NONE % tempURL)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME)
      return(None)

    self.SetFormObject(tempFormObject)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_FUNCTIONALMESSAGE % tempURL)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME)

    return

  def SetFieldValue(self,tempFieldName, tempFieldValue):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME,[tempFieldName,tempFieldValue])

    if (tempFieldName is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if not(isinstance(tempFieldName,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if (tempFieldValue is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if not(isinstance(tempFieldValue,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDVALUE_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if (self.GetScraperObject().GetBrowserObject()[tempFieldName] is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONE % tempFieldName)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    if not(isinstance(tempFieldName,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_TEMPFIELDNAMEFORM_NONSTRING % tempFieldName)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

    self.GetScraperObject().GetBrowserObject()[tempFieldName] = tempFieldValue

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_FUNCTIONALMESSAGE % (tempFieldName,tempFieldValue))

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

  def SubmitForm(self):
    # Submit the form and store the response

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME,[])

    # Submit the form and store result
    tempResponse = self.GetScraperObject().GetBrowserObject().submit()
    if (tempResponse is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_RESPONSE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
      return(None)
    
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMSUBMITTED)

    # Read the response in
    tempFormResponse = tempResponse.read()
    if (tempFormResponse is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
      return(None)
    
    # Parse response into form
    tempFormResponseObject = lxml.html.fromstring(tempFormResponse)
    if (tempFormResponseObject is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
      return(None)
    
    self.SetFormResponseObject(tempFormResponseObject)

    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_FUNCTIONALMESSAGE_FORMREADSTORED)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)

  def ParseCSS(self,tempTargetCSS,tempDataToParse):
    # This function receives a string with which to parse a received form and then extracts the portion
    # of the returned form with that CSS and returns a reference to that extracted result

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME,[tempTargetCSS])

    if (tempDataToParse is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPDATATOPARSE_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    # AR: add a checking routine to ensure that tempDataToParse is an object of the proper type
    #if (!isinstance(tempDataToParse,str):
    #  ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPDATATOPARSE_NONSTRING)
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    if (tempTargetCSS is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    if not(isinstance(tempTargetCSS,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_TEMPTARGETCSS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    tempParsedCSS = tempDataToParse.cssselect(tempTargetCSS)
    
    ScraperDebugFunctionalMessage("ScraperForm.ParseCSS found (%s)" % tempParsedCSS)

    if (not tempParsedCSS):
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMISS % tempTargetCSS)
      return(None)
      
    # Must not have been a MISS so is a MATCH
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSECSS_FUNCTIONALMESSAGEMATCH % tempTargetCSS)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSECSS_NAME)

    return(tempParsedCSS)
    
  def ParseFormCSS(self,tempTargetCSS):
    # This function receives a string with which to seek within a received form and then extracts the portion
    # of the returned form with that CSS and returns a reference to that extracted result

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME,[tempTargetCSS])

    if (tempTargetCSS is None):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME)

    if not(isinstance(tempTargetCSS,str)):
      ScraperDebugErrorMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_TEMPTARGETCSS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME)

    tempFormResponseObject = self.GetFormResponseObject()
    tempParsedCSS = self.ParseCSS(tempTargetCSS,tempFormResponseObject) # returns an array of HTML elements
    
    if (tempParsedCSS is None): # if array is empty must not have found it (so abort)
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMISS % tempTargetCSS)
      return(None)
      
    # Must not have been a MISS so is a MATCH
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_FUNCTIONALMESSAGEMATCH % tempTargetCSS)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMCSS_NAME)

    return(tempParsedCSS)

  def GetFormNameList(self):
    # This function creates a list of form names returned from a URL

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_NAME,[])

    tempFormString = CONST_EMPTYSTRING
    for tempForm in self.GetScraperObject().GetBrowserObject().forms():
      tempFormString = tempFormString + CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_STRING % tempForm.name

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMNAMELIST_NAME)

    return(tempFormString)

  def ParseFormResponse(self):
    # This member function will get overloaded by an implementing subclass

    # This function must consider three scenarios:
    # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
    # 2. one page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">
    # 3. multiple pages of data was returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_NAME,[])

    # Handle scenario 1 first - check received form for CSS ID that reflects "no match"
    tempParsedFormCSS = self.ParseFormCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO1)
    if (tempParsedFormCSS):
      # Found the CSS class that reflects "no match"
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO1)
      return
      
    # Must be either the 2nd or 3rd scenario.
    # Evaluating the 2nd scenario

    tempRows = self.ParseFormCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_RESULTTABLE)

    # Generate a string comprising only the rows
    tempRowsString = CONST_EMPTYSTRING
    for tempCurrentRow in tempRows:
      tempRowsString = tempRowsString + lxml.html.tostring(tempCurrentRow)

    # Now extract the rows containing useful data, which have class 'resultTableData'
    tempRowsOnlyString = lxml.html.fromstring(tempRowsString)
    tempRowsUsefulOdd = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_ODDROW,tempRowsOnlyString)
    tempRowsUsefulEven = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_EVENROW,tempRowsOnlyString)

    # Combine even and odd rows into a single array of rows that can be processed
    tempRowsUsefulCombined = []
    for tempCurrentRow in tempRowsUsefulOdd:
      tempRowsUsefulCombined.append(tempCurrentRow)
    for tempCurrentRow in tempRowsUsefulEven:
      tempRowsUsefulCombined.append(tempCurrentRow)

    #print "The length of tempRowsUsefulCombined is %i" % len(tempRowsUsefulCombined)

    # Now parse the combined rows and store them
    for tempCurrentRow in tempRowsUsefulCombined:
      tempColumns = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_COLUMNS,tempCurrentRow)
      #print "The number of columns found is %i" % len(tempColumns)

      tempFRN = self.ParseCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_TEMPFRN,tempCurrentRow)[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_FRN]
      #tempColumns = tempCurrentRow.cssselect(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_COLUMNS)
      #tempFRN = tempCurrentRow.cssselect(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_TEMPFRN)[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_FRN]
      #print "Found tempFRN of %s" % tempFRN

    # the FRN will be the unique ID for each record
      scraperwiki.sqlite.save(unique_keys=[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_UNIQUEKEYS], 
        data={CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_FRN:tempFRN.text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGISTRANT:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGISTRANT].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CONTACT:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CONTACT].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ADDRESS:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ADDRESS].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_CITY:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_CITY].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_STATE:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_STATE].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_ZIP:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_ZIP].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_COUNTRY:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_COUNTRY].text, 
            CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELD_REGDATE:tempColumns[CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_FIELDCOLUMN_REGDATE].text})

    # Now determine whether the current page is not the last page. If a next page exists, the following HTML will be present: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt="Next Page">

    tempNextPageIcon = self.ParseFormCSS(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_TARGETCSS_SCENARIO2_NEXTPAGE)

    if (tempNextPageIcon):
      # Not null so must have found the next page icon
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGEFOUND)
    else:
      ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO2_NEXTPAGENOTFOUND)
      return # return because no 'next page' to process - we are done with the second scenario

    # must be third scenario - extract the next page link and parse its data
    # In this scenario, we want to mimic clicking on this link: <a href='/coresWeb/advancedSearch.do?next=true'>

    #tempNextPageResponse = br.open(tempNextPageTarget) # The response object
    #response_page_next = response_next_page.read()
    #response_next_page_object = lxml.html.fromstring(response_page_next)

    # Generate a form object by retrieving the next form page from the Internet
    #self.SetURL(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO3_TARGETURL)
    #tempFormObject = self.RetrieveForm()
    
    self.SetFormResponseObject(lxml.html.fromstring(self.GetScraperObject().GetBrowserObject().open(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_FUNCTIONALMESSAGESCENARIO3_TARGETURL).read()))

    # now parse it
    #parseResponseObject(response_next_page_object)
    self.ParseFormResponse()

    #print "Current table processing completed."

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_PARSEFORMRESPONSE_NAME)
    return


# ------------------------------------------------------------------------------------------------------

ScraperDebugFunctionEntry(CONST_FUNCTION_MAIN,[])

DebugLevel = 1 # turn results and errors on (only)

# This is the webform that the FCC presents to users for querying the manufacturer database
tempTarget = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?btnSearch=true"

# This string is used for iterating on search characters
alphabet = "bcdefghijklmnopqrstuvwxyz"

# Create a form object with the name and target specified
# Processing proceeds as follows: 
# 1. Retrieve one or more forms at the URL provided (and store those forms)
# 2. Within the retrieved URL, select the form we want
# 3. Modify the selected form to reflect data settings for that form
# 4. Submit the modified form
# 5. Interpret the result received after submitting the modified form
# 6. Act on the interpreted result, which may lead to recursive processing


for tempFirstLetter in alphabet:
  ScraperDebugFunctionalMessage("Processing first letter (%s)" % tempFirstLetter )
  for tempSecondLetter in alphabet:
    ScraperDebugFunctionalMessage("Processing second letter (%s)" % tempSecondLetter )
    
    tempScraper = Scraper() # Create a Scraper object

    if (tempScraper is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_MAIN_FAILEDTOALLOCATESCRAPER)
      ScraperDebugFunctionExit(CONST_FUNCTION_MAIN,[])

    ScraperDebugFunctionalMessage("A Scraper object has been created.")
    # AR: check that Scraper is of a Scraper() class

    # Set a name to refer to the form
    tempTargetFormName = "FCC third-party identifier form"

    tempScraper.DefineForm(tempTargetFormName,tempTarget)

    tempScraperForm = tempScraper.GetForm(tempTargetFormName)

    ScraperDebugFunctionalMessage("A ScraperForm object has been defined with the name (%s)" % tempTargetFormName)


    # Get the form from the Internet and store results internal to ScraperForm
    tempScraperForm.RetrieveForm()

    # The following line was used during debug to identify the name of the form we wish to utilize (advancedSearchForm)
    #print "These are the forms that were retrieved from the Internet:",[ form.name  for form in Scraper.GetBrowserObject().forms() ]
    tempFormString = tempScraperForm.GetFormNameList()
    ScraperDebugFunctionalMessage("Found the following forms: %s" % tempFormString)

    # This is the form to focus on within the page returned
    tempTargetForm = 'advancedSearchForm'

    # store the form class sought and then select the form with that class from within the URL retrieved
    tempScraperForm.SetFormClass(tempTargetForm)

    # This is the field within the selected form that we wish to set prior to POSTing the form
    tempTargetFormField = 'bizName'

    # Set the form field to the business name we wish to search for
    #br[tempTargetFormField] = 'samsung*'
    #tempCurrentSearchString = current_first_letter + current_second_letter + "*"
    #tempCurrentSearchString = "samsung*"
    tempCurrentSearchString = tempFirstLetter + tempSecondLetter + "*"
    ScraperDebugFunctionalMessage("Current business name search string is: %s" % tempCurrentSearchString)

    #br[tempTargetFormField] = tempCurrentSearchString
    # Identify form field to be modified and value of modified field
    tempScraperForm.SetFieldValue(tempTargetFormField,tempCurrentSearchString)

    # Submit the form, store the response to the submitted form in an object named "response", convert the response to a text page, and then convert the text page to an object
    #response = br.submit()
    #response_page = response.read()
    #response_object = lxml.html.fromstring(response_page)
    #parseResponseObject(response_object)
    
    # Submit the form so we can parse the results
    tempScraperForm.SubmitForm()
    
    # Parse the results
    tempScraperForm.ParseFormResponse()

    ScraperDebugFunctionalMessage("Processing complete for second letter (%s)" % tempSecondLetter )

    #print "second letter %s has been processed" % (current_second_letter)

    ScraperDebugFunctionalMessage("Processing complete for first letter (%s)" % tempFirstLetter )
    #print "first letter %s has been processed" % (current_first_letter)

    #ScraperForm = Scraper.GetForm(tempTargetFormName) # refetch the input form so we can provide another search string

ScraperDebugFunctionalMessage("All processing complete.")

ScraperDebugFunctionExit(CONST_FUNCTION_MAIN)

# ------------------------------------------------------------------------------------------------------

