import scraperwiki
import lxml.html
import urlparse

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

def clean_and_makefloat(strval,rmvtext): 
#where value needs to be converted to float, strip down characters

    if strval is not None:
        retval = strval.replace(rmvtext, "")
        retval = retval.replace("-", "")
        retval = retval.replace(" ", "")
        if retval == "":
            retval = 0
        else:
            retval = float(retval)
    else:
        retval = 0

    return retval

def build_url_list(baseurl,suburl, startpage, maxpage):

    starting_url = urlparse.urljoin(baseurl, suburl)

    for pageno in range(startpage,maxpage):

        url = starting_url+str(pageno)
        root = fetch_html(url)

        rows = root.cssselect("table.players-table tr")

        urllist = []


        for row in rows:
            oviewinfo = {}
            table_cells = row.cssselect("td a")
            table_cells2 = row.cssselect("td")
            if table_cells:
                    oviewinfo['Player URL'] = urlparse.urljoin(baseurl,table_cells[0].get('href'))
                    oviewinfo['First Season'] = table_cells2[2].text
                    oviewinfo['Last Season'] = table_cells2[3].text
                    oviewinfo['Active'] = table_cells2[4].text
                    urllist.append(oviewinfo)

        print urllist
        extract_page(urllist)


def extract_page(pageurls):
#goes through each page from the pageurls list and gets data from each
# some useful info on oview page so this now passed in as a list of dicts

    data= []

    #loop through each page
    for playerpageurl in pageurls:

        playerinfo = {}

        #ADD DATA FROM O/VIEW PAGE TO DICT
        playerinfo['Player URL'] = playerpageurl['Player URL']
        playerinfo['First Season'] = playerpageurl['First Season']
        playerinfo['Last Season'] = playerpageurl['Last Season']
        playerinfo['Active'] = playerpageurl['Active']

        
        pageurl = playerpageurl['Player URL']

        root2 = fetch_html(pageurl)

        #dictionary to store info for each player

        #this will be key as names not necessarily unique
        playerinfo['Player URL'] = pageurl

        for nmel in root2.cssselect("div.breadcrumb"):

            elsp = nmel.cssselect("span")

            playerinfo['Player Name'] = elsp[0].text_content()


        #GET VALUES FOR CURRENT CLUB AND POSITION

        for li in root2.cssselect("ul.stats"):
            lisp = li.cssselect("span")
            lip = li.cssselect("p")

            
            spkey = ""
            pval = ""
            for sp in range(len(lip)):
                if sp <= len(lip):
                    spkey = lisp[sp].text_content()
                    pp = lip[sp].cssselect("p")

                    if spkey == "CLUB" or spkey == "POSITION":
                        pval = pp[0].text_content()
                        #where no club replace '-' with empty
                        playerinfo[str(spkey)] = pval.replace("-", "")
                
        #GET ALL OTHER FIELDS FROM OVERVIEW PAGE
        for tr in root2.cssselect("table.contentTable tr"):

            table_cells = tr.cssselect("td")

            # loop through every other column to get keys, then offset to right to get value
            val = ""
            rawval = ""
            key = ""
            for cells in range(0,len(table_cells),2):
                
                key = table_cells[cells].text

                #value is adjacent column to key
                #clean and convert values as appropriate
                if len(table_cells) >1:
                    if key == 'Nationality':
                        val = table_cells[cells+1].text_content()
                    elif key == 'Home grown player':
                        val = table_cells[cells+1].text.strip()
                    elif key == 'Height':
                        rawval = table_cells[cells+1].text
                        val = clean_and_makefloat(rawval,"m")

                    elif key == 'Weight':
                        rawval = table_cells[cells+1].text
                        val = clean_and_makefloat(rawval,"kg")
                    elif key in ('Red cards','Yellow cards','Appearances','Goals') :
                        rawval = table_cells[cells+1].text
                        if rawval is None or rawval.replace("-", "") == "":
                            val = 0
                        else:
                            val = int(rawval)
                    else:
                        rawval = table_cells[cells+1].text
                        if rawval is not None:
                            val = rawval.replace("-", "")
                        else:
                            val = rawval
                #only save if proper key
                if type(key) in [unicode, str]:
                    stripkey = key.strip()
                    if len(stripkey)>0:
                        playerinfo[stripkey] = val

        # add player record to data
        data.append(playerinfo)

    print data


        # To extend to CAREER HISTORY pages, replace part of url to match below
        # http://www.premierleague.com/en-gb/players/profile.career-history.html
        # 3 levels of data- o/view, clubs, club stats



    #WRITE DATA TO SQL - one page's worth of players at a time
    scraperwiki.sqlite.save(['Player URL'], data)
    scraperwiki.sqlite.save_var('last_url', pageurl)
    #print scraperwiki.sqlite.select("* from swdata")


base_url = 'http://www.premierleague.com'
sub_url = '/en-gb/players/index.html?paramSeason=all&paramSearchType=A_TO_Z&paramSelectedPageIndex='

# set start and end pages based on previous runs
build_url_list(base_url,sub_url,105,272)


import scraperwiki
import lxml.html
import urlparse

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

def clean_and_makefloat(strval,rmvtext): 
#where value needs to be converted to float, strip down characters

    if strval is not None:
        retval = strval.replace(rmvtext, "")
        retval = retval.replace("-", "")
        retval = retval.replace(" ", "")
        if retval == "":
            retval = 0
        else:
            retval = float(retval)
    else:
        retval = 0

    return retval

def build_url_list(baseurl,suburl, startpage, maxpage):

    starting_url = urlparse.urljoin(baseurl, suburl)

    for pageno in range(startpage,maxpage):

        url = starting_url+str(pageno)
        root = fetch_html(url)

        rows = root.cssselect("table.players-table tr")

        urllist = []


        for row in rows:
            oviewinfo = {}
            table_cells = row.cssselect("td a")
            table_cells2 = row.cssselect("td")
            if table_cells:
                    oviewinfo['Player URL'] = urlparse.urljoin(baseurl,table_cells[0].get('href'))
                    oviewinfo['First Season'] = table_cells2[2].text
                    oviewinfo['Last Season'] = table_cells2[3].text
                    oviewinfo['Active'] = table_cells2[4].text
                    urllist.append(oviewinfo)

        print urllist
        extract_page(urllist)


def extract_page(pageurls):
#goes through each page from the pageurls list and gets data from each
# some useful info on oview page so this now passed in as a list of dicts

    data= []

    #loop through each page
    for playerpageurl in pageurls:

        playerinfo = {}

        #ADD DATA FROM O/VIEW PAGE TO DICT
        playerinfo['Player URL'] = playerpageurl['Player URL']
        playerinfo['First Season'] = playerpageurl['First Season']
        playerinfo['Last Season'] = playerpageurl['Last Season']
        playerinfo['Active'] = playerpageurl['Active']

        
        pageurl = playerpageurl['Player URL']

        root2 = fetch_html(pageurl)

        #dictionary to store info for each player

        #this will be key as names not necessarily unique
        playerinfo['Player URL'] = pageurl

        for nmel in root2.cssselect("div.breadcrumb"):

            elsp = nmel.cssselect("span")

            playerinfo['Player Name'] = elsp[0].text_content()


        #GET VALUES FOR CURRENT CLUB AND POSITION

        for li in root2.cssselect("ul.stats"):
            lisp = li.cssselect("span")
            lip = li.cssselect("p")

            
            spkey = ""
            pval = ""
            for sp in range(len(lip)):
                if sp <= len(lip):
                    spkey = lisp[sp].text_content()
                    pp = lip[sp].cssselect("p")

                    if spkey == "CLUB" or spkey == "POSITION":
                        pval = pp[0].text_content()
                        #where no club replace '-' with empty
                        playerinfo[str(spkey)] = pval.replace("-", "")
                
        #GET ALL OTHER FIELDS FROM OVERVIEW PAGE
        for tr in root2.cssselect("table.contentTable tr"):

            table_cells = tr.cssselect("td")

            # loop through every other column to get keys, then offset to right to get value
            val = ""
            rawval = ""
            key = ""
            for cells in range(0,len(table_cells),2):
                
                key = table_cells[cells].text

                #value is adjacent column to key
                #clean and convert values as appropriate
                if len(table_cells) >1:
                    if key == 'Nationality':
                        val = table_cells[cells+1].text_content()
                    elif key == 'Home grown player':
                        val = table_cells[cells+1].text.strip()
                    elif key == 'Height':
                        rawval = table_cells[cells+1].text
                        val = clean_and_makefloat(rawval,"m")

                    elif key == 'Weight':
                        rawval = table_cells[cells+1].text
                        val = clean_and_makefloat(rawval,"kg")
                    elif key in ('Red cards','Yellow cards','Appearances','Goals') :
                        rawval = table_cells[cells+1].text
                        if rawval is None or rawval.replace("-", "") == "":
                            val = 0
                        else:
                            val = int(rawval)
                    else:
                        rawval = table_cells[cells+1].text
                        if rawval is not None:
                            val = rawval.replace("-", "")
                        else:
                            val = rawval
                #only save if proper key
                if type(key) in [unicode, str]:
                    stripkey = key.strip()
                    if len(stripkey)>0:
                        playerinfo[stripkey] = val

        # add player record to data
        data.append(playerinfo)

    print data


        # To extend to CAREER HISTORY pages, replace part of url to match below
        # http://www.premierleague.com/en-gb/players/profile.career-history.html
        # 3 levels of data- o/view, clubs, club stats



    #WRITE DATA TO SQL - one page's worth of players at a time
    scraperwiki.sqlite.save(['Player URL'], data)
    scraperwiki.sqlite.save_var('last_url', pageurl)
    #print scraperwiki.sqlite.select("* from swdata")


base_url = 'http://www.premierleague.com'
sub_url = '/en-gb/players/index.html?paramSeason=all&paramSearchType=A_TO_Z&paramSelectedPageIndex='

# set start and end pages based on previous runs
build_url_list(base_url,sub_url,105,272)


