import scraperwiki
import requests
import lxml.html
import re
import urllib
import simplejson

#setup
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
search_url = 'http://www.vi.virginia.gov/vdacs_dd/public/cgi-bin/public.cgi'
id_regex = re.compile("\d+")
geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input=%s&outFields=&outSR=&f=json'
batch_for_details = 30
requests.defaults.defaults['max_retries'] = 5


def collect_localities():
    initial_page = requests.get(search_url,headers=headers)
    root = lxml.html.fromstring(initial_page.text)
    localities = root.xpath('//form//select/option')
    batch=[]
    for locality in localities:
        record = {}
        record['name'] = locality.text.strip()
        record['id'] = locality.attrib['value']
        batch.append(record)
    scraperwiki.sqlite.save(["id"],data=batch,table_name="localities")

def collect_dogs():
    print 'Collecting dangerous dogs ids'
    localities = scraperwiki.sqlite.select("* from localities")
    for locality in localities:
        print 'Collecting dogs for ', locality['name']
        payload = {'loc':locality['id'],'submit':'Go'}
        response = requests.post(search_url,data=payload,headers=headers)
        root = lxml.html.fromstring(response.text)
        dogs = root.xpath('//table/tr/td/a')
        if len(dogs) != 0:
            batch = []
            for dog in dogs:
                record = {}
                record['locality'] = locality['name']
                record['sys_id'] = id_regex.findall(dog.attrib['href'])[0]
                batch.append(record)
            scraperwiki.sqlite.save(["sys_id"],data=batch,table_name="dogs")
            print 'Saved ', len(batch), ' dogs for ', locality['name']
        else:
            print 'No dogs found for ', locality['name']

def process_dog_detail(sys_id):
    record = {}
    record['sys_id'] = sys_id
    response = requests.get('http://www.vi.virginia.gov/vdacs_dd/public/cgi-bin/public.cgi?sysdogno=%s&submit=detail' % sys_id)
    root = lxml.html.fromstring(response.text)

    #Detail url
    record['detail_ur'] = 'http://www.vi.virginia.gov/vdacs_dd/public/cgi-bin/public.cgi?sysdogno=%s&submit=detail' % sys_id

    #Dog nr
    try:
        record['dog_nr']= id_regex.findall(root.xpath('//span[@class="body3"]')[0].text)[0]
    except:
        pass

    #Animal control contact phone number
    animal_control = root.xpath('//p/span[@class="body2"][contains(text(),"Main Animal Control Contact Number:")]/../span[@class="body2"][2]')
    record['animal_control_phone_number'] = animal_control[0].text_content().strip()
    
    #Get primary owner and lat,lng
    primary_owner = root.xpath('//p/span[@class="body2"][contains(text(),"Primary Owner Information:")]/..')
    record['primary_owner_name'] = primary_owner[0][1].tail.strip()
    record['primary_owner_address'] = primary_owner[0][2].tail.strip()
    record['primary_owner_locality'] = primary_owner[0][3].tail.strip()    
    geocode_address = urllib.quote_plus(record['primary_owner_address'] + ' ' + record['primary_owner_locality'].replace(',',''))
    geocoded = simplejson.loads(requests.get(geocode_url % geocode_address).text)
    if len(geocoded['candidates']):
        record['lat'] = geocoded['candidates'][0]['location']['y']
        record['lng'] = geocoded['candidates'][0]['location']['x']
    
    #Get secondary owner ( if exists)    
    secondary_owner = root.xpath('//p/span[@class="body2"][contains(text(),"Secondary Owner Information:")]/..')
    if secondary_owner:
        record['secondary_owner_name'] = secondary_owner[0][1].tail.strip()
        record['secondary_owner_address'] = secondary_owner[0][2].tail.strip()
        record['secondary_owner_locality'] = secondary_owner[0][3].tail.strip()

    #Dog info  
    dog_info = root.xpath('//p/span[@class="body2"][contains(text(),"Dog Information:")]/..')
    record['dog_name'] = dog_info[0][1].tail.strip().replace('Name of Dangerous Dog: ','')
    record['dog_primary_breed'] = dog_info[0][2].tail.strip().replace('Primary Breed: ','')
    record['dog_secondary_breed'] = dog_info[0][3].tail.strip().replace('Secondary Breed: ','')
    record['dog_color_markings'] = dog_info[0][4].tail.strip().replace('Color and Markings: ','')

    #Trial docket info
    
    trial_docket_info = root.xpath('//p/span[@class="body2"][contains(text(),"Trial Docket Info:")]/..')
    record['trial_docket_act'] = trial_docket_info[0][1].tail.strip().replace('Acts resulting in the dog being declared dangerous: ','')
    record['trial_docket_number'] = trial_docket_info[0][2].tail.strip().replace('Docket Number: ','')
    record['trial_docket_parties'] = trial_docket_info[0][3].tail.strip().replace('Parties: ','')
    record['trial_docket_court'] = trial_docket_info[0][4].tail.strip().replace('Court: ','')
    record['trial_docket_judge'] = trial_docket_info[0][5].tail.strip().replace('Judge: ','')
    record['trial_docket_adjudication_date'] = trial_docket_info[0][6].tail.strip().replace('Adjudication Date: ','')
    record['trial_docket_requirements_imposed '] = trial_docket_info[0][7].tail.strip().replace('Requirements imposed on owner by judge: ','')
    return record

def collect_dog_details(number_in_batch):
    dogs_todo = scraperwiki.sqlite.execute("SELECT dogs.sys_id FROM dogs LEFT JOIN dog_details ON dogs.sys_id = dog_details.sys_id WHERE dog_details.sys_id IS NULL LIMIT " + str(number_in_batch))
    dogs_todo = [u[0]  for u in dogs_todo["data"]]
    if not dogs_todo:
        return False
    batch = [ ]
    for dog_sys_id in dogs_todo:
        print 'Processing dog with sys_id: ', dog_sys_id
        data = process_dog_detail(dog_sys_id)
        batch.append(data)
    scraperwiki.sqlite.save(["sys_id"],data=batch,table_name="dog_details")
    print 'Saved ',len(batch),' dogs'
    return True

#Collect localities  - only needed on first run
collect_localities()
exit()
#Collect dogs from all the localities
collect_dogs()


# Process details for dogs that have not been processed before in batches of whatever you decide

dogs_todo_count = scraperwiki.sqlite.execute("SELECT dogs.sys_id FROM dogs LEFT JOIN dog_details ON dogs.sys_id = dog_details.sys_id WHERE dog_details.sys_id IS NULL")
dogs_todo_count = [u[0]  for u in dogs_todo_count["data"]]
print
print 'Dogs that have not been processed for details: ',len(dogs_todo_count)
if len(dogs_todo_count) > 0:
    print 'Processing dogs in batches of ',batch_for_details
    print
    while collect_dog_details(batch_for_details): pass
else:
    print
    print 'Nothing to do today. See you tomorrow'



import scraperwiki
import requests
import lxml.html
import re
import urllib
import simplejson

#setup
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'}
search_url = 'http://www.vi.virginia.gov/vdacs_dd/public/cgi-bin/public.cgi'
id_regex = re.compile("\d+")
geocode_url = 'http://tasks.arcgisonline.com/ArcGIS/rest/services/Locators/TA_Streets_US_10/GeocodeServer/findAddressCandidates?Single+Line+Input=%s&outFields=&outSR=&f=json'
batch_for_details = 30
requests.defaults.defaults['max_retries'] = 5


def collect_localities():
    initial_page = requests.get(search_url,headers=headers)
    root = lxml.html.fromstring(initial_page.text)
    localities = root.xpath('//form//select/option')
    batch=[]
    for locality in localities:
        record = {}
        record['name'] = locality.text.strip()
        record['id'] = locality.attrib['value']
        batch.append(record)
    scraperwiki.sqlite.save(["id"],data=batch,table_name="localities")

def collect_dogs():
    print 'Collecting dangerous dogs ids'
    localities = scraperwiki.sqlite.select("* from localities")
    for locality in localities:
        print 'Collecting dogs for ', locality['name']
        payload = {'loc':locality['id'],'submit':'Go'}
        response = requests.post(search_url,data=payload,headers=headers)
        root = lxml.html.fromstring(response.text)
        dogs = root.xpath('//table/tr/td/a')
        if len(dogs) != 0:
            batch = []
            for dog in dogs:
                record = {}
                record['locality'] = locality['name']
                record['sys_id'] = id_regex.findall(dog.attrib['href'])[0]
                batch.append(record)
            scraperwiki.sqlite.save(["sys_id"],data=batch,table_name="dogs")
            print 'Saved ', len(batch), ' dogs for ', locality['name']
        else:
            print 'No dogs found for ', locality['name']

def process_dog_detail(sys_id):
    record = {}
    record['sys_id'] = sys_id
    response = requests.get('http://www.vi.virginia.gov/vdacs_dd/public/cgi-bin/public.cgi?sysdogno=%s&submit=detail' % sys_id)
    root = lxml.html.fromstring(response.text)

    #Detail url
    record['detail_ur'] = 'http://www.vi.virginia.gov/vdacs_dd/public/cgi-bin/public.cgi?sysdogno=%s&submit=detail' % sys_id

    #Dog nr
    try:
        record['dog_nr']= id_regex.findall(root.xpath('//span[@class="body3"]')[0].text)[0]
    except:
        pass

    #Animal control contact phone number
    animal_control = root.xpath('//p/span[@class="body2"][contains(text(),"Main Animal Control Contact Number:")]/../span[@class="body2"][2]')
    record['animal_control_phone_number'] = animal_control[0].text_content().strip()
    
    #Get primary owner and lat,lng
    primary_owner = root.xpath('//p/span[@class="body2"][contains(text(),"Primary Owner Information:")]/..')
    record['primary_owner_name'] = primary_owner[0][1].tail.strip()
    record['primary_owner_address'] = primary_owner[0][2].tail.strip()
    record['primary_owner_locality'] = primary_owner[0][3].tail.strip()    
    geocode_address = urllib.quote_plus(record['primary_owner_address'] + ' ' + record['primary_owner_locality'].replace(',',''))
    geocoded = simplejson.loads(requests.get(geocode_url % geocode_address).text)
    if len(geocoded['candidates']):
        record['lat'] = geocoded['candidates'][0]['location']['y']
        record['lng'] = geocoded['candidates'][0]['location']['x']
    
    #Get secondary owner ( if exists)    
    secondary_owner = root.xpath('//p/span[@class="body2"][contains(text(),"Secondary Owner Information:")]/..')
    if secondary_owner:
        record['secondary_owner_name'] = secondary_owner[0][1].tail.strip()
        record['secondary_owner_address'] = secondary_owner[0][2].tail.strip()
        record['secondary_owner_locality'] = secondary_owner[0][3].tail.strip()

    #Dog info  
    dog_info = root.xpath('//p/span[@class="body2"][contains(text(),"Dog Information:")]/..')
    record['dog_name'] = dog_info[0][1].tail.strip().replace('Name of Dangerous Dog: ','')
    record['dog_primary_breed'] = dog_info[0][2].tail.strip().replace('Primary Breed: ','')
    record['dog_secondary_breed'] = dog_info[0][3].tail.strip().replace('Secondary Breed: ','')
    record['dog_color_markings'] = dog_info[0][4].tail.strip().replace('Color and Markings: ','')

    #Trial docket info
    
    trial_docket_info = root.xpath('//p/span[@class="body2"][contains(text(),"Trial Docket Info:")]/..')
    record['trial_docket_act'] = trial_docket_info[0][1].tail.strip().replace('Acts resulting in the dog being declared dangerous: ','')
    record['trial_docket_number'] = trial_docket_info[0][2].tail.strip().replace('Docket Number: ','')
    record['trial_docket_parties'] = trial_docket_info[0][3].tail.strip().replace('Parties: ','')
    record['trial_docket_court'] = trial_docket_info[0][4].tail.strip().replace('Court: ','')
    record['trial_docket_judge'] = trial_docket_info[0][5].tail.strip().replace('Judge: ','')
    record['trial_docket_adjudication_date'] = trial_docket_info[0][6].tail.strip().replace('Adjudication Date: ','')
    record['trial_docket_requirements_imposed '] = trial_docket_info[0][7].tail.strip().replace('Requirements imposed on owner by judge: ','')
    return record

def collect_dog_details(number_in_batch):
    dogs_todo = scraperwiki.sqlite.execute("SELECT dogs.sys_id FROM dogs LEFT JOIN dog_details ON dogs.sys_id = dog_details.sys_id WHERE dog_details.sys_id IS NULL LIMIT " + str(number_in_batch))
    dogs_todo = [u[0]  for u in dogs_todo["data"]]
    if not dogs_todo:
        return False
    batch = [ ]
    for dog_sys_id in dogs_todo:
        print 'Processing dog with sys_id: ', dog_sys_id
        data = process_dog_detail(dog_sys_id)
        batch.append(data)
    scraperwiki.sqlite.save(["sys_id"],data=batch,table_name="dog_details")
    print 'Saved ',len(batch),' dogs'
    return True

#Collect localities  - only needed on first run
collect_localities()
exit()
#Collect dogs from all the localities
collect_dogs()


# Process details for dogs that have not been processed before in batches of whatever you decide

dogs_todo_count = scraperwiki.sqlite.execute("SELECT dogs.sys_id FROM dogs LEFT JOIN dog_details ON dogs.sys_id = dog_details.sys_id WHERE dog_details.sys_id IS NULL")
dogs_todo_count = [u[0]  for u in dogs_todo_count["data"]]
print
print 'Dogs that have not been processed for details: ',len(dogs_todo_count)
if len(dogs_todo_count) > 0:
    print 'Processing dogs in batches of ',batch_for_details
    print
    while collect_dog_details(batch_for_details): pass
else:
    print
    print 'Nothing to do today. See you tomorrow'



