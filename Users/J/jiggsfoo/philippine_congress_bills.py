import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import base64

# retrieve list page
list_url = 'http://www.congress.gov.ph/members/'
list_html = scraperwiki.scrape(list_url)
list_soup = BeautifulSoup(list_html)

def process_bills(website_id):
    profile_url = 'http://www.congress.gov.ph/members/search.php?congress=15&id=' + website_id
    profile_html = scraperwiki.scrape(profile_url)
    profile_soup = BeautifulSoup(profile_html)
    
    for section in profile_soup('div', 'col_hdr_2'):
        # save sponsored/authored measures
        if (section.string.find('House Measures Sponsored/Authored') >= 0):
            # get bill count
            mcount = int(re.findall(r'House Measures Sponsored/Authored \((.*?)\)', section.string)[0])
            print 'House Measures Sponsored/Authored: ' + str(mcount)
            # loop through sponsored bills
            for measure in section.parent('p', 'p_bordered'):
                bill_no = measure('span','p_hdr')[0].string
                if (bill_no != None):
                    bill_title = measure('span','sm_font_dark')[0].string
                    try:
                        bill_history_link = measure('a','hist_link')[0]['onclick'].split("'")[1]
                    except IndexError:
                        bill_history_link = ''
                    try:
                        bill_status = measure('span','sm_font')[0].string.split('Status:')[1].strip()
                    except IndexError:
                        bill_status = ''
                    # prepare data
                    data = {
                        "website_id":website_id,
                        "bill_no":bill_no,
                        "title":bill_title,
                        "history_link":bill_history_link,
                        "status":bill_status,
                        "type":"sponsored/authored"
                    }
                    # save to database
                    scraperwiki.sqlite.save(unique_keys=["website_id","bill_no"], data=data, table_name="congbills")
            
        # save co-authored measures
        elif (section.string.find('House Measures Co-Authored') >= 0):
            # get bill count
            mcount = int(re.findall(r'House Measures Co-Authored \((.*?)\)', section.string)[0])
            print 'House Measures Co-Authored: ' + str(mcount)
            # loop through sponsored bills
            for measure in section.parent('p', 'p_bordered'):
                bill_no = measure('span','p_hdr')[0].string
                if (bill_no != None):
                    bill_title = measure('span','sm_font_dark')[0].string
                    try:
                        bill_history_link = measure('a','hist_link')[0]['onclick'].split("'")[1]
                    except IndexError:
                        bill_history_link = ''
                    try:
                        bill_status = measure('span','sm_font')[0].string.split('Status:')[1].strip()
                    except IndexError:
                        bill_status = ''
                    # prepare data
                    data = {
                        "website_id":website_id,
                        "bill_no":bill_no,
                        "title":bill_title,
                        "history_link":bill_history_link,
                        "status":bill_status,
                        "type":"co-authored"
                    }
                    # save to database
                    scraperwiki.sqlite.save(unique_keys=["website_id","bill_no"], data=data, table_name="congbills")


for alist in list_soup('ul', id="nostylelist"):
    for item in alist('li'):
        website_id = item.a['href'].split('id=')[1]
        process_bills(website_id)

