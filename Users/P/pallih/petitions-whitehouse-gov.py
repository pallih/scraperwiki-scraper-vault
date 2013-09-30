# -*- coding: utf-8 -*-
import os
import requests
import lxml.html
import scraperwiki
try:
    import json
except ImportError:
    import simplejson as json
import time
import random
import string
import StringIO
import csv

chars = string.letters + string.digits
randomstring =  ''.join([random.choice(chars) for i in xrange(4)])
petition_url = os.getenv("QUERY_STRING")
response_petition_url = 'https://petitions.whitehouse.gov/signatures/more/%s/%s/%s'

def process_response(response,page):
    root = lxml.html.fromstring (response)
    data = []
    record = {}
    if page == 1:
        creator = root.xpath('div[@class="entry entry-creator "]/div')
        record['name'] = creator[1].text.replace("\n ", "").strip()
        record['location'] = creator[2].text.replace("\n ", "").strip()
        record['date'] = creator[2][0].tail.replace("\n ", "").strip()
        record['nr'] = creator[2][1].tail.strip().replace('Signature # ','').replace("\n ", "")
        data.append(record)
        record = {}
    end_of_line_registrants = root.xpath('div[@class="entry entry-reg last"]')
    for registrant in end_of_line_registrants:
        record['name'] = registrant[0].text.replace("\n ", "").strip()
        record['location'] = registrant[2].text.replace("\n ", "").strip()
        record['date'] = registrant[2][0].tail.replace("\n ", "").strip()
        record['nr'] = registrant[2][1].tail.strip().replace('Signature # ','').replace("\n ", "")
        data.append(record)
        record = {}
    registrants = root.xpath('div[@class="entry entry-reg "]')
    for registrant in registrants:
        record['name'] = registrant[0].text.replace("\n ", "").strip()
        record['location'] = registrant[2].text.replace("\n ", "").strip()
        record['date'] = registrant[2][0].tail.replace("\n ", "").strip()
        record['nr'] = registrant[2][1].tail.strip().replace('Signature # ','').replace("\n ", "")
        data.append(record)
        record = {}
    try:
        arg = root.xpath('//a[@class="load-next no-follow"]')[0].attrib['rel']
        last_id = root.xpath('//div[@id="last-signature-id"]')[0].text_content()
        #print 'Found',len(data),'signatures on result page',page
        return arg,last_id,data
    except:
        # Done
        #print 'Found', len(data),'signatures on result page',page
        return '','',data

def get_response(arg,page,last_id):
    response = requests.get(response_petition_url % (arg,page,last_id),verify=False).text
    json_response = json.loads(response)
    new_arg,new_last_id,data = process_response(json_response['markup'],page)
    return new_arg,new_last_id,data

def printcsv(csv_result):
    #scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    #print 'name'+','+'location'+','+'date'+','+'nr'
    for dictionary in csv_result:
        #myWriter.writerow(row)
        for row in dictionary:
            print '"'+row['name']+'","'+row['location']+'","'+row['date']+'","'+row['nr']+'"'
    exit()


page = 1
#get first page

if petition_url:
    #mtime = time.time()
    #tempfilename= '/tmp/'+randomstring+'.csv'
    #sendcsvfilename = petition_url+'.csv'
    #f = open(tempfilename,'wt')
    #fieldnames = ('name', 'location', 'date', 'nr')
    #myWriter = csv.DictWriter(f,delimiter=',',fieldnames=fieldnames,quoting=csv.QUOTE_NONNUMERIC)
    #myWriter.writerow(dict((fn,fn) for fn in fieldnames))
    petition_html = requests.get(petition_url,verify=False).text
    root = lxml.html.fromstring (petition_html)
    try:
        total_signatures = str(root.xpath('//span[@class="total-count"]')[0].text)
        #print 'total signatures: ', total_signatures
    except Exception,e:
        print 'Something went wrong! Could it be that the URL you provided is not correct?'
        print
        parser.print_help()
        exit(-1)
    arg = root.xpath('//a[@class="load-next no-follow active"]')[0].attrib['rel']
    last_id = root.xpath('//div[@id="last-signature-id"]')[0].text_content()
    if last_id:
        next = True
    csv_result = []
    while next == True:
        if last_id != '':
            arg,last_id,data = get_response(arg,page,last_id)
            #print data
            #printcsv ( data )
            #print data
            csv_result.append( data)
            page = page+1
        else:
            next = False
    
    
    #f.close
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    printcsv( csv_result)
    #scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename="+sendtarfilename)

    #fn = open(tempfilename,"r")
    #output = fn.read()
    #print output
    #fn.close
    

print 'Pass in a url to a petition on petitions.whitehouse.gov to get signatures - like this:<br><br>'
print 'https://views.scraperwiki.com/run/petitions-whitehouse-gov/?LINK TO URL<br>'
print '<br>'
print 'Try this: <a href="https://views.scraperwiki.com/run/petitions-whitehouse-gov/?https://petitions.whitehouse.gov/petition/address-current-autism-crisis-light-autism-hearings-time-has-come-answers-time-now/LvnJZLVW">https://views.scraperwiki.com/run/petitions-whitehouse-gov/?https://petitions.whitehouse.gov/petition/address-current-autism-crisis-light-autism-hearings-time-has-come-answers-time-now/LvnJZLVW</a>'
print '<br><br>'
print 'Response is in a csv file'
# -*- coding: utf-8 -*-
import os
import requests
import lxml.html
import scraperwiki
try:
    import json
except ImportError:
    import simplejson as json
import time
import random
import string
import StringIO
import csv

chars = string.letters + string.digits
randomstring =  ''.join([random.choice(chars) for i in xrange(4)])
petition_url = os.getenv("QUERY_STRING")
response_petition_url = 'https://petitions.whitehouse.gov/signatures/more/%s/%s/%s'

def process_response(response,page):
    root = lxml.html.fromstring (response)
    data = []
    record = {}
    if page == 1:
        creator = root.xpath('div[@class="entry entry-creator "]/div')
        record['name'] = creator[1].text.replace("\n ", "").strip()
        record['location'] = creator[2].text.replace("\n ", "").strip()
        record['date'] = creator[2][0].tail.replace("\n ", "").strip()
        record['nr'] = creator[2][1].tail.strip().replace('Signature # ','').replace("\n ", "")
        data.append(record)
        record = {}
    end_of_line_registrants = root.xpath('div[@class="entry entry-reg last"]')
    for registrant in end_of_line_registrants:
        record['name'] = registrant[0].text.replace("\n ", "").strip()
        record['location'] = registrant[2].text.replace("\n ", "").strip()
        record['date'] = registrant[2][0].tail.replace("\n ", "").strip()
        record['nr'] = registrant[2][1].tail.strip().replace('Signature # ','').replace("\n ", "")
        data.append(record)
        record = {}
    registrants = root.xpath('div[@class="entry entry-reg "]')
    for registrant in registrants:
        record['name'] = registrant[0].text.replace("\n ", "").strip()
        record['location'] = registrant[2].text.replace("\n ", "").strip()
        record['date'] = registrant[2][0].tail.replace("\n ", "").strip()
        record['nr'] = registrant[2][1].tail.strip().replace('Signature # ','').replace("\n ", "")
        data.append(record)
        record = {}
    try:
        arg = root.xpath('//a[@class="load-next no-follow"]')[0].attrib['rel']
        last_id = root.xpath('//div[@id="last-signature-id"]')[0].text_content()
        #print 'Found',len(data),'signatures on result page',page
        return arg,last_id,data
    except:
        # Done
        #print 'Found', len(data),'signatures on result page',page
        return '','',data

def get_response(arg,page,last_id):
    response = requests.get(response_petition_url % (arg,page,last_id),verify=False).text
    json_response = json.loads(response)
    new_arg,new_last_id,data = process_response(json_response['markup'],page)
    return new_arg,new_last_id,data

def printcsv(csv_result):
    #scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    #print 'name'+','+'location'+','+'date'+','+'nr'
    for dictionary in csv_result:
        #myWriter.writerow(row)
        for row in dictionary:
            print '"'+row['name']+'","'+row['location']+'","'+row['date']+'","'+row['nr']+'"'
    exit()


page = 1
#get first page

if petition_url:
    #mtime = time.time()
    #tempfilename= '/tmp/'+randomstring+'.csv'
    #sendcsvfilename = petition_url+'.csv'
    #f = open(tempfilename,'wt')
    #fieldnames = ('name', 'location', 'date', 'nr')
    #myWriter = csv.DictWriter(f,delimiter=',',fieldnames=fieldnames,quoting=csv.QUOTE_NONNUMERIC)
    #myWriter.writerow(dict((fn,fn) for fn in fieldnames))
    petition_html = requests.get(petition_url,verify=False).text
    root = lxml.html.fromstring (petition_html)
    try:
        total_signatures = str(root.xpath('//span[@class="total-count"]')[0].text)
        #print 'total signatures: ', total_signatures
    except Exception,e:
        print 'Something went wrong! Could it be that the URL you provided is not correct?'
        print
        parser.print_help()
        exit(-1)
    arg = root.xpath('//a[@class="load-next no-follow active"]')[0].attrib['rel']
    last_id = root.xpath('//div[@id="last-signature-id"]')[0].text_content()
    if last_id:
        next = True
    csv_result = []
    while next == True:
        if last_id != '':
            arg,last_id,data = get_response(arg,page,last_id)
            #print data
            #printcsv ( data )
            #print data
            csv_result.append( data)
            page = page+1
        else:
            next = False
    
    
    #f.close
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    printcsv( csv_result)
    #scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename="+sendtarfilename)

    #fn = open(tempfilename,"r")
    #output = fn.read()
    #print output
    #fn.close
    

print 'Pass in a url to a petition on petitions.whitehouse.gov to get signatures - like this:<br><br>'
print 'https://views.scraperwiki.com/run/petitions-whitehouse-gov/?LINK TO URL<br>'
print '<br>'
print 'Try this: <a href="https://views.scraperwiki.com/run/petitions-whitehouse-gov/?https://petitions.whitehouse.gov/petition/address-current-autism-crisis-light-autism-hearings-time-has-come-answers-time-now/LvnJZLVW">https://views.scraperwiki.com/run/petitions-whitehouse-gov/?https://petitions.whitehouse.gov/petition/address-current-autism-crisis-light-autism-hearings-time-has-come-answers-time-now/LvnJZLVW</a>'
print '<br><br>'
print 'Response is in a csv file'
