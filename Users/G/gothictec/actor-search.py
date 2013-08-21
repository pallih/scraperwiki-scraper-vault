###
#
# 0916162 (Luke Mills)
# University of Wolverhampton
# 
# Scraper WIKI assignment
# CP4010 Programming for Application Development - Sarah Mount
#
#  Application Purpose:
#   
#
###


###
# IMPORTS
###
import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Actor 1', 'Actor 2', 'Films', 'Quantity'])


###
# VARS
###

#GLOBAL Dictionaries
actorlist = {}                                   # A Dictionary of actors (keys) and filmlist - Dictionary  as  values
filmlist={}                                      # A list of films - destroyed after each actor is finished
uniquefilmlist = {}                              # A full list of films to look at.  Used to ensure that we only process each film once!
actorKeys = []
actorQty = []

#GLOBAL Vars
actor_depth_to_go = 3                            # How many actors in each film to look at.  The more actors to look at the bigger the tree
film_depth_to_go = 10                            # How many films to look at that each actor has been involved in
unique_film_depth_to_go = 200                    # The threshold of unique films to collect
base_url = 'http://uk.imdb.com'                  # Base URL
starting_url = base_url + '/title/tt1504320/'    # Starting Path from URL




####
#METHODS
####

def scrape_and_get_actor_list(url):
    """
        Description
        -------------
        Scrape a URL to get a list of all the actors.  Then for each actor 
        the sub method to extract a film list is called.  That film list
        is then applied to the actor.
        
        scrape_and_get_actor_list(url)

        Example
        -------
            scrape_and_get_actor_list(""http://uk.imdb.com/title/tt1504320"")

        Dependencies
        -------------
            None
    """
    try:                                    # TRY START - this is because sometimes we may get time-outs from the servers
        html = scraperwiki.scrape(url)      # Get HTML from URL
        soup = BeautifulSoup(html)          # Convert HTML to a soup Object

        data_table = soup.find("table",  {"class": "cast_list"})   # Find the correct table containing cast_list as class
                                                                   # and table object
        rows = data_table.findAll("tr")                            # Extract ALL table Rows (TR)
        actorDepth= 0
        for row in rows:                                           # Loop through all rows


            table_cells = row.findAll("td")                        # Extract ALL table Cells (TD)
            if(len(table_cells)>1):                                # Check - Do we have any cells?
                if table_cells: 
                    if(actorDepth< actor_depth_to_go):             # Check to see if we have reached our actor depth on each film
                        innerHTML = table_cells[1]

                        if(findItemInList(table_cells[1].text, actorlist) != True):  # If we have not already processed this film lets do it
                            global filmlist                                          # redefine filmlist from global variable
                            filmlist = extract_actor_url(innerHTML,actorDepth)                 # call extract film list
                            actorlist[table_cells[1].text] = filmlist 
                        filmlist = {}                                               # reset film list to blank ready for next actor
                    else:
                        break                                                       # exit actor loop once enough have been scraped
                    actorDepth+=1;
                        
    except:
        print "error"

def findItemInList(itemName, list_items):
    """
    Description
    -----------    
    Checks the list to see if the film already exists in the list!
    returns True if actor exists in list
    
    findItemInList(itemName, list_items)

    Example
    -------
         findItemInList("Se7en", DisctionaryList)

    Dependencies
    -------------
        None
    """
    if itemName in list_items:
        return True
    else:
        return False
    


def extract_actor_url(html,actorDepth):
    """
    Description
    -----------    
    From the inner HTML extract the URL for the actress - This function will
    then return all the films that each actor has worked on
    (to the depth set in film_depth_to_go)
    
    extract_film_url(html,actorDepth)

    Example
    -------
         extract_film_url("<a href="/name/nm0005109/">Mila Kunis</a>", 2)

    Dependencies
    -------------
        None
    """
    actor_links= html.findAll('a')                           # Extract ALL link tags (A)
    for links in actor_links:                                # There should only be one link - however loop through
        actorlink= links ['href']                            # Extract URL from page
        film_list =scrape_and_look_for_films(base_url  + actorlink, actorDepth)  # Call sub function to scrape URL's of each film
                                                                        # returning film list
        break                                                # ONLY PROCESS FIRST HYPERLINK so BREAK!
    return(film_list)                                        # return film list
        


def scrape_and_look_for_films(url,actorDepth):
    """
    Description
    -----------    
    Checks the list to see if the film already exists in the list!
    returns True if actor exists in list
    
    scrape_and_look_for_films(url, actorDepth)

    Example
    -------
         scrape_and_look_for_films("http://uk.imdb.com/name/nm0005109/", 2)

    Dependencies
    -------------
        None
    """

    try:                                                            #Start Try - just incase Scrape fails
        html = scraperwiki.scrape(url)                              # Get HTML from URL
        soup = BeautifulSoup(html)                                  # Convert HTML to a soup Object
        divs = soup.findAll('div', {"class": re.compile('^filmo-row')})      # Find all divs for the films (odd and even rows)

        filmLength = 0                                              # Set filmLength as 0 for actor - we only want to process
        
        
                                                                    # up to the constant variable of films per actor
                                                                    # as defined in "film_depth_to_go"
        for div in divs:                                            # Loop round all divs
            years = div.findAll("span",{"class": "year_column"})    # extract the year
            yearOfFilm  = ""                                        # define temp variable to store year
            for year in years:                                      
                try:
                    yearOfFilm = year.contents[0]                   # get contents of year
                except:
                    yearOfFilm = 'UKN'                              # if no year set as Unkown
            if(filmLength <film_depth_to_go):                       # if we have not reached oput limit lets store the film name in the list
                film = extract_filmname(div)

                if(findItemInList(film,uniquefilmlist )!=True):     # Check Film is not in the unique list - if not add
                    if(  len(uniquefilmlist) < unique_film_depth_to_go ):
                        uniquefilmlist[film] = base_url   + extract_filmlink(div)
        
                if(findItemInList(film, filmlist)!=True):           # Check film is not in actor list if not add
                    filmlist[film] = yearOfFilm
            else:                                                   # Break out of loop once we have reached our limit
                break
            filmLength +=1
    except:                                                         # Print out exception error
        print "error"
    return(filmlist)                                                # return film list




def extract_filmname(html):
    """
    Description
    -----------    
    Extracts the Film Name from the HTML
    
    extract_filmname(html)

    Example
    -------
         extract_filmname("<a href="/title/tt1320261/">Gulliver's Travels</a>")

    Dependencies
    -------------
        None
    """
    films_links= html.findAll('a')
    for links in films_links:
        filmlink= links ['href']
        return((links.contents[0]))
    

def extract_filmlink(html):
    """
    Description
    -----------    
    Extracts the Film Name from the HTML
    
    extract_filmnlink(html)

    Example
    -------
         extract_filmnlink("<a href="/title/tt1320261/">Gulliver's Travels</a>")

    Dependencies
    -------------
        None
    """
    films_links= html.findAll('a')
    for links in films_links:
        filmlink= links ['href']
        return(filmlink)
        

def startprocess():
    """
    Description
    -----------    
        Starts the process for scraping the films
        and calls a recursive loop until we have scoured enough films
    
    startprocess()

    Example
    -------
        startprocess()

    Dependencies
    -------------
        None
    """
    print "Processing Initial Film "

    scrape_and_get_actor_list(starting_url)  # Do Initial scrap from starting URL - to get n depth of actors and nn depth of films
    counter = 0;
    for v in uniquefilmlist.keys():
        print "Processing Film " + v + " : Total Films in list (" + str(len(uniquefilmlist)) + ")" + " : Total Actors in list (" + str(len(actorlist)) + ") :" + str(counter)
        scrape_and_get_actor_list(uniquefilmlist[v] )           # for each film in the film list scrape the n actors and extract nn more films
        uniquefilmlist.update()                                 #
        counter +=1


def processResults():
    """
    Description
    -----------    
        Loops throuhg all actors lists and finds any 
        occurance where actors have worked together
        
        ##For each actor searh list of films
        ##    See if any other actor has worked with them
        ##        if there is a first match
        ##            Create a Dictionary Entry 'Colin Firth -> Helen Bohem Carter',  1, Film
        ##        else
        ##            Increment Dictionary Value by 1
        ##        Move on to next actors Film
        ##    Move on to next actor
        ##
        ##Loop through Dictionary and Store in Table

    
    processResults()

    Example
    -------
        processResults()

    Dependencies
    -------------
        None
    """
    actorCollaborationsTimes = {} # define temp dictionary for Times that actors have worked together
    actorCollaborationsFilms = {} # define temp dictionary for Films that actors have worked together on
    countval = 1                  # Starting Value (ignoring the first element
    for v in actorlist.keys():                                       # For each actor
        for filmName in actorlist[v].keys():                         # For each of the films within the list
            
            filmalist = searchActorsforFilms(filmName, countval)     # Find all other actors that have worked on this film
                                                                     # starting only from where we left (hence countval)
            
            x = 0                                                    # Process the list and create a dictionary entry if it does not exist and amend if it does
            while x < len(filmalist ):
                
                ActorConcat = v + "|" + filmalist[x]
                if(findItemInList(ActorConcat ,actorCollaborationsTimes) !=True):
                    actorCollaborationsTimes[v + "|" + filmalist[x]] = 1
                    actorCollaborationsFilms [v + "|" + filmalist[x]] = [filmName]
                else:
                    actorCollaborationsTimes[v + "|" + filmalist[x]] += 1
                    actorCollaborationsFilms [v + "|" + filmalist[x]] += [filmName]

                x+=1
            
            


    
        countval+=1 # increment countval

  

    # get ready to sort these
    global actorQty  
    global actorKeys 

    for v in actorCollaborationsTimes.keys():     # Loop round films and store data
        actorKeys += [v]
        actorQty += [actorCollaborationsTimes[v]]


    print actorKeys

    sortValues( )
    y =0
    while y < len(actorKeys):     # Loop round films and store data
        record = {}
        
        
        actorKeyVal = actorKeys[y]
        
        record['Actor 1'] = actorKeyVal.partition("|")[0]
        record['Actor 2'] = actorKeyVal.partition("|")[2]
        x = 0
        filmstring = ""
        filmList = actorCollaborationsFilms[actorKeys[y]]
       
        while x < len(filmList):
            filmstring +=filmList[x]
            filmstring +=","
            x+=1
        record['Films'] = filmstring [:len(filmstring )-1]
        record['Quantity'] = actorCollaborationsTimes[actorKeys[y]]
        print record
        scraperwiki.datastore.save(["Actor 1"],record)
        y+=1



def sortValues():
    """sortValues

     create_list()
      i.e.
     create_list()
    ?? Can't help thinking after writing Bubble sorts for years I may have done the same here!
    """

    newtupleset = actorQty 
    newtupleset2 = actorKeys
    x = 0
    while (x < len(newtupleset)):
        y = x + 1
        while (y < len(newtupleset)):
            if(newtupleset[x]<newtupleset[y]):

                tempval1 = newtupleset[x]
                tempval2 = newtupleset[y]
                tempval3 = newtupleset2[x]
                tempval4 = newtupleset2[y]

                newtupleset[y] = tempval1
                newtupleset[x] = tempval2
                newtupleset2[y] = tempval3
                newtupleset2[x] = tempval4

            y+=1
        x+=1
    global actorQty  
    global actorKeys 
    actorQty  =newtupleset 
    actorKeys = newtupleset2 






def searchActorsforFilms(filmname, startactorCountVal):
    """
    Description
    -----------    
        Loops through all lists of actors to see if they have worked on the same film as we have
        in the list
    
    searchActorsforFilms(filmname, startactorCountVal)

    Example
    -------
        searchActorsforFilms("Psychoville", 2)

    Dependencies
    -------------
        None
    """
    countval = 1
    filmalist = []
    for v in actorlist.keys():
        actor = ""
        actor = v
        if(countval >startactorCountVal):
            for film in actorlist[v].keys():
                if(film == filmname):
                    filmalist += [actor]


        countval += 1
    return (filmalist )





startprocess()   
print actorlist 
print uniquefilmlist
processResults()
