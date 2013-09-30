import urllib2
import urllib
import cookielib
import re
import scraperwiki
from scrapemark import scrape
from pprint import pprint


#GLOBALS:
base_url = "http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp="
fileid = "653312"
debug_yn = "Y"

def GetPage2 ( fileid ):

#<th colspan="2" class="cgiTableHead2">Alexander Broadcasting Company, Inc. </th>
#<td style="width: 35%" class="cgiTableBody2">Entity ID Number</td> 
#<td class="cgiTableBody1">032 - 246</td> 

    fin = urllib2.urlopen(base_url + fileid)
    text= fin.read()
    fin.close()

    pprint(text)

    pprint( scrape("{* <td>{{ [x] }}</td> *}",html=text))


# ##################################
def GetPage( fileid ):


    fin = urllib2.urlopen(base_url + fileid)
    text= fin.read()
    fin.close()

    #debug:
    print "GetPage: output html: " + text


    # all relevant <th> tags
    th_lists = re.findall('(?si)cgiTableHead2">(.*?)</th>', text)

    # all relevant <td> tags
    td_lists = re.findall('(?si)cgiTableBody1">(.*?)</td>', text)

    #debug:
    for i, b in enumerate(th_lists):
        print i, b


    #debug:
    for j, c in enumerate(td_lists):
        print j, c

    #return 0

    # check to see if its a bad page: - contains "No matches found. Please try a new search"
    badpage = re.search("No matches found", text)

    if badpage:
        debug("badpage: " + str(fileid))
        #SaveCompanyUpsert( str(fileid), "", "", "", "", "", "", "BAD" )
        SaveCompanyUpsert( str(fileid), "", "", "", "", "", "", "", "", "", "", "", "", "", "", "BAD" )

    else:
        #get data & add to record

        #scraperwiki.sqlite.execute("create table company (entity_id , entity_name , entity_type text, principal_addr text, principal_mail_addr text, entity_status text, 
        #dissolved_date text, [dissolved only]
        #place_of_formation text, formation_date text, 
        #qualify_date str(td_lists[7]) [foreign only] td_lists[1] = "Foreign Corporation"
        #reg_agent_name text, reg_office_street_addr text, reg_office_mail_addr text, nature_of_business text, capital_authorised text, capital_paid_in text, scrapedate text, scrapestatus text)")
        # previous name in "transactions" section http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=704527&page=name&file=V
        # merged_date, merged_into http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=032246&page=name&file=M
        # cancelled_date, service_of_formation: http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=602286&page=name&file=P
        #consolidated_date, consolidated_to: http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=752058&page=name&file=C
        #revoked_date http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=884338&page=name&file=R

        if str(td_lists[4]) == "Dissolved":
            #dissolved date will be in td_lists[5]
            SaveCompanyUpsert( str(td_lists[0]), str(th_lists[0]), str(td_lists[1]), str(td_lists[2]), str(td_lists[3]), str(td_lists[4]), str(td_lists[5]), str(td_lists[6]), str(td_lists[7]), str(td_lists[8]), str(td_lists[9]), str(td_lists[10]), str(td_lists[11]), str(td_lists[12]), str(td_lists[13]), "OK" )
        elif str(td_lists[1]) == "Foreign Corporation":
            #qualify_date str will be in td_lists[7]
            # http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=922716
            SaveCompanyUpsert( str(td_lists[0]), str(th_lists[0]), str(td_lists[1]), str(td_lists[2]), str(td_lists[3]), str(td_lists[4]), str(td_lists[5]), str(td_lists[6]), str(td_lists[7]), str(td_lists[8]), str(td_lists[9]), str(td_lists[10]), str(td_lists[11]), str(td_lists[12]), str(td_lists[13]), "OK" )
        else:
            SaveCompanyUpsert( str(td_lists[0]), str(th_lists[0]), str(td_lists[1]), str(td_lists[2]), str(td_lists[3]), str(td_lists[4]), "", str(td_lists[5]), str(td_lists[6]), str(td_lists[7]), str(td_lists[8]), str(td_lists[9]), str(td_lists[10]), str(td_lists[11]), str(td_lists[12]), "OK" )


def debug( txt ):
    if debug_yn == "Y":
        print txt


def SaveCompanyUpsert(entity_id, entity_name, entity_type, principal_addr, principal_mail_addr, entity_status, dissolved_date, place_of_formation, formation_date, reg_agent_name, reg_office_street_addr, reg_office_mail_addr, nature_of_business, capital_authorised, capital_paid_in, scrapestatus):

    scraperwiki.sqlite.execute("INSERT OR IGNORE INTO company (entity_id, entity_name, entity_type, principal_addr, principal_mail_addr, entity_status, dissolved_date, place_of_formation, formation_date, reg_agent_name, reg_office_street_addr, reg_office_mail_addr, nature_of_business, capital_authorised, capital_paid_in, scrapedate, scrapestatus) VALUES ('" + entity_id + "', '" + entity_name + "', '" + entity_type + "', '" + principal_addr + "', '" + principal_mail_addr + "', '" + entity_status + "', '" + dissolved_date + "', '" + place_of_formation + "', '" + formation_date+ "', '" + reg_agent_name + "', '" + reg_office_street_addr + "', '" + reg_office_mail_addr + "', '" + nature_of_business+ "', '" + capital_authorised + "', '" + capital_paid_in + "', current_timestamp, '" + scrapestatus +"')")

    scraperwiki.sqlite.execute("UPDATE company SET entity_name= '"+entity_name+"', entity_type= '"+entity_type+"', principal_addr= '"+principal_addr+"', principal_mail_addr= '"+principal_mail_addr+"', entity_status= '"+entity_status+"', dissolved_date= '"+dissolved_date+"', place_of_formation= '"+place_of_formation+"', formation_date= '"+formation_date+"', reg_agent_name= '"+reg_agent_name+"', reg_office_street_addr= '"+reg_office_street_addr+"', reg_office_mail_addr= '"+reg_office_mail_addr+"', nature_of_business= '"+nature_of_business+"', capital_authorised= '"+capital_authorised+"', capital_paid_in= '"+capital_paid_in+"', scrapedate = current_timestamp, scrapestatus = '"+scrapestatus+"' WHERE entity_id= '"+entity_id+"' AND (entity_name<> '"+entity_name+"' OR entity_type<> '"+entity_type+"' OR principal_addr<> '"+principal_addr+"' OR principal_mail_addr<> '"+principal_mail_addr+"' OR entity_status<> '"+entity_status+"' OR dissolved_date<> '"+dissolved_date+"' OR place_of_formation<> '"+place_of_formation+"' OR formation_date<> '"+formation_date+"' OR reg_agent_name<> '"+reg_agent_name+"' OR reg_office_street_addr<> '"+reg_office_street_addr+"' OR reg_office_mail_addr<> '"+reg_office_mail_addr+"' OR nature_of_business<> 'nature_of_business' OR capital_authorised<> '"+capital_authorised+"' OR capital_paid_in<> '"+capital_paid_in+"')")


    scraperwiki.sqlite.commit()


def MakeTables():
    debug ("MakeTables: start")

    scraperwiki.sqlite.execute("drop table if exists company")
    scraperwiki.sqlite.execute("create table company (entity_id text primary key, entity_name text, entity_type text, principal_addr text, principal_mail_addr text, entity_status text, dissolved_date text, place_of_formation text, formation_date text, reg_agent_name text, reg_office_street_addr text, reg_office_mail_addr text, nature_of_business text, capital_authorised text, capital_paid_in text, scrapedate text, scrapestatus text)")

    #Entity ID Number - format nnn-nnn
    #Entity Type 
    #Principal Address - need to remove <br> tags
    #Principal Mailing Address - need to remove <br> tags
    #Status 
    #Dissolved Date - format M/D/YYYY - only shown if status = "Dissolved"
    #Place of Formation
    #Formation Date- format M/D/YYYY
    #Registered Agent Name
    #Registered Office Street Address
    #Registered Office Mailing Address
    #Nature of Business
    #Capital Authorized
    #Capital Paid In
    
    # all text fields: need to remove <br> tags
    # date fields: convert to DD/MM/YYYY



print "hello"
#MakeTables()

#loop:
#get pages for the good ids
#for l in range(922712,922718):
    #this will also save data
#    GetPage( str(l) )


GetPage2("032246")
#GetPage("000000")




import urllib2
import urllib
import cookielib
import re
import scraperwiki
from scrapemark import scrape
from pprint import pprint


#GLOBALS:
base_url = "http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp="
fileid = "653312"
debug_yn = "Y"

def GetPage2 ( fileid ):

#<th colspan="2" class="cgiTableHead2">Alexander Broadcasting Company, Inc. </th>
#<td style="width: 35%" class="cgiTableBody2">Entity ID Number</td> 
#<td class="cgiTableBody1">032 - 246</td> 

    fin = urllib2.urlopen(base_url + fileid)
    text= fin.read()
    fin.close()

    pprint(text)

    pprint( scrape("{* <td>{{ [x] }}</td> *}",html=text))


# ##################################
def GetPage( fileid ):


    fin = urllib2.urlopen(base_url + fileid)
    text= fin.read()
    fin.close()

    #debug:
    print "GetPage: output html: " + text


    # all relevant <th> tags
    th_lists = re.findall('(?si)cgiTableHead2">(.*?)</th>', text)

    # all relevant <td> tags
    td_lists = re.findall('(?si)cgiTableBody1">(.*?)</td>', text)

    #debug:
    for i, b in enumerate(th_lists):
        print i, b


    #debug:
    for j, c in enumerate(td_lists):
        print j, c

    #return 0

    # check to see if its a bad page: - contains "No matches found. Please try a new search"
    badpage = re.search("No matches found", text)

    if badpage:
        debug("badpage: " + str(fileid))
        #SaveCompanyUpsert( str(fileid), "", "", "", "", "", "", "BAD" )
        SaveCompanyUpsert( str(fileid), "", "", "", "", "", "", "", "", "", "", "", "", "", "", "BAD" )

    else:
        #get data & add to record

        #scraperwiki.sqlite.execute("create table company (entity_id , entity_name , entity_type text, principal_addr text, principal_mail_addr text, entity_status text, 
        #dissolved_date text, [dissolved only]
        #place_of_formation text, formation_date text, 
        #qualify_date str(td_lists[7]) [foreign only] td_lists[1] = "Foreign Corporation"
        #reg_agent_name text, reg_office_street_addr text, reg_office_mail_addr text, nature_of_business text, capital_authorised text, capital_paid_in text, scrapedate text, scrapestatus text)")
        # previous name in "transactions" section http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=704527&page=name&file=V
        # merged_date, merged_into http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=032246&page=name&file=M
        # cancelled_date, service_of_formation: http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=602286&page=name&file=P
        #consolidated_date, consolidated_to: http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=752058&page=name&file=C
        #revoked_date http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=884338&page=name&file=R

        if str(td_lists[4]) == "Dissolved":
            #dissolved date will be in td_lists[5]
            SaveCompanyUpsert( str(td_lists[0]), str(th_lists[0]), str(td_lists[1]), str(td_lists[2]), str(td_lists[3]), str(td_lists[4]), str(td_lists[5]), str(td_lists[6]), str(td_lists[7]), str(td_lists[8]), str(td_lists[9]), str(td_lists[10]), str(td_lists[11]), str(td_lists[12]), str(td_lists[13]), "OK" )
        elif str(td_lists[1]) == "Foreign Corporation":
            #qualify_date str will be in td_lists[7]
            # http://arc-sos.state.al.us/cgi/corpdetail.mbr/detail?corp=922716
            SaveCompanyUpsert( str(td_lists[0]), str(th_lists[0]), str(td_lists[1]), str(td_lists[2]), str(td_lists[3]), str(td_lists[4]), str(td_lists[5]), str(td_lists[6]), str(td_lists[7]), str(td_lists[8]), str(td_lists[9]), str(td_lists[10]), str(td_lists[11]), str(td_lists[12]), str(td_lists[13]), "OK" )
        else:
            SaveCompanyUpsert( str(td_lists[0]), str(th_lists[0]), str(td_lists[1]), str(td_lists[2]), str(td_lists[3]), str(td_lists[4]), "", str(td_lists[5]), str(td_lists[6]), str(td_lists[7]), str(td_lists[8]), str(td_lists[9]), str(td_lists[10]), str(td_lists[11]), str(td_lists[12]), "OK" )


def debug( txt ):
    if debug_yn == "Y":
        print txt


def SaveCompanyUpsert(entity_id, entity_name, entity_type, principal_addr, principal_mail_addr, entity_status, dissolved_date, place_of_formation, formation_date, reg_agent_name, reg_office_street_addr, reg_office_mail_addr, nature_of_business, capital_authorised, capital_paid_in, scrapestatus):

    scraperwiki.sqlite.execute("INSERT OR IGNORE INTO company (entity_id, entity_name, entity_type, principal_addr, principal_mail_addr, entity_status, dissolved_date, place_of_formation, formation_date, reg_agent_name, reg_office_street_addr, reg_office_mail_addr, nature_of_business, capital_authorised, capital_paid_in, scrapedate, scrapestatus) VALUES ('" + entity_id + "', '" + entity_name + "', '" + entity_type + "', '" + principal_addr + "', '" + principal_mail_addr + "', '" + entity_status + "', '" + dissolved_date + "', '" + place_of_formation + "', '" + formation_date+ "', '" + reg_agent_name + "', '" + reg_office_street_addr + "', '" + reg_office_mail_addr + "', '" + nature_of_business+ "', '" + capital_authorised + "', '" + capital_paid_in + "', current_timestamp, '" + scrapestatus +"')")

    scraperwiki.sqlite.execute("UPDATE company SET entity_name= '"+entity_name+"', entity_type= '"+entity_type+"', principal_addr= '"+principal_addr+"', principal_mail_addr= '"+principal_mail_addr+"', entity_status= '"+entity_status+"', dissolved_date= '"+dissolved_date+"', place_of_formation= '"+place_of_formation+"', formation_date= '"+formation_date+"', reg_agent_name= '"+reg_agent_name+"', reg_office_street_addr= '"+reg_office_street_addr+"', reg_office_mail_addr= '"+reg_office_mail_addr+"', nature_of_business= '"+nature_of_business+"', capital_authorised= '"+capital_authorised+"', capital_paid_in= '"+capital_paid_in+"', scrapedate = current_timestamp, scrapestatus = '"+scrapestatus+"' WHERE entity_id= '"+entity_id+"' AND (entity_name<> '"+entity_name+"' OR entity_type<> '"+entity_type+"' OR principal_addr<> '"+principal_addr+"' OR principal_mail_addr<> '"+principal_mail_addr+"' OR entity_status<> '"+entity_status+"' OR dissolved_date<> '"+dissolved_date+"' OR place_of_formation<> '"+place_of_formation+"' OR formation_date<> '"+formation_date+"' OR reg_agent_name<> '"+reg_agent_name+"' OR reg_office_street_addr<> '"+reg_office_street_addr+"' OR reg_office_mail_addr<> '"+reg_office_mail_addr+"' OR nature_of_business<> 'nature_of_business' OR capital_authorised<> '"+capital_authorised+"' OR capital_paid_in<> '"+capital_paid_in+"')")


    scraperwiki.sqlite.commit()


def MakeTables():
    debug ("MakeTables: start")

    scraperwiki.sqlite.execute("drop table if exists company")
    scraperwiki.sqlite.execute("create table company (entity_id text primary key, entity_name text, entity_type text, principal_addr text, principal_mail_addr text, entity_status text, dissolved_date text, place_of_formation text, formation_date text, reg_agent_name text, reg_office_street_addr text, reg_office_mail_addr text, nature_of_business text, capital_authorised text, capital_paid_in text, scrapedate text, scrapestatus text)")

    #Entity ID Number - format nnn-nnn
    #Entity Type 
    #Principal Address - need to remove <br> tags
    #Principal Mailing Address - need to remove <br> tags
    #Status 
    #Dissolved Date - format M/D/YYYY - only shown if status = "Dissolved"
    #Place of Formation
    #Formation Date- format M/D/YYYY
    #Registered Agent Name
    #Registered Office Street Address
    #Registered Office Mailing Address
    #Nature of Business
    #Capital Authorized
    #Capital Paid In
    
    # all text fields: need to remove <br> tags
    # date fields: convert to DD/MM/YYYY



print "hello"
#MakeTables()

#loop:
#get pages for the good ids
#for l in range(922712,922718):
    #this will also save data
#    GetPage( str(l) )


GetPage2("032246")
#GetPage("000000")




