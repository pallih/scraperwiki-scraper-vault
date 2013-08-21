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
CONST_DEBUGLEVEL_MINIMUM = CONST_MESSAGES_ERROR
CONST_DEBUGLEVEL_MAXIMUM = CONST_MESSAGES_FUNCTIONS

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

CONST_FUNCTION_SCRAPERFORM_GETURL_NAME = "ScraperForm.GetURL"

CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME = "ScraperForm.SetFormObject"

CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME = "ScraperForm.GetFormObject"

CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME = "ScraperForm.SetFormObjectFiltered"

CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME = "ScraperForm.GetFormObjectFiltered"

CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME = "ScraperForm.RetrieveForm"

CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME = "ScraperForm.SetFieldValue"

CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME = "ScraperForm.SubmitForm"

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

  if (!isinstance(tempDebugMessage, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGMESSAGE_NONSTRING
    return

  if (tempDebugLevel is None):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONE
    return

  if (!isinstance(tempDebugLevel, int)):
    print CONST_ERRORSTRING_SCRAPERDEBUG_TEMPDEBUGLEVEL_NONINTEGER
    return

  if ((tempDebugLevel > CONST_DEBUGLEVEL_MAXIMUM) or (tempDebugLevel < CONST_DEBUGLEVEL_MINIMUM)):
    print CONST_ERRORSTRING_DEBUGLEVEL_OUTOFRANGE % (tempDebugLevel, CONST_DEBUGLEVEL_MINIMUM, CONST_DEBUGLEVEL_MAXIMUM)
    return

  # ARGVs were apparently OK - proceed with debug message
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

  if (!isinstance(tempFunctionName, str)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPDEBUGMESSAGE_NONSTRING
    return

  if (tempMessageArray is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONE
    return

  if (!isinstance(tempMessageArray, arr)):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_TEMPMESSAGEARRAY_NONARRAY
    return

  for tempCurrentArrayElement in tempMessageArray:
    if (!tempFirstElementFlag):
      # Add a comma to the working string before adding the next ARGV component
      tempDebugString = tempDebugString + CONST_COMMA

    if (isinstance(tempCurrentArrayElement,str):
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_STRING % tempCurrentArrayElement
    elif (isinstance(tempCurrentArrayElement,int):
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_INTEGER % tempCurrentArrayElement
    else
      tempArgvString = CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONENTRY_ARGVSTRING_UNKNOWN

    tempDebugString = tempDebugString + tempArgvString
    tempFirstElementFlag = CONST_BOOLEAN_FALSE # Commas should be added before each subsequent ARGV string

  ScraperDebug(CONST_OKSTRING_SCRAPERDEBUGFUNCTIONENTRY_MESSAGE % (tempFunctionName,currentArgvString),CONST_DEBUGLEVEL_FUNCTIONS)
  return

def ScraperDebugFunctionExit(tempFunctionName):

  # ARGV error checking
  if (tempFunctionName is None):
    print CONST_ERRORSTRING_SCRAPERDEBUGFUNCTIONEXIT_TEMPFUNCTIONNAME_NONE
    return

  if (!isinstance(tempFunctionName, str)):
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

  if (!isinstance(tempObjectName, str)):
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

  if (!isinstance(tempFunctionalMessage, str)):
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

  if (!isinstance(tempErrorMessage, str)):
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
  self.BrowserObject = CONST_EMPTYSTRING 

  self.FormObjects = {}
  self.PageObjects = {}

  def __init__(self):
    # This is the constructor for the Scraper class. This class shares a Browser instance for
    # each instance of the class but also contains separate variable data for instances of the
    # class reflecting pages or forms.

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPER_INIT_NAME,[])

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

    if (!isinstance(self.IgnoreRobots, int)):
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

    if (!isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if (tempURL is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_DEFINEFORM_TEMPURL_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_DEFINEFORM_NAME)
      return(CONST_BOOLEAN_ERROR)

    if (!isinstance(tempURL, str)):
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

    if (!isinstance(tempFormName, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)
      return(None)

    if (!self.FormObject.has_key(tempFormName)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_NONEXISTENT % (tempFormName)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPER_GETFORM_NAME)  
      return(None)

    tempFormObject = self.FormObject[tempFormName]
    if (tempFormObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPER_GETFORM_TEMPFORMNAME_VALUE_NONE % (tempFormName)
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

    if (!isinstance(tempFormName, str)):
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

Class ScraperForm:
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

    if (!isinstance(tempURL, str)):
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

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME,[tempFormClass])

    # ARGV error checking
    if (tempFormClass is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)
      return

    if (!isinstance(tempFormClass, str)):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_SETFORMCLASS_TEMPFORMCLASS_NONSTRING)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)
      return

    self.FormClass = tempFormClass
    ScraperDebugFunctionalMessage(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_FUNCTIONALMESSAGE % tempFormClass)

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMCLASS_NAME)

  def GetFormClass(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME,[])

    # Do error checking to ensure that the form class had previously been set
    if (self.FormResponseObject is None):
      ScraperDebugErrorMessage(CONST_ERRORSTRING_SCRAPERFORM_GETFORMCLASS_FORMRESPONSEOBJECT_NONE)
      ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)
      return(None)

    # AR: add an error check to ensure that self.ScraperObject refers to a scraper object
    #if (!isinstance(self.FormResponseObject, str)):
    #  ScraperDebugErrorMessage("ERROR: ScraperForm.GetFormClass() found that ScraperObject.FormResponseObject did not refer to an instance of ScraperObject")
    #  ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)
    #  return(None)


    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMCLASS_NAME)

    return(self.FormClass)

  def SetURL(self,tempURL):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME,[tempURL])

    self.URL = tempURL

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETURL_NAME)

  def GetURL(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME,[])

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETURL_NAME)

    return(self.URL)

  def SetFormObject(self, tempFormObject):
    # This member function simply stores the form object returned from the Internet

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME,[tempFormObject])

    self.FormObject = tempFormObject

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECT_NAME)

  def GetFormObject(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME,[])

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECT_NAME)

    return(self.FormObject)

  def SetFormObjectFiltered(self, tempFormObjectFiltered):
    # This member function stores the form object representing just the form itself rather than the full page

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME,[tempFormObjectFiltered])

    self.FormObjectFiltered = tempFormObjectFiltered

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFORMOBJECTFILTERED_NAME)

  def GetFormObjectFiltered(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME,[])

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_GETFORMOBJECTFILTERED_NAME)

    return(self.FormObjectFiltered)

  def RetrieveForm(self):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME,[])

    tempBrowserObject = self.GetScraperObject().GetBrowserObject()
    tempURL = self.GetURL()
    tempFormClass = self.GetFormClass()

    # Pull the form from the Internet
    SetFormObject(self.tempBrowserObject.open(tempURL))

    # Extract the identified form class from the returned page
    self.SetFormObjectFiltered(tempBrowserObject.select_form(name=tempFormClass))

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_RETRIEVEFORM_NAME)

  def SetFieldValue(self,tempFieldName, tempFieldValue):

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME,[tempFieldName,tempFieldValue])

    self.GetScraperObject().GetBrowserObject()[tempFieldName] = tempFieldValue

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SETFIELDVALUE_NAME)

  def SubmitForm(self):
    # Submit the form and store the response

    ScraperDebugFunctionEntry(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME,[])

    self.SetFormResponseObject(lxml.html.fromstring(self.GetScraperObject().GetBrowserObject().submit().read()))

    ScraperDebugFunctionExit(CONST_FUNCTION_SCRAPERFORM_SUBMITFORM_NAME)
    
  def ParseFormResponse(self):
    # This member function will get overloaded by an implementing subclass

    # This function must consider three scenarios:
    # 1. no data was returned. This condition is reflected by the presence of this HTML: <div id="noMatch">
    # 2. one page of data was returned. This condition is reflected by the lack of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">
    # 3. multiple pages of data was returned. This condition is reflected by the presence of this HTML: <img name="nextPgIcon" src="images/icons/nextArrow-blue.gif" alt-"Next Page">

    ScraperDebugFunctionEntry("ScraperForm.ParseFormResponse",[])

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

    ScraperDebugFunctionExit("ScraperForm.ParseFormResponse")
    return

Class ScraperPage:
  # This class comprises an object for storing data concerning a specific web page.
  
  def __init__(self):

    ScraperDebugFunctionEntry("ScraperPage.__init__",[])

    self.URL = ""

    ScraperDebugFunctionExit("ScraperPage.__init__")

  def __init__(self,tempURL):

    ScraperDebugFunctionEntry("ScraperPage.__init__",[tempURL])

    self.URL = tempURL

    ScraperDebugFunctionExit("ScraperPage.__init__")

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

ScraperDebugFunctionEntry(CONST_FUNCTION_MAIN,[])

# This is the webform that the FCC presents to users for querying the manufacturer database
target = "https://fjallfoss.fcc.gov/coresWeb/advancedSearch.do?btnSearch=true"

# This string is used for iterating on search characters
alphabet = "abcdefghijklmnopqrstuvwxyz"

# Pull the initial webform from the FCC server
##br = mechanize.Browser()
##br.set_handle_robots(False) # This disables voluntary consideration of the robots.txt file

Scraper = Scraper() # Create a Scraper object
# PRINT THAT THIS CLASS HAS BEEN INSTANTIATED: CONST_CLASSNAME_SCRAPER
if (Scraper is None):
  ScraperDebugErrorMessage(CONST_ERRORSTRING_MAIN_FAILEDTOALLOCATESCRAPER)
  ScraperDebugFunctionExit(CONST_FUNCTION_MAIN,[])

# AR: check that Scraper is of a Scraper() class

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

ScraperDebugFunctionExit(CONST_FUNCTION_MAIN,[])

# ------------------------------------------------------------------------------------------------------

