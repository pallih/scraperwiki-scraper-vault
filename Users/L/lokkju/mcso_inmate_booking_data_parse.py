import scraperwiki
import urllib2, urllib, urlparse
import re
import datetime
import httplib
import time
import mechanize
import lxml.html
import sys
import traceback

from BeautifulSoup import BeautifulSoup

base_url = "http://www.mcso.us/PAID/"

def UnixTimeOrNone(d):
    try:
        return time.mktime(time.strptime(d, '%m/%d/%Y %I:%M %p'))
    except ValueError:
        return 0
    
def MakeTables():
    bookings_fields = ["booking_id TEXT PRIMARY KEY","last_scrapedate INTEGER","rescrape INTEGER"]
    booking_detail_fields = ["booking_id TEXT PRIMARY KEY","swis_id TEXT","arresting_agency TEXT","arrest_date INTEGER","status TEXT","facility TEXT","projected_release_date INTEGER","release_date INTEGER","release_reason TEXT","booking_date INTEGER"]
    person_fields = ["booking_id TEXT PRIMARY KEY","name TEXT","firstname TEXT","middlename TEXT","lastname TEXT","age INTEGER","gender TEXT","race TEXT","height TEXT","weight TEXT","hair TEXT","eyes TEXT"]
    charge_fields = ["id INTEGER PRIMARY KEY","case_id INTEGER","charge TEXT","status TEXT","bail TEXT"]
    case_fields   = ["id INTEGER PRIMARY KEY","booking_id TEXT","court_case TEXT","da_case TEXT","citation TEXT"]
    
    scraperwiki.sqlite.execute("drop table if exists bookings")
    scraperwiki.sqlite.execute("drop table if exists booking_detail")
    scraperwiki.sqlite.execute("drop table if exists person")
    scraperwiki.sqlite.execute("drop table if exists 'case'")
    scraperwiki.sqlite.execute("drop table if exists charge")

    scraperwiki.sqlite.execute("create table if not exists bookings (%s)" % ",".join(bookings_fields))
    scraperwiki.sqlite.execute("create table if not exists booking_detail (%s)" % ",".join(booking_detail_fields))
    scraperwiki.sqlite.execute("create table if not exists person (%s)" % ",".join(person_fields))
    scraperwiki.sqlite.execute("create table if not exists 'case' (%s)" % ",".join(case_fields))
    scraperwiki.sqlite.execute("create table if not exists charge (%s)" % ",".join(charge_fields))

def ScrapeOldIds():
    f = scraperwiki.scrape("http://pastebin.com/download.php?i=yfNVgM2m")
    ids = f.split("\r\n")
    for id in ids:
        scraperwiki.sqlite.execute("insert or ignore into bookings values (?,?,?)",(id,0,1),verbose=0)
    scraperwiki.sqlite.commit()

def ScrapeRecentChanges():
    print 'getting all changes from last 7 days...'
    for sidx in ["3","2","1",]:
        print 'initializing browser...'
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_debug_redirects(True)
        br.set_debug_responses(True)
        br.set_debug_http(True)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open(base_url,timeout=5)
        print "Getting records for sidx %s" % sidx
        br.select_form(name='aspnetForm')
        searchType = br.form.find_control(type="select")
        searchType.get(sidx).selected = True
        try:
            response2 = br.submit()
        except:
            print "An exception occured getting list of records for idx %s" % sidx
            traceback.print_exc()
            continue
        print 'got %s bookings' % len(list(br.links(url_regex="BookingDetail")))
        for link in list(br.links(url_regex="BookingDetail")):
            try:
                id = link.url.split("ID=")[1]
                scraperwiki.sqlite.execute("insert or ignore into bookings values (?,?,?)",(id,0,1),verbose=0)
            except:
                print "An exception occured getting record for %s" % link.url
                traceback.print_exc()
                continue
    print 'commiting changes...'
    scraperwiki.sqlite.commit()
    print 'all recent changes scraped'

def ScrapeBookings():
    counter = 0
    limit_date = datetime.datetime.today() - datetime.timedelta(hours=4)
    result = scraperwiki.sqlite.select("booking_id from bookings where rescrape=1 AND last_scrapedate < ?",(limit_date.strftime("%s"),),verbose=0)
    print "Processing %s records" % len(result)
    for rdata in result:
        try:
            html = scraperwiki.scrape("%sBookingDetail.aspx?ID=%s" % (base_url,urllib.quote_plus(rdata["booking_id"])))
            UpdateBooking(rdata["booking_id"],html)
            counter = counter + 1
            if(counter % 10 == 0):
                print "Processed %s records" % counter
        except:
            print "An exception occured processing record for %s" % rdata["booking_id"]
            print sys.exc_info()
            continue
    print "Processed %s records" % counter


def UpdateBooking(id,html):
    soup = BeautifulSoup(html)
    
    el_person_name   = soup.find(id="ctl00_MainContent_labelName")
    el_person_age    = soup.find(id="ctl00_MainContent_labelAge")
    el_person_gender = soup.find(id="ctl00_MainContent_labelGender")
    el_person_race   = soup.find(id="ctl00_MainContent_labelRace")
    el_person_height = soup.find(id="ctl00_MainContent_labelHeight")
    el_person_weight = soup.find(id="ctl00_MainContent_labelWeight")
    el_person_hair   = soup.find(id="ctl00_MainContent_labelHair")
    el_person_eyes   = soup.find(id="ctl00_MainContent_labelEyes")
    person_name      = el_person_name.string if el_person_name else ""
    person_age       = el_person_age.string if el_person_age else ""
    person_gender    = el_person_gender.string if el_person_gender else ""
    person_race      = el_person_race.string if el_person_race else ""
    person_height    = el_person_height.string if el_person_height else ""
    person_weight    = el_person_weight.string if el_person_weight else ""
    person_hair      = el_person_hair.string if el_person_hair else ""
    person_eyes      = el_person_eyes.string if el_person_eyes else ""
    (person_lastname,tmp) = person_name.split(", ",1)
    (person_firstname,person_middlename) = tmp.split(" ",1)
    scraperwiki.sqlite.execute("insert or replace into person values (?,?,?,?,?,?,?,?,?,?,?,?)",
        (id,person_name,person_firstname,person_middlename,person_lastname,person_age,person_gender,
         person_race,person_height,person_weight,person_hair,person_eyes),verbose=0)
    el_swis_id                        = soup.find(id="ctl00_MainContent_labelSwisID")
    el_booking_arresting_agency       = soup.find(id="ctl00_MainContent_labelArrestingAgency")
    el_booking_arrest_date            = soup.find(id="ctl00_MainContent_labelArrestDate")
    el_booking_booking_date           = soup.find(id="ctl00_MainContent_labelBookingDate")
    el_booking_status                 = soup.find(id="ctl00_MainContent_labelCurrentStatus")
    el_booking_facility               = soup.find(id="ctl00_MainContent_labelAssignedFac")
    el_booking_projected_release_date = soup.find(id="ctl00_MainContent_labelProjRelDate")
    el_booking_release_date           = soup.find(id="ctl00_MainContent_labelReleaseDate")
    el_booking_release_reason         = soup.find(id="ctl00_MainContent_labelReleaseReason")
    
    booking_swis_id                = el_swis_id.string if el_swis_id else ""
    booking_arresting_agency       = el_booking_arresting_agency.string if el_booking_arresting_agency else ""
    booking_status                 = el_booking_status.string if el_booking_status else ""
    booking_facility               = el_booking_facility.string if el_booking_facility else ""
    booking_release_reason         = el_booking_release_reason.string if el_booking_release_reason else ""
    booking_projected_release_date = UnixTimeOrNone(el_booking_projected_release_date.string) if el_booking_projected_release_date else 0
    booking_arrest_date            = UnixTimeOrNone(el_booking_arrest_date.string) if el_booking_arrest_date else 0
    booking_release_date           = UnixTimeOrNone(el_booking_release_date.string) if el_booking_release_date else 0
    booking_date                   = UnixTimeOrNone(el_booking_booking_date.string) if el_booking_booking_date else 0
    scraperwiki.sqlite.execute("insert or replace into booking_detail values (?,?,?,?,?,?,?,?,?,?)",
        (id,booking_swis_id,booking_arresting_agency,booking_arrest_date,booking_status,booking_facility,
        booking_projected_release_date,booking_release_date,booking_release_reason,booking_date),verbose=0)
    
    # clear old case & charge info
    scraperwiki.sqlite.execute("DELETE FROM charge WHERE case_id IN (SELECT id FROM 'case' WHERE booking_id=?)",(id,),verbose=0)
    scraperwiki.sqlite.execute("DELETE FROM 'case' WHERE booking_id=?",(id,),verbose=0)

    # add case and charge info
    
    el_table_cases = soup.find(id="ctl00_MainContent_CaseDataList")
    if el_table_cases:
        #for each case
        for el_case_tr in el_table_cases.findAll("tr",recursive=False):
            # case information
            case_court = ""
            case_da = ""
            case_citation = ""
            td = el_case_tr.td.table.tr.td
            while td:
                label = td.span
                td = td.findNextSibling("td")
                data = td.span
                if label and data:
                    if "Court" in label.string:
                        case_court = data.string
                    elif "DA" in label.string:
                        case_da = data.string
                    elif "Citation" in label.string:
                        case_citation = data.string
                td = td.findNextSibling("td")
            scraperwiki.sqlite.execute("INSERT into 'case' values(?,?,?,?,?);",(None,id,case_court,case_da,case_citation),verbose=0)
            # FIXME: there has to be a better way to do this!
            case_id = scraperwiki.sqlite.select("last_insert_rowid();",verbose=0)[0]["last_insert_rowid()"]

            #charges
            el_charge_table = el_case_tr.find("table",attrs={"class" : "Grid"})
            tr = el_charge_table.tr
            tr = tr.findNextSibling("tr")
            while tr:
                (el_charge_text,el_charge_bail,el_charge_status) = tr.findAll("td")
                charge_text = el_charge_text.string if el_charge_text else ""
                charge_bail = el_charge_bail.string if el_charge_bail else ""
                charge_status = el_charge_status.string if el_charge_status else ""

                scraperwiki.sqlite.execute("INSERT into charge values(?,?,?,?,?);",(None,case_id,charge_text,charge_status,charge_bail),verbose=0)
                tr = tr.findNextSibling("tr")
                    
    scraperwiki.sqlite.execute("UPDATE bookings SET last_scrapedate=strftime('%s', 'now') WHERE booking_id=?",(id,),verbose=0)
    if booking_status == "Released":
        scraperwiki.sqlite.execute("UPDATE bookings SET rescrape=0 WHERE booking_id=?",(id,),verbose=0)

    scraperwiki.sqlite.commit()

#ScrapeOldIds()    
#MakeTables()
ScrapeRecentChanges()
ScrapeBookings()