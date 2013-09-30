import scraperwiki
import string
import lxml.html           

for YEAR in range(1957, 2012):
    MONTHS = ["","JAN", "FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    for page_num in range(1,27):
        page='http://waterresources.rajasthan.gov.in/Daily_Rainfall_Data/'+str(YEAR)+'_files/sheet'+string.zfill(page_num, 3)+".htm"
        print page
        html = scraperwiki.scrape(page)
        
        
        root = lxml.html.fromstring(html)
        row_number = 1
        STATION = ''
        DISTRICT = ''
        HEADER_SECTION = False
        RAIN_SECTION = False
        MONTH = 0
        DATE = 0
        print "Staring rows"
        for tr in root.cssselect("tr"):
            tds = tr.cssselect("td")
            column_number = 0
            for td in tds:
                column_number = column_number + 1
                if column_number == 1 and 'STATION' in td.text_content():
                    print "##################### HEADER SECTION #######################################"
                    HEADER_SECTION = True
                    RAIN_SECTION = False
                    STATION = tds[1].text_content()
                    DISTRICT = tds[4].text_content()
                    print DISTRICT+","+STATION+","+str(YEAR)        
                    break
                elif column_number == 1 and 'DATE' in td.text_content():
                    print "##################### RAIN SECTION #######################################"
                    HEADER_SECTION = False
                    RAIN_SECTION = True
                    DATE = 0
                    break
                elif column_number == 1 and  '-' in td.text_content():
                    #break this row      
                    break
                elif column_number == 1:
                    DATE = td.text_content()
                    continue
                elif RAIN_SECTION:
                    MONTH = MONTH+1
                    RAIN_FALL = td.text_content()
                    insert_data={"DISTRICT":DISTRICT, "STATION":STATION,"YEAR":str(YEAR),"MONTH":MONTHS[MONTH],"DATE":str(DATE),"RAIN_FALL":str(RAIN_FALL)}
                    scraperwiki.sqlite.save(unique_keys=["DISTRICT","STATION","YEAR","MONTH","DATE"],data=insert_data )
                    if DATE == '31':                
                        HEADER_SECTION = False
                        RAIN_SECTION = False
                        print "################## END rain Section #######################################"
                    if MONTH == 12:
                        MONTH = 0
        ############### END of One row ###############################
            row_number = row_number + 1
            MONTH = 0

    import scraperwiki
import string
import lxml.html           

for YEAR in range(1957, 2012):
    MONTHS = ["","JAN", "FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    for page_num in range(1,27):
        page='http://waterresources.rajasthan.gov.in/Daily_Rainfall_Data/'+str(YEAR)+'_files/sheet'+string.zfill(page_num, 3)+".htm"
        print page
        html = scraperwiki.scrape(page)
        
        
        root = lxml.html.fromstring(html)
        row_number = 1
        STATION = ''
        DISTRICT = ''
        HEADER_SECTION = False
        RAIN_SECTION = False
        MONTH = 0
        DATE = 0
        print "Staring rows"
        for tr in root.cssselect("tr"):
            tds = tr.cssselect("td")
            column_number = 0
            for td in tds:
                column_number = column_number + 1
                if column_number == 1 and 'STATION' in td.text_content():
                    print "##################### HEADER SECTION #######################################"
                    HEADER_SECTION = True
                    RAIN_SECTION = False
                    STATION = tds[1].text_content()
                    DISTRICT = tds[4].text_content()
                    print DISTRICT+","+STATION+","+str(YEAR)        
                    break
                elif column_number == 1 and 'DATE' in td.text_content():
                    print "##################### RAIN SECTION #######################################"
                    HEADER_SECTION = False
                    RAIN_SECTION = True
                    DATE = 0
                    break
                elif column_number == 1 and  '-' in td.text_content():
                    #break this row      
                    break
                elif column_number == 1:
                    DATE = td.text_content()
                    continue
                elif RAIN_SECTION:
                    MONTH = MONTH+1
                    RAIN_FALL = td.text_content()
                    insert_data={"DISTRICT":DISTRICT, "STATION":STATION,"YEAR":str(YEAR),"MONTH":MONTHS[MONTH],"DATE":str(DATE),"RAIN_FALL":str(RAIN_FALL)}
                    scraperwiki.sqlite.save(unique_keys=["DISTRICT","STATION","YEAR","MONTH","DATE"],data=insert_data )
                    if DATE == '31':                
                        HEADER_SECTION = False
                        RAIN_SECTION = False
                        print "################## END rain Section #######################################"
                    if MONTH == 12:
                        MONTH = 0
        ############### END of One row ###############################
            row_number = row_number + 1
            MONTH = 0

    