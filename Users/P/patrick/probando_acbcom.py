# This is a work in progress to scrape ACB.COM for player/game info

import scraperwiki
import lxml.html

def ScrapeTeam(url):
    # Grab the web page and scrape using lxml.html
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)


    # Select all <tr> elements that are inside <table class="plantilla">
    # but stop when "promedios" is reached (end of the player list)
    n = 0
    for el in root.cssselect("table.plantilla tr"):
        if "promedios" not in el.text_content():   
            n = n+1
            if n == 1: # These are the column headers
                #RowTitles = el.text_content().encode('ascii', 'ignore') # to be sorted out: unicode strings can't be used as dict keys
                #RowTitles = RowTitles.split()+["PlayerUrl"]+["Team"]    # We define RowTitles manually for the moment
                RowTitles = ['dorsal', 'nombre', 'pos', 'pais', 'lic', 'alt', 'edad', 'temp', 'url', 'team']
                #print "ColumnTitles : "
                #print RowTitles
                #print ""
                #print "Players:"
            else:      # Here the real data starts
                RowData = el.text_content().split()
                print RowData, RowData[-4],len(RowData)
                if len(RowData[0]) > 2:  # Handle players without number
                    if RowData[0] in ["De","de","La","la"]:
                        RowData[0:1] = ' '
                    else:
                        RowData[0:0] = ' '
                if RowData[1] in ["De","de","La","la"]:
                    if RowData[2] in ["De","de","La","la"]:
                        RowData[1] = (RowData[1] +' '+ RowData[2] +' '+ RowData[3])
                        RowData[2:4] = []
                    else:
                        RowData[1] = (RowData[1] +' '+ RowData[2])
                        RowData[2:3] = []
                if RowData[-4] not in ("EUR","JFL","EXT"): # Test if Lic is a valid code (suposing these are the only lic)
                    RowData[-3:-3] = ' '
                #print RowData
                if len(RowData) != 9: # Handles multiple names (eg. Navarro, Juan Carlos)
                    RowData[1] = (RowData[1] +' '+ RowData[2] +' '+ RowData[3])
                    RowData[2:4] = []
                else:
                    RowData[1] = RowData[1] +' '+ RowData[2] # Combine name, surname 
                    RowData[2:3] = []
                RowData.append(TeamCod)
                assert len(RowData) == 9
                for el2 in el:       
                    if el2.cssselect("td.beige a"):
                        for el3 in el2:
                            PlayerUrl = LeagueUrl + el3.attrib['href']
                            RowData = RowData + [PlayerUrl]
                            print RowData
                data = {}
                for k,v in zip(RowTitles,RowData):
                    data[k] = v
                #print "Writing info to table..."
                #scraperwiki.sqlite.save(unique_keys=sorted(RowTitles), data=data)
        else:
            break
    return #data

LeagueUrl = "http://www.acb.com/"
TeamUrl = "plantilla.php?cod_equipo="
TeamCod = "BAR"
TeamList = ["BAR","MAD","BAS","PAM","GBC","BLB","SEV","ALI","RON","ZZA","JOV","MAN","OBR","CLA","MUR","FUE","EST","VAL"]



for TeamCod in TeamList:
    RowTitles = []
    RowData = []
    #data = []
    url = LeagueUrl+TeamUrl+TeamCod
    ScrapeTeam(url)



# This is a work in progress to scrape ACB.COM for player/game info

import scraperwiki
import lxml.html

def ScrapeTeam(url):
    # Grab the web page and scrape using lxml.html
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)


    # Select all <tr> elements that are inside <table class="plantilla">
    # but stop when "promedios" is reached (end of the player list)
    n = 0
    for el in root.cssselect("table.plantilla tr"):
        if "promedios" not in el.text_content():   
            n = n+1
            if n == 1: # These are the column headers
                #RowTitles = el.text_content().encode('ascii', 'ignore') # to be sorted out: unicode strings can't be used as dict keys
                #RowTitles = RowTitles.split()+["PlayerUrl"]+["Team"]    # We define RowTitles manually for the moment
                RowTitles = ['dorsal', 'nombre', 'pos', 'pais', 'lic', 'alt', 'edad', 'temp', 'url', 'team']
                #print "ColumnTitles : "
                #print RowTitles
                #print ""
                #print "Players:"
            else:      # Here the real data starts
                RowData = el.text_content().split()
                print RowData, RowData[-4],len(RowData)
                if len(RowData[0]) > 2:  # Handle players without number
                    if RowData[0] in ["De","de","La","la"]:
                        RowData[0:1] = ' '
                    else:
                        RowData[0:0] = ' '
                if RowData[1] in ["De","de","La","la"]:
                    if RowData[2] in ["De","de","La","la"]:
                        RowData[1] = (RowData[1] +' '+ RowData[2] +' '+ RowData[3])
                        RowData[2:4] = []
                    else:
                        RowData[1] = (RowData[1] +' '+ RowData[2])
                        RowData[2:3] = []
                if RowData[-4] not in ("EUR","JFL","EXT"): # Test if Lic is a valid code (suposing these are the only lic)
                    RowData[-3:-3] = ' '
                #print RowData
                if len(RowData) != 9: # Handles multiple names (eg. Navarro, Juan Carlos)
                    RowData[1] = (RowData[1] +' '+ RowData[2] +' '+ RowData[3])
                    RowData[2:4] = []
                else:
                    RowData[1] = RowData[1] +' '+ RowData[2] # Combine name, surname 
                    RowData[2:3] = []
                RowData.append(TeamCod)
                assert len(RowData) == 9
                for el2 in el:       
                    if el2.cssselect("td.beige a"):
                        for el3 in el2:
                            PlayerUrl = LeagueUrl + el3.attrib['href']
                            RowData = RowData + [PlayerUrl]
                            print RowData
                data = {}
                for k,v in zip(RowTitles,RowData):
                    data[k] = v
                #print "Writing info to table..."
                #scraperwiki.sqlite.save(unique_keys=sorted(RowTitles), data=data)
        else:
            break
    return #data

LeagueUrl = "http://www.acb.com/"
TeamUrl = "plantilla.php?cod_equipo="
TeamCod = "BAR"
TeamList = ["BAR","MAD","BAS","PAM","GBC","BLB","SEV","ALI","RON","ZZA","JOV","MAN","OBR","CLA","MUR","FUE","EST","VAL"]



for TeamCod in TeamList:
    RowTitles = []
    RowData = []
    #data = []
    url = LeagueUrl+TeamUrl+TeamCod
    ScrapeTeam(url)



