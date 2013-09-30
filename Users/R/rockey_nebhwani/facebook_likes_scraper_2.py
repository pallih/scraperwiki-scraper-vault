import scraperwiki
import json
import datetime
import urllib2
import csv

data = scraperwiki.scrape("http://leapgradient.com/asda/ASDA_Search_Insights_Report_W20130221.csv")
reader = csv.reader(data.splitlines())

for row in reader:
    url = 'http://completion.amazon.co.uk/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=3&fb=1&xcat=0&q=' + row[1]
    print url
    # download the json string
    json_string = urllib2.urlopen(url).read()
    # de-serialize the string so that we can work with it
    the_data = json.loads(json_string)
    print the_data

    # get the list of trends
    #trends = the_data[2][0]['nodes'][0]['name']
    trends = the_data[2][0]['nodes']
    
    print trends
    print "hi"
    print type(trends)
    
    # print the name of each trend
    for trend in trends:
        print trend['name']


import scraperwiki
import json
import datetime
import urllib2
import csv

data = scraperwiki.scrape("http://leapgradient.com/asda/ASDA_Search_Insights_Report_W20130221.csv")
reader = csv.reader(data.splitlines())

for row in reader:
    url = 'http://completion.amazon.co.uk/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=3&fb=1&xcat=0&q=' + row[1]
    print url
    # download the json string
    json_string = urllib2.urlopen(url).read()
    # de-serialize the string so that we can work with it
    the_data = json.loads(json_string)
    print the_data

    # get the list of trends
    #trends = the_data[2][0]['nodes'][0]['name']
    trends = the_data[2][0]['nodes']
    
    print trends
    print "hi"
    print type(trends)
    
    # print the name of each trend
    for trend in trends:
        print trend['name']


import scraperwiki
import json
import datetime
import urllib2
import csv

data = scraperwiki.scrape("http://leapgradient.com/asda/ASDA_Search_Insights_Report_W20130221.csv")
reader = csv.reader(data.splitlines())

for row in reader:
    url = 'http://completion.amazon.co.uk/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=3&fb=1&xcat=0&q=' + row[1]
    print url
    # download the json string
    json_string = urllib2.urlopen(url).read()
    # de-serialize the string so that we can work with it
    the_data = json.loads(json_string)
    print the_data

    # get the list of trends
    #trends = the_data[2][0]['nodes'][0]['name']
    trends = the_data[2][0]['nodes']
    
    print trends
    print "hi"
    print type(trends)
    
    # print the name of each trend
    for trend in trends:
        print trend['name']


import scraperwiki
import json
import datetime
import urllib2
import csv

data = scraperwiki.scrape("http://leapgradient.com/asda/ASDA_Search_Insights_Report_W20130221.csv")
reader = csv.reader(data.splitlines())

for row in reader:
    url = 'http://completion.amazon.co.uk/search/complete?method=completion&search-alias=aps&client=amazon-search-ui&mkt=3&fb=1&xcat=0&q=' + row[1]
    print url
    # download the json string
    json_string = urllib2.urlopen(url).read()
    # de-serialize the string so that we can work with it
    the_data = json.loads(json_string)
    print the_data

    # get the list of trends
    #trends = the_data[2][0]['nodes'][0]['name']
    trends = the_data[2][0]['nodes']
    
    print trends
    print "hi"
    print type(trends)
    
    # print the name of each trend
    for trend in trends:
        print trend['name']


