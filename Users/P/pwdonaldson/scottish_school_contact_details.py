import scraperwiki
import lxml.html
import urllib

FUNDINGTYPE = ['State Funded',
                'Independent']

SCHOOLTYPE =  [('issecondaryschool', 'Secondary School'),('isprimaryschool','Primary School'),('isspecial','Special School')]          

def ParseContactSummaryPage(allContactPages):
    #Code to parse one page worth of results
    #Modified to pick up from where it left off as we don't have enough time to parse all seven pages in one run
    startPage = int(scraperwiki.sqlite.get_var('page', 0))
    listSchData = []
    print "Starting at page " + str(startPage)
    pagesStillToParse = allContactPages[startPage:]
    for contactPage in pagesStillToParse:
    #For each schools contact card
        for schoolDetails in contactPage.cssselect("div.vcard"):
        #For each schools set of location details   
            for locationDetails in schoolDetails.cssselect("div.vcardcol1"):
            #Get and store the schools name
                schName = locationDetails[0].text_content()
                #For each part of the schools address
                for addressDetails in locationDetails.cssselect("div.adr"):
                    schStreet = addressDetails[0].text_content()
                    #School place is set to the locality if the extended address is blank
                    if (addressDetails[1].text is None):
                        schPlace = addressDetails[2].text_content()
                    else:
                        schPlace = addressDetails[1].text_content()
                        
                    schRegion = addressDetails[3].text_content()
                    schPostcode = addressDetails[4].text_content()
                    schCountry = addressDetails[5].text_content()
                        
                    for coordinates in addressDetails.cssselect("div.geo"):
                        schLatitude = coordinates[0].text_content()
                        schLongitude = coordinates[1].text_content()

            #For each schools set of contact details
            #for contactDetails in schoolDetails.cssselect("div.vcardcol2"):
                #Get and store the schools main telephone and fax numbers
               # print "contact details"
            
                #if (contactDetails.cssselect("a.email") != []):
                   #Get and store the school's email address
                   #print "email link found"
                  # for schoolEmail in contactDetails.cssselect("a.email"):
                      # schEmail = schoolEmail[0].text_content()
               # else:
                #   schEmail = 'null'

                 #if (contactDetails.cssselect("a.url") != []):
                  # print "web address found"
                  # #Get and store the school's website address from the href attribute of the anchor
                  #  for webAddress in contactDetails.cssselect("a.url"):
                   #     schWebsite = webAddress.attrib['href']
                 #else:
                    #schEmail = 'null'

               #Create a dictionary with the collected information for each school
        schData = {
                    'authority_area' : schRegion,
                    #'school_type' : schType,
                    #'funding' : fundingType,
                    'school_name' : schName,
                    'school_street' : schStreet,
                    'school_place' : schPlace,
                    'school_postcode' : schPostcode,
                    'school_country' : schCountry,
                    'school_latitude' : float(schLatitude),
                    'school_longitude' : float(schLongitude)#,
                   # 'school_email' : schEmail,
                #'school_website' : schWebsite
        }
        listSchData.append(schData)
    
    scraperwiki.sqlite.save(['school_name'], data=listSchData)
    #increment the number of completely parsed pages and then save it to the data store
    startPage += 1
    scraperwiki.sqlite.save_var('page', startPage)

def DetermineNumberOfPages(contactPage):
    
    #Count the number of list items in the page navigation section
    listItems = 0

    for navItems in contactPage.cssselect("div.pagenav li"):
        listItems += 1
        #Number of results pages is number of items in page navigation - the previous and next page items
    pages = listItems - 2
        
    #Return the number of search result pages    
    return pages


#Main program starts here

domain='http://www.ltscotland.org.uk/scottishschoolsonline/othersearches.asp?'

resultSet = 0
#create an empty list to store all of the contact pages for a particular search query
allContactPages = []

#Fetch all of the search results pages first for efficiency
for currentFunding in FUNDINGTYPE:
    print currentFunding
    for currentSchoolType in SCHOOLTYPE:
        print currentSchoolType
        urlQueryString=urllib.urlencode({'iPage':'1',
                                         'strSubmit':'True',
                                         'strSearchText':'',
                                         'bSubmit':'1',
                                         'cLetter':'',
                                         'authority':'',
                                         'strTypes': currentSchoolType[0],
                                         'strAdditionalServices':'',
                                         'strFundingType': currentFunding,
                                         'schoolsearchstring':'',
                                         'addresssearchstring':''})
        urlSearchString = domain + urlQueryString
        currentHTML = scraperwiki.scrape(urlSearchString)
        firstSearchResultsPage = lxml.html.fromstring(currentHTML)
        #Determine the number of pages for this set of schools
        totalPages = DetermineNumberOfPages(firstSearchResultsPage)
        print totalPages
        print "Result set " + str(resultSet)

        for currentResultsPage in range(1,totalPages+1):
            print "Contact page " + str(currentResultsPage)
            urlQueryString=urllib.urlencode({'iPage':str(currentResultsPage),
                                             'strSubmit':'True',
                                             'strSearchText':'',
                                             'bSubmit':'1',
                                             'cLetter':'',
                                             'authority': '',
                                             'strTypes': currentSchoolType[0],
                                             'strAdditionalServices':'',
                                             'strFundingType': currentFunding,
                                             'schoolsearchstring':'',
                                             'addresssearchstring':''})
            urlCurrentResults = domain + urlQueryString
            currentHTML = scraperwiki.scrape(urlCurrentResults)
            currentContactPage = lxml.html.fromstring(currentHTML)
            allContactPages.append(currentContactPage)

        resultSet += 1

ParseContactSummaryPage(allContactPages)

