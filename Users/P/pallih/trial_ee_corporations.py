# -*- coding: iso-8859-4 -*


#opencorporates Estonia

import scraperwiki,re
#from lxml import etree
import lxml.html
import mechanize
import re
import urllib
import time
import datetime
import random



# syntax for search: https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&nimi=*a*&rkood=&qs=20

#nimi = searchword
#lang = language
#qs = page (increment by 10, 0 is first)
#rkood = number

# wildcards supported are '*' and '%' for one or more characters and '_' for one character


# syntax for detail pages: https://ariregister.rik.ee/ettevotja.py?id=6000000642&lang=eng

# id is the code number given in the javascript url - it does not correspond to the "commercial registry code" number in search results nor the "Number of business register" - it seems to be some internal number



b = mechanize.Browser()
b.set_handle_robots(False)
b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Estonian alphabet
#alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'Š', 'Z', 'Ž', 'T', 'U', 'V', 'W', 'Õ', 'Ä', 'Ö', 'Ü', 'X', 'Y']
#for x in alphabet:
#    record = {}
#    record['letter'] = x
#    record['last_page_qs'] = '0'
#    record['done_date'] = '2011-04-22'
#    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')

#exit()
#baseurl = 'https://ariregister.rik.ee/lihtparing.py'

#url = 'https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&nimi=*v*'

days_between_big_run = int(0)
today_date = str(datetime.date.today())


def process_results(url,qs,letter):
    gotourl = url + '&qs=' + str(qs)
    #gotourl = 'https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&nimi=*' + letter + '*' + '&qs=' + qs
    record = {}
    b.open(gotourl)
    response = b.response().read()
    root = lxml.html.fromstring(response)
    while True:
        try:
            b.select_form("navform")
            number_of_results = root.xpath('//span[contains(@class,"batch_count")]')
            print number_of_results[0].text
            results = root.xpath ('//table[contains(@class,"tbl_listing")]/tr[position()>1]/.')
            for x in results:
                record['name'] = x[1].text_content()
                if x[1][0].attrib:
                    record['url']= 'https://ariregister.rik.ee/ettevotja.py?id=' + filter(lambda x: x.isdigit(), x[1][0].attrib['href'].split(',')[1])
                else:
                    record['url'] ='n/a'
                record['invalid names'] =  x[2].text_content().strip()
                record['code'] = x[3].text_content().strip()
                record['entrydate'] = x[4].text_content().strip()
                record['status'] = x[5].text_content().strip()
                record['area'] = x[6].text_content().strip()
                record['address'] = x[7].text_content().strip()
                record['capital'] = x[8].text_content().strip() 
                record['webpage'] = x[9].text_content().strip()
            #print record
                scraperwiki.sqlite.save(['code'], data=record, table_name='estonia_corporate_entities')
            update_statement= 'update runtime_info SET last_page_qs=' + '"' + qs + '"' + ' WHERE letter='+ '"' + letter.decode('utf-8')+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            print 'Sleep 4'
            time.sleep(4)
            next_page_link = root.xpath("//a[re:match(text(), 'Next')]", namespaces={"re": "http://exslt.org/regular-expressions"})
            if next_page_link:
                current_page = root.xpath('//span[contains(@class,"bb")]')
                page = current_page[0].text
                qs_value = page + '0'
                qs_value_current = int(qs_value) - 10
                print "Done with page: " + str(page) + ' of letter ' + letter
                for x in next_page_link:
                    #print 'next page url: ' + url + '&qs=' + filter(lambda x: x.isdigit(),x.attrib['href'].replace("javascript:nav_navform3",''))
                    next_page_url = url + '&qs=' + filter(lambda x: x.isdigit(),x.attrib['href'].replace("javascript:nav_navform3",''))
                    #time.sleep(7 * random.random()) #sleep to try to stop the evil captcha from appearing ...
                    process_results(url,str(qs_value),letter)
            else:
                print "No more results for letter: ", letter
                print "--------------"
                update_statement1= 'update runtime_info SET done_date=' + '"' + today_date + '"' + ' WHERE letter='+ '"' + letter.decode('utf-8')+ '"'
                update_statement2= 'update runtime_info SET last_page_qs="0" WHERE letter='+ '"' + letter.decode('utf-8')+ '"'
                scraperwiki.sqlite.execute(update_statement1)
                scraperwiki.sqlite.execute(update_statement2)
                scraperwiki.sqlite.commit()
                #yield
        except:
            print "Got the CAPTCHA - let's bypass it"
            print response
            #print 'Sleep 30'
            #time.sleep(30)
            b._factory.is_html = True
            b.select_form("captcha_form")
            b.form.set_all_readonly(False)
            b.form['sess'] = '6954515375905017851567245797948813358345085625982119809575056054' # Session number for CAPTCHA
            b.form['_captcha_text_session'] = 'E63B 8C59' # CAPTCHA solution
            response = b.submit().read()
            print response
        break
    #print "here we are after WHILE"
# START

#selection_statement = '* from runtime_info where letter="Ž"'
selection_statement = '* from runtime_info'
letter = scraperwiki.sqlite.select(selection_statement)
random.shuffle(letter)

for letter in letter:
        compare_date = letter['done_date']
        qs = letter['last_page_qs']
        page = int(qs) + 10
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
            letter = letter['letter']
            letter = letter.encode( 'utf-8' )
            url = 'https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&sess=2431750306592631774425558642374724758538334208075233891292197961&_captcha_text_session=FEC7+71CB&nimi=*' + letter + '*'
            print 'starting from page: ' + str(page)[:-1]            
            process_results(url,qs,letter)
            




# -*- coding: iso-8859-4 -*


#opencorporates Estonia

import scraperwiki,re
#from lxml import etree
import lxml.html
import mechanize
import re
import urllib
import time
import datetime
import random



# syntax for search: https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&nimi=*a*&rkood=&qs=20

#nimi = searchword
#lang = language
#qs = page (increment by 10, 0 is first)
#rkood = number

# wildcards supported are '*' and '%' for one or more characters and '_' for one character


# syntax for detail pages: https://ariregister.rik.ee/ettevotja.py?id=6000000642&lang=eng

# id is the code number given in the javascript url - it does not correspond to the "commercial registry code" number in search results nor the "Number of business register" - it seems to be some internal number



b = mechanize.Browser()
b.set_handle_robots(False)
b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Estonian alphabet
#alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'Š', 'Z', 'Ž', 'T', 'U', 'V', 'W', 'Õ', 'Ä', 'Ö', 'Ü', 'X', 'Y']
#for x in alphabet:
#    record = {}
#    record['letter'] = x
#    record['last_page_qs'] = '0'
#    record['done_date'] = '2011-04-22'
#    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')

#exit()
#baseurl = 'https://ariregister.rik.ee/lihtparing.py'

#url = 'https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&nimi=*v*'

days_between_big_run = int(0)
today_date = str(datetime.date.today())


def process_results(url,qs,letter):
    gotourl = url + '&qs=' + str(qs)
    #gotourl = 'https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&nimi=*' + letter + '*' + '&qs=' + qs
    record = {}
    b.open(gotourl)
    response = b.response().read()
    root = lxml.html.fromstring(response)
    while True:
        try:
            b.select_form("navform")
            number_of_results = root.xpath('//span[contains(@class,"batch_count")]')
            print number_of_results[0].text
            results = root.xpath ('//table[contains(@class,"tbl_listing")]/tr[position()>1]/.')
            for x in results:
                record['name'] = x[1].text_content()
                if x[1][0].attrib:
                    record['url']= 'https://ariregister.rik.ee/ettevotja.py?id=' + filter(lambda x: x.isdigit(), x[1][0].attrib['href'].split(',')[1])
                else:
                    record['url'] ='n/a'
                record['invalid names'] =  x[2].text_content().strip()
                record['code'] = x[3].text_content().strip()
                record['entrydate'] = x[4].text_content().strip()
                record['status'] = x[5].text_content().strip()
                record['area'] = x[6].text_content().strip()
                record['address'] = x[7].text_content().strip()
                record['capital'] = x[8].text_content().strip() 
                record['webpage'] = x[9].text_content().strip()
            #print record
                scraperwiki.sqlite.save(['code'], data=record, table_name='estonia_corporate_entities')
            update_statement= 'update runtime_info SET last_page_qs=' + '"' + qs + '"' + ' WHERE letter='+ '"' + letter.decode('utf-8')+ '"'
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            print 'Sleep 4'
            time.sleep(4)
            next_page_link = root.xpath("//a[re:match(text(), 'Next')]", namespaces={"re": "http://exslt.org/regular-expressions"})
            if next_page_link:
                current_page = root.xpath('//span[contains(@class,"bb")]')
                page = current_page[0].text
                qs_value = page + '0'
                qs_value_current = int(qs_value) - 10
                print "Done with page: " + str(page) + ' of letter ' + letter
                for x in next_page_link:
                    #print 'next page url: ' + url + '&qs=' + filter(lambda x: x.isdigit(),x.attrib['href'].replace("javascript:nav_navform3",''))
                    next_page_url = url + '&qs=' + filter(lambda x: x.isdigit(),x.attrib['href'].replace("javascript:nav_navform3",''))
                    #time.sleep(7 * random.random()) #sleep to try to stop the evil captcha from appearing ...
                    process_results(url,str(qs_value),letter)
            else:
                print "No more results for letter: ", letter
                print "--------------"
                update_statement1= 'update runtime_info SET done_date=' + '"' + today_date + '"' + ' WHERE letter='+ '"' + letter.decode('utf-8')+ '"'
                update_statement2= 'update runtime_info SET last_page_qs="0" WHERE letter='+ '"' + letter.decode('utf-8')+ '"'
                scraperwiki.sqlite.execute(update_statement1)
                scraperwiki.sqlite.execute(update_statement2)
                scraperwiki.sqlite.commit()
                #yield
        except:
            print "Got the CAPTCHA - let's bypass it"
            print response
            #print 'Sleep 30'
            #time.sleep(30)
            b._factory.is_html = True
            b.select_form("captcha_form")
            b.form.set_all_readonly(False)
            b.form['sess'] = '6954515375905017851567245797948813358345085625982119809575056054' # Session number for CAPTCHA
            b.form['_captcha_text_session'] = 'E63B 8C59' # CAPTCHA solution
            response = b.submit().read()
            print response
        break
    #print "here we are after WHILE"
# START

#selection_statement = '* from runtime_info where letter="Ž"'
selection_statement = '* from runtime_info'
letter = scraperwiki.sqlite.select(selection_statement)
random.shuffle(letter)

for letter in letter:
        compare_date = letter['done_date']
        qs = letter['last_page_qs']
        page = int(qs) + 10
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
            letter = letter['letter']
            letter = letter.encode( 'utf-8' )
            url = 'https://ariregister.rik.ee/lihtparing.py?lang=eng&search=1&sess=2431750306592631774425558642374724758538334208075233891292197961&_captcha_text_session=FEC7+71CB&nimi=*' + letter + '*'
            print 'starting from page: ' + str(page)[:-1]            
            process_results(url,qs,letter)
            




