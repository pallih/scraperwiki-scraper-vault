import scraperwiki
from BeautifulSoup import BeautifulSoup
import re


z = ""

# retrieve a page
"""
base = "http://www.bocaagency.com"
starting_url = base + '/Default.asp'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
tds = soup.findAll('a') 
x = []
for td in tds:
    if td:
        link = td['href']
        if link and link.find("City_") > -1 and link.find("?city=") > -1:
            link = base + "/" + link
            x.append( "'" + link + "'" )
print x
"""

urls = ['http://www.bocaagency.com/City_Aventura.asp?city=AVENTUR', 'http://www.bocaagency.com/City_BalHarbour.asp?city=BALHARBR', 'http://www.bocaagency.com/City_BayHarborIslands.asp?city=BAYHARIS', 'http://www.bocaagency.com/City_BiscayneGardens.asp?city=BISGRDNS', 'http://www.bocaagency.com/City_BiscaynePark.asp?city=BISCPARK', 'http://www.bocaagency.com/City_CoconutGrove.asp?city=COCOGROV', 'http://www.bocaagency.com/City_CoralGables.asp?city=CORALGBL', 'http://www.bocaagency.com/City_Doral.asp?city=DORAL', 'http://www.bocaagency.com/City_EasternShores.asp?city=EASTERNS', 'http://www.bocaagency.com/City_ElPortal.asp?city=ELPORTAL', 'http://www.bocaagency.com/City_FisherIsland.asp?city=FISHISLD', 'http://www.bocaagency.com/City_FloridaCity.asp?city=FLACITY', 'http://www.bocaagency.com/City_GoldenBeach.asp?city=GOLDNBCH', 'http://www.bocaagency.com/City_Hialeah.asp?city=HIALEAH', 'http://www.bocaagency.com/City_HialeahGardens.asp?city=HIALGRDN', 'http://www.bocaagency.com/City_Homestead.asp?city=HOMESTED', 'http://www.bocaagency.com/City_Kendall.asp?city=KENDALL', 'http://www.bocaagency.com/City_KeyBiscayne.asp?city=KEYBISCY', 'http://www.bocaagency.com/City_Miami.asp?city=MIAMI', 'http://www.bocaagency.com/City_MiamiBeach.asp?city=MIAMIBCH', 'http://www.bocaagency.com/City_MiamiGardens.asp?city=MIAMIGAR', 'http://www.bocaagency.com/City_MiamiLakes.asp?city=MIAMILKE', 'http://www.bocaagency.com/City_MiamiShores.asp?city=MIAMISHR', 'http://www.bocaagency.com/City_MiamiSprings.asp?city=MIAMISPR', 'http://www.bocaagency.com/City_Naranja.asp?city=NARANJA', 'http://www.bocaagency.com/City_NorthBayVillage.asp?city=NBAYVLGE', 'http://www.bocaagency.com/City_NorthMiamiBeach.asp?city=NMIAMIBC', 'http://www.bocaagency.com/City_NorthMiami.asp?city=NMIAMI', 'http://www.bocaagency.com/City_Opalocka.asp?city=OPALOCKA', 'http://www.bocaagency.com/City_PalmettoBay.asp?city=PALMEBAY', 'http://www.bocaagency.com/City_Perrine.asp?city=PERRINE', 'http://www.bocaagency.com/City_Pinecrest.asp?city=PINECRST', 'http://www.bocaagency.com/City_SouthMiami.asp?city=SMIAMI', 'http://www.bocaagency.com/City_SunnyIsles.asp?city=SUNNYISL', 'http://www.bocaagency.com/City_Surfside.asp?city=SURFSIDE', 'http://www.bocaagency.com/City_DadeCounty.asp?city=DADECNTY', 'http://www.bocaagency.com/City_VirginiaGardens.asp?city=VIRGRDNS', 'http://www.bocaagency.com/City_VirginiaKey.asp?city=VIRGKEY', 'http://www.bocaagency.com/City_WestMiami.asp?city=WMIAMI', 'http://www.bocaagency.com/City_CoconutCreek.asp?city=COCOCRK', 'http://www.bocaagency.com/City_CooperCity.asp?city=COOPERCI', 'http://www.bocaagency.com/City_CoralSprings.asp?city=CORALSPR', 'http://www.bocaagency.com/City_Dania.asp?city=DANIA', 'http://www.bocaagency.com/City_Davie.asp?city=DAVIE', 'http://www.bocaagency.com/City_DeerfieldBeach.asp?city=DEERFLD', 'http://www.bocaagency.com/City_FortLauderdale.asp?city=FORTLAUD', 'http://www.bocaagency.com/City_Hallandale.asp?city=HALLNDLE', 'http://www.bocaagency.com/City_HillsboroBeach.asp?city=HILLSBRO', 'http://www.bocaagency.com/City_Hollywood.asp?city=HOLLYWD', 'http://www.bocaagency.com/City_Lauderdale-By-The-Sea.asp?city=LAUDBSEA', 'http://www.bocaagency.com/City_LauderdaleLakes.asp?city=LAUDLAKE', 'http://www.bocaagency.com/City_Lauderhill.asp?city=LAUDHILL', 'http://www.bocaagency.com/City_LazyLake.asp?city=LAZYLAKE', 'http://www.bocaagency.com/City_LighthousePoint.asp?city=LHPOINT', 'http://www.bocaagency.com/City_Margate.asp?city=MARGATE', 'http://www.bocaagency.com/City_Miramar.asp?city=MIRAMAR', 'http://www.bocaagency.com/City_NorthLauderdale.asp?city=NLAUDER', 'http://www.bocaagency.com/City_OaklandPark.asp?city=OAKPARK', 'http://www.bocaagency.com/City_Parkland.asp?city=PARKLAND', 'http://www.bocaagency.com/City_PembrokePark.asp?city=PEMBPARK', 'http://www.bocaagency.com/City_PembrokePines.asp?city=PEMBPINE', 'http://www.bocaagency.com/City_Plantation.asp?city=PLANTATN', 'http://www.bocaagency.com/City_PompanoBeach.asp?city=POMPANO', 'http://www.bocaagency.com/City_SeaRanches.asp?city=SEARANCH', 'http://www.bocaagency.com/City_SouthWestRanches.asp?city=SWRANCH', 'http://www.bocaagency.com/City_Sunrise.asp?city=SUNRISE', 'http://www.bocaagency.com/City_Tamarac.asp?city=TAMARAC', 'http://www.bocaagency.com/City_BrowardCounty.asp?city=BRWDCNTY', 'http://www.bocaagency.com/City_Weston.asp?city=WESTON', 'http://www.bocaagency.com/City_WiltonManors.asp?city=WILTONMN', 'http://www.bocaagency.com/City_Atlantis.asp?city=ATLANTIS', 'http://www.bocaagency.com/City_BellGlade.asp?city=BELLEGLA', 'http://www.bocaagency.com/City_BocaRaton.asp?city=BOCA', 'http://www.bocaagency.com/City_BoyntonBeach.asp?city=BOYNTON', 'http://www.bocaagency.com/City_DelrayBeach.asp?city=DELRAY', 'http://www.bocaagency.com/City_Haverhill.asp?city=HAVERHIL', 'http://www.bocaagency.com/City_HighlandBeach.asp?city=HIGHLAND', 'http://www.bocaagency.com/City_Hypoluxo.asp?city=HYPOLUXO', 'http://www.bocaagency.com/City_JunoBeach.asp?city=JUNO', 'http://www.bocaagency.com/City_Jupiter.asp?city=JUPITER', 'http://www.bocaagency.com/City_LakePark.asp?city=LAKEPARK', 'http://www.bocaagency.com/City_LakeWorth.asp?city=LAKEWORT', 'http://www.bocaagency.com/City_Lantana.asp?city=LANTANA', 'http://www.bocaagency.com/City_Loxahatchee.asp?city=LOXAHAT', 'http://www.bocaagency.com/City_NorthPalmBeach.asp?city=NPALMBEA', 'http://www.bocaagency.com/City_OceanRidge.asp?city=OCEANRID', 'http://www.bocaagency.com/City_Pahokee.asp?city=PAHOKEE', 'http://www.bocaagency.com/City_PalmBeach.asp?city=PALMBEAC', 'http://www.bocaagency.com/City_PalmBeachGardens.asp?city=PBGARDEN', 'http://www.bocaagency.com/City_PalmSprings.asp?city=PALMSPRG', 'http://www.bocaagency.com/City_PortSaintLucie.asp?city=PTSTLUCE', 'http://www.bocaagency.com/City_RivieraBeach.asp?city=RIVIERA', 'http://www.bocaagency.com/City_RoyalPalmBeach.asp?city=ROYALPB', 'http://www.bocaagency.com/City_SingerIsland.asp?city=SINGRISL', 'http://www.bocaagency.com/City_SouthBay.asp?city=SOBAY', 'http://www.bocaagency.com/City_SouthPalmBeach.asp?city=SPALMBEA', 'http://www.bocaagency.com/City_Tequesta.asp?city=TEQUESTA', 'http://www.bocaagency.com/City_VillagesGolf.asp?city=VLGGOLF', 'http://www.bocaagency.com/City_Wellington.asp?city=WELLINGT', 'http://www.bocaagency.com/City_WestPalmBeach.asp?city=WPALMBEA']




for url in urls:
    html = scraperwiki.scrape(url)
    content = html
    soup = BeautifulSoup(content)
    if html:
        piece = 'IN </span><b class="style12">'
        start = html.find(piece)
        html = html[start:]
        html = html.replace('IN </span><b class="style12">', '')
        location = html[0:]
        end = location.find("</b></TD>")
        location = location[0:end]
        print location
        city = location[ : location.find("(") ]
        county = location.replace( city, "" ).replace("(","").replace(")","")
        links = soup.findAll('a', href=re.compile('http://www.bocaagency.com/MLS/CommunityNameLink.asp'))
        if links:
            for link in links:
                sql = "insert into associations (name, location, city, state) values ('%s', '%s', '%s', 'FL');" % ( link.text, county, city )
                z = z + sql + "\n"
                #print sql
        
print zimport scraperwiki
from BeautifulSoup import BeautifulSoup
import re


z = ""

# retrieve a page
"""
base = "http://www.bocaagency.com"
starting_url = base + '/Default.asp'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
tds = soup.findAll('a') 
x = []
for td in tds:
    if td:
        link = td['href']
        if link and link.find("City_") > -1 and link.find("?city=") > -1:
            link = base + "/" + link
            x.append( "'" + link + "'" )
print x
"""

urls = ['http://www.bocaagency.com/City_Aventura.asp?city=AVENTUR', 'http://www.bocaagency.com/City_BalHarbour.asp?city=BALHARBR', 'http://www.bocaagency.com/City_BayHarborIslands.asp?city=BAYHARIS', 'http://www.bocaagency.com/City_BiscayneGardens.asp?city=BISGRDNS', 'http://www.bocaagency.com/City_BiscaynePark.asp?city=BISCPARK', 'http://www.bocaagency.com/City_CoconutGrove.asp?city=COCOGROV', 'http://www.bocaagency.com/City_CoralGables.asp?city=CORALGBL', 'http://www.bocaagency.com/City_Doral.asp?city=DORAL', 'http://www.bocaagency.com/City_EasternShores.asp?city=EASTERNS', 'http://www.bocaagency.com/City_ElPortal.asp?city=ELPORTAL', 'http://www.bocaagency.com/City_FisherIsland.asp?city=FISHISLD', 'http://www.bocaagency.com/City_FloridaCity.asp?city=FLACITY', 'http://www.bocaagency.com/City_GoldenBeach.asp?city=GOLDNBCH', 'http://www.bocaagency.com/City_Hialeah.asp?city=HIALEAH', 'http://www.bocaagency.com/City_HialeahGardens.asp?city=HIALGRDN', 'http://www.bocaagency.com/City_Homestead.asp?city=HOMESTED', 'http://www.bocaagency.com/City_Kendall.asp?city=KENDALL', 'http://www.bocaagency.com/City_KeyBiscayne.asp?city=KEYBISCY', 'http://www.bocaagency.com/City_Miami.asp?city=MIAMI', 'http://www.bocaagency.com/City_MiamiBeach.asp?city=MIAMIBCH', 'http://www.bocaagency.com/City_MiamiGardens.asp?city=MIAMIGAR', 'http://www.bocaagency.com/City_MiamiLakes.asp?city=MIAMILKE', 'http://www.bocaagency.com/City_MiamiShores.asp?city=MIAMISHR', 'http://www.bocaagency.com/City_MiamiSprings.asp?city=MIAMISPR', 'http://www.bocaagency.com/City_Naranja.asp?city=NARANJA', 'http://www.bocaagency.com/City_NorthBayVillage.asp?city=NBAYVLGE', 'http://www.bocaagency.com/City_NorthMiamiBeach.asp?city=NMIAMIBC', 'http://www.bocaagency.com/City_NorthMiami.asp?city=NMIAMI', 'http://www.bocaagency.com/City_Opalocka.asp?city=OPALOCKA', 'http://www.bocaagency.com/City_PalmettoBay.asp?city=PALMEBAY', 'http://www.bocaagency.com/City_Perrine.asp?city=PERRINE', 'http://www.bocaagency.com/City_Pinecrest.asp?city=PINECRST', 'http://www.bocaagency.com/City_SouthMiami.asp?city=SMIAMI', 'http://www.bocaagency.com/City_SunnyIsles.asp?city=SUNNYISL', 'http://www.bocaagency.com/City_Surfside.asp?city=SURFSIDE', 'http://www.bocaagency.com/City_DadeCounty.asp?city=DADECNTY', 'http://www.bocaagency.com/City_VirginiaGardens.asp?city=VIRGRDNS', 'http://www.bocaagency.com/City_VirginiaKey.asp?city=VIRGKEY', 'http://www.bocaagency.com/City_WestMiami.asp?city=WMIAMI', 'http://www.bocaagency.com/City_CoconutCreek.asp?city=COCOCRK', 'http://www.bocaagency.com/City_CooperCity.asp?city=COOPERCI', 'http://www.bocaagency.com/City_CoralSprings.asp?city=CORALSPR', 'http://www.bocaagency.com/City_Dania.asp?city=DANIA', 'http://www.bocaagency.com/City_Davie.asp?city=DAVIE', 'http://www.bocaagency.com/City_DeerfieldBeach.asp?city=DEERFLD', 'http://www.bocaagency.com/City_FortLauderdale.asp?city=FORTLAUD', 'http://www.bocaagency.com/City_Hallandale.asp?city=HALLNDLE', 'http://www.bocaagency.com/City_HillsboroBeach.asp?city=HILLSBRO', 'http://www.bocaagency.com/City_Hollywood.asp?city=HOLLYWD', 'http://www.bocaagency.com/City_Lauderdale-By-The-Sea.asp?city=LAUDBSEA', 'http://www.bocaagency.com/City_LauderdaleLakes.asp?city=LAUDLAKE', 'http://www.bocaagency.com/City_Lauderhill.asp?city=LAUDHILL', 'http://www.bocaagency.com/City_LazyLake.asp?city=LAZYLAKE', 'http://www.bocaagency.com/City_LighthousePoint.asp?city=LHPOINT', 'http://www.bocaagency.com/City_Margate.asp?city=MARGATE', 'http://www.bocaagency.com/City_Miramar.asp?city=MIRAMAR', 'http://www.bocaagency.com/City_NorthLauderdale.asp?city=NLAUDER', 'http://www.bocaagency.com/City_OaklandPark.asp?city=OAKPARK', 'http://www.bocaagency.com/City_Parkland.asp?city=PARKLAND', 'http://www.bocaagency.com/City_PembrokePark.asp?city=PEMBPARK', 'http://www.bocaagency.com/City_PembrokePines.asp?city=PEMBPINE', 'http://www.bocaagency.com/City_Plantation.asp?city=PLANTATN', 'http://www.bocaagency.com/City_PompanoBeach.asp?city=POMPANO', 'http://www.bocaagency.com/City_SeaRanches.asp?city=SEARANCH', 'http://www.bocaagency.com/City_SouthWestRanches.asp?city=SWRANCH', 'http://www.bocaagency.com/City_Sunrise.asp?city=SUNRISE', 'http://www.bocaagency.com/City_Tamarac.asp?city=TAMARAC', 'http://www.bocaagency.com/City_BrowardCounty.asp?city=BRWDCNTY', 'http://www.bocaagency.com/City_Weston.asp?city=WESTON', 'http://www.bocaagency.com/City_WiltonManors.asp?city=WILTONMN', 'http://www.bocaagency.com/City_Atlantis.asp?city=ATLANTIS', 'http://www.bocaagency.com/City_BellGlade.asp?city=BELLEGLA', 'http://www.bocaagency.com/City_BocaRaton.asp?city=BOCA', 'http://www.bocaagency.com/City_BoyntonBeach.asp?city=BOYNTON', 'http://www.bocaagency.com/City_DelrayBeach.asp?city=DELRAY', 'http://www.bocaagency.com/City_Haverhill.asp?city=HAVERHIL', 'http://www.bocaagency.com/City_HighlandBeach.asp?city=HIGHLAND', 'http://www.bocaagency.com/City_Hypoluxo.asp?city=HYPOLUXO', 'http://www.bocaagency.com/City_JunoBeach.asp?city=JUNO', 'http://www.bocaagency.com/City_Jupiter.asp?city=JUPITER', 'http://www.bocaagency.com/City_LakePark.asp?city=LAKEPARK', 'http://www.bocaagency.com/City_LakeWorth.asp?city=LAKEWORT', 'http://www.bocaagency.com/City_Lantana.asp?city=LANTANA', 'http://www.bocaagency.com/City_Loxahatchee.asp?city=LOXAHAT', 'http://www.bocaagency.com/City_NorthPalmBeach.asp?city=NPALMBEA', 'http://www.bocaagency.com/City_OceanRidge.asp?city=OCEANRID', 'http://www.bocaagency.com/City_Pahokee.asp?city=PAHOKEE', 'http://www.bocaagency.com/City_PalmBeach.asp?city=PALMBEAC', 'http://www.bocaagency.com/City_PalmBeachGardens.asp?city=PBGARDEN', 'http://www.bocaagency.com/City_PalmSprings.asp?city=PALMSPRG', 'http://www.bocaagency.com/City_PortSaintLucie.asp?city=PTSTLUCE', 'http://www.bocaagency.com/City_RivieraBeach.asp?city=RIVIERA', 'http://www.bocaagency.com/City_RoyalPalmBeach.asp?city=ROYALPB', 'http://www.bocaagency.com/City_SingerIsland.asp?city=SINGRISL', 'http://www.bocaagency.com/City_SouthBay.asp?city=SOBAY', 'http://www.bocaagency.com/City_SouthPalmBeach.asp?city=SPALMBEA', 'http://www.bocaagency.com/City_Tequesta.asp?city=TEQUESTA', 'http://www.bocaagency.com/City_VillagesGolf.asp?city=VLGGOLF', 'http://www.bocaagency.com/City_Wellington.asp?city=WELLINGT', 'http://www.bocaagency.com/City_WestPalmBeach.asp?city=WPALMBEA']




for url in urls:
    html = scraperwiki.scrape(url)
    content = html
    soup = BeautifulSoup(content)
    if html:
        piece = 'IN </span><b class="style12">'
        start = html.find(piece)
        html = html[start:]
        html = html.replace('IN </span><b class="style12">', '')
        location = html[0:]
        end = location.find("</b></TD>")
        location = location[0:end]
        print location
        city = location[ : location.find("(") ]
        county = location.replace( city, "" ).replace("(","").replace(")","")
        links = soup.findAll('a', href=re.compile('http://www.bocaagency.com/MLS/CommunityNameLink.asp'))
        if links:
            for link in links:
                sql = "insert into associations (name, location, city, state) values ('%s', '%s', '%s', 'FL');" % ( link.text, county, city )
                z = z + sql + "\n"
                #print sql
        
print z