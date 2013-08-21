import scraperwiki
import lxml.html
import requests
import re
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
swutils = scraperwiki.utils.swimport("swutils")


# Renaming of columns

#sql = 'CREATE  TABLE `sw_backup` (`status` text, `date_scraped` text, `consultation_start_date` text, `case_officer` text, `associated_application_uid` text, `uid` text, `agent_name` text, `application_type` text, `date_received` text, `ward_name` text, `coordinates` text, `applicant_address` text, `description` text, `target_decision_date` text, `address` text, `agent_address` text, `consultation_end_date` text, `start_date` text, `applicant_name` text, `date_validated` text, `decided_by` text, `decision_date` text, `decision` text, `meeting_date` text, `appeal_date` text, `appeal_decision_date` text)'

#sql = 'INSERT INTO sw_backup (status , date_scraped , consultation_start_date , case_officer , associated_application_uid , uid , agent_name , application_type , date_received , ward_name , coordinates , applicant_address , description , target_decision_date , address , agent_address , consultation_end_date , start_date , applicant_name , date_validated , decided_by , decision_date , decision , meeting_date , appeal_date , appeal_decision_date) SELECT status , date_scraped , consultation_start_date , case_officer , associated_application_uid , uid , agent_name , application_type , date_recieved , ward_name , coordinates , applicant_address , details , target_decision_date , address , agent_address , consultation_end_date , start_date , applicant_name , date_validated , decided_by , decision_date , decision , meeting_date , appeal_date , appeal_decision_date FROM swdata'

#scraperwiki.sqlite.execute(sql)
#scraperwiki.sqlite.commit()

#scraperwiki.sqlite.execute("drop table if exists swdata")

#sql = 'ALTER TABLE sw_backup RENAME TO swdata'
#scraperwiki.sqlite.execute(sql)
#exit()



#*** CONSTANTS ***
DATE_FORMAT = "%d/%m/%Y"
tz = timezone('Europe/London')
rfc3339_date = "%Y-%m-%dT%H:%M:%SZ"
minus_one_week = (date.today() + relativedelta( weeks = -1 )).strftime(DATE_FORMAT)
minus_60_days = (date.today() + relativedelta( days = -60 )).strftime('%Y-%m-%d')
thisday =  date.today()
#minus_month = (datetime.strptime(last_old,DATE_FORMAT) + relativedelta( months = -1 )).strftime(DATE_FORMAT)
today_date = date.today().strftime(DATE_FORMAT)
searchurl = 'http://www2.elmbridge.gov.uk/Planet/ispforms.asp?serviceKey=SysDoc-PlanetApplicationEnquiry'
pages_regex = re.compile("(\d*.) appl[\s\w\W]*Page (\d*.) of (\d*)")
results_xpath = '//tr/td/table/tr'
next_page_xpath = '//input[@alt="Next Page"][@disabled="true"]'
detail_tables_xpath = '//table[@class="table"]'
detail_tables_available_xpath = '//td[@class="label1"]'
initial_fields = {'ACTION':'NEXT','STEP':'Planet_SearchCriteria'}
detail_fields = {'ACTION':'NEXT','STEP':'Planet_SearchResults'}
next_page_fields = {'ACTION':'NEXT','STEP':'Planet_SearchResults','X.searchDirection':'NEXT'}
detail_fields =  {}
headers = swutils.get_user_agent()
d = requests.session(headers=headers)
test_date = '01/01/1998'
#*** - ***



#*** DEFS ***

def test_dt(date_to_test, ref_date, date_format=DATE_FORMAT):
    try:
        test_dt = datetime.strptime(date_to_test, date_format)
        ref_dt = datetime.strptime(ref_date, date_format)
        if test_dt > ref_dt:
            return 1
        elif test_dt < ref_dt:
            return -1
        elif test_dt == ref_dt:
            return 0
        else:
            return None
    except:
        return None

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def get_dt(date_string, date_format=DATE_FORMAT): # taken from scraperwiki.com/scrapers/utility_library/
    try:
        dt = datetime.strptime(date_string, date_format)
        return dt.date()
    except:
        return None

def process_details(results,fields):
    root = lxml.html.fromstring(results)
    tables = root.xpath (detail_tables_xpath)
    available = root.xpath (detail_tables_available_xpath)
    record = {}
    record['uid'] = fields['X.searchCriteria_ApplicationReference']
    record['date_scraped'] = datetime.now(tz).strftime(rfc3339_date)
        
    
    # First table - Application Details
    tds = tables[0].xpath('tr/td') 
    record['address'] = tds[3].text
    record['description'] = tds[4].text
    try:
        record['ward_name'] = tds[6].text
    except:
        pass
    try:
        record['coordinates'] = tds[8].text
        record['easting'] =tds[8].text.split(',')[0]
        record['northing'] =tds[8].text.split(',')[1]
    except:
        pass

    #Second table - Applicant Details
    tds = tables[1].xpath('tr/td') 
    record['applicant_name'] = tds[3].text
    record['agent_name'] = tds[5].text
    record['applicant_address'] = tds[7].text
    record['agent_address'] = tds[9].text
    
    #Third table - Administration Details
    tds = tables[2].xpath('tr/td') 
    record['case_officer'] = tds[3].text
    record['status'] = tds[5].text
    try:
        record['date_validated'] = str(get_dt(str(tds[9].text),DATE_FORMAT))
    except: 
        pass
    try:
        record['target_decision_date'] = str(get_dt(str(tds[13].text),DATE_FORMAT))
    except:
        pass
    
    #Fourth table - Key Dates
    tds = tables[3].xpath('tr/td')
    record['date_received'] = str(get_dt(str(tds[3].text),DATE_FORMAT))
    if not tds[5].text == 'not available':
        record['meeting_date'] = str(get_dt(str(tds[5].text),DATE_FORMAT))
    try:
        if not tds[9].text == 'not available':
            record['decision_date'] = str(get_dt(str(tds[9].text),DATE_FORMAT))
    except:
        pass
    try:
        record['consultation_start_date'] = str(get_dt(str(tds[11].text).strip(),DATE_FORMAT))
        if not tds[13].text == 'not available':
            record['appeal_date'] = str(get_dt(str(tds[13].text),DATE_FORMAT))
        record['consultation_end_date'] = str(get_dt(str(tds[15].text),DATE_FORMAT))
        if not tds[17].text == 'not available':
            record['appeal_decision_date'] = str(get_dt(str(tds[17].text),DATE_FORMAT))
    except:
        pass
    if record['date_received']:
        record['start_date'] = record['date_received']
    else:
        record['start_date'] = record['date_validated']


    #Fifth table  or sixth table - Application details or Department decision

    if available[5].text_content() == 'Planning Application Details':
        tds = tables[4].xpath('tr/td') 
        record['application_type'] = tds[3].text
        try:
            associated_applications_text = tds[5].text_content().strip()
            if len(associated_applications_text) > 9:
                associated_applications = chunks(associated_applications_text,9)
            else:
                associated_applications = associated_applications_text.strip()
            record['associated_application_uid'] = associated_applications
        except:
            pass
    #print record

    if available[5].text_content() == 'Planning Department Decision':
        tds = tables[4].xpath('tr/td')  # Department decision
        record['decision'] = tds[3].text
        record['decided_by'] = tds[5].text

        tds = tables[5].xpath('tr/td')  # Application details
        record['application_type'] = tds[3].text
        try:
            associated_applications_text = tds[5].text_content()
            if len(associated_applications_text) > 9:
                associated_applications = chunks(associated_applications_text,9)
            else:
                associated_applications = associated_applications_text
            record['associated_application_uid'] = associated_applications
        except:
            pass

    scraperwiki.sqlite.save(unique_keys=['uid'], data=record, verbose=0)

def process_result_list(results,startdate,enddate):
    root = lxml.html.fromstring(results)
    resultlist = root.xpath (results_xpath)
    for result in resultlist[:-1]:
        fields =  {'X.searchCriteria_ApplicationReference':str(result[0][0].text)}
        get('detail',fields,startdate,enddate)
    if not root.xpath(next_page_xpath):
        #print 'There is a next page'
        pages = pages_regex.search(results)
        current_page = pages.groups()[1]
        next_page_fields['X.pageNumber']= str(current_page) #first page is zero in the form (not 1)
        get('next',next_page_fields,startdate,enddate)
    else:
        pass

def get(action,fields,startdate,enddate):
    if action == 'start':
        global s 
        s = requests.session(headers=headers)
        # get the cookie
        s.get('http://www2.elmbridge.gov.uk/Planet/ispforms.asp?serviceKey=SysDoc-PlanetApplicationEnquiry')
        #get the search results
        fields['X.searchCriteria_StartDate']= startdate
        fields['X.searchCriteria_EndDate']= enddate 
        r = s.post(searchurl, data = fields, headers = headers)
        results = r.text
        pages = pages_regex.search(results)
        print 'It is now: ', today_date, datetime.now(tz).strftime('%H:%M')
        print "Fetching last week (",startdate, "-", enddate, "). ", pages.groups()[0], " applications in ",pages.groups()[2], " pages."
        process_result_list(results,startdate,enddate)
        print ' -- Done fetching at ', datetime.now(tz).strftime('%H:%M')
    elif action == 'next':
        fields['X.searchCriteria_StartDate']= startdate
        fields['X.searchCriteria_EndDate']= enddate
        r = s.post(searchurl, data = fields, headers = headers)
        results = r.text
        process_result_list(results,startdate,enddate)
    elif action == 'detail':
        fields['ACTION']= 'NEXT'
        fields['STEP'] = 'Planet_SearchResults'
        if not d.cookies: #if it's the first detail request then get a cookie for the session
            d.get('http://www2.elmbridge.gov.uk/Planet/ispforms.asp?serviceKey=SysDoc-PlanetApplicationEnquiry')
        r = d.post(searchurl, data = fields, headers = headers)
        results = r.text
        process_details(results,fields)
    elif action == 'old':
        #global s 
        s = requests.session(headers=headers)
        # get the cookie
        s.get('http://www2.elmbridge.gov.uk/Planet/ispforms.asp?serviceKey=SysDoc-PlanetApplicationEnquiry')
        #get the search results
        fields['X.searchCriteria_StartDate']= startdate
        fields['X.searchCriteria_EndDate']= enddate 
        r = s.post(searchurl, data = fields, headers = headers)
        results = r.text
        pages = pages_regex.search(results)
        print "Fetching 5 days of old applications (",startdate, "-", enddate, "). ", pages.groups()[0], " applications in ",pages.groups()[2], " pages."
        process_result_list(results,startdate,enddate)
        print ' -- Done fetching at ', datetime.now(tz).strftime('%H:%M')
        scraperwiki.sqlite.save_var('last_old', str(startdate)) 

#*** - ***


# First get last week
get('start',initial_fields, minus_one_week, today_date)


# Then find the 50 oldest that have the start_date within the last 60 days and update them.  

sql_expression = '* from "swdata" WHERE "start_date" BETWEEN "%s" AND "%s" ORDER BY "date_scraped" ASC LIMIT 50' % (minus_60_days, thisday, )
sql_registered_count = 'count(*) from "swdata" WHERE "start_date" BETWEEN "%s" AND "%s"' % (minus_60_days, thisday, )
last_60_days = scraperwiki.sqlite.select(sql_registered_count)
to_update = scraperwiki.sqlite.select(sql_expression)

print 'Now updating ',len(to_update), ' applications with start_date within the last 60 days (out of ', last_60_days[0]['count(*)'], ' records matching criteria)'

for uid in to_update:
    fields =  {'X.searchCriteria_ApplicationReference':str(uid['uid'])}
    get('detail',fields,'','')
print ' -- Done updating ',len(to_update), ' applications'

# Next check if we are back to 1998 in our old collection
last_old = scraperwiki.sqlite.get_var('last_old')
if test_dt(last_old, test_date) == 1:
    # We are not: get 30 days back from the latest collection of old applications in 5 days increments
    counter = 0
    while (counter < 6):
        last_old = scraperwiki.sqlite.get_var('last_old')
        minus_five_days = (datetime.strptime(last_old,DATE_FORMAT) + relativedelta( days = -5 )).strftime(DATE_FORMAT)
        get('old',initial_fields, minus_five_days, last_old)
        counter = counter +1 
else:
    print 'Old collection is permanently done!'

print
print '--- Done for today ---'

