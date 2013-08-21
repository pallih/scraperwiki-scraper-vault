# -*- coding: ISO-8859-1 -*-
# This is a work in progress to scrape ACB.COM for game info

import scraperwiki
import lxml.html


def ScrapeGameStats(url):
    # Grab the web page and scrape using lxml.html
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # Select all <td> elements that are inside <div class="titulopartidonew">
    # to get the 2 teams and the score
    n = 0
    for el in root.cssselect("div.titulopartidonew td"):
        #print el.text_content().strip(' |')
        #print el.attrib['align']
        if el.attrib['align'] == "right":  #!! Left and right are reversed on the page
            if n == 0:
                HomeTeam = el.text_content().strip(' |')
                n = n+1
            else:
                HomeScore = el.text_content().strip(' |')     
        if el.attrib['align'] == "left":  #!! Left and right are reversed on the page
            if n == 1:
                VisTeam = el.text_content().strip()
                n = n+1
            else:
                VisScore = el.text_content().strip()
                n = 0
    print HomeTeam," received ",VisTeam," and the result was ",HomeScore," - ",VisScore

    # Next selection: Game details (date, time, place, audience)
    # Data is separated by "|" so we split the string using "|" as separator
    el = root.cssselect("tr.estnegro td")
    text = '\xa0'.decode('ISO-8859-1') 
    line = el[0].text_content()
    print line
    line = el[0].text_content().split("|")
    #print line
    print "Jornada :",line[0].strip('J ')
    for l in line[:]:
        newl = l.strip(' ')  # doesn't work ¿UNICODE?
        #print "+",newl,"+"
    print line
    
    # Next selection: Quarter results
    # Data is separated by "|" so we split the string using "|" as separator
    n=0
    HomeScoreQ = []
    VisScoreQ = []
    for el in root.cssselect("tr.estnaranja td"):
        #print el
        if n >= 2:
            #print n
            line = el.text_content().split("|")  # doesn't work ¿UNICODE?
            HomeScoreQ.append(line[0])
            VisScoreQ.append(line[1])
            #print line
        n = n+1
    print "Parciales de ",HomeTeam," : ",HomeScoreQ
    return

LeagueUrl = "http://www.acb.com/"
GameUrl = "fichas/"
LeagueCod = "LACB"
Season = "56"
GameNum = "004"
GameList = ["004"]#,"015","022"]

for GameNum in GameList:
    RowTitles = []
    RowData = []
    #data = []
    url = LeagueUrl+GameUrl+LeagueCod+Season+GameNum+".php"
    ScrapeGameStats(url)



