#############################################################
# For a defined period, retrieves the shows from Classic FM #
# on those days, and all of the tracks played               #
#                                                           #
# Interesting issue picked up                               #
#  one show runs 2200-0200, therefore was appearing on pages#
#  for consecutive days causing duplicates.                 #
#  - resolved by checking show url against run day's date   #
#  - with a show loop, if start time pm, adds one to date   #
#     for any tracks after midnight (i.e. am track times)   #
# Page for first show of 14/01/13 contains erroneous info   #
#   might be best to ignore/delete                          #
#                                                           #
#01-03-13 February's extract- composer element has changed  #
#          need to fix as most appearing null in data now   #
#############################################################


import scraperwiki
import lxml.html
import dateutil.parser
import datetime

def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return

#Generate a list of dates working back from a date (e.g. passing daysback 14 gives list for last 2 weeks)
def generate_dates(start_date, daysback):
    counter = 0

    datelist = []
    for a in range(0,daysback):
        outdate = start_date - datetime.timedelta(a)

        datelist.append(outdate)

    print datelist
    return datelist
    

def build_url_list(baseurl, firstdate, retrodays):

    suburl = baseurl+"/radio/playlist/"

    start_date = firstdate
    #start_date = datetime.date.today()

    archdates= []

    #call function to generate a list of dates
    archdates = generate_dates(start_date, retrodays)

    #print "bul2", archdates 


    for archdate in archdates:

        #For each date retrieve the day's schedule and add to a list
        urllist = []

        #print archdate
        archyear = archdate.year
        archmonth = archdate.strftime("%B")   #need name of month for url
        archday = archdate.day                #uses 1,2,3 etc for single digits
        print archyear, archmonth, archday

        datestring = "%s/%s/%s" %(archyear,archmonth.lower(),archday)
        pageurl= suburl + datestring

        root = fetch_html(pageurl)
        html = scraperwiki.scrape(pageurl)
        root = lxml.html.fromstring(html)
        print pageurl

        #get the show page links
        for a in root.cssselect("div.show_carousel li"):
            hrefs = a.cssselect("a")
            #print hrefs

            if len(hrefs) >0:
                fullurl = baseurl + hrefs[0].get('href')
                #only append show url if date matches current date
                print datestring, fullurl
                if datestring in  fullurl:
                    urllist.append(fullurl)
        print archdate, urllist

        #use this function to extract one day's playlist at a time
        #could have done calls the other way around, but this breaks out processing
        extract_playlist(urllist, archdate)


def extract_playlist(showurls,showdate):
#goes through all of the shows for one date and scrapes tracks played

    #loop through the page for each show
    for showurl in showurls:
        
        root2 = fetch_html(showurl)
        html = scraperwiki.scrape(showurl)
        root2 = lxml.html.fromstring(html)

        #intialise for each show
        showstart = ''
        trackcount = 0

        #loop through each track

        for el2 in root2.cssselect("ul.track_list div.playlist_entry_info"):
            trackinfo = {}
            trackcount += 1


            #TIME track played
            elp = el2.cssselect("p")

            tracktime =''
            tracktime2 =''
            trackdate =''
            #TIME track played - change to a datetime, more flexible
            if len(elp)>0:
                tracktime = elp[0].text_content()

            if trackcount == 1:
                showstart = tracktime

            #if a show starts in the evening, any tracks after midnigh should be dated next day
            if 'pm' in showstart and 'am' in tracktime:
                trackdate = showdate + datetime.timedelta(1)
            else:
                trackdate = showdate

            tracktime2 = dateutil.parser.parse(str(trackdate)+' '+tracktime)

            ##ADD TO DICTIONARY FOR WRITING TO SQL
            trackinfo['Track Time'] = tracktime2
            
            ##ADD TO DICTIONARY FOR WRITING TO SQL
            trackinfo['Track Date'] = trackdate


            #either of these can contain TRACK NAME
            elb = el2.cssselect("h3.track span")
            elb2 = el2.cssselect("h3.track a")

            #COMPOSER INFO
            elh3 = el2.cssselect("h3.artist")

            #OTHER ATTRIBUTES- CONDUCTOR, ENSEMBLE, LABEL, CATALOG NO
            extattr = el2.cssselect("ul.extended_attributes li")
            
            #TRACK NAME
            #some artists have birth info included- strip off
            
            #should only be one of the first two
            clntrackname =''
            trackname =''
            tmp=''
            if len(elb)>0 or len(elb2)>0:
                if len(elb)>0:
                    trackname = elb[0].text_content()
                elif len(elb2)>0:
                    trackname = elb2[0].text_content()

                #if track name has 'Watch' at the start, remove it
                tmp = trackname.split(' ')
                if "Watch " in trackname:
                    tmp.remove("Watch")
                #if track name has ')' at end, remove last word e.g. '(2)'
                if trackname[-1] == ')':
                    del tmp[-1]
                clntrackname = " ".join(tmp)

            ##ADD TO DICTIONARY FOR WRITING TO SQL
            trackinfo['Track Name'] = clntrackname

            #print "track", clntrackname



            #COMPOSER- can have birth info appended, separate out
            #doesn't currently deal with joint compositions/arrangements
            #specific exclusion added for names suffixed with '(II)'- but doesn't yet deal with properly
            #probably a more pythonic way to initialise multiple variables than this...
            complifespan =''
            compbirthloc =''
            clncomposer =''
            ctmp =''
            ctmp2 =''
            ctmp3 =''
            ctmp4 =''
            ctmp5 =''
            ctmp6 =''
            if len(elh3)>0:
                composer = elh3[0].text_content()
                if '(' in composer and '(II)' not in composer:
                    ctmp = composer.split(' (')
                    #separate out last bit- birth info
                    ctmp2 = ctmp[-1]
                    #split birth country and lifespan
                    ctmp3 = ctmp2.split(' : ')
                    complifespan = ctmp3[0]
                    #quick fix where no second part
                    if len(ctmp3)>1:
                        ctmp4 =  ctmp3[1]
                        #strip ')' from country
                        ctmp5 = ctmp4[0:-1]
                        compbirthloc = "".join(ctmp5)
                    del ctmp[-1]
                    clncomposer =  " ".join(ctmp)
                else:
                    clncomposer = composer
                #print "comp", clncomposer 
                #print "lifespan", complifespan
                #print "loc", compbirthloc

            #birth info not always present, if required this would be better picked
            # up elsewhere and written to a specific composers table

            ##ADD TO DICTIONARY FOR WRITING TO SQL
            trackinfo['Composer Name'] = clncomposer.strip()


            #OTHER INFO- can contain variable fields which are self-labelled
            #split fields into label and value
            eatmp = ''
            eatmp2= ''
            for attr in range(len(extattr)):
                eatmp = extattr[attr].text_content()
                eatmp2 = eatmp.split(': ')

                ##ADD TO DICTIONARY FOR WRITING TO SQL
                trackinfo[eatmp2[0]] = eatmp2[1]




            #WRITE DATA TO SQL - one track at a time for the moment
            try:
                scraperwiki.sqlite.save(unique_keys=['Track Time'], data=trackinfo)
            except:
                print "Failed on: %s - %s - %s --> " % (showurl, trackinfo['Track Date'],trackinfo['Track Time'])

            #print trackinfo

# last param is number of days to go back
build_url_list("http://www.classicfm.com",datetime.date(2013, 1,29),1)

