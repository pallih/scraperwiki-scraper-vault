# Halton Borough Council Planning Applications #

import scraperwiki
import mechanize
import re
from scraperwiki import datastore

# Source
url = "http://www.halton.gov.uk/planningapps/index.asp"

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)

# Select the form
# FIXME: This is fragile (already broken once, when search forms got added to the header), but this is the minimal change required to make it work.
br.select_form(nr=3)
# Select by constituency (Aberavon for now)
br["DropAppealStatus"] = ["%"]
# Submit the form
response = br.submit(name="Action")
#page = response.read()

# FIXME: This range is out of date -- should autodetect end?
for x in range(1, 46):
    print "------------------------------------------------------------------------------------------"
    print "PAGE: ", x
    print "------------------------------------------------------------------------------------------"
    page = response.read()
    # FIXME: Should use an html parsing library.
    records = re.findall("(?si)<TABLE align='center' width='100%' border=1 cellspacing=2 bgcolor=\"#F5F5F5\">", page)
    
    for i in records:
        rows = re.findall('(?si)<tr.*?>(.*?)</tr>', i)        
        num = re.findall('(?si)\s*<td .*>Record: (.*?)</td>\s*', rows[0])
        print "------------------------------------------------------------------------------------------"
        print "------------------------------------------------------------------------------------------"
        print "RECORD: ", num[0]
        print "------------------------------------------------------------------------------------------"

        # ROW 1 - Case No. & Officer Name
        case_no = re.findall('(?si)\s*<td .*>Case No:</td>\s*<td .*>(.*)</td>\s*<td .*>Officer Name:</td>\s*<td .* >\s*.*</td>\s*', rows[1])
        off_name = re.findall('(?si)\s*<td .*>Case No:</td>\s*<td .*>.*</td>\s*<td .*>Officer Name:</td>\s*<td .* >\s*(.*)</td>\s*', rows[1])

        # ROW 2 - Applicants Name & Applicants Address
        app_name = re.findall('(?si)\s*<td .*>Applicants Name:</td>\s*<td .*>(.*)</td>\s*<td .*>Applicants Address:</td>\s*<td .*>.*</td>\s*', rows[2])
        app_address = re.findall('(?si)[^\r*]\s*<td .*>Applicants Name:</td>\s*<td .*>.*</td>\s*<td .*>Applicants Address:</td>\s*<td .*>(.*)</td>\s*', rows[2])
        app_address = re.sub('\r', ' ', app_address[0])

        # ROW 3 - Agents Name & Agents Address
        agent_name = re.findall('(?si)\s*<td .*>Agents Name:</td>\s*<td .*>\s*(.*?)\s*</td>\s*<td .*>Agents Address:</td>\s*<td .*>.*</td>\s*', rows[3])
        agent_address = re.findall('(?si)\s*<td .*>Agents Name:</td>\s*<td .*>.*</td>\s*<td .*>Agents Address:</td>\s*<td .*>\s*(.*?)\s*</td>\s*', rows[3])
        agent_name = re.sub('&lt;|&gt;', '', agent_name[0])
        agent_address = re.sub('\r', ' ', agent_address[0])
        agent_address = re.sub('&lt;|&gt;', '', agent_address)
        
        # ROW 4 - Details of Proposal
        details = re.findall('(?si)\s*<td .*>Details of proposal:</td>\s*<td .*>(.*?)</td>\s*', rows[4])
        details = re.sub('\r', ' ', details[0])

        # ROW 5 - Status & Date Received
        status = re.findall('(?si)\s*<td .*>Status:</td>\s*<td .*>(.*?)</td>\s*<td .*>Date Received</td>\s*<td .*>.*?</td>\s*', rows[5])
        date_received = re.findall('(?si)\s*<td .*>Status:</td>\s*<td .*>.*?</td>\s*<td .*>Date Received</td>\s*<td .*>(.*?)</td>\s*', rows[5])

        # ROW 6 - Date Valid & Comment Between
        date_valid = re.findall('(?si)\s*<td .*>Date Valid:</td>\s*<td .*>(.*?)</td>\s*<td .*>Comment Between</td>\s*<td .*>.*?</td>\s*', rows[6])
        comment = re.findall('(?si)\s*<td .*>Date Valid:</td>\s*<td .*>.*?</td>\s*<td .*>Comment Between</td>\s*<td .*>(.*?)</td>\s*', rows[6])

        # ROW 7 - 8 Week Target Date & Decision Date
        target_date = re.findall('(?si)\s*<td .*>8 Week Target Date</td>\s*<td .*>(.*?)</td>\s*<td .*>Decision Date</td>\s*<td .*>.*?</td>\s*', rows[7])
        decision_date = re.findall('(?si)\s*<td .*>8 Week Target Date</td>\s*<td .*>.*?</td>\s*<td .*>Decision Date</td>\s*<td .*>(.*?)</td>\s*', rows[7])

        # ROW 8 - Application Form & Plans
        application_form = re.findall('(?si)\s*<td .*>Application Form</td>\s*<td .*>\s*<input .*>\s*</td>\s*<td .*>Plans</td>\s*<form METHOD=post ACTION=".(.*?)" id=form2 name=form2 style="">\s*<td .*><input .*></td>\s*</form>\s*</td>\s*', rows[8])
        plans = re.findall('(?si)\s*<td .*>Application Form</td>\s*<td .*>\s*.*?\s*</td>\s*<td .*>Plans</td>\s*<form METHOD=post ACTION=".(.*)" id=form2 name=form2 style="">\s*<td .*><input .*></td>\s*</form>\s*</td>\s*', rows[8])
        if application_form == []:
            application_form = re.findall('(?si)\s*<td .*>Application Form</td>\s*<td .*>\s*(.*?)\s*</td>\s*<td .*>Plans</td>\s*<form METHOD=post ACTION=".*" id=form2 name=form2 style="">\s*<td .*><input .*></td>\s*</form>\s*</td>\s*', rows[8])
            if application_form == []:
                application_form = re.findall('(?si)\s*<td .*>Application Form</td>\s*<td .*>\s*(.*?)\s*</td>\s*<td .*>Plans</td>\s*<td>.*?</td>\s*</td>\s*', rows[8])
        if plans != []:
            a = ["http://www.halton.gov.uk/planningapps", plans[0]]
            plans = ''.join(a)
        else:
            plans = "Plans unavailable"
            
        data = { 'case number' : case_no[0], 'officer name' : off_name[0], 'applicants name' : app_name[0], 'applicants address' : app_address, 'agent name' : agent_name, 'agent address' : agent_address, 'proposal details' : details, 'status' : status[0], 'date received' : date_received[0], 'date valid' : date_valid[0], 'comment between' : comment[0], 'target date' : target_date[0], 'decision date' : decision_date[0], 'plans' : plans, 'application form' : application_form[0] }
        print "DATA: ", data
        datastore.save(unique_keys=['case number'], data=data)
    
    br.select_form('formNext')
    response = br.submit(name='Action')
    
    
