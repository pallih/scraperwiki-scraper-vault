###############################################################################
# Road Traffic Accident Scraper
###############################################################################

# (Apologies, this database is way too big to migrate.  Have to drop it so it can rebuild again)

import scraperwiki
import mechanize 
import csv
import datetime
from BeautifulSoup import BeautifulSoup
import time
import json
import traceback,sys

username = "sjf@o2.ie"
password = "GS5#Q{Ld"  

login_url = "http://reports.roadcasualtiesonline.org.uk/Login"
download_url = "http://reports.roadcasualtiesonline.org.uk/Reports/DownloadList"
# This is a dictionary too big to fit in the scraper source
codes_url = "http://cudame.com/~sjf/traffic/codes.json"

save_interval = 500

TEST = False
#Test data set, contains 10 records in each file
test_url = "http://cudame.com/~sjf/traffic/sml"

def run_scraper():
    br = mechanize.Browser()
    login(br)
    urls = get_dataset_urls(br)
    codes = get_codes()
    for name,url in urls:
        process_dataset(name, url, br, codes)

def login(br):
    br.open(login_url)
    # Select the login form
    br.select_form(nr=0)

    # Set the fields
    br["Username"] = username
    br["Password"] = password

    # and submit the form
    br.submit()
    resp = br.response().read() 

    # Login failure doesn't throw an error here, check for login failure message
    soup = BeautifulSoup(resp)
    td = soup.find('td')
    if td and td.string and "we were unable to log you in" in td.string.lower():
        raise Exception("Login failure", td)
    
def get_dataset_urls(br):
    br.open(download_url)
    
    # Get all the links to the datasets
    soup = BeautifulSoup(br.response().read())
    links = []
    for link in soup.findAll('a'):    
        if link.string and link.string.endswith(".txt"):
            links.append((link.string, link['href']))
    links.sort()
    return links

def get_codes():
    br = mechanize.Browser()
    br.open(codes_url)
    return json.loads(br.response().read())

def retry(closure, max):
    count = 0
    while count < max:
        try:
            return closure()
        except Exception,e:
            print e
            traceback.print_exc(file=sys.stdout)
            time.sleep(2)
        count += 1

def save_metadata(k,v):
    retry(lambda : scraperwiki.metadata.save(k, v), 10)
def get_metadata(k):
    return retry(lambda : scraperwiki.metadata.get(k, None), 10)
    

# Record types
ACCIDENT = "Accident"
VEHICLE = "Vehicle"
CASUALTY = "Casualty"
file_types = {'acc' : ACCIDENT, 'veh' : VEHICLE, 'cas' : CASUALTY}

def timestamp():
    return time.asctime(time.localtime(time.time()))

def process_dataset(name, url, br, codes):
    print timestamp(), "Scraping",name,url

    if TEST:
        url = test_url+url
        print url

    meta_key = name.replace(".",'') # keys with periods don't work
    #status = scraperwiki.metadata.get(meta_key, None)
    status = get_metadata(meta_key)

    print name, " status is ", status

    #if status and status[0] == "Completed":
    #    return
    if status and status[0] == "Started":
        # Resume
        record_num = status[1]
    else:        
        # Start at the first record
        print "Starting scrape from begining"
        record_num = 0

    short_name = name.lower()[:3]
    if short_name in file_types:
        dataset = file_types[short_name]
    else:
        print "Warn: unrecognised txt file:", name
        return

    print timestamp(), "Downloading"
    try: 
        br.open(url)
    except Exception,e:
        print e
        traceback.print_exc(file=sys.stdout)
        return

    # Parse CSV
    resp = br.response().read()
    print timestamp(), "Download complete"

    rows = list(csv.reader(resp.split("\n")))
    header = rows.pop(0)   # set 'header' to be the first row of the CSV file

    if record_num > len(rows):
        print "Error resuming from record #", record, "total number of records is ",len(rows)
        return

    i = record_num
    while i < len(rows):
        row = rows[i]
        data = dict(zip(header, row)) # and use 'dict' to create a dictionary for each row
        if data: 
            map_codes_to_values(data, codes)
            data['Record_Type'] = dataset
            #print data
            # Save to datastore
            if dataset == ACCIDENT:
                date = datetime.datetime.strptime(data['Date'],'%d/%M/%Y')
                del data['Date']
                try:
                    lat = float(data['Latitude'])
                    lng = float(data['Longitude'])
                    latlng = (lat,lng)
                except:
                    # Error converting string to float
                    latlng = None
                del data['Latitude']
                del data['Longitude']
                scraperwiki.datastore.save(['Accident_Index'], data, date, latlng)
            elif dataset == VEHICLE:
                scraperwiki.datastore.save(['Acc_Index', 'Vehicle_Reference'], data)
            else: # dataset == CASUALTY:
                scraperwiki.datastore.save(['Acc_Index', 'Vehicle_Reference', 'Casualty_Reference'], data)

            if i % save_interval == 0:
                # Save progress of the scrape
                #scraperwiki.metadata.save(meta_key, ("Started", i))
                save_metadata(meta_key, ("Started", i))
            if i % 2000 == 0: # Try not to output too many lines, they just get cut off in the log file
                print timestamp(), "Progress:",name, " record ", i, "..."
        i+=1

    #scraperwiki.metadata.save(meta_key, ("Started", i))
    save_metadata(meta_key, ("Started", i))
    print timestamp(), "Completed ",name+"!"

def map_codes_to_values(data, codes):
    for key,code in data.items():
        #try:
        #    code = int(code)
        #except:
        #    continue # Code is non-numeric
        if code == "-1":
            data[key] = None # Data is missing
        elif key in codes.keys(): # Code can be mapped to string value
            if not code in codes[key]:
                print "Warn: Invalid value for ",key,":",code
                del data[key]
            else:
                data[key] = codes[key][code]

run_scraper()