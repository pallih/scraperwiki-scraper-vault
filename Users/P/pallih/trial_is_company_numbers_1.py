# -*- coding: utf-8 -*


#opencorporates Iceland

import scraperwiki,re
from lxml import etree
import lxml.html
import time
import datetime
from urllib2 import Request, urlopen, URLError, HTTPError 
from httplib import HTTPException
import string
from random import choice
import timeit



#ISIC4 and ISAT2008 codes merge START
'''
scraperwiki.sqlite.attach('xml2dic')


done = companies = scraperwiki.sqlite.select("CompanyNumber from iceland_corporate_entities_2")
done_count = len(done)
print done_count

isat_2008_select = "* from xml2dic.swdata ORDER by CompanyNumber Limit 100 OFFSET " + str(done_count)
companies_select = "* from iceland_corporate_entities ORDER by CompanyNumber Limit 100 OFFSET " + str(done_count)

print isat_2008_select
print companies_select

#isat2008 = scraperwiki.sqlite.select("* from xml2dic.swdata ORDER by CompanyNumber Limit 5000 OFFSET 5000")
#companies = scraperwiki.sqlite.select("* from iceland_corporate_entities ORDER by CompanyNumber Limit 5000 OFFSET 5000")

isat2008 = scraperwiki.sqlite.select(isat_2008_select)
companies = scraperwiki.sqlite.select(companies_select)


def merge_lists(l1, l2, key):
    merged = {}
    for item in l1+l2:
        #print item[key]
        if item[key] in merged:
            merged[item[key]].update(item)
        else:
            merged[item[key]] = item
    return [val for (_, val) in merged.items()]

combined = merge_lists(isat2008, companies, 'CompanyNumber')

newlist = sorted(combined, key=lambda k: k['CompanyNumber'])

for n in newlist:
    scraperwiki.sqlite.save(['CompanyNumber'], data=n, table_name='iceland_corporate_entities_2')

exit()

#ISIC4 and ISAT2008 codes merge END
'''



#http://rsk.is/fyrirtaekjaskra/thjonusta/leit?name=1&kt=&addr=

baseurl = 'http://rsk.is/fyrirtaekjaskra/thjonusta/leit?name='
days_between_big_run = int(3)
compare_date= scraperwiki.sqlite.select('last_run from runtime_info where letter="all"')
compare_date = str(compare_date[0]['last_run'])
today_date = str(datetime.date.today())
chars = string.letters + string.digits
random =  ''.join([choice(chars) for i in xrange(4)]) # create a random string for url appending to avoid cache

print "The date is", today_date

scraperwiki.sqlite.attach('isat2008')
isat2008 = scraperwiki.sqlite.select("* from isat2008")

#done_numbers = scraperwiki.sqlite.select("CompanyNumber from iceland_corporate_entities_2")
#print "done numbers is now: ", len(done_numbers)

#print done_numbers
#exit()


# - GENERATE A TABLE WITH LETTERS TO USE IN SEARCH FORM - MAKES IT EASIER TO RESTART SCRAPER IF SOMETHING GOES WRONG
# - THIS WAY WE CAN KEEP TRACK OF WHAT WE HAVE DONE - AFTER INITAL RUN THE TABLE CREATION CODE IS COMMENTED OUT:

#numbers = range(10)
#alphabet = map(chr, range(97, 123))
#alphabet.extend(['æ', 'ö', 'í', 'é', 'þ', 'ð', 'á', 'ó', 'ý', 'ú'])
#alphabet = alphabet + numbers

#for letter in alphabet:
#    record = {}
#    record['letter'] = letter
#    record['last_run'] = '2012-03-20'
#    record['last_page'] = '1'
#    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')
#exit()

# IF WE NEED TO SCHEDULE THE BIG RUN THEN UNCOMMENT THIS WITH A DATE THAT IS MORE THAN 7 DAYS IN THE PAST
#record = {}
#record ['letter'] = 'all'
#record ['last_run'] = '2012-03-21'
#scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')
#exit()

# --------------------------------

#CHECK IF DONE

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper
 
#@print_timing
def done_check(number):
    if not any(d.get('CompanyNumber') == number for d in done_numbers): #check if the number is already stored - if so then skip
        check = "false"
        return check
    else:
        done_numbers[:] = [d for d in done_numbers if d.get('CompanyNumber') != number] #remove the number from the list to speed up subsequent lookups
        check = "true"
        return check



#PROCESS XML

def process_xml(url,number):
  url = url + "?x=" + str(random) #append a random string to url to avoid bad status line / cache ...
  req = Request(url)
  record = {}
  attempt = 0
  HTTP_RETRIES = 4
  while attempt < HTTP_RETRIES:
    attempt += 1
    try:
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server. Reason: ', e.reason
        elif hasattr(e, 'code'):
            if e.code == 404:
                print "The company is defunct - mark it!"
                #record['CompanyNumber'] = number
                record['defunc'] = 1
                #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=record)
                return record
            else:
                print "The server couldn\'t fulfill the request.'Error code: ", e.code
                break
                # record['CompanyNumber'] = number
                # record['defunc'] = 1
            #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=record)
            #print record
    except HTTPError, error:
        response = error.read()
        print "something"
        break
    except HTTPException, e:
        print "error - try again"
        print 'this is attempt:' + str(attempt)
        continue
    else:
    # everything is fine
        xml = response.read()
        root = etree.fromstring(xml)
        record['legal-address'] = root.xpath('//legaladdr/addr/text()')[0]
        record['legal-zip'] = root.xpath('//legaladdr/zip/text()')[0]
        record['legal-place'] = root.xpath('//legaladdr/place/text()')[0]
                
        isat2008_number = root.xpath('//isat[@class="2008"]/number')
        isat2008_desc = root.xpath('//isat[@class="2008"]/name')
        isat95_number = root.xpath('//isat[@class="95"]/number')
        isat95_desc = root.xpath('//isat[@class="95"]/name')
        registration_type = root.xpath('//type')
        if isat95_number:
            record['isat95_number']=isat95_number[0].text
            record['isat95_desc']=isat95_desc[0].text
        if isat2008_number:
            record['isat2008_number']=isat2008_number[0].text
            record['isat2008_desc']=isat2008_desc[0].text
            isic4 = filter( lambda x: x['ISAT2008']==isat2008_number[0].text[:5], isat2008 )
        else:
             isic4 = None   
        record['registration_type']=registration_type[0].text
        if isic4:
            record['isic4_number']= isic4[0]['ISIC4']
            record['isat2008_desc_en']= isic4[0]['description_en']
        #record['CompanyNumber'] = number
        record['defunc'] = 0
        #print record
        return record
        #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=record)


# SCRAPE ALL CORPORATIONS (BIG RUN):
def scrape_result(url, letter, last_page):
    url = url + '&p=' + str(last_page)
    url = url + "&x=" + str(random) #append a random string to url to avoid bad status line / cache ...
    html = scraperwiki.scrape(url)

    print "PROCESSING LETTER: " + letter + " -- Last page done: " + str(last_page)
    root = lxml.html.fromstring(html)
    #number = root.xpath ('//td[@class="number"]/nobr/a')
    content = root.xpath ('//div[contains(@class,"linkicons")]/*[2]//tr/.')
    #for x in content[1:]:

     #   check = done_check(x[0][0][0].text.replace('-',''))
        #print check
        #if x[0][0][0].text.replace('-','') == '1701663109':
      #  if check == 'true':
       #     content.remove(x)
    #exit()
    #if (len(content[1:]))>0:
    batch = []
    for m in content[1:]:
        record ={}
        name =  m[1].text
        name = name.encode( "ISO-8859-1" )
        number = m[0][0][0].text
        number = number.replace('-','')
        #check = done_check(number)
        #if check == "false":
        #if not any(d.get('CompanyNumber') == number for d in done_numbers): #check if the number is already stored - if so then skip
        detail_url = 'http://rsk.is/ws/other/enterprisereg/' + str(number) + ".xml"
        record = process_xml(detail_url,number)
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        record['CompanyName'] = name
        record['CompanyNumber'] = number
        record['RegistryUrl'] = detail_url
        #print "ADDED ", name,", ", number
        batch.append(record)
        #scraperwiki.sqlite.save(['CompanyNumber'], data=record, table_name='iceland_corporate_entities', verbose=0)
        #else:
        #    print name, ", ", number, " is already in database - skipping"
            #continue
        #print record
    #print batch
    scraperwiki.sqlite.save(['CompanyNumber'], data=batch, table_name='iceland_corporate_entities', verbose=2)
    update_statement= 'update runtime_info SET last_page=' + str(last_page) + ' WHERE letter ='+ '"' + letter.decode('ISO-8859-1')+ '"'
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
        
    if root.xpath ('//ul[@class="pagnation"]/li[last()]/a/@href'):
        #next_link = root.xpath ('//ul[@class="pagnation"]/li[last()]/a/@href')
        #url = 'http://rsk.is' + next_link[0]
        next_page = int(last_page) + 1
        url = baseurl + letter
        scrape_result(url, letter, next_page)
    else:
        print
        print "DONE WITH LETTER: " + letter
        update_statement= 'update runtime_info SET last_run=' + '"' + today_date + '"' + ' WHERE letter='+ '"' + letter.decode('ISO-8859-1')+ '"'
        update_statement2= 'update runtime_info SET last_page=1 WHERE letter ='+ '"' + letter.decode('ISO-8859-1')+ '"'

        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.execute(update_statement2)
        scraperwiki.sqlite.commit()


# SCRAPE 20 MOST RECENT DAILY
def scrape_daily_result(url):
    #proxy = urllib2.ProxyHandler({'http': 'http://178.18.115.73/'})
    #opener = urllib2.build_opener(proxy)
    #urllib2.install_opener(opener)
    #html = urllib2.urlopen('http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra/').read()
    html = scraperwiki.scrape(url)


    print "PROCESSING 20 MOST RECENT ADDITIONS"
    print
    root = lxml.html.fromstring(html)
    #number = root.xpath ('//td[@class="number"]/nobr/a')
    content = root.xpath ('//div[contains(@class,"linkicons")]/*//tr/.')
    for m in content[1:]:
        record ={}
        name =  m[1].text
        name = name.encode( "ISO-8859-1" )
        number = m[0][0][0].text
        number = number.replace('-','')
        detail_url = 'http://rsk.is/ws/other/enterprisereg/' + str(number) + ".xml"
        record = process_xml(detail_url,number)
        record['CompanyName'] = name
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        record['CompanyNumber'] = number
        record['RegistryUrl'] = detail_url
        record['defunc'] = 0
        print name,", ", number
        #print record
        scraperwiki.sqlite.save(['CompanyNumber'], data=record, table_name="iceland_corporate_entities")
    print "20 latest corporations added to database."


# TIME STUFF

y1, m1, d1 = (int(x) for x in compare_date.split('-'))
y2, m2, d2 = (int(x) for x in today_date.split('-'))
 
date1 = datetime.date(y1, m1, d1)
date2 = datetime.date(y2, m2, d2)
 
dateDiff = date2 - date1

# ----------------------------------

# DAILY RUN - EITHER A SMALL ONE (FETCHING 20 LATES ADDITIONS) OR A BIG ONE (PROCESSING EVERY CORPORATION)

print 'Last big run was %d days ago' % dateDiff.days
if int(dateDiff.days) < days_between_big_run:
    print "Nothing big to do today. Next big run in" , 3 - dateDiff.days, " day(s)"
    print 
    print "Fetch 20 latest daily additions"
    scrape_daily_result('http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra')
    print "Done for today. See you tomorrow"
else:
    print 'Big run is scheduled for now. First fetch 20 latest daily additions'
    print "Fetch 20 lates daily additions"
    scrape_daily_result('http://rsk.is/fyrirtaekjaskra/thjonusta/nyskra')

    # SELECTION OF LETTERS FOR BIG RUN TO SCRAPE
    print
    print "BIG RUN COMMENCING:"
    print
    #info = scraperwiki.sqlite.select("count() from iceland_corporate_entities")
    #print "There are " + str(info[0]['count()']) + " entries in the database"
    print
    selection_statement = '* from runtime_info where letter <> ' + '"' + 'all' + '"'
    #selection_statement = '* from runtime_info where letter =2' #----- TEST STATEMENT
    letter = scraperwiki.sqlite.select(selection_statement)

    for letter in letter:
        compare_date = letter['last_run']
        y1, m1, d1 = (int(x) for x in compare_date.split('-'))
        y2, m2, d2 = (int(x) for x in today_date.split('-'))
        date1 = datetime.date(y1, m1, d1)
        date2 = datetime.date(y2, m2, d2)
        dateDiff = date2 - date1
        if int(dateDiff.days) < days_between_big_run:
            print
            print "The letter", letter['letter'],  " is up to date. On to the next one"
        else:
            print
            print "THE LETTER", letter['letter'],  " IS NOT UP TO DATE. LETS PROCESS IT."
            last_page = letter['last_page']
            letter = letter['letter']

            letter = letter.encode( "ISO-8859-1" )
            url = baseurl + letter
            scrape_result(url, letter, last_page)
    print
    update_statement= 'update runtime_info SET last_run=' + '"' + today_date + '"' + ' WHERE letter='+ '"' + 'all' + '"'
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    print 'The big run is finished. Quitting for today. See you tomorrow.'

