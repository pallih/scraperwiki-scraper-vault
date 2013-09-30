import scraperwiki

import scraperwiki

# Helping https://scraperwiki.com/scrapers/gordo
# Currently this scrapes div id="detailtext" in each page
# Needs to be refined so that you're grabbing <b> and <br/> tags within that - or regex?
# Also needs simplifying/renaming of variables/comments etc.

#If you want to understand this scraper - start at the bottom where it says 'base_url' (line 52 or so)

import scraperwiki
#import urlparse
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'rows'
    #there's more than one table, so we need to specify the class="destinations", represented by the full stop
    rows = root.cssselect("div#detailtext")
    for row in rows:
        #Create a new empty record
        record = {}
            #Put the contents of the first <td> into a record in the column 'FSM'
        record['FSM'] = row.text_content()
            #this takes the ID number, which has been named item in the for loop below
        record['ID'] = item
        print record, '------------'
            #Save in the SQLite database, with the ID code to be used as the unique reference
        scraperwiki.sqlite.save(["ID"], record)


#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://marinetraffic.com/ais/shipdetails.aspx?MMSI='
#And these are the numbers which we need to complete that URL to make each individual URL
#This list has been compiled using the =JOIN formula in Google Docs on a column of mmsi numbers
schoolIDs = ['1007885719','1007887074','1007912027','1009894269','1000721789','1006240062','1007899527','1004743621','1006189007','1008353067','518490000','351236000','1000316019','1006127538','1007907509','1000316019','1004136141','1004670822','1005381683','1007901775','1009244213','1000808972','1006200722','1007887600','1009222596','1007873487','1007874940','1007889717','1009264399','1009918532','1006231200','1006235544','1006508813','1007888681','1008064875','518461000','1000090398','518461000','351236000','351236000','1007050514','1007696592','1007696592','253380000','518461000','351236000','1008510256','1009641250','1000088331','1000808972','1000913738','1006271453','1006466474','1007897677','211770000','1008504340','1008528059','1002026459','1005051348','1007434163','1007884629','1008214068','1008519369','1006339031','1002497350','710000358','1001381632','1007892826','992191525','1006343493','1008581520','219368000','1009455141','1009923222','1007457280','1007533761','1003595580','1004823341','1005790212','1006129982','226329000','226330000','253380000','538003797','538003797','538090388','1000085461','1000403963','1002206331','1004145705','1004296923','1004514100','1004568046','1004880112','1004963601','1005376173','1005788604','1005866464','1006342968','1008934942','1009109679','1009553210','1009567061','1009635345','1009952156','1009998942','1010079568','538090388','992191524','1000268180','1000324157','1000660243','1000822661','1001785372','1001800465','1002291313','1004873452','1006898249','1007933987','1009799098','1009994578','240799000','1000729481','1001964806','1002333320','1003129552','1005190530','1009307247','1000033316','1000115732','1000122494','1000135704','1000155292','1000162195','1000233877','1004317992','1004325283','1004325472','1004346913','1004367229','1004456978','1004499444','1004553405','1004555544','1004684485','1004788833','1004859676','1004899838','1004934886','1005023804','1005478702','1005578156','1005619718','1005631894','1005730006','1006042934','1006147121','1006252839','1006602965','1006700452','1007188529','1007341683','1007705209','1007871506','1008213070','1008231968','1008298034','1008539457','1008546915','1009057530','1009068063','1009112746','1009446970','1009746865','1009988862','1010178319','1010181699','226329000','249612000','1000187518','1000225530','1000793375','1000970886','1001259190','1001275181','1001380851','1001731547','1001973547','1002516893','1003593013','1003637848','1004506663','1004553251','1004631672','1005082191','1005568739','1005893835','1005910311','1006027299','1006143216','1006150139','1006150760','1006186198','1006209105','1006362788','1006424782','1006428147','1006452229','1006487417','1006509532','1006552243','1006554445','1006651218','1006761955','1007054974','1007103252','1007116169','1007117221','1007121766','1007194893','1007228244','1007264085','1007335298','1007685452','1007874438','1007896801','1007907013','1007961278','1007978811','1008055375','1008110392','1008110392','1008118417','1008320591','1008366955','1008600562','1008670768','1008805873','1008811282','1008820298','1008922637','1009058200','1009097480','1009127670','1009135627','1009165840','1009372778','1009379921','1009403617','1009457448','1009467086','1009469481','1009689518','1009756091','1009764878','1009770847','1009848790','1009913903','1009921446','1009966297','1006966580','1008200816','1007641886','992191524','992191525','1006351154','219368000','1001424153','1004832546','1008200816','1005376173','1005381982','1005393845','1005652609','1006352626','1006648280','1007871200','1007909549','1009220402'
]

#go through the schoolIDs list above, and for each ID...
for item in schoolIDs:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
import scraperwiki

import scraperwiki

# Helping https://scraperwiki.com/scrapers/gordo
# Currently this scrapes div id="detailtext" in each page
# Needs to be refined so that you're grabbing <b> and <br/> tags within that - or regex?
# Also needs simplifying/renaming of variables/comments etc.

#If you want to understand this scraper - start at the bottom where it says 'base_url' (line 52 or so)

import scraperwiki
#import urlparse
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'rows'
    #there's more than one table, so we need to specify the class="destinations", represented by the full stop
    rows = root.cssselect("div#detailtext")
    for row in rows:
        #Create a new empty record
        record = {}
            #Put the contents of the first <td> into a record in the column 'FSM'
        record['FSM'] = row.text_content()
            #this takes the ID number, which has been named item in the for loop below
        record['ID'] = item
        print record, '------------'
            #Save in the SQLite database, with the ID code to be used as the unique reference
        scraperwiki.sqlite.save(["ID"], record)


#this creates a new function and (re)names whatever parameter is passed to it - i.e. 'next_link' below - as 'url'
def scrape_page(url):
    #now 'url' is scraped with the scraperwiki library imported above, and the contents put into a new object, 'html'
    html = scraperwiki.scrape(url)
    print html
    #now we use the lxml.html function imported above to convert 'html' into a new object, 'root'
    root = lxml.html.fromstring(html)
    #now we call another function on root, which we write - above
    scrape_table(root)

#START HERE: This is the part of the URL which all our pages share
base_url = 'http://marinetraffic.com/ais/shipdetails.aspx?MMSI='
#And these are the numbers which we need to complete that URL to make each individual URL
#This list has been compiled using the =JOIN formula in Google Docs on a column of mmsi numbers
schoolIDs = ['1007885719','1007887074','1007912027','1009894269','1000721789','1006240062','1007899527','1004743621','1006189007','1008353067','518490000','351236000','1000316019','1006127538','1007907509','1000316019','1004136141','1004670822','1005381683','1007901775','1009244213','1000808972','1006200722','1007887600','1009222596','1007873487','1007874940','1007889717','1009264399','1009918532','1006231200','1006235544','1006508813','1007888681','1008064875','518461000','1000090398','518461000','351236000','351236000','1007050514','1007696592','1007696592','253380000','518461000','351236000','1008510256','1009641250','1000088331','1000808972','1000913738','1006271453','1006466474','1007897677','211770000','1008504340','1008528059','1002026459','1005051348','1007434163','1007884629','1008214068','1008519369','1006339031','1002497350','710000358','1001381632','1007892826','992191525','1006343493','1008581520','219368000','1009455141','1009923222','1007457280','1007533761','1003595580','1004823341','1005790212','1006129982','226329000','226330000','253380000','538003797','538003797','538090388','1000085461','1000403963','1002206331','1004145705','1004296923','1004514100','1004568046','1004880112','1004963601','1005376173','1005788604','1005866464','1006342968','1008934942','1009109679','1009553210','1009567061','1009635345','1009952156','1009998942','1010079568','538090388','992191524','1000268180','1000324157','1000660243','1000822661','1001785372','1001800465','1002291313','1004873452','1006898249','1007933987','1009799098','1009994578','240799000','1000729481','1001964806','1002333320','1003129552','1005190530','1009307247','1000033316','1000115732','1000122494','1000135704','1000155292','1000162195','1000233877','1004317992','1004325283','1004325472','1004346913','1004367229','1004456978','1004499444','1004553405','1004555544','1004684485','1004788833','1004859676','1004899838','1004934886','1005023804','1005478702','1005578156','1005619718','1005631894','1005730006','1006042934','1006147121','1006252839','1006602965','1006700452','1007188529','1007341683','1007705209','1007871506','1008213070','1008231968','1008298034','1008539457','1008546915','1009057530','1009068063','1009112746','1009446970','1009746865','1009988862','1010178319','1010181699','226329000','249612000','1000187518','1000225530','1000793375','1000970886','1001259190','1001275181','1001380851','1001731547','1001973547','1002516893','1003593013','1003637848','1004506663','1004553251','1004631672','1005082191','1005568739','1005893835','1005910311','1006027299','1006143216','1006150139','1006150760','1006186198','1006209105','1006362788','1006424782','1006428147','1006452229','1006487417','1006509532','1006552243','1006554445','1006651218','1006761955','1007054974','1007103252','1007116169','1007117221','1007121766','1007194893','1007228244','1007264085','1007335298','1007685452','1007874438','1007896801','1007907013','1007961278','1007978811','1008055375','1008110392','1008110392','1008118417','1008320591','1008366955','1008600562','1008670768','1008805873','1008811282','1008820298','1008922637','1009058200','1009097480','1009127670','1009135627','1009165840','1009372778','1009379921','1009403617','1009457448','1009467086','1009469481','1009689518','1009756091','1009764878','1009770847','1009848790','1009913903','1009921446','1009966297','1006966580','1008200816','1007641886','992191524','992191525','1006351154','219368000','1001424153','1004832546','1008200816','1005376173','1005381982','1005393845','1005652609','1006352626','1006648280','1007871200','1007909549','1009220402'
]

#go through the schoolIDs list above, and for each ID...
for item in schoolIDs:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)
