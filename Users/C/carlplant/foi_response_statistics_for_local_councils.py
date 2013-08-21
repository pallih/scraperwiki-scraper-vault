import scraperwiki
import BeautifulSoup
import re
import sys
from scraperwiki import datastore

# FOI request statistics for nhs trusts from WhatDoTheyKnow.com #

# function to extract the request statistics                                      
def extract_dictionary(next_html):
    #print "extract_dictionary"
    nhstrust_statistics = {"total_num_requests":0, "successful":0, "partially_successful":0, "rejected":0,
                                "waiting_response":0, "waiting_classification":0, "waiting_clarification":0,
                                "waiting_response_overdue":0, "waiting_response_very_overdue":0,
                                "not_held":0, "requires_admin":0, "internal_review":0,
                                "user_withdrawn":0, "error_message":0, "gone_postal":0}
    while True:
        #print "next_html = "  + str(next_html)
        # classify each request
        for request_span in next_html.findAll(attrs={'class' : re.compile("^bottomline")}): 
            nhstrust_statistics["total_num_requests"] +=1
            type_of_request = re.split('\W+', request_span['class'])[1]
            type_of_request = re.sub("icon_", "", type_of_request)
            # add it to the dictionary, checking if it exists
            try: 
                nhstrust_statistics[type_of_request] += 1
            except:
                print "Ooops - no " + type_of_request + " entry in dictionary! Stopping scraping..."
                sys.exit(0)
            # print "Number " + str(nhstrust_statistics["total_num_requests"]) + ": " + type_of_request
            
        # once the for loop is finished, check whether there are additional pages for this nhstrust: 
        # look for "next" link and loop again if so
        if next_html.find("a", "next_page") is None:
            return nhstrust_statistics
        #print "next page found"
        next_link = base_url + next_html.find("a", "next_page")['href']
        temp_html = scraperwiki.scrape(next_link)
        next_html = BeautifulSoup.BeautifulSoup(temp_html)

# base URLs and initial scrape
base_url = 'http://www.whatdotheyknow.com'
home_url = base_url + '/body/list/nhstrust'
scraped_html = scraperwiki.scrape(home_url)
list_of_nhstrust = BeautifulSoup.BeautifulSoup(scraped_html)

# extract the link to each nhstrust page, start processing
for each_nhstrust in list_of_nhstrust.findAll("span", "head")[:300]: 
    
    # extract the nhs trust name and page 
    nhstrust_link = each_nhstrust.a
    nhstrust_name = nhstrust_link.string   
    nhstrust_page = base_url + nhstrust_link['href']
    
    # now scrape the nhstrust page
    temp_html = scraperwiki.scrape(nhstrust_page)
    next_html = BeautifulSoup.BeautifulSoup(temp_html)
    nhstrust_statistics = extract_dictionary(next_html)
    
    # before saving data, check the numbers add up, in case we missed any requests
    count = sum(nhstrust_statistics.itervalues())
    num_requests = nhstrust_statistics["total_num_requests"] 
    if count/2 != num_requests:
        print "May have missed requests: count is %s and total_num_requests is %s, stopping scraping" % (count, nhstrust_statistics["total_num_requests"])
        sys.exit(0)
    
    # when all is complete, save to datastore
    data = { 
            'nhstrust name' : nhstrust_name, 
            'nhstrust page' : nhstrust_page, 
            'Total requests' : nhstrust_statistics["total_num_requests"],
            'Successful' : nhstrust_statistics["successful"],
            'Partly successful' : nhstrust_statistics["partially_successful"],
            'Rejected' : nhstrust_statistics["rejected"],
            'Awaiting response' : nhstrust_statistics["waiting_response"],
            'Awaiting classification' : nhstrust_statistics["waiting_classification"],
            'Awaiting clarification' : nhstrust_statistics["waiting_clarification"],
            'Overdue' : nhstrust_statistics["waiting_response_overdue"],
            'Long overdue' : nhstrust_statistics["waiting_response_very_overdue"],
            'Info not held' : nhstrust_statistics["not_held"],
            'Requires admin' : nhstrust_statistics["requires_admin"],
            'Internal review' : nhstrust_statistics["internal_review"],
            'Withdrawn by user' : nhstrust_statistics["user_withdrawn"],
            'Error message' : nhstrust_statistics["error_message"],
            'Handled by post' : nhstrust_statistics["gone_postal"],
     }                 
    
    scraperwiki.sqlite.save(unique_keys=['nhstrust name' ], data=data)
                                #'Total requests', 'Successful', 'Partially successful',
                                #'Rejected', 'Awaiting response', 'Awaiting classification',
                                #'Awaiting clarification', 'Overdue', 'Long overdue',
                                #'Info not held', 'Requires admin', 'Internal review', 
                                #'Withdrawn by user', 'Error message', 'Handled by post'], data=data)


