import scraperwiki
import lxml.etree
import urllib
import urllib2
import re
import sys
from time import gmtime, strftime

utf8_parser = lxml.etree.XMLParser(encoding='utf-8')

# this scraper is meant to supercede the one that queries DBpedia (https://scraperwiki.com/scrapers/wikipedia_power_plants).
# different language links will be checked, coordinates will be extracted

# Category tree will be traversed starting at "http://en.wikipedia.org/wiki/Category:Power_stations_by_country"

try:
    # code below may not need to be run, it at least shows the schemas that will (likely) be employed
    # Table 1 - different language links, also include namespace
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS languageLinks (NameSpace TEXT, LastChecked DATETIME)")
    
    # Table 2 - page and coordinates - language, namespace, title, lat, lon
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS pageCoordinates (NameSpace TEXT, Language TEXT, Title TEXT, Latitude NUMBER, Longitude NUMBER, LastChecked DATETIME)")
    
    # Table 3 - subcategories and pages in categories - language, category, namespace, title
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS categoryStructure (Language TEXT, FromTitle TEXT, NameSpaceToTitle TEXT, ToTitle TEXT, LastChecked DATETIME)")
    
    # Table 4 - coordinates from lists - language, namespace, title, lat, lon, listTitle
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS listCoordinates (NameSpace TEXT, Language TEXT, Title TEXT, Latitude NUMBER, Longitude NUMBER, ListTitle TEXT, Section TEXT, LastChecked DATETIME)")
    
    scraperwiki.sqlite.commit()
except:
    print "Error creating tables: " + str(sys.exc_info()[1])


# need several functions:
# 1) recursive category traversal
# 2) get subcategories for category
# 3) get pages for category
# 4) get language links for a page
# 5) get coordinates for a page
# 6) get coordinates for a list

def createAPICallURL(language, params):
    # unquote url before quoting - have run into an issue where escaped characters were re-escaped - Category%3AHydroelectric_power_stations_in_Paran%25C3%25A1_%28state%29
    qs = ""
    try:
        qs = "&".join("%s=%s" % (k, urllib.quote(urllib.unquote(v)))  for k, v in params.items())
    except:
        print "Error encoding url: " + str(sys.exc_info()[1])
    url = "http://" + language + ".wikipedia.org/w/api.php?%s" %qs
    return url
    

# language links for a page are stored in the languageLinks table
def getLanguageLinks(language, title):
    params = { "format":"xml", "action":"query", "prop":"langlinks", "lllimit":"500", "titles":title }
    url = createAPICallURL(language, params)

    allLanguageLinks = []

    print "language url: " + url
    try:
        #tree = lxml.etree.parse(urllib.urlopen(url))
        page = urllib2.urlopen(url)
        pagecontents = page.read()
    except:
        print "Error opening url " + url + ": " + str(sys.exc_info()[1])
        return
    tree = lxml.etree.fromstring(pagecontents, utf8_parser)
    
    pages = tree.xpath('//page')
    for page in pages:
    
        languageInfo = dict()
        languageInfo["NameSpace"] = page.xpath("./@ns")[0]
        languageInfo["PageTitle"] = page.xpath("./@title")[0]
        languageInfo["PageID"] = page.xpath("./@pageid")[0]
        languageInfo[language] = languageInfo["PageTitle"] # include value for the language version we already know about - the API call only finds the other ones

        languageLinks = page.xpath("./langlinks/ll")
        for languageLink in languageLinks:
            languageTag = languageLink.xpath("@lang")[0]
            # title = urllib.quote(languageLink.text.encode('utf-8'))
            title = languageLink.text
            languageInfo[str(languageTag)] = title
    
        # TODO check that the handling of wikipedia and scraperwiki python time is done correctly
        # "2013-02-26T01:49:36Z"  wikipedia
        # '2009-01-05 22:14:39' python
    
        languageInfo["LastChecked"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        #print languageInfo
    
        # Having a primary key of pageID is a bit awkward.  The links between languages should be bidirectional
        # and the setup below may lead to multiple entries if api calls are done for the same page in different languages
        # This code is also intended to handle interlanguage links for pages that may not have a version in English
        scraperwiki.sqlite.save(unique_keys=["PageID"], data=languageInfo, table_name="languageLinks")

        # clean up the dictionary, about to append it to a list containing information about the language links for all the entries
        del languageInfo["NameSpace"]
        del languageInfo["PageTitle"]
        del languageInfo["PageID"]
        del languageInfo["LastChecked"]
        allLanguageLinks.append(languageInfo)
    return allLanguageLinks

def getSubCategories(language, title):
    subCategoryList = []
    params = { "action":"query", "format":"xml", "list":"categorymembers", "cmtype":"subcat", "cmlimit":"500", "cmtitle": title }
    url = createAPICallURL(language, params)
    try:
        #tree = lxml.etree.parse(urllib.urlopen(url))
        page = urllib2.urlopen(url)
        pagecontents = page.read()
    except:
        print "Error opening url " + url + ": " + str(sys.exc_info()[1])
        return
    tree = lxml.etree.fromstring(pagecontents, utf8_parser)

    subcategories = tree.xpath('//cm')
    for subcategory in subcategories:
        subCategoryTitle = subcategory.xpath("./@title")[0]
        nameSpace = subcategory.xpath("./@ns")[0]
        subCategoryList.append(subCategoryTitle)

        catStructureInfo = dict()
        catStructureInfo["Language"] = language
        catStructureInfo["FromTitle"] = title
        catStructureInfo["NameSpaceToTitle"] = nameSpace
        catStructureInfo["ToTitle"] = subCategoryTitle
        catStructureInfo["LastChecked"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        scraperwiki.sqlite.save(unique_keys=["Language", "FromTitle", "NameSpaceToTitle", "ToTitle"], data=catStructureInfo, table_name="categoryStructure")

    return subCategoryList

def getPagesInCategory(language, title):
    # pages in category
    pagesList = []
    params = { "action":"query", "format":"xml", "list":"categorymembers", "cmtype":"page", "cmlimit":"500", "cmtitle": title }
    url = createAPICallURL(language, params)
    print url

    try:
        #tree = lxml.etree.parse(urllib.urlopen(url))
        page = urllib2.urlopen(url)
        pagecontents = page.read()
    except:
        print "Error opening url " + url + ": " + str(sys.exc_info()[1])
        return
    tree = lxml.etree.fromstring(pagecontents, utf8_parser)

    pages = tree.xpath("//categorymembers/cm")
    for page in pages:
        nameSpace = page.xpath("./@ns")[0]
        toTitle = page.xpath("./@title")[0]
        pagesList.append(toTitle)
        catStructureInfo = dict()
        catStructureInfo["Language"] = language
        catStructureInfo["FromTitle"] = title
        catStructureInfo["NameSpaceToTitle"] = nameSpace
        catStructureInfo["ToTitle"] = toTitle
        catStructureInfo["LastChecked"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        scraperwiki.sqlite.save(unique_keys=["Language", "FromTitle", "NameSpaceToTitle", "ToTitle"], data=catStructureInfo, table_name="categoryStructure")
    return pagesList

# could be multiple titles separated by "|"
def getPageCoordinates(language, title):
    # get coordinates
    # http://en.wikipedia.org/w/api.php?action=query&format=xml&prop=coordinates&titles=Genesee_Generating_Station
    params = { "action":"query", "format":"xml", "prop":"coordinates", "coprop":"country", "colimit":"500", "titles": title }
    url = createAPICallURL(language, params)
    print "coordinates url: " + url

    try:
        #tree = lxml.etree.parse(urllib.urlopen(url))
        page = urllib2.urlopen(url)
        pagecontents = page.read()
    except:
        print "Error opening url " + url + ": " + str(sys.exc_info()[1])
        return
    tree = lxml.etree.fromstring(pagecontents, utf8_parser)

    pages = tree.xpath("//page")
    for page in pages:
        coordinatesInfo = dict()
        coordinatesInfo["Title"] = page.xpath("./@title")[0]
        lat = page.xpath("./coordinates/co/@lat")
        lon = page.xpath("./coordinates/co/@lon")
        if len(lat) > 0 and len(lon) > 0 :
            print "...getting coords for " + coordinatesInfo["Title"]
            coordinatesInfo["NameSpace"] = page.xpath("./@ns")[0]
            coordinatesInfo["Language"] = language
            coordinatesInfo["Latitude"] = lat[0]
            coordinatesInfo["Longitude"] = lon[0]
            coordinatesInfo["LastChecked"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            scraperwiki.sqlite.save(unique_keys=["Title", "NameSpace", "Language"], data=coordinatesInfo, table_name="pageCoordinates")
        else:
            print "...no coords for " + coordinatesInfo["Title"]
    # TODO return something?

def getListCoordinates(language, title):
    # get KML export with coordinates
    # http://toolserver.org/~para/cgi-bin/kmlexport?article=List_of_power_stations_in_England
    try:
        url = "http://toolserver.org/~para/cgi-bin/kmlexport?article=" + urllib.quote(urllib.unquote(title).encode('utf8'))
    except:
        print "Error encoding url for " + title + ": " + str(sys.exc_info()[1])
        return
    if language != "en":
        url = url + "&project=" + language
    print "getting coords from " + title

    #tree = lxml.etree.parse(urllib.urlopen(url))
    page = urllib2.urlopen(url)
    pagecontents = page.read()
    tree = lxml.etree.fromstring(pagecontents, utf8_parser)

    pages = tree.xpath("//kml:Placemark", namespaces={"kml": "http://earth.google.com/kml/2.1"})
    print "%d plants found" % len(pages)
    for page in pages:
        coordinatesInfo = dict()
        coordinatesInfo["Title"] = page.xpath("./kml:name/text()", namespaces={"kml": "http://earth.google.com/kml/2.1"})[0]
        coordinatesInfo["ListTitle"] = title
        section = page.xpath("./parent::kml:Folder/kml:name/text()", namespaces={"kml": "http://earth.google.com/kml/2.1"})
        if len(section) > 0:
            coordinatesInfo["Section"] =  section[0]
        coords = page.xpath("string(./kml:Point/kml:coordinates)", namespaces={"kml": "http://earth.google.com/kml/2.1"}).split(",")
        if len(coords) >= 2:
            coordinatesInfo["Language"] = language
            coordinatesInfo["Latitude"] = coords[1]
            coordinatesInfo["Longitude"] = coords[0]
            coordinatesInfo["LastChecked"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            scraperwiki.sqlite.save(unique_keys=["Title", "ListTitle"], data=coordinatesInfo, table_name="listCoordinates")
    # TODO return something?

def filterRelevantSubCategories(subCategories):
    # "power station", "power plant", "CHP plants", "Wave farms", "Wind farms"  
    relevantSubCategories = []
    pattern = "power station|power plant|CHP plants|Wave farms|Wind farms"
    for subCategory in subCategories:
        if re.search(pattern, subCategory, re.IGNORECASE):
            relevantSubCategories.append(subCategory)
    return relevantSubCategories
    
def processPagesFromCategory(language, title, pagesWithCoordinates):
    pagesInCategory = getPagesInCategory(language, title)
    print "pagesInCategory"
    print pagesInCategory

    # TODO this doesn't work since the language is not appended to pagesInCategory
    pagesToFindCoordinatesFor = list(set(pagesInCategory) - set(pagesWithCoordinates))

    for page in pagesToFindCoordinatesFor:
         if page.find("List") == 0:
             getListCoordinates(language, page)

    # api only allows for 50 titles, chunk the list
    for i in range(0, len(pagesToFindCoordinatesFor), 50):
        getPageCoordinates(language.encode("utf-8"), "|".join(pagesToFindCoordinatesFor[i:i+50]).encode("utf-8"))
    return pagesInCategory

# For now only doing this for english categories, not sure how to deal with foreign language categories yet
# The main issue is how to know in a foreign language if we're diverting into non-relevant categories
# The main idea is that for each english categories, the corresponding foregin categories are found, pages are searched for in all of these
# and coordinates + foreign language links are found for all of them.  English provides the backbone and we then branch out from there.
def traverseCategoryHierarchy(language, title, pagesWithCoordinates):
    print "looking at title " + title

    #resultCount = scraperwiki.sqlite.execute("SELECT COUNT(*) as ResultCount FROM categoryStructure WHERE Language='" + language + "' AND FromTitle='" + title + "'")  
    # This is really silly
    resultCount = 0 #resultCount[u'data'][0][0]

    # TODO would be nice to have some way to rerun the scraper without having to download everything again
    # categories with no known subcategories and pages could be checked, with everything else being skipped
    # also don't check for coordinates if we already know them (or LastChanged date is still recent)
    
    if resultCount > -1:
        # TODO it would be nice to extract the country as well so that the data can be visualized without loading too many points.
        # The top level categories should have this in there.  Once this is found, it can be passed through the recursive function call

        subCategories = getSubCategories(language, title)
        print "subCategories"
        print subCategories

        pagesInCategory = processPagesFromCategory(language, title, pagesWithCoordinates)

        # get all the different language versions of the pages encountered
        languageLinks = getLanguageLinks(language, "|".join(pagesInCategory).encode("utf-8"))
        print "languageLinks"
        print languageLinks

        # for each of the language links, we want to check for coordinates as well
        # TODO set up a check to see if coordinates conflict, or only exist on one language version but not another
        
        # what's returned it a list of dictionaries
        # we want to group these by language, and then check for coordinates for all of them
        pagesToCheckForCoordinates = dict()
        for languageLinkInfo in languageLinks:
            for key in languageLinkInfo.keys():
                if key in pagesToCheckForCoordinates:
                    pagesToCheckForCoordinates[key] = pagesToCheckForCoordinates[key] + "|" + languageLinkInfo[key]
                else:
                    pagesToCheckForCoordinates[key] = languageLinkInfo[key]

        print "pagesToCheckForCoordinates"
        print pagesToCheckForCoordinates

        for key in pagesToCheckForCoordinates:
            print "getting coordinates for " + key + " language plants"
            getPageCoordinates(key.encode("utf-8"), pagesToCheckForCoordinates[key].encode('utf-8'))

        # for a given category, visit its equivalent pages in other languages, find those pages, and get the coordinates from them.
        languageLinks = getLanguageLinks(language, title) #this returns a dictionary
        print "category languageLinks"
        print languageLinks
        if len(languageLinks) > 0:
            for key in languageLinks[0].keys():
                processPagesFromCategory(key, languageLinks[0][key].encode("utf-8"), pagesWithCoordinates)

        relevantSubCategories = filterRelevantSubCategories(subCategories)
        print "relevantSubCategories"
        print relevantSubCategories
        
        for subCat in relevantSubCategories:
            traverseCategoryHierarchy(language, subCat, pagesWithCoordinates)

title = "Category:Power_stations_by_country"
# title = "Category:Former oil-fired power stations in the United States"
# title = "Category:Combined heat and power plants in Denmark"

# parent category of this is http://en.wikipedia.org/wiki/Category:Hydroelectric_power_stations_in_Brazil
# title = "Category:Hydroelectric_power_stations_in_Paran%C3%A1_(state)"
language = "en"
#scraperwiki.sqlite.execute("delete from CategoryStructure where FromTitle = 'Category:Lists_of_power_stations_by_country'")
#scraperwiki.sqlite.commit()
title = "Category:Renewable_energy_power_stations_by_country"
traverseCategoryHierarchy(language, title, [])
title = "Category:Lists_of_power_stations_by_country"
traverseCategoryHierarchy(language, title, [])

# get all the pages with coordinates, want to reduce the number of API calls
results = scraperwiki.sqlite.execute("SELECT DISTINCT Language || ':' || Title FROM pageCoordinates")
results = results[u'data']
pagesWithCoordinates = []
for pageWithCoordinates in results:
    pagesWithCoordinates.append(pageWithCoordinates[0])

print pagesWithCoordinates

# what about pages with language links?  need to join everything together except for the metadata columns

# these categories look unexplored - they have no subcategories or pages recorded for them
results = scraperwiki.sqlite.execute("SELECT DISTINCT T2.ToTitle FROM categoryStructure T2 WHERE T2.ToTitle NOT IN (SELECT T1.FromTitle FROM categoryStructure T1) AND NameSpaceToTitle == '14'")

unExploredCategories = results[u'data']
for unExploredCategory in unExploredCategories:
    category = unExploredCategory[0]
    traverseCategoryHierarchy(language.encode("utf-8"), category.encode("utf-8"), pagesWithCoordinates)



# when restarting the scraper from an error, we want to locate all the categories without known subcategories and without known pages



# get time stamp of last revision - to be used when updating the data - see if we already have the latest
# http://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Albert_Einstein&rvprop=timestamp

