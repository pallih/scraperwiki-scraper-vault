# -*- coding: ISO-8859-1 -*-
# This is a work in progress to scrape ACB.COM for game info
# text to number conversion copied from http://datapatterns.org/howtogetdata.html#extracting-data

import scraperwiki
import lxml.html

#
# UTILITY FUNCTIONS
#

def to_int(number, european=False):
    """
    >>> to_int('32')
    32
    >>> to_int('3,998')
    3998
    >>> to_int('3.998', european=True)
    3998
    """
    if european:
        number = number.replace('.', '')
    else:
        number = number.replace(',', '')
    return int(number)

def to_sec(string):
    """
    >>> to_sec('1:0')
    60
    >>> to_int('10:13')
    613
    """
    time = string.partition(':')
    sec = int(time[0])*60 + int(time[2])
    return int(sec)

def split_pair(string,sep):
    """
    >>> split_pair('2/4','/')
    2,4 
    """
    pair = []
    trio = list(string.partition(sep))
    trio.remove(sep)
    pair = tuple(trio)
    return pair

def to_float(number, european=False):
    """
    >>> to_float(u'42.1')
    42.1
    >>> to_float(u'32,1', european=True)
    32.1
    >>> to_float('3,132.87')
    3132.87
    >>> to_float('3.132,87')
    3132.87
    >>> to_float('(54.12)')
    -54.12

    Warning
    -------

    Incorrectly declaring `european` leads to troublesome results:

    >>> to_float('54.2', european=True)
    542
    """
    import string
    if european:
        table = string.maketrans(',.','.,')
        number = string.translate(number, table)
    number = number.replace(',', '')
    if number.startswith('(') and number.endswith(')'):
        number = '-' + number[1:-1]
    return float(number)

def pad_zeroes(number):
    num = str(number)
    while len(num) < 3:
        num = '0' + num
    return num

def convertStr(s):
    """Convert string to either int or float."""
    try:
        ret = int(s)
    except ValueError:
    #Try float.
        ret = float(s)
    return ret

def CreateTablePartidos():
# I created this function to try and get the columns in the right order.
# It seems to do the job :-)
# First we erase previous versions of the table
#    scraperwiki.sqlite.execute("drop table if exists Partidos")
# Next we create the table "Partidos" to store the game results
    scraperwiki.sqlite.execute("create table Partidos (GameId string, LeagueCod string, Season int, GameNum string, GameDate string, GameTime string, HomeTeam string, HomeScore int, VisTeam string, VisScore int, HomeScoreP0 int, VisScoreP0 int,HomeScoreP1 int, VisScoreP1 int, HomeScoreP2 int, VisScoreP2 int, HomeScoreP3 int, VisScoreP3 int, GameJ string, GamePlace string, Audience string)")
    return

def CreateTablePartidos_Detalles():
# First we erase previous versions of the table
#    scraperwiki.sqlite.execute("drop table if exists Partidos_Detalles")
# Next we create the table "Partidos_Detalles" to store the game details by player
    scraperwiki.sqlite.execute("create table Partidos_Detalles (GameId string, PlayerId string, ShirtNum string, PlayerName string, PlayTime int, P int, T2I int, T2C int, T3I int, T3C int, T1I int, T1C int, REBD int, REBO int, A int, BR int, BP int, C int, TAPF int, TAPC int, M int, FPF int, FPC int, PlusMin int, ACBEval int)")
    return
#
# SCRAPE FUNCTIONS
#

def ScrapeTeams(url):
    # This is a small function to get the team names from the stat sheet
    # As of now it's not being called. I'll try to figure out a way to include the team
    # of the player in the detailed table. Untill then we'll have to find the team
    # joining another table.
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # Select all <td> elements of class="estverdel">
    # to get the 2 teams
    n = 0
    for e in root.cssselect("td.estverdel"):
        Team = ''
        Team = Team.join(e.text_content().split()[0:-1])
        print Team
    return

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
                HomeScore = int(el.text_content().strip(' |'))     
        if el.attrib['align'] == "left":  #!! Left and right are reversed on the page
            if n == 1:
                VisTeam = el.text_content().strip()
                n = n+1
            else:
                VisScore = int(el.text_content().strip())
                n = 0
    
    # Next selection: Game details (date, time, place, audience)
    # Data is separated by "|" so we split the string using "|" as separator
    # Does not work as of now because of the unicode 
    # NEW TEMPORARY APPROACH: we'll write the data to a table and clean-up further using google refine
    el = root.cssselect("tr.estnegro td")
    #text = '\xa0'.decode('ISO-8859-1') 
    #line = el[0].text_content()
    #print line
    GameInfo = el[0].text_content().split("|")
    print GameInfo
    # example: [u'\xa0J 1 ', u' 09/10/2011 ', u' 18:00 ', u' Palacio De Deportes Comunidad De Madrid ', u' P\xfablico:11000']
    # the spaces will be removed in Google Refine

    # Next selection: Quarter (partial) results
    # Data is separated by "|" so we split the string using "|" as separator
    n=0
    HomeScoreP = []
    VisScoreP = []
    for el in root.cssselect("tr.estnaranja td"):
        if n >= 2:     # To skip the first two td elements (referees and whitespace)
            #print n
            line = el.text_content().split("|") # Partials are given as 20|19
            HomeScoreP.append(int(line[0]))   # gives us the text before the "|"
            VisScoreP.append(int(line[1]))    # gives us the text after the "|"
        n = n+1
    #print "Parciales de ",HomeTeam," : ",HomeScoreP
    data = [GameId, LeagueCod, int(Season), GameNum, GameInfo[1], GameInfo[2], HomeTeam, HomeScore, VisTeam, VisScore, HomeScoreP[0], VisScoreP[0],HomeScoreP[1], VisScoreP[1],HomeScoreP[2], VisScoreP[2],HomeScoreP[3], VisScoreP[3], GameInfo[0], GameInfo[3], GameInfo[4]]
    #print data

    # -- The next five lines aren't used anymore as direct sql is used
    #datadic = {}
    #RowTitles = ['GameId','LeagueCod','Season','GameNum','HomeTeam','HomeScore','VisTeam','VisScore','HomeScoreP1','VisScoreP1',
#'HomeScoreP2','VisScoreP2','HomeScoreP3','VisScoreP3','HomeScoreP4','VisScoreP4']
    #for k,v in zip(RowTitles,data):
    #    datadic[k] = v
    # print datadic

    # Writing info to table...
    # I tried using the usual command scraperwiki.sqlite.save(unique_keys=RowTitles, data=datadic)
    # but the column order was messed up, so I opted for direct sql commands.
    scraperwiki.sqlite.execute("insert into Partidos values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (GameId, LeagueCod, int(Season), GameNum, GameInfo[1], GameInfo[2], HomeTeam, HomeScore, VisTeam, VisScore, HomeScoreP[0], VisScoreP[0],HomeScoreP[1], VisScoreP[1],HomeScoreP[2], VisScoreP[2],HomeScoreP[3], VisScoreP[3], GameInfo[0], GameInfo[3], GameInfo[4]))
    scraperwiki.sqlite.commit()  # VERY IMPORTANT
    return

def ScrapeGamePlayerStats(url):
    # Grab the web page and scrape using lxml.html
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    # Can probably be improved. As the player stats are in a <tr> tag without name
    # we look for the player name (td class="naranjaclaro") and then go up the xml
    # tree two steps.
    #for e in root.cssselect("td.estverdel a"):
    for el in root.cssselect("td.naranjaclaro a"):
        #print el.attrib #{'href': '/jugador.php?id=BHG'} we want to extract the player id to use it as key
        Player = el.attrib['href'].partition('=') # Returns a tuple with 3 elements
        PlayerId = Player[2]
        line = el.getparent().getparent().text_content().split() # Now we can start parsing the line info...
        #print line
        ShirtNum=int(line[0])      # "Dorsal"
        l = len(line)
        if l <= 5:
        # We have a problem if some player doesn't play because the values are empty instead of '0'
        # If only the ShirtNum and the PlayerName are given we set the other fields to 0
            Name = ''
            PlayerName = Name.join(line[1:l])
            #print PlayerName
            scraperwiki.sqlite.execute("insert into Partidos_Detalles values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (GameId, PlayerId, ShirtNum, PlayerName, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            scraperwiki.sqlite.commit()  # VERY IMPORTANT
        else:
            l = len(line)
            #print l
            #print line[(l-21)] 
            test=line[1:l-21]
            #print test
            Name=''
            PlayerName=Name.join(test)
            #print PlayerName
            PlayTime=to_sec(line[(l-21)]) # We convert the played time to seconds
            P=int(line[l-20])             # Total points scored
            T2=split_pair(line[l-19],'/') # 2 points attempts and scored
            T3=split_pair(line[l-17],'/') # 3 points attempts and scored
            T1=split_pair(line[l-15],'/') # 1 point attempts and scored
            REBDO=split_pair(line[l-12],'+') # Defensive and Offensive rebounds
            A=int(line[l-11])             # Assists
            BR=int(line[l-10])            # "Balon recuperado"
            BP=int(line[l-9])             # "Balon perdido"
            C=int(line[l-8])              # ?
            TAPF=int(line[l-7])           # "Tapon efectuado"
            TAPC=int(line[l-6])           # "Tapon recibido"
            M=int(line[l-5])              # ?
            FPF=int(line[l-4])            # "Falta personal cometida"
            FPC=int(line[l-3])            # "Falta personal recibida"
            PlusMin=int(line[l-2])
            ACBEval=int(line[l-1])
            scraperwiki.sqlite.execute("insert into Partidos_Detalles values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (GameId, PlayerId, ShirtNum, PlayerName, PlayTime, P, T2[0], T2[1], T3[0], T3[1], T1[0], T1[1], REBDO[0], REBDO[1], A, BR, BP, C, TAPF, TAPC, M, FPF, FPC, PlusMin, ACBEval))
            scraperwiki.sqlite.commit()  # VERY IMPORTANT
    return

LeagueUrl = "http://www.acb.com/"
GameUrl = "fichas/"
LeagueCod = "LACB"
Season = "56"
#GameNum = "004"
GameList = [318, 319, 320, 321, 322, 323, 324, 325, 326, 328]
#last = 314
#GameList = [ x for x in range(201,last+1)]
#GameList = Gamelist.add("328","250")
#print GameList
# During testing previous tables were erased
#CreateTablePartidos()
#CreateTablePartidos_Detalles()
#info = scraperwiki.sqlite.table_info(name="Partidos")
#for column in info:
#    print column

for n in GameList:
    GameNum = pad_zeroes(n)
    GameId = LeagueCod+Season+GameNum
    RowTitles = []
    RowData = []
    #data = []
    url = LeagueUrl+GameUrl+GameId+".php"
    #print url
    #ScrapeTeams(url)
    ScrapeGameStats(url)
    ScrapeGamePlayerStats(url)
#print scraperwiki.sqlite.show_tables()
    
