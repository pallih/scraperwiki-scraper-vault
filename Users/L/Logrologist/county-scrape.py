import scraperwiki
import lxml.html
import re

def record_validator(record):
    active_check = re.search('\s\(active\s', record, re.I|re.S|re.M)
    emeritus = re.search('\s\(emeritus\)', record, re.I|re.S|re.M)
    
    if active_check or emeritus:
        return True
    else:
        return False
row_count = 40710
max_record = 90001
record_id = 85366   #(START HERE NEXT TIME)
while record_id < max_record:
    # base url to me ammended with each record to scrape.
    base_url = "http://www.michbar.org/memberdirectory/detail.cfm?PID="
    # assembled URL for each record page.
    url = base_url + str(record_id)
    
    html = scraperwiki.scrape(url)

    root = lxml.html.fromstring(html)
    # print root.text_content()

       # mark the record being viewed currently:
    # print '\n\n'
    print record_id

    # Using 'try' to avoid hard break if web not found.
    try:
        non_record_check = root.cssselect("p.headerBLUE")[0]  
        print non_record_check.text_content()

        if non_record_check:
            # time.sleep(1)
            record_id+=1
            continue
    except:
        # locate all the 'table' elements on the page, find the table we want.
        
        name_bar = root.cssselect("td.clsMemberFinderHeader")[0]
        print name_bar.text_content()
        if name_bar:
            if record_validator(name_bar.text_content()) == False:
                print "This person is either dead, suspended, inactive, or they've had their license revoked."
                record_id+=1
                # time.sleep(1)
                continue

        email_check = re.search('e-Mail:\s([A-Za-z0-9-.]{1,}@.*?[.][a-z]{3})', root.text_content(), re.I|re.S|re.M)
        if email_check:
            print email_check.group(1)
            email = email_check.group(1)
        else:
            print 'No email provided.'
            email = 'None provided.'
    
        scraperwiki.sqlite.save(unique_keys=["id"], data={"id": row_count, "email": email })
        row_count+=1

    record_id+=1import scraperwiki
import lxml.html
import re

def record_validator(record):
    active_check = re.search('\s\(active\s', record, re.I|re.S|re.M)
    emeritus = re.search('\s\(emeritus\)', record, re.I|re.S|re.M)
    
    if active_check or emeritus:
        return True
    else:
        return False
row_count = 40710
max_record = 90001
record_id = 85366   #(START HERE NEXT TIME)
while record_id < max_record:
    # base url to me ammended with each record to scrape.
    base_url = "http://www.michbar.org/memberdirectory/detail.cfm?PID="
    # assembled URL for each record page.
    url = base_url + str(record_id)
    
    html = scraperwiki.scrape(url)

    root = lxml.html.fromstring(html)
    # print root.text_content()

       # mark the record being viewed currently:
    # print '\n\n'
    print record_id

    # Using 'try' to avoid hard break if web not found.
    try:
        non_record_check = root.cssselect("p.headerBLUE")[0]  
        print non_record_check.text_content()

        if non_record_check:
            # time.sleep(1)
            record_id+=1
            continue
    except:
        # locate all the 'table' elements on the page, find the table we want.
        
        name_bar = root.cssselect("td.clsMemberFinderHeader")[0]
        print name_bar.text_content()
        if name_bar:
            if record_validator(name_bar.text_content()) == False:
                print "This person is either dead, suspended, inactive, or they've had their license revoked."
                record_id+=1
                # time.sleep(1)
                continue

        email_check = re.search('e-Mail:\s([A-Za-z0-9-.]{1,}@.*?[.][a-z]{3})', root.text_content(), re.I|re.S|re.M)
        if email_check:
            print email_check.group(1)
            email = email_check.group(1)
        else:
            print 'No email provided.'
            email = 'None provided.'
    
        scraperwiki.sqlite.save(unique_keys=["id"], data={"id": row_count, "email": email })
        row_count+=1

    record_id+=1