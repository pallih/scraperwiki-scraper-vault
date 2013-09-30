import scraperwiki
import cookielib
import socket
import urllib
import urllib2
import json                                                                     
                                                                     
                                                                     
                                             
##############################################################
# Program name: St. Paul Crime Data Scraper
# Version: 0.1-alpha
# By: Rodrigo Zamith
# Additional thanks: Michael Altmann 
##############################################################

xlsurl_base = "http://stpaul.gov/DocumentCenter/View/"


debug = False  # Set debug mode to True or False

### DEFINE OUR FUNCTIONS HERE

# Function to grab data
def grabber(url, params, http_header):
    # Create a cookie handler, if necessary
    cookie_jar = cookielib.LWPCookieJar()
    cookie = urllib2.HTTPCookieProcessor(cookie_jar)
    
    # Create an urllib2 opener() using our cookie jar
    opener = urllib2.build_opener(cookie)
    
    # Create the HTTP request
    req = urllib2.Request(url, urllib.urlencode(params), http_header)
    
    # Submit the request
    res = opener.open(req)
    data = res.read()
    return(data)

def json_convert(data):
    # Convert the output into a nice JSON data set
    data_string = json.loads(data)
    return data_string

### Grab data

# PART 1: GET LIST OF CRIME REPORT FOLDERS, one for each week
url = 'http://www.stpaul.gov/Admin/DocumentCenter/Home/_AjaxLoading'
params = {
          'Text' : 'District Council Reports',
          'Value' : '863'
          }
http_header = {
            "Host": "www.stpaul.gov",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://www.stpaul.gov/DocumentCenter/",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
                }
url_data = grabber(url, params, http_header)
json_data = json_convert(url_data)
folders = []
for i in range(0, len(json_data)):
    folderid = json_data[i]["Value"] 
    foldername = json_data[i]["Text"]
    if debug : print  str(i) + " folder id: " + folderid + " name:" + foldername
    folders.append([folderid, foldername])


# PART 2: GET LIST OF DOCUMENTS FOR EACH FOLDER
# The folder typically has a single XLS spreadsheet with the week's crime report
for pair in folders:
    folderid = pair[0]
    foldername = pair[1]
    foundXls = False
    url = 'http://www.stpaul.gov/Admin/DocumentCenter/Home/Document_AjaxBinding?folder=&document='
    params = {
              'getDocuments' : '1',
              'id' : folderid,
              'page' : '1'
              }
    http_header = {
                "Host": "www.stpaul.gov",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "DNT": "1",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "http://www.stpaul.gov/DocumentCenter/",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
                }
    url_data = grabber(url, params, http_header)
    json_data = json_convert(url_data)
    
    for i in range(0, len(json_data['data'])):
        if json_data['data'][i]["FileType"] == "xls":
            foundXls = True
            data = dict()
            xlsid = json_data['data'][i]["ID"]
            xlsurl = str(xlsurl_base) + str(xlsid)
            if debug : print "The XLS file for folder with ID: " + str(folderid) + " name: " + foldername+ " is id: " + str(xlsid) + " URL: " + xlsurl 
            data['folderid'] = folderid
            data['foldername'] = foldername
            data['xlsid'] = xlsid 
            data['xlsurl'] = xlsurl
            scraperwiki.sqlite.save(unique_keys=['folderid'], data=data)
    if foundXls == False:
        print "No XLS file for folder with ID: " + str(folderid) + " name: " + foldername



import scraperwiki
import cookielib
import socket
import urllib
import urllib2
import json                                                                     
                                                                     
                                                                     
                                             
##############################################################
# Program name: St. Paul Crime Data Scraper
# Version: 0.1-alpha
# By: Rodrigo Zamith
# Additional thanks: Michael Altmann 
##############################################################

xlsurl_base = "http://stpaul.gov/DocumentCenter/View/"


debug = False  # Set debug mode to True or False

### DEFINE OUR FUNCTIONS HERE

# Function to grab data
def grabber(url, params, http_header):
    # Create a cookie handler, if necessary
    cookie_jar = cookielib.LWPCookieJar()
    cookie = urllib2.HTTPCookieProcessor(cookie_jar)
    
    # Create an urllib2 opener() using our cookie jar
    opener = urllib2.build_opener(cookie)
    
    # Create the HTTP request
    req = urllib2.Request(url, urllib.urlencode(params), http_header)
    
    # Submit the request
    res = opener.open(req)
    data = res.read()
    return(data)

def json_convert(data):
    # Convert the output into a nice JSON data set
    data_string = json.loads(data)
    return data_string

### Grab data

# PART 1: GET LIST OF CRIME REPORT FOLDERS, one for each week
url = 'http://www.stpaul.gov/Admin/DocumentCenter/Home/_AjaxLoading'
params = {
          'Text' : 'District Council Reports',
          'Value' : '863'
          }
http_header = {
            "Host": "www.stpaul.gov",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://www.stpaul.gov/DocumentCenter/",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
                }
url_data = grabber(url, params, http_header)
json_data = json_convert(url_data)
folders = []
for i in range(0, len(json_data)):
    folderid = json_data[i]["Value"] 
    foldername = json_data[i]["Text"]
    if debug : print  str(i) + " folder id: " + folderid + " name:" + foldername
    folders.append([folderid, foldername])


# PART 2: GET LIST OF DOCUMENTS FOR EACH FOLDER
# The folder typically has a single XLS spreadsheet with the week's crime report
for pair in folders:
    folderid = pair[0]
    foldername = pair[1]
    foundXls = False
    url = 'http://www.stpaul.gov/Admin/DocumentCenter/Home/Document_AjaxBinding?folder=&document='
    params = {
              'getDocuments' : '1',
              'id' : folderid,
              'page' : '1'
              }
    http_header = {
                "Host": "www.stpaul.gov",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0",
                "Accept": "text/plain, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "DNT": "1",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "http://www.stpaul.gov/DocumentCenter/",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache"
                }
    url_data = grabber(url, params, http_header)
    json_data = json_convert(url_data)
    
    for i in range(0, len(json_data['data'])):
        if json_data['data'][i]["FileType"] == "xls":
            foundXls = True
            data = dict()
            xlsid = json_data['data'][i]["ID"]
            xlsurl = str(xlsurl_base) + str(xlsid)
            if debug : print "The XLS file for folder with ID: " + str(folderid) + " name: " + foldername+ " is id: " + str(xlsid) + " URL: " + xlsurl 
            data['folderid'] = folderid
            data['foldername'] = foldername
            data['xlsid'] = xlsid 
            data['xlsurl'] = xlsurl
            scraperwiki.sqlite.save(unique_keys=['folderid'], data=data)
    if foundXls == False:
        print "No XLS file for folder with ID: " + str(folderid) + " name: " + foldername



