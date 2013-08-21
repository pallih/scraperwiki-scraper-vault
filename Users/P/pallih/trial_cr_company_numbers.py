# -*- coding: iso-8859-2 -*-
import scraperwiki
import mechanize
import lxml.html
import re
import itertools
import calendar,datetime
import time

# DICTIONARY OF START DATE AND END DATE FOR EACH MONTH FROM 1994. DATES ARE FROM 1-10, 11-19 AND 20-END OF MONTH
# THAT SHOULD TAKE CARE OF THE LIMIT THE APPLICATION IMPOSES ON RETURNED RECORDS FROM THE SEARCH (1000)
# IT ALSO SLOWS US DOWN ...

#years = range(1994,2012)
#months = range (1,13)
#for year in years:

#    for month in months:
#        monthdict = {}

#        lastday1 = calendar.monthrange(year, month)
#        lastday2=datetime.date(year,month,lastday1[1])
#        lastday3 = datetime.datetime.strptime(str(lastday2), "%Y-%m-%d").strftime("%d.%m.%Y")
#        firstday1 = '01.' + str(month) + '.' + str(year)
#        lastday4 = '19.' + str(month) + '.' + str(year)

#        firstday2 = '20.' + str(month) + '.' + str(year)
#        firstday3 = '11.' + str(month) + '.' + str(year)
#        middleday = '10.' + str(month) + '.' + str(year)
#        monthdict['range'] = firstday1 + ' - ' + middleday
#        monthdict['scraped'] = '0'
#        scraperwiki.sqlite.save(['range'], data=monthdict, table_name='month_span')
#        monthdict = {}

#        monthdict['range'] = firstday2 + ' - ' + lastday3
#        monthdict['scraped'] = '0'
#        scraperwiki.sqlite.save(['range'], data=monthdict, table_name='month_span')
#        monthdict = {}

#        monthdict['range'] = firstday3 + ' - ' + lastday4
#        monthdict['scraped'] = '0'
#        scraperwiki.sqlite.save(['range'], data=monthdict, table_name='month_span')


# REPLACE 'bankrupt' in Company name
#select = scraperwiki.sqlite.select("* from croatia_corporate_entities WHERE CompanyName LIKE '%u stečaju'")
#print len(select)
#for s in select:
#    companyname = s['CompanyName']
#    companyname2 = re.sub('u ste.*', '', companyname)
#    update_statement= 'update croatia_corporate_entities SET CompanyName="'+companyname2+'" WHERE CompanyName LIKE "' +companyname + '"'
#    scraperwiki.sqlite.execute(update_statement)
#scraperwiki.sqlite.commit()
#exit()


#for s in select:
#    companynumber = s['CompanyNumber']
#    CompanyContact = s['RegistryUrl']
#    update_statement= 'update croatia_corporate_entities SET CompanyContact="" WHERE companynumber='+ '"' + companynumber + '"'
#    scraperwiki.sqlite.execute(update_statement)
#    scraperwiki.sqlite.commit()
#exit()





url = 'http://www1.biznet.hr/HgkWeb/do/advsearch'


def process_and_save(results):
    for tr in results:
        record = {}
        CompanyName = ' '.join(tr[2][0].text_content().split())
        if re.search('u ste.*', CompanyName):
            CompanyName = re.sub('u ste.*', '', CompanyName)
        CompanyNumber = ' '.join(tr[1].text_content().split())
        RegistryUrl= ''.join(tr[2][0].get('href').split())
        RegistryUrl = 'http://www1.biznet.hr' + RegistryUrl
        CompanyCounty = ' '.join(tr[3].text_content().split())
        CompanyAddress = ' '.join(tr[4].text_content().split())
        CompanyTelephone =  ' '.join(tr[5].text_content().split())
        CompanyTelefax = ''.join(tr[6].text_content().split())
        CompanyEmail = ' '.join(tr[7].text_content().split())
        CompanyContact = ' '.join(tr[8].text_content().split())
        if CompanyContact == '- -, Bez podataka':
            CompanyContact = ''
        record['CompanyName'] = CompanyName
        record['CompanyNumber'] = CompanyNumber
        record['RegistryUrl'] = RegistryUrl
        record['CompanyCounty'] = CompanyCounty
        record['CompanyAddress'] = CompanyAddress
        record['CompanyTelephone'] = CompanyTelephone
        record['CompanyTelefax'] = CompanyTelefax
        record['CompanyEmail'] = CompanyEmail
        record['CompanyContact'] = CompanyContact
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())

        #print record

        scraperwiki.sqlite.save(['CompanyNumber'], data=record, table_name='croatia_corporate_entities')


def scrape_result(response, range, page):
    response = response.decode('iso-8859-2') #THIS IS NEEDED FOR LXML TO PROPERLY REPRESENT UNICODE - TOOK ME AGES TO FIND THIS OUT ...

    root = lxml.html.fromstring(response)
    print "Processing page: " + str(page)
    if not re.search('No entity found matching requested criteria', response) == None:
        print 'No results. Onwards!'
        #update_statement= 'update month_span SET scraped=1 WHERE range='+ '"' + range + '"'
        #scraperwiki.sqlite.execute(update_statement)
        #scraperwiki.sqlite.commit()
        return
    
    numbers = root.xpath ('//td[contains(@class,"def_srednji_tekst")][1]/text()[7]')[0]
    check = re.findall(r'\d+', numbers)
    print numbers
    #We skipped the results that were more than 1000 (since the system only returns 1000)
    if int(check[0]) > 999:
        print "Too many results (" + str(check[0]) + "). Skipping for now. Will deal with at the end."
        return

            
    results = root.xpath ('//tr[contains(@bgcolor,"#efefef")]/.| //tr[contains(@bgcolor,"#ffffff")]/.')

    process_and_save(results)

    next_page_url = root.xpath ('//td[contains(@class,"naglaseni_tekst")]/a[text()="Next >> "]/@href')
    if next_page_url:
        response1 = br.follow_link(text_regex=r"Next", nr=0)
        page = int(page) + 1
        response1 = response1.read()
        scrape_result(response1,range,page)
    else:
        print "Done with this section"
        #update_statement= 'update month_span SET scraped=1 WHERE range='+ '"' + range + '"'
        #scraperwiki.sqlite.execute(update_statement)
        #scraperwiki.sqlite.commit()


# ----------------------------------
# HERE IS THE BIG RUN START

#selection_statement = '* from month_span where scraped =0' # ' + '"' + 'all' + '"'
#todo = scraperwiki.sqlite.select(selection_statement)
#
#if len(todo) == 0:
#    print "Nothing to do"
#
#for item in todo:
#
#    start = item['range'].partition(' - ')[0]
#    end = item['range'].partition(' - ')[2]
#
#    br = mechanize.Browser()
#    br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
#    response = br.open(url)
#    response1 = br.follow_link(text_regex=r"poslovnih", nr=0)
#    response2 = br.follow_link(nr=1)
#    response2 = br.follow_link(nr=0)
#    br.select_form("advsearch")
#    br.form.set_all_readonly(False)
#    br.form['tvrtkeTip'] = ["1"] # we want all companies
#    br.form['limit'] = '1000' #1000 seems to be the max number of results returned
#    br.form['datRegOd'] = start
#    br.form['datRegDo'] = end
#    print ' Fetching: ' + item['range']
#    response = br.submit().read()
#    page = '1'
#    scrape_result(response, item['range'], page)

# ------------------------

# DAILY RUN - FETCH LAST 30 DAYS

base = datetime.datetime.today()
dateList = [ base - datetime.timedelta(days=x) for x in range(0,30) ]
print dateList
start_date = dateList[29].strftime("%d.%m.%Y") 
end_date = dateList[0].strftime("%d.%m.%Y")
#start_date = '15.09.2011' 
#end_date = '01.10.2011' 
range = start_date + ' - ' + end_date
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
response = br.open(url)
response1 = br.follow_link(text_regex=r"poslovnih", nr=0)
response2 = br.follow_link(nr=1)
response2 = br.follow_link(nr=0)
br.select_form("advsearch")
br.form.set_all_readonly(False)
br.form['tvrtkeTip'] = ["1"] # we want all companies
br.form['limit'] = '1000' #1000 seems to be the max number of results returned
br.form['datRegOd'] = start_date
br.form['datRegDo'] = end_date
print ' Fetching: ' + range
response = br.submit().read()
page = '1'
scrape_result(response, range, page)
