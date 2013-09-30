import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'divdata'
    #there's more than one div, so we need to specify the class="Data", represented by the full stop
    divdata = root.cssselect("div.Data")
    for pars in divdata:
        #Create a new empty record
        record = {}
        #Assign the contents of <td> to a new object called 'table_cells'
        lines = pars.cssselect("p")
        spans = pars.cssselect("p span")
        #If there's anything
#TO ADD: AN ELSE TO ADDRESS DATE/URLCODE WHICH ARE 'OUT OF RANGE' ON SOME PAGES        
        if lines:
            #Put the contents of the first <p> into a record in the column 'pubdate'
            record['pubdate'] = spans[0].text
            record['noticecode'] = spans[1].text
            record['registry'] = spans[3].text
            record['company number'] = spans[5].text
            record['company name'] = spans[4].text
            record['nature of business'] = spans[6].text
            record['trade classification'] = spans[7].text
            record['date of appointment'] = spans[8].text
            record['principal trading address'] = spans[15].text
            record['registered office of company'] = spans[11].text
            record['sector'] = spans[14].text
            record['date of appointment'] = spans[16].text
            record['court'] = spans[2].text
#           record['date'] = lines[13].text
#           record['urlcode'] = lines[14].text
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
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes =['60109/notices/1565700', '60109/notices/1564986', '60110/notices/1566352', '60110/notices/1566359', '60110/notices/1566333', '60110/notices/1565940', '60112/notices/1567763', '60112/notices/1566579', '60113/notices/1568812', '60113/notices/1568825', '60113/notices/1568225', '60113/notices/1568226', '60114/notices/1569198', '60114/notices/1569891', '60114/notices/1569904', '60114/notices/1569805', '60114/notices/1569201', '60114/notices/1569830', '60115/notices/1570064', '60115/notices/1570067', '60115/notices/1570804', '60115/notices/1570825', '60116/notices/1572774', '60116/notices/1570941', '60118/notices/1572579', '60118/notices/1573808', '60118/notices/1573809', '60118/notices/1573810', '60118/notices/1574010', '60118/notices/1571719', '60118/notices/1572594', '60118/notices/1573572', '60119/notices/1573321', '60119/notices/1572674', '60121/notices/1575380', '60121/notices/1573756', '60121/notices/1573721', '60122/notices/1575259', '60122/notices/1576342', '60122/notices/1574606', '60124/notices/1575449', '60124/notices/1576493', '60124/notices/1575480', '60124/notices/1575479', '60124/notices/1575995', '60124/notices/1576022', '60124/notices/1576062', '60124/notices/1575701', '60124/notices/1575697', '60124/notices/1575472', '60124/notices/1575482', '60124/notices/1576051', '60124/notices/1575702', '60124/notices/1575698', '60126/notices/1577030', '60126/notices/1576531', '60126/notices/1576995', '60126/notices/1577044', '60126/notices/1576532', '60127/notices/1577803', '60127/notices/1577767', '60127/notices/1577156', '60127/notices/1577383', '60128/notices/1579329', '60128/notices/1579660', '60128/notices/1579489', '60129/notices/1579541', '60129/notices/1579523', '60129/notices/1579336', '60129/notices/1579599', '60129/notices/1579337', '60129/notices/1578797', '60129/notices/1579594', '60130/notices/1582280', '60130/notices/1580054', '60130/notices/1579870', '60130/notices/1580510', '60130/notices/1580524', '60130/notices/1582281', '60130/notices/1579843', '60130/notices/1580491', '60130/notices/1579845', '60130/notices/1581644', '60105/notices/1563127', '60105/notices/1563981', '60105/notices/1564009', '60105/notices/1563941', '60105/notices/1563943', '60108/notices/1564929', '60108/notices/1564811', '60108/notices/1564751', '60108/notices/1564750', '60108/notices/1565103', '60108/notices/1564103', '60109/notices/1565636', '60109/notices/1565639', '60109/notices/1565638', '60109/notices/1565637', '60109/notices/1565635', '60109/notices/1566820', '60109/notices/1565641', '60109/notices/1565640', '60110/notices/1565726', '60110/notices/1566374', '60110/notices/1566899', '60110/notices/1566337', '60112/notices/1567722', '60112/notices/1567754', '60112/notices/1567902', '60112/notices/1567771', '60113/notices/1568778', '60113/notices/1568433', '60113/notices/1570570', '60113/notices/1568829', '60113/notices/1568781', '60114/notices/1568971', '60114/notices/1569801', '60114/notices/1569928', '60115/notices/1570800', '60116/notices/1572907', '60116/notices/1571629', '60116/notices/1571572', '60116/notices/1571698', '60118/notices/1572563', '60118/notices/1573472', '60119/notices/1573325', '60119/notices/1572673', '60119/notices/1574635', '60119/notices/1574918', '60121/notices/1574458', '60121/notices/1574441', '60121/notices/1574425', '60122/notices/1575298', '60122/notices/1576105', '60122/notices/1576106', '60122/notices/1576107', '60122/notices/1576108', '60124/notices/1576011', '60124/notices/1575485', '60124/notices/1577064', '60126/notices/1576231', '60126/notices/1576940', '60127/notices/1577821', '60127/notices/1577820', '60127/notices/1577801', '60129/notices/1580752', '60129/notices/1579551', '60130/notices/1581643', '60130/notices/1580498', '60130/notices/1580544', '60105/notices/1564010', '60108/notices/1564744', '60115/notices/1571550', '60115/notices/1570869', '60130/notices/1580546', '60109/notices/1565630']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)

import scraperwiki

# Blank Python

# typical URL is http://www.london-gazette.co.uk/id/issues/60112/notices/1568529
# list of URLs collected by scraper at https://scraperwiki.com/scrapers/bankruptcies/
# Downloaded as CSV and codes extracted in Google Docs by using =RIGHT(A2, 7)
# Cycle through a list of those codes, created by using the =JOIN formula in Google Docs

#If you want to understand this scraper - start at the bottom where it says 'base_url'

import scraperwiki
#import urlparse
import lxml.html

#Create a function called 'scrape_table' which is called in the function 'scrape_page' below
#The 'scrape_page' function also passed the contents of the page to this function as 'root'
def scrape_table(root):
    #Use cssselect to find the contents of a particular HTML tag, and put it in a new object 'divdata'
    #there's more than one div, so we need to specify the class="Data", represented by the full stop
    divdata = root.cssselect("div.Data")
    for pars in divdata:
        #Create a new empty record
        record = {}
        #Assign the contents of <td> to a new object called 'table_cells'
        lines = pars.cssselect("p")
        spans = pars.cssselect("p span")
        #If there's anything
#TO ADD: AN ELSE TO ADDRESS DATE/URLCODE WHICH ARE 'OUT OF RANGE' ON SOME PAGES        
        if lines:
            #Put the contents of the first <p> into a record in the column 'pubdate'
            record['pubdate'] = spans[0].text
            record['noticecode'] = spans[1].text
            record['registry'] = spans[3].text
            record['company number'] = spans[5].text
            record['company name'] = spans[4].text
            record['nature of business'] = spans[6].text
            record['trade classification'] = spans[7].text
            record['date of appointment'] = spans[8].text
            record['principal trading address'] = spans[15].text
            record['registered office of company'] = spans[11].text
            record['sector'] = spans[14].text
            record['date of appointment'] = spans[16].text
            record['court'] = spans[2].text
#           record['date'] = lines[13].text
#           record['urlcode'] = lines[14].text
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
base_url = 'http://www.london-gazette.co.uk/issues/'

#And these are the numbers which we need to complete that URL to make each individual URL
#This array has been compiled using the =JOIN formula in Google Docs on a column of URL codes
codes =['60109/notices/1565700', '60109/notices/1564986', '60110/notices/1566352', '60110/notices/1566359', '60110/notices/1566333', '60110/notices/1565940', '60112/notices/1567763', '60112/notices/1566579', '60113/notices/1568812', '60113/notices/1568825', '60113/notices/1568225', '60113/notices/1568226', '60114/notices/1569198', '60114/notices/1569891', '60114/notices/1569904', '60114/notices/1569805', '60114/notices/1569201', '60114/notices/1569830', '60115/notices/1570064', '60115/notices/1570067', '60115/notices/1570804', '60115/notices/1570825', '60116/notices/1572774', '60116/notices/1570941', '60118/notices/1572579', '60118/notices/1573808', '60118/notices/1573809', '60118/notices/1573810', '60118/notices/1574010', '60118/notices/1571719', '60118/notices/1572594', '60118/notices/1573572', '60119/notices/1573321', '60119/notices/1572674', '60121/notices/1575380', '60121/notices/1573756', '60121/notices/1573721', '60122/notices/1575259', '60122/notices/1576342', '60122/notices/1574606', '60124/notices/1575449', '60124/notices/1576493', '60124/notices/1575480', '60124/notices/1575479', '60124/notices/1575995', '60124/notices/1576022', '60124/notices/1576062', '60124/notices/1575701', '60124/notices/1575697', '60124/notices/1575472', '60124/notices/1575482', '60124/notices/1576051', '60124/notices/1575702', '60124/notices/1575698', '60126/notices/1577030', '60126/notices/1576531', '60126/notices/1576995', '60126/notices/1577044', '60126/notices/1576532', '60127/notices/1577803', '60127/notices/1577767', '60127/notices/1577156', '60127/notices/1577383', '60128/notices/1579329', '60128/notices/1579660', '60128/notices/1579489', '60129/notices/1579541', '60129/notices/1579523', '60129/notices/1579336', '60129/notices/1579599', '60129/notices/1579337', '60129/notices/1578797', '60129/notices/1579594', '60130/notices/1582280', '60130/notices/1580054', '60130/notices/1579870', '60130/notices/1580510', '60130/notices/1580524', '60130/notices/1582281', '60130/notices/1579843', '60130/notices/1580491', '60130/notices/1579845', '60130/notices/1581644', '60105/notices/1563127', '60105/notices/1563981', '60105/notices/1564009', '60105/notices/1563941', '60105/notices/1563943', '60108/notices/1564929', '60108/notices/1564811', '60108/notices/1564751', '60108/notices/1564750', '60108/notices/1565103', '60108/notices/1564103', '60109/notices/1565636', '60109/notices/1565639', '60109/notices/1565638', '60109/notices/1565637', '60109/notices/1565635', '60109/notices/1566820', '60109/notices/1565641', '60109/notices/1565640', '60110/notices/1565726', '60110/notices/1566374', '60110/notices/1566899', '60110/notices/1566337', '60112/notices/1567722', '60112/notices/1567754', '60112/notices/1567902', '60112/notices/1567771', '60113/notices/1568778', '60113/notices/1568433', '60113/notices/1570570', '60113/notices/1568829', '60113/notices/1568781', '60114/notices/1568971', '60114/notices/1569801', '60114/notices/1569928', '60115/notices/1570800', '60116/notices/1572907', '60116/notices/1571629', '60116/notices/1571572', '60116/notices/1571698', '60118/notices/1572563', '60118/notices/1573472', '60119/notices/1573325', '60119/notices/1572673', '60119/notices/1574635', '60119/notices/1574918', '60121/notices/1574458', '60121/notices/1574441', '60121/notices/1574425', '60122/notices/1575298', '60122/notices/1576105', '60122/notices/1576106', '60122/notices/1576107', '60122/notices/1576108', '60124/notices/1576011', '60124/notices/1575485', '60124/notices/1577064', '60126/notices/1576231', '60126/notices/1576940', '60127/notices/1577821', '60127/notices/1577820', '60127/notices/1577801', '60129/notices/1580752', '60129/notices/1579551', '60130/notices/1581643', '60130/notices/1580498', '60130/notices/1580544', '60105/notices/1564010', '60108/notices/1564744', '60115/notices/1571550', '60115/notices/1570869', '60130/notices/1580546', '60109/notices/1565630']

#go through the schoolIDs array above, and for each ID...
for item in codes:
    #show it in the console
    print item
    #create a URL called 'next_link' which adds that ID to the end of the base_url variable
    next_link = base_url+item
    #pass that new concatenated URL to a function, 'scrape_page', which is scripted above
    scrape_page(next_link)

