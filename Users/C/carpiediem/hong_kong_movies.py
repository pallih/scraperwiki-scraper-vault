# Scraper Name: hong_kong_movies

import lxml.html
from lxml import etree
import urllib2
from BeautifulSoup import BeautifulSoup
import datetime
import urllib
import json
import re
import scraperwiki
today = datetime.datetime.now()

def modifyDatabase():
    #  ERASE OLD SHOWINGS
    #expiration = datetime.datetime.now() - datetime.timedelta(days=14)
    #print "DELETE FROM Showings WHERE Time < '" + str(expiration.year) + "-" + str(expiration.month) + "-" + str(expiration.day) + "'"
    #scraperwiki::sqliteexecute("DELETE FROM Showings WHERE Time < '" + str(expiration.year) + "-" + str(expiration.month) + "-" + str(expiration.day) + "'");

    #  MODIFY SPECIFIC RECORDS
    #scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='', RTjson='' WHERE key=''")
    #scraperwiki.sqlite.execute("UPDATE Movies SET Alias=51 WHERE key=''")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.rottentomatoes.com/m/the_metropolitan_opera_don_giovanni_live/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771247696.json' WHERE key='dongiovann1'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.hk.artsfestivalplus.org/event!view.action?eventId=245', RTjson='' WHERE key='dreamofbabel'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.rottentomatoes.com/m/the_metropolitan_opera_faust_encore/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771247699.json' WHERE key='faust'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Title='From Up on Poppy Hill', Language='Jap', RTurl='http://www.rottentomatoes.com/m/from_up_on_poppy_hill/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771253145.json' WHERE key='fromuponpoppyhilljapanese'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.rottentomatoes.com/m/metropolitan_opera_gotterdammerung/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771247701.json' WHERE key='gtterdmmerung'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=7 WHERE key='happyfeet4dexperience'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=7 WHERE key='happyfeettwo'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://taiwanreview.nat.gov.tw/fp.asp?xItem=171093&ctNode=1900', RTjson='' WHERE key='homeintwocities'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=46 WHERE key='journey2mysteriouislandversion'")
    scraperwiki.sqlite.execute("UPDATE Movies SET RTurl='http://www.rottentomatoes.com/m/journey_to_the_center_of_the_earth_2_3d/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771042281.json' WHERE key='journey2mysteriouisland'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.rottentomatoes.com/m/the_metropolitan_opera_la_traviata/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771247702.json' WHERE key='latraviata'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.langlang.com/us/news/lang-lang-live-franz-liszt-s-200th-birthday-pre-sale-tickets', RTjson='' WHERE key='langlangconcertfranzliszt200thbirthday'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.rottentomatoes.com/m/the_metropolitan_opera_manon_2012/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771247705.json' WHERE key='manon'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.hk.artsfestivalplus.org/event!list.action?categoryId=49', RTjson='' WHERE key='miniatures'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=10 WHERE key='missionimpossibleghostprotocolver'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0097661', Language='Jap' WHERE key='mobilesuitgundam0080warinpocketparta'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0097661', Language='Jap' WHERE key='mobilesuitgundam0080warinpocketpartb'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0159508', Language='Jap' WHERE key='mobilesuitgundam0083afterglowofzeonja'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0095262', Language='Jap' WHERE key='mobilesuitgundamcharcounterattackjapanese'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0159568', Language='Jap' WHERE key='mobilesuitgundamf91japanese'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0260191', Language='Jap' WHERE key='mobilesuitgundammovieijapanese'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0159510', Language='Jap' WHERE key='mobilesuitgundammovieiisoliderofsorrow'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0159511', Language='Jap', Title='Mobile Suit Gundam The Movie III Encounter in Space' WHERE key='mobilesuitgundammovieiiiencounterinspac'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0435202', Language='Jap' WHERE key='mobilesuitzgundamiheirtostarjapanes'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0468812', Language='Jap' WHERE key='mobilesuitzgundamiiloverjapanese'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0488584', Language='Jap', Title='Mobile Suit Z Gundam III Love is the Pulse of the Stars' WHERE key='mobilesuitzgundamiiiloveipulseof'")
    scraperwiki.sqlite.execute("UPDATE Movies SET RTurl='http://www.rottentomatoes.com/m/new_years_eve_2011/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771105127.json' WHERE key='newyearieve'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt2077886' WHERE key='phantomofoperaatroyalalberthall'")
    scraperwiki.sqlite.execute("UPDATE Movies SET RTurl='http://www.taipeitimes.com/News/feat/archives/2011/04/22/2003501378/2' WHERE key='portofmists'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='' WHERE key='rodelinda'")
    scraperwiki.sqlite.execute("UPDATE Movies SET RTurl='http://sup3rjunior.wordpress.com/2011/07/06/super-junior-kry-at-ss3-3d-movie-premiere-in-japan-news-from-110706/', Language='Kor' WHERE key='ss3superjunior'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=21 WHERE key='satvagraha'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=11 WHERE key='sherlockholmesagameofshadows'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='' WHERE key='siegfried'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt2118727' WHERE key='speedangels'")
    scraperwiki.sqlite.execute("UPDATE Movies SET Alias=32 WHERE key='texakillingfield'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt1687901', RTurl='http://www.rottentomatoes.com/m/the_awakening_2011/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771249985.json' WHERE key='awakening'")
    scraperwiki.sqlite.execute("UPDATE Movies SET RTurl='http://www.taipeitimes.com/News/feat/archives/2011/04/22/2003501378/2' WHERE key='comingoftulku'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='' WHERE key='enchantedisland'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt1568346', RTurl='http://www.rottentomatoes.com/m/the_girl_with_the_dragon_tattoo/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771202144.json' WHERE key='girlwithdragontattoo'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt0063828', RTurl='', RTjson='' WHERE key='pregnantmaiden'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.taipeitimes.com/News/feat/archives/2011/04/22/2003501378/2' WHERE key='untrammeledtraveler'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://asianmediawiki.com/Turning_Point_2', Language='Can' WHERE key='turningpoint2'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='tt1324999', RTurl='http://www.rottentomatoes.com/m/twilight_saga_breaking_dawn/', RTjson='http://api.rottentomatoes.com/api/public/v1.0/movies/771040381.json' WHERE key='twilightsagabreakingdawnpart1'")
    scraperwiki.sqlite.execute("UPDATE Movies SET IMDBid='', RTurl='http://www.hk.artsfestivalplus.org/event!list.action?categoryId=49', RTjson='' WHERE key='zerodegrees'")
    
    #  UPDATE SHOWINGS POINTING TO OLD ALIASES
    #scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=? WHERE MovieId=?") #
    scraperwiki.sqlite.execute("DELETE FROM Showings WHERE MovieId=8")
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=51 WHERE MovieId=8") #alvinandchipmunk3
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=7 WHERE MovieId=65") #happyfeet4dexperience
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=7 WHERE MovieId=52") #happyfeettwo
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=46 WHERE MovieId=37") #journey2mysteriouislandversion
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=10 WHERE MovieId=39") #missionimpossibleghostprotocolver
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=21 WHERE MovieId=41") #satvagraha
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=11 WHERE MovieId=67") #sherlockholmesagameofshadows
    scraperwiki.sqlite.execute("UPDATE Showings SET MovieId=3 WHERE MovieId=66") #texakillingfield
    scraperwiki.sqlite.commit()


def scrapeAllSites():

    #  ADD TO SCRAPER LOG
    beginCount = 0
    dbCount = scraperwiki.sqlite.execute("SELECT COUNT(rowid) FROM Showings")
    if len(dbCount['data'])>0:
        beginCount = dbCount['data'][0][0]
    scraperwiki.sqlite.save(unique_keys=["Started"], data={"Started":today, "BeginCount":beginCount}, table_name= "Runs")


    #  SCRAPE WEBPAGES
    cinemaArray = scraperwiki.sqlite.execute("select Id, Parser, Name from Cinemas")
    index = 0
    for dataCinema in cinemaArray.values()[1]:
        index += 1
        #if index<40:
        #    continue
        print "Getting showimes from "+str(dataCinema[2]) + " (" + str(100*(index-1)/len(cinemaArray.values()[1])) + "% done)"
        cinemaShowings = eval(dataCinema[1])
        print "Found " + str(len(cinemaShowings)) + " showings.  Updating database..."
        
        #  You can also list a list of dicts in the save for greater speed
        #data = [ {"a":x*x}  for x in range(99) ]
        #scraperwiki.sqlite.save(["a"], data)
        
        for s in cinemaShowings:
            if index!=40 and index!=41:
                s['CinemaId'] = dataCinema[0]
            scraperwiki.sqlite.save(unique_keys=["CinemaId", "MovieId", "Time"], data=s, table_name= "Showings")

    #  ADD TO SCRAPER LOG
    endCount = 0
    dbCount = scraperwiki.sqlite.execute("SELECT COUNT(rowid) FROM Showings")
    if len(dbCount['data'])>0:
        endCount = dbCount['data'][0][0]
    scraperwiki.sqlite.save(unique_keys=["Started"], data={"Started":today, "BeginCount":beginCount, "Finished":datetime.datetime.now(), "EndCount":endCount}, table_name= "Runs")

    return



#  CREATE CINEMA TABLE
dataCinemas = [
    { "Id": 0, "Name": "AMC Pacific Place", "MTR": "Admiralty", "Address": "Level 1, Pacific Place, 88 Queensway Road, Hong Kong Island", "Latitude": 22.277692, "Longitude": 114.165644, "Parser": "AMC_Parser(16)" },
    { "Id": 1, "Name": "AMC Festival Walk", "MTR": "Kowloon Tong", "Address": "Level U/G, Festival Walk, 80 Tat Chee Avenue, Kowloon Tong, Kowloon", "Latitude": 22.33776, "Longitude": 114.17390, "Parser": "AMC_Parser(15)" },
    { "Id": 2, "Name": "Palace ifc", "MTR": "Hong Kong", "Address": "Podium L1, IFC Mall, 8 Finance Street, Central, Hong Kong Island", "Latitude": 22.28586, "Longitude": 114.15860, "Parser": "Broadway_Parser(12)" },
    { "Id": 3, "Name": "Broadway Cyberport", "MTR": "None", "Address": "Shop L1 - 3, Level 1, The Arcade, 100 Cyberport Road, Hong Kong", "Latitude": 22.261198, "Longitude": 114.129667, "Parser": "Broadway_Parser(13)" },
    { "Id": 4, "Name": "Broadway Hollywood", "MTR": "Diamond Hill", "Address": "3/F, Plaza Hollywood, 3 Lung Poon Street, Diamond Hill, Kowloon", "Latitude": 22.34096, "Longitude": 114.20163, "Parser": "Broadway_Parser(18)" },
    { "Id": 5, "Name": "Broadway The One", "MTR": "Tsim Sha Tsui", "Address": "6-11/F, The ONE, No. 100 Nathan Road, Tsim Sha Tsui, Kowloon", "Latitude": 22.29994, "Longitude": 114.17307, "Parser": "Broadway_Parser(17)" },
    { "Id": 6, "Name": "Broadway Cinematheque", "MTR": "Yau Ma Tei", "Address": "Prosperous Garden, 3 Public Square Street, Yau Ma Tei, Kowloon", "Latitude": 22.31071, "Longitude": 114.16897, "Parser": "Broadway_Parser(10)" },
    { "Id": 7, "Name": "Broadway Mongkok", "MTR": "Mongkok", "Address": "6-12 Sai Yeung Choi Street, Mongkok, Kowloon", "Latitude": 22.31711, "Longitude": 114.17064, "Parser": "Broadway_Parser(5)" },
    { "Id": 8, "Name": "Broadway Olympian City", "MTR": "Olympic", "Address": "UG68, Olympian City 2, 18 Hoi Ting Road, West Kowloon", "Latitude": 22.31522, "Longitude": 114.16208, "Parser": "Broadway_Parser(11)" },
    { "Id": 9, "Name": "Palace apm", "MTR": "Kwun Tong", "Address": "Shop No. L6-1, Level 6, apm, Millennium City 5, 418 Kwun Tong Road, Kowloon", "Latitude": 22.31218, "Longitude": 114.22528, "Parser": "Broadway_Parser(14)" },
    { "Id": 10, "Name": "Broadway Kwai Fong", "MTR": "Kwai Fong", "Address": "L1-L4 Metroplaza, 223 Hing Fong Road, Kwai Fong, New Territories", "Latitude": 22.35748, "Longitude": 114.12625, "Parser": "Broadway_Parser(6)" },
    { "Id": 11, "Name": "Broadway Tseun Wan", "MTR": "Tseun Wan West", "Address": "L1-L3 Tsuen Wan Plaza, 4-30 Tai Pa Street, Tsuen Wan, New Territories", "Latitude": 22.37095, "Longitude": 114.11129, "Parser": "Broadway_Parser(3)" },
    { "Id": 12, "Name": "Broadway Yuen Long", "MTR": "Yuen Long", "Address": "Sun Yuen Long Centre, 8 Long Yat Road, Yuen Long, New Territories", "Latitude": 22.44521, "Longitude": 114.03569, "Parser": "Broadway_Parser(1)" },
    { "Id": 13, "Name": "Broadway Kingswood Ginza", "MTR": "Tin Shui Wai", "Address": "Kingswood Ginza, 18 Tin Yan Road, Tin Shui Wai, Yuen Long, New Territories", "Latitude": 22.4580, "Longitude": 114.0040, "Parser": "Broadway_Parser(9)" },
    { "Id": 14, "Name": "UA Times Square", "MTR": "Causeway Bay", "Address": "Times Square. 1 Matheson St, Causeway Bay, Hong Kong Island", "Latitude": 22.278452, "Longitude": 114.181793, "Parser": "UA_Parser(4)" },
    { "Id": 15, "Name": "UA iSQUARE", "MTR": "Tsim Sha Tsui", "Address": "7/F, iSQUARE, 63 Nathan Road, Tsim Sha Tsui", "Latitude": 22.29668, "Longitude": 114.17191, "Parser": "UA_Parser([18,19])" },
    { "Id": 16, "Name": "UA MegaBox", "MTR": "Kowloon Bay", "Address": "Level 11, MegaBox, Enterprise Square 5, 38 Wang Chiu Road, Kowloon Bay", "Latitude": 22.31964, "Longitude": 114.20827, "Parser": "UA_Parser([14,15])" },
    { "Id": 17, "Name": "UA Cityplaza", "MTR": "Tai Koo", "Address": "5/F Cityplaza, 18 Taikoo Shing Road, Taikoo Shing, Hong Kong Island", "Latitude": 22.28585, "Longitude": 114.21694, "Parser": "UA_Parser([7,11])" },
    { "Id": 19, "Name": "Windsor Cinema", "MTR": "Causeway Bay", "Address": "407, 4/F Windsor House, 311 Gloucester Road, Causeway Bay, Hong Kong Island", "Latitude": 22.28049, "Longitude": 114.18648, "Parser": "UA_Parser(10)" },
    { "Id": 20, "Name": "UA Langham Place", "MTR": "Mongkok", "Address": "L8-11, Langham Place, 8 Argyle Street, Mongkok, Kowloon", "Latitude": 22.317602, "Longitude": 114.168852, "Parser": "UA_Parser(9)" },
    { "Id": 21, "Name": "UA Shatin", "MTR": "Sha Tin", "Address": "Shop L1, LB&UB, Phase 1, New Town Plaza, Shatin", "Latitude": 22.38090, "Longitude": 114.18832
, "Parser": "UA_Parser(1)" },
    { "Id": 22, "Name": "UA tmtplaza", "MTR": "Tuen Mun", "Address": "Shop 3201, 3/F, Tuen Mun Town Plaza Phase 1, Tuen Mun, New Territories", "Latitude": 22.39303, "Longitude": 113.97717, "Parser": "UA_Parser(17)" },
    { "Id": 23, "Name": "UA Citygate", "MTR": "Tung Chung", "Address": "G/F-6/F, Citygate, 20 Tat Tung Road, Tung Chung, Lantau Island", "Latitude": 22.28935, "Longitude": 113.94052, "Parser": "UA_Parser(6)" },
    { "Id": 24, "Name": "Grand Ocean", "MTR": "Tsim Sha Tsui", "Address": "Ocean Centre, 3 Canton Road, Kowloon", "Latitude": 22.295298, "Longitude": 114.169077
, "Parser": "GH_Parser('grand_ocean')" },
    { "Id": 25, "Name": "Golden Gateway", "MTR": "Tsim Sha Tsui", "Address": "G/F The Gateway, 25 Canton Road, Kowloon", "Latitude": 22.299624, "Longitude": 114.168085, "Parser": "GH_Parser('gateway')" },
    { "Id": 26, "Name": "GH Mongkok", "MTR": "Mongkok", "Address": "G/F Grand Century Place, 193 Prince Edward Rd West, Mongkok, Kowloon", "Latitude": 22.323942, "Longitude": 114.172937, "Parser": "GH_Parser('gh_mk')" },
    { "Id": 27, "Name": "GH Tsing Yi", "MTR": "Tsing Yi", "Address": "G/F Maritime Square, 33 Tsing King Road, Tsing Yi, New Territories", "Latitude": 22.359247, "Longitude": 114.108022, "Parser": "GH_Parser('gh_ty')" },
    { "Id": 28, "Name": "GH Citywalk", "MTR": "Tseun Wan", "Address": "Shop 121, Citywalk 2, 18 Yeung Uk Road, Tsuen Wan, New Territories", "Latitude": 22.36768, "Longitude": 114.11549, "Parser": "GH_Parser('gh_citywalk')" },
    { "Id": 29, "Name": "GH Whampoa", "MTR": "Hung Hom", "Address": "Level 2, Whampoa Plaza, Whampoa Garden, 7 Tak On Street, Hunghom, Kowloon", "Latitude": 22.304795, "Longitude": 114.190390, "Parser": "GH_Parser('gh_whampoa')" },
    { "Id": 30, "Name": "President Theatre", "MTR": "Causeway Bay", "Address": "517 Jaffe Road, Causeway Bay, Hong Kong Island", "Latitude": 22.281197, "Longitude": 114.183483, "Parser": "Newport_Parser(1)" },
    { "Id": 31, "Name": "Hyland Theatre", "MTR": "Siu Hei (Tuen Mun)", "Address": "136 Heung Sze Wui Road, Tuen Mun, New Territories", "Latitude": 22.398578, "Longitude": 113.975797, "Parser": "Newport_Parser(2)" },
    { "Id": 32, "Name": "Newport Theatre", "MTR": "Mongkok", "Address": "60 Soy Street, Mongkok, Kowloon", "Latitude": 22.316848, "Longitude": 114.171818, "Parser": "Newport_Parser(3)" },
    { "Id": 33, "Name": "Dynasty Theatre", "MTR": "Mongkok", "Address": "4 Mongkok Road, Kowloon", "Latitude": 22.320589, "Longitude": 114.166703, "Parser": "Newport_Parser(4)" },
    { "Id": 34, "Name": "MCL JP Cinema", "MTR": "Causeway Bay", "Address": "JP Plaza, 22-36 Paterson Street, Causeway Bay, Hong Kong Island", "Latitude": 22.280695, "Longitude": 114.185674, "Parser": "MCL_Parser(1)" },
    { "Id": 35, "Name": "MCL Kornhill", "MTR": "Tai Koo", "Address": "4/F, Kornhill Plaza South, 2 Kornhill Road, Quarry Bay, Hong Kong Island", "Latitude": 22.284185, "Longitude": 114.216375, "Parser": "MCL_Parser(6)" },
    { "Id": 36, "Name": "MCL Metro Cinema", "MTR": "Po Lam", "Address": "G/F, Metro City, Phase 2, 8 Yan King Road, Tseung Kwan O, New Territories", "Latitude": 22.322495, "Longitude": 114.259328, "Parser": "MCL_Parser(2)" },
    { "Id": 37, "Name": "MCL Telford Cinema", "MTR": "Kowloon Bay", "Address": "Telford Gardens, No. 33 Wai Yip Street, Kowloon Bay, Kowloon", "Latitude": 22.322845, "Longitude": 114.212244, "Parser": "MCL_Parser(5)" },
    { "Id": 38, "Name": "4D Extreme Screen", "MTR": "Airport", "Address": "Level 6, Terminal 2, Hong Kong International Airport", "Latitude": 22.31714, "Longitude": 113.93787, "Parser": "MCL_Parser(3)" },
    { "Id": 39, "Name": "The Grand Cinema", "MTR": "Kowloon", "Address": "2/F, Elements, 1 Austin Road West, Kowloon", "Latitude": 22.30374, "Longitude": 114.16242, "Parser": "Grand_Parser()" },
    { "Id": 40, "Name": "Chinachem Golden Plaza", "MTR": "Tsim Sha Tsui East", "Address": "G/F, Chinachem Golden Plaza, 77 Mody Road, TST East, Kowloon", "Latitude": 22.299944, "Longitude": 114.179326, "Parser": "CC_Parser()" },
    { "Id": 41, "Name": "Paris London New York Cinema", "MTR": "Tuen Mun", "Address": "Hong Lai Garden, Ho Pong Street, TMTL 280, Tuen Mun, New Territories", "Latitude": 22.398176, "Longitude": 113.974743, "Parser": "[]" },
    { "Id": 42, "Name": "Ma On Shan Classics", "MTR": "Ma On Shan", "Address": "2/F, Sunshine City Plaza, 18 On Luk Street, Ma On Shan, New Territories", "Latitude": 22.42432, "Longitude": 114.23175, "Parser": "[]" },
    { "Id": 43, "Name": "Cine-Art House", "MTR": "Kowloon Bay", "Address": "G/F Amoy Plaza, Amoy Gardens, 77 Ngau Tau Kok Road, Ngau Tau Kok, Kowloon", "Latitude": 22.32414, "Longitude": 114.21703, "Parser": "CL_Parser(8)" },

]
#for datum in dataCinemas:
#    scraperwiki.sqlite.save(unique_keys=["Id"], data=datum, table_name= "Cinemas")


#  CREATE OTHER TABLES
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS Movies (Title, Key, RTurl, RTjson, IMDBid, Alias, Language)");
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS Showings (CinemaId, MovieId, Language, Is3D, IsIMAX, Time, Screen, Price, BuyURL)");

#  DEFINE PARSER FUNCTIONS

monthInt = { "Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12 }

def checkTitle(toTest):
    if re.search("3D",toTest) <> None:
        is3D = 1
    else:
        is3D = 0
    if re.search("IMAX(?:\sDMR)?",toTest) <> None:
        isIMAX = 1
    else:
        isIMAX = 0
    
    language = ""
    if re.search("Eng",toTest) <> None:
        language = "Eng"
    if re.search("Cantonese",toTest) <> None:
        language = "Can"
    if re.search("Chi",toTest) <> None:
        language = "Can"
    
    # remove "Motion Chair D-BOX"
    title = re.sub(r'(?:\sin\s)?[23]D|IMAX(?:\sDMR)?|(?:Motion\sChair\sD\-BOX)', '', toTest)
    title = re.sub(r'(?:English|Cantonese|Mandarin|Putonghua)(?:\sVer)?(?:sion)?', '', title)
    title = re.sub(r'(?:Eng|Chi)\sVer(?:sion)?', '', title)
    title = re.sub(r'\(Special\sScreening\)', '', title)
    title = re.sub(r'\(.*\)', '', title)
    title = re.sub(r'\s\s+', ' ', title).strip()
    key   = re.sub(r'[^\w\d\s]', '', title).lower()
    key   = re.sub(r's\s|2011?2?|the', '', key, flags=re.IGNORECASE)
    key   = re.sub(r'\s', '', key)
    key   = re.sub(r'iii$', '3', key)
    key   = re.sub(r'ii$', '2', key)
    key   = re.sub(r'i$', '1', key)

    # Check if a movie already exists with this key
    sql = "SELECT rowid, Alias FROM Movies WHERE Key='" + key + "'"
    dbMatch = scraperwiki.sqlite.execute(sql)
    if len(dbMatch['data'])>0:
        # Check if an alias has been set for this key, which points to the correct movie
        if dbMatch['data'][0][1]==-1:
              return {"MovieId":dbMatch['data'][0][0], "Language":language, "Is3D":is3D, "IsIMAX":isIMAX}
        else:
              return {"MovieId":dbMatch['data'][0][1], "Language":language, "Is3D":is3D, "IsIMAX":isIMAX}

    # If no match was found, create a new entry in the Movies table
    RTurl = ""
    RTjson = ""
    
    # Lookup the title in Rotten Tomatoes
    RTxmlURL = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?q=" + urllib.quote(title.encode("utf-8")) + "&apikey=2mcruwycgux87nwgsphw3keu"
    RTresults = json.load(urllib2.urlopen(RTxmlURL))
    if len(RTresults["movies"])>0:
        y = 0
        newest = []
        for r in RTresults["movies"]:
            if r["year"] > y:
                y = r["year"]
                newest = r
        RTurl = newest["links"]["alternate"]
        RTjson = newest["links"]["self"]

    # Lookup the title in IMDB
    IMDBxmlURL = "http://www.imdbapi.com/?i=&t=" + urllib.quote(title.encode("utf-8"))
    IMDBresults = json.load(urllib2.urlopen(IMDBxmlURL))
    if isinstance(IMDBresults, dict):
        if "ID" in IMDBresults:
            IMDBid = IMDBresults["ID"]
        else:
            IMDBid = ""
    else:
        IMDBid = ""
    
    # Alias & Language are always blank when a movie is defined.  These are used to overrule assumptions made by the parser (like that two similar titles are actually different movies)
    scraperwiki.sqlite.save(unique_keys=["Key"], data={"Title":title, "Key":key, "RTurl":RTurl, "RTjson":RTjson, "IMDBid":IMDBid, "Alias":-1, "Language":"", "FirstListed":today}, table_name= "Movies")
    dbMatch = scraperwiki.sqlite.execute(sql)
    return {"MovieId":dbMatch['data'][0][0], "Language":language, "Is3D":is3D, "IsIMAX":isIMAX}




def AMC_Parser( Id ):
    showingArray = []
    url = "http://www.amccinemas.com.hk/cinema_every.php?lang=e&cinema_id="+str(Id)
    root = lxml.html.parse(url).getroot()
    tableKey = 0
    tables = root.cssselect("table.left")
    for table in tables:
        tableKey += 1
        if tableKey == 1:
            continue
        for row in table:
            if row.attrib == {}:
                continue
            cells = row.getchildren()
            if len(cells)<=1:
                continue
            movieTitle = cells[1].cssselect("a")[0].text
            info = checkTitle(movieTitle)
            movieURL = "http://www.amccinemas.com.hk/"+cells[1].cssselect("a")[0].attrib['href']
            select = row.cssselect("select.pink_pulldown")[0]
            values = select.value_options
            valueKey = 0
            for option in select:
                buyURL = "http://www.amccinemas.com.hk/show_seat.php?lang=e&show_id="+values[valueKey]
                valueKey += 1
                if option.text == "-----------------------------------":
                    continue
                r = re.search("(\d+)\/(\d+)\s(\d+):(\d+)(\wM)\s\(\w{3}\)\s([^$]+)\s\$(\d+)", option.text )
                if r == None:
                    continue
                if (r.group(5) == "PM") & (r.group(3) != "12"):
                    PM = 12
                else:
                    PM = 0
                if int(r.group(2))-today.month < -1:
                    y = today.year+1
                else:
                    y = today.year
                time = datetime.datetime(y, int(r.group(2)), int(r.group(1)), int(r.group(3))+PM, int(r.group(4)))
                screen = r.group(6)
                price = int(r.group(7))
                showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )
    return showingArray

def Broadway_Parser( Id ):
    showingArray = []
    url = "http://www3.cinema.com.hk/revamp/html/cinema_every.php?lang=e&cinema_id="+str(Id)
    root = lxml.html.parse(url).getroot()
    rows = root.cssselect("tr.listingbg")
    for row in rows:
        if row.attrib == {}:
            continue
        cells = row.getchildren()
        if len(cells)<=1:
            continue
        movieTitle = cells[0].cssselect("a")[0].text
        info = checkTitle(movieTitle)
        movieURL = "http://www3.cinema.com.hk/revamp/html/"+cells[0].cssselect("a")[0].attrib['href']
        select = row.cssselect("select.movie_listbox")[0]
        values = select.value_options
        valueKey = 0
        for option in select:
            buyURL = "http://www3.cinema.com.hk/revamp/html/show_seat.php?lang=e&show_id="+values[valueKey]
            valueKey += 1
            if option.text == "-----------------------------------":
                continue
            t = option.text
            if (t[11:12] == "P") & (t[6:8] != "12"):
                PM = 12
            else:
                PM = 0
            if int(t[3:5])-today.month < -1:
                y = today.year+1
            else:
                y = today.year
            time = datetime.datetime(y, int(t[3:5]), int(t[0:2]), int(t[6:8])+PM, int(t[9:11]))
            screen = t[21:28]
            price = int(re.split("\$", t)[1])
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )
    return showingArray

def UA_Parser( Id ):
    showingArray = []
    if isinstance(Id, list):
        for i in Id:
            showingArray.extend(UA_Parser(i))
        return showingArray
    url = "http://www.uacinemas.com.hk/eng/cinema/CinemaList?id="+str(Id)
    root = lxml.html.parse(url).getroot()
    tables = root.cssselect("table.cin_mov_bg")
    for table in tables:
        if len(table.cssselect("span")) == 0:
            continue
        if len(table.attrib) == 8:
            continue
        movieTitle = table.cssselect("span.content_white_new")[0].text
        info = checkTitle(movieTitle)
        movieURL = "http://www.uacinemas.com.hk/eng"+table.cssselect("a")[3].attrib['href'][2:999]
        select = table.cssselect("select.ScheduleListCombo")[0]
        values = select.value_options
        valueKey = 0
        for option in select:
            buyURL = "https://www.cityline.com/eng/movie/overviewBo.jsp?eventGroupKey=1&showSelection="+values[valueKey]
            valueKey += 1
            if option.text == "----------------------------------------------------":
                continue
            t = re.split("M[\s\xa0]+|[\s\xa0]+\$",option.text)  #Wed, Nov 23, 11:30  AM   Hitchcock    $175.00
                                                                #Wed, Nov 23, 05:50 PM  Hitchcock    $175.00
            if (t[0][-1] == "P") & (t[0][13:15] != "12"):
                PM = 12
            else:
                PM = 0
            if monthInt[t[0][5:8]]-today.month < -1:
                y = today.year+1
            else:
                y = today.year
            time = datetime.datetime(y, monthInt[t[0][5:8]], int(t[0][9:11]), int(t[0][13:15])+PM, int(t[0][16:18]))
            screen = t[1]
            price = int(t[2][:-3])
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )
    return showingArray

def GH_Parser( Id ):
    showingArray = []
    url = "http://www.goldenharvest.com/booking/cinema.aspx?lang=en&cinema="+str(Id)
    root = lxml.html.parse(url).getroot()
    rows = root.cssselect("div#cinema_movie")[0].cssselect("tr")
    for row in rows:
        if len(row.cssselect("td")) == 1:
            continue
        movieTitle = row.cssselect("td")[0].text.strip()
        info = checkTitle(movieTitle)
        movieURL = ""
        queryParams = re.split("\(\'|\'\,\'", row.cssselect("td")[1].cssselect("script")[0].text )
        queryURL = "http://www.goldenharvest.com/booking/WebService.asmx/GetFilmOptionList?lang=en&film_id="+queryParams[1]+"&cinema="+queryParams[2]
        queryRoot = lxml.html.parse(queryURL).getroot()
        if queryRoot == None:
            continue
        options = re.split("\<option", queryRoot.cssselect("string")[0].text )
        for option in options:
            optArray = re.split('"|\,\s|M\s|\<\/', option)
            if optArray[0] == "<select id=":
                continue
            buyURL = optArray[1]
            if len(optArray) < 6:
                continue
            timeArray = re.split("\/|\s", optArray[3])
            if (timeArray[2][-1] == "P") & (timeArray[2][0:2] != "12"):
                PM = 12
            else:
                PM = 0
            if int(timeArray[1])-today.month < -1:
                y = today.year+1
            else:
                y = today.year
            time = datetime.datetime(y, int(timeArray[1]), int(timeArray[0]), int(timeArray[2][0:2])+PM, int(timeArray[2][3:5]))
            screen = optArray[4].strip()
            price = ""
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )
    return showingArray

def Newport_Parser( Id ):
    showingArray = []
    url = "http://www.theatre.com.hk/cinema.asp?id="+str(Id)
    root = lxml.html.parse(url).getroot()
    table = root.cssselect("table.text14")[0]
    links = table.cssselect("a")
    times = table.cssselect("td.12textabout")  #Time:?Nov 17, Nov 21-23?12:15 14:15 18:15 20:15 22:15 |     ?Nov 18-20?12:15 14:15 18:15 20:15 22:15 24:15 |
    linkKey = 0
    for link in links:
        movieTitle = link.text
        info = checkTitle(movieTitle)
        movieURL = "http://www.theatre.com.hk/"+link.attrib['href']
        slices = re.split(ur'\uff1a\u3010|\u3011|\s+\|\s+\u3010', times[linkKey].text[6:-2] )
        linkKey +=1
        dateStrings = slices[::2]
        timeStrings = slices[1::2]
        dateKey = 0
        for dateString in dateStrings:
            showingArray.extend( DateRange_Parser( dateString, timeStrings[dateKey], info, movieTitle, movieURL, Id ) )
            dateKey += 1

    return showingArray

def DateRange_Parser( dateString, timeString, info, movieTitle, movieURL, Id ):
    showingArray = []
    dateList = []
    buyURL = "http://www.theatre.com.hk/price_eng.htm"
    screen = ""
    price = 0
    dateMatches = re.findall("(\w{3})\s(\d{2})\-?(\d*)", dateString)
    for dM in dateMatches:
        if monthInt[dM[0]]-today.month < -1:
            y = today.year+1
        else:
            y = today.year
        if dM[2] != '':
            for d in range(int(dM[1]),int(dM[2])):
                dateList.append([ y, monthInt[dM[0]], d ])
        else:
            dateList.append([ y, monthInt[dM[0]], int(dM[1]) ])
    timeMatches = re.findall("(\d+)\:(\d{2})", timeString)
    for tM in timeMatches:
        for d in dateList:
            if tM[0] == "24":
                h = 0
            else:
                h = int(tM[0])
            time = datetime.datetime(d[0], d[1], d[2], h, int(tM[1]))
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )

    return showingArray

def MCL_Parser( Id ):
    showingArray = []
    url = "http://www.mclcinema.com/visMovieSelect.aspx?visSearchBy=cin&visLang=2&visCinID=00"+str(Id)
    root = lxml.html.parse(url).getroot()
    selects = root.cssselect("select.Combo")
    titles = root.cssselect("a.content_link")
    titleKey = 0
    for title in titles:
        movieTitle = title.text
        info = checkTitle(movieTitle)
        movieURL = "http://www.mclcinema.com/" + title.attrib['href']
        values = selects[titleKey].value_options
        valueKey = -1
        for option in selects[titleKey]:
            valueKey += 1
            if option.text == "-----------------------------------------------------":
                continue
            realstr = re.split(" ", values[valueKey] )
            buyURL = "http://www.mclcinema.com/viewseat.aspx?txtSessionId=" + realstr[0] + "&cinemacode=" + realstr[1] +"&visLang=2"
            t = option.text  #Thu, 11/24/2011 05:50 PM, House 2
            if (t[22:23] == "P") & (t[16:18] != "12"):
                PM = 12
            else:
                PM = 0
            time = datetime.datetime(int(t[11:15]), int(t[5:7]), int(t[8:10]), int(t[16:18])+PM, int(t[19:21]))
            screen = t[26:33]
            price = 0
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )
        titleKey += 1
    return showingArray

def Grand_Parser():
    Id = 0
    showingArray = []
    url = "http://www.thegrandcinema.com.hk/?visLang=2"
    root = lxml.html.parse(url).getroot()
    rows = root.cssselect("#tblSession tr")
    for row in rows:
        if len(row.cssselect("#TableCell1")) > 0:
            continue
        movieTitle = row.cssselect("a.mcl_moviename_sessionname2")[0].text
        info = checkTitle(movieTitle)
        movieURL = "http://www.thegrandcinema.com.hk/"+row.cssselect("a.mcl_moviename_sessionname2")[0].attrib['href']
        select = row.cssselect("select.mcl_session_list")[0]
        values = select.value_options
        valueKey = 0
        for option in select:
            buyURL = "https://www.thegrandcinema.com.hk/visSelectTickets.aspx?visLang=2&cinemacode=009&txtSessionId="+values[valueKey]
            valueKey += 1
            if option.text == "--------------------------------------":
                continue
            t = re.split("\,\s|M\s", option.text )  #Sun, Dec 4, 04:10PM House 5 - Standard Chartered Starsuite
            d = re.split(" ", t[1] )
            if (t[2][-1] == "P") & (t[2][0:2] != "12"):
                PM = 12
            else:
                PM = 0
            if monthInt[d[0]]-today.month < -1:
                y = today.year+1
            else:
                y = today.year
            time = datetime.datetime(y, monthInt[d[0]], int(d[1]), int(t[2][0:2])+PM, int(t[2][3:5]))
            screen = t[3]
            price = ""
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )

    return showingArray

def CC_Parser():
    cinemaIds = { "Chinachem Golden Plaza Cinema":40, "Paris London New York Milano Cinema":41 }
    showingArray = []
    url = "http://www.cel-cinemas.com/movie_showing.jsp?lang=E"
    #print lxml.html.parse(url)
    root = lxml.html.parse(url).getroot()
    movieForms = root.cssselect("form")
    for mf in movieForms:
        if mf.attrib['name'] != "showingMovie":
            continue
        movieTitle = mf.cssselect("td.movietitle")[0].text.strip()
        info = checkTitle(movieTitle)
        movieKey = mf.cssselect("input")[0].attrib['value']
        movieURL = ""
        root2 = lxml.html.parse("http://www.cel-cinemas.com/movieDetail.jsp?lang=E&movieid="+movieKey).getroot()
        if root2 == None:
            continue
        cinemaForms = root2.cssselect("form")
        for cf in cinemaForms:
            if cf.attrib['name'] != "selectMovie":
                continue
            Id = cinemaIds[ cf.cssselect("td.movietitle")[0].text.strip() ]
            select = cf.cssselect("select.text")[0]
            values = select.value_options
            valueKey = 0
            for option in select:
                buyURL = "http://www.cel-cinemas.com/SelectSeat.jsp?movieKey="+values[valueKey]
                valueKey += 1
                if option.text == "----------------------------------------------------------------------":
                    continue
                if option.text == "- - - Showing Date/Time/House/Price- - -":
                    continue
                t = re.split("\s\s\s+|\s\(|\)\s|\s\$\s|\.", option.text )  #Nov 27 2011   09:50PM  (Sun) House 1 $ 65.0
                d = re.split("\s+", t[0] )
                if (t[1][-2] == "PM") & (t[1][0:2] != "12"):
                    PM = 12
                else:
                    PM = 0
                time = datetime.datetime(int(d[2]), monthInt[d[0]], int(d[1]), int(t[1][0:2])+PM, int(t[1][3:5]))
                screen = t[3]
                price = int(t[4])
                showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )

    return showingArray

def CL_Parser( Id ):
    showingArray = []
    url = "http://www.cityline.com/eng/movie/byCinemaStep2.jsp?venueKey="+str(Id)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    bsSelects = soup('select')
    bsFonts = soup('font')
    fontKey = 2
    for select in bsSelects:
        movieTitle = bsFonts[fontKey].text
        info = checkTitle(movieTitle)
        movieURL = ""
        fontKey += 1
        values = select.value_options
        valueKey = 0
        for option in select:
            buyURL = url
            if str(option) == '<option value="0">----------------------------------------------------</option>':
                    continue
            r = re.search("(\w{3})\s(\d+),\s(\d+):(\d+)\s(\wM)(?:&nbsp;)+([^&]+)(?:&nbsp;)+\$(\d+)", str(option) )
            if r == None:
                continue
            if (r.group(4) == "PM") & (r.group(2) != "12"):
                PM = 12
            else:
                PM = 0
            if monthInt[r.group(1)]-today.month < -1:
                y = today.year+1
            else:
                y = today.year
            time = datetime.datetime(y, monthInt[r.group(1)], int(r.group(2)), int(r.group(3))+PM, int(r.group(4)))
            screen = r.group(6)
            price = int(r.group(7))
            showingArray.append( {"CinemaId": Id, "MovieId": info["MovieId"], "Language": info["Language"], "Is3D": info["Is3D"], "IsIMAX": info["IsIMAX"], "Time": time, "Screen": screen, "Price": price, "BuyURL": buyURL} )

    return showingArray

modifyDatabase()
scrapeAllSites()
#print Broadway_Parser(12)