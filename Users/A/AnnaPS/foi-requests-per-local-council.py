import scraperwiki
import BeautifulSoup
import re
import sys
from scraperwiki import datastore

# FOI request statistics for local councils from WhatDoTheyKnow.com #

# function to extract the request statistics                                      
def extract_dictionary(next_html):
    #print "extract_dictionary"
    council_statistics = {"total_num_requests":0, "successful":0, "partially_successful":0, "rejected":0,
                                "waiting_response":0, "waiting_classification":0, "waiting_clarification":0,
                                "waiting_response_overdue":0, "waiting_response_very_overdue":0,
                                "not_held":0, "requires_admin":0, "internal_review":0,
                                "user_withdrawn":0, "error_message":0, "gone_postal":0}
    while True:
        #print "next_html = "  + str(next_html)
        # classify each request
        for request_span in next_html.findAll(attrs={'class' : re.compile("^bottomline")}): 
            council_statistics["total_num_requests"] +=1
            type_of_request = re.split('\W+', request_span['class'])[1]
            type_of_request = re.sub("icon_", "", type_of_request)
            # add it to the dictionary, checking if it exists
            try: 
                council_statistics[type_of_request] += 1
            except:
                print "Ooops - no " + type_of_request + " entry in dictionary! Stopping scraping..."
                sys.exit(0)
            # print "Number " + str(council_statistics["total_num_requests"]) + ": " + type_of_request
            
        # once the for loop is finished, check whether there are additional pages for this council: 
        # look for "next" link and loop again if so
        if next_html.find("a", "next_page") is None:
            return council_statistics
        #print "next page found"
        next_link = base_url + next_html.find("a", "next_page")['href']
        temp_html = scraperwiki.scrape(next_link)
        next_html = BeautifulSoup.BeautifulSoup(temp_html)

# base URLs and initial scrape
base_url = 'http://www.whatdotheyknow.com'
home_url = base_url + '/body/list/local_council'
scraped_html = scraperwiki.scrape(home_url)
list_of_councils = BeautifulSoup.BeautifulSoup(scraped_html)

# extract the link to each council page, start processing
for each_council in list_of_councils.findAll("span", "head")[:300]: 
    
    # extract the council name and page 
    council_link = each_council.a
    council_name = council_link.string   
    council_page = base_url + council_link['href']
    
    # now scrape the council page
    temp_html = scraperwiki.scrape(council_page)
    next_html = BeautifulSoup.BeautifulSoup(temp_html)
    council_statistics = extract_dictionary(next_html)
    
    # before saving data, check the numbers add up, in case we missed any requests
    count = sum(council_statistics.itervalues())
    num_requests = council_statistics["total_num_requests"] 
    if count/2 != num_requests:
        print "May have missed requests: count is %s and total_num_requests is %s, stopping scraping" % (count, council_statistics["total_num_requests"])
        sys.exit(0)
    
    # when all is complete, save to datastore
    data = { 
            'Council name' : council_name, 
            'Council page' : council_page, 
            'Total requests' : council_statistics["total_num_requests"],
            'Successful' : council_statistics["successful"],
            'Partly successful' : council_statistics["partially_successful"],
            'Rejected' : council_statistics["rejected"],
            'Awaiting response' : council_statistics["waiting_response"],
            'Awaiting classification' : council_statistics["waiting_classification"],
            'Awaiting clarification' : council_statistics["waiting_clarification"],
            'Overdue' : council_statistics["waiting_response_overdue"],
            'Long overdue' : council_statistics["waiting_response_very_overdue"],
            'Info not held' : council_statistics["not_held"],
            'Requires admin' : council_statistics["requires_admin"],
            'Internal review' : council_statistics["internal_review"],
            'Withdrawn by user' : council_statistics["user_withdrawn"],
            'Error message' : council_statistics["error_message"],
            'Handled by post' : council_statistics["gone_postal"],
     }                 
    
    datastore.save(unique_keys=['Council name' ], data=data)
                                #'Total requests', 'Successful', 'Partially successful',
                                #'Rejected', 'Awaiting response', 'Awaiting classification',
                                #'Awaiting clarification', 'Overdue', 'Long overdue',
                                #'Info not held', 'Requires admin', 'Internal review', 
                                #'Withdrawn by user', 'Error message', 'Handled by post'], data=data)


