#from __future__ import division
import scraperwiki
import mechanize
import lxml.html
import re
import urllib
import time
import string


# RUNTIME INFO SETUP
'''
alphabet = list(string.ascii_lowercase) + list(string.digits) + ['"',"'",'.']
scraperwiki.sqlite.execute("drop table if exists runtime_info")
letters = ['"', "'", '.','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
count = 1
for letter in letters:
    record = {}
    record ['letter'] = letter
    record ['value'] = count
    record ['done'] = '0'
    print record
    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info') 
    count = count + 1
exit()
'''
#select replace(' sd d ',' ','')
#all = scraperwiki.sqlite.select('replace("CompanyNumber"," ","") from malta_companies')

#for a in all:
#    print a
    
# - Definition til að extracta streng ef við vitum tákn til beggja hliða

def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

b = mechanize.Browser()
b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
l = range(21, 1000, 10)

def process_companies(response,letter,page):
    root = lxml.html.fromstring(response)
    #print lxml.html.tostring(root)
    results = root.xpath ('//tr[contains(@class,"rgRow")]/.| //tr[contains(@class,"rgAltRow")]/.')
    print 'Processing: ', letter, 'page: ', page
    if results:
        for tr in results:
            record = {}
            record['CompanyName'] = tr[0].text
            record['CompanyNumber'] = tr[1].text
            record['CompanyAddress'] = tr[2].text
            record['CompanyLocality'] = tr[3].text
            record['CompanyComment'] = tr[4].text
            record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())

            scraperwiki.sqlite.save(['CompanyNumber'], data=record, table_name='malta_companies')

        for link in b.links(url_regex ='javascript:'):          
            if re.search("rgCurrentPage", str(link.attrs)):
                next_page_to_do = int(link.text) + 1
        try:
            if next_page_to_do == 11:
                next_link_to_do = b.find_link(text_regex='\.\.\.', nr = 0)
            elif next_page_to_do in l:
                next_link_to_do = b.find_link(text_regex='\.\.\.', nr = 1)
            else:
                next_link_to_do = b.find_link(text=str(next_page_to_do))

            eventtarget = extract(next_link_to_do.url, "javascript:__doPostBack('","','')")
            b.select_form(name="aspnetForm")
            b.form.set_all_readonly(False)
            b.form['__EVENTTARGET'] = eventtarget
            b.form['__EVENTARGUMENT'] = ''
            response = b.submit().read()
            process_companies(response,letter,next_page_to_do)
        except:
            letter = letter.replace("\\",'')
            print "NO MORE PAGES FOR LETTER: ", letter
            if letter == "'":
                update_statement= 'update runtime_info SET done=1 WHERE letter='+ '"'+ letter + '"'
            else:
                update_statement= "update runtime_info SET done=1 WHERE letter="+ "'"+ letter + "'"
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            return
    else:
        letter = letter.replace("\\",'')
        print "No companies begin with the letter: ", letter
        if letter == "'":
            update_statement= 'update runtime_info SET done=1 WHERE letter='+ '"'+ letter + '"'
        else:
            update_statement= "update runtime_info SET done=1 WHERE letter="+ "'"+ letter + "'"
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        
def get_letter_start_page(letter,value):
    page = '1'
    print 'Processing first page of companies starting with letter: ', letter
    b.select_form(name="aspnetForm")
    b.form.set_all_readonly(False)
    b.form['__EVENTTARGET'] = 'ctl00$cphMain$RadComboBoxFirstLetter'
    b.form['ctl00$cphMain$RadComboBoxFirstLetter'] =  str(letter)
    b.form['__EVENTARGUMENT'] = '{"Command":"Select","Index":' + str(value) + '}'
    b.form['ctl00_cphMain_RadComboBoxFirstLetter_ClientState'] = '{"logEntries":[],"value":"' +  str(letter) +'","text":"' + str(letter) + '","enabled":true}'

    response = b.submit().read()

    root = lxml.html.fromstring(response)
    number_of_results = root.xpath ('//div[contains(@class,"rgWrap rgInfoPart")]/*/text()')
    #print number_of_results
    if number_of_results:
        b.select_form(name="aspnetForm")
        b.form.set_all_readonly(False)
        b.form['ctl00$cphMain$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox'] = '50'
        b.form['ctl00_cphMain_RadGrid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState'] = '{"logEntries":[],"value":"50","text":"50","enabled":true}'
        b.form['__EVENTTARGET'] = 'ctl00$cphMain$RadGrid1'
        b.form['__EVENTARGUMENT'] = 'cFireCommand:ctl00$cphMain$RadGrid1$ctl00;PageSize;50'
        response = b.submit().read()
        #newroot = lxml.html.fromstring(response)
        #number_of_results = newroot.xpath ('//div[contains(@class,"rgWrap rgInfoPart")]/*/text()')
        #print 'There are ', number_of_results[0], ' companies in ', number_of_results[1], ' pages'
        process_companies(response,letter,page)
    else:
        print 'There is only one result page with companies starting with letter: ', letter
        process_companies(response,letter,page)

def do_big_run():
    # LIST OF PAGENUMBERS WHO NEED SPECIAL PROCESSING
    #l = range(21, 1000, 10)
#    b = mechanize.Browser()
#    b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
#    b.open("http://rocsupport.mfsa.com.mt/pages/SearchCompanyInformation.aspx")
    response = b.response().read()
    root = lxml.html.fromstring(response)

    # GET A DICTIONARY OF STARTING LETTERS TO ITERATE THROUGH
    selection_statement = '* from runtime_info where done=0'
    letters = scraperwiki.sqlite.select(selection_statement)
    if letters:
        for key in letters:
            letter = key['letter']
            value = key['value']
            # PROCESS EACH LETTER
            if letter == '"':
                letter = '\\'+letter
            get_letter_start_page(letter, value)
    else:
        print "All done - let's drop runtime_info table to start again next time"
        scraperwiki.sqlite.execute("drop table if exists runtime_info")
        letters = ['"', "'", '.','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        count = 1
        for letter in letters:
            record = {}
            record ['letter'] = letter
            record ['value'] = count
            record ['done'] = '0'
            print record
            scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info') 
            count = count + 1


b = mechanize.Browser()
b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
b.open("http://rocsupport.mfsa.com.mt/pages/SearchCompanyInformation.aspx")

do_big_run()
#from __future__ import division
import scraperwiki
import mechanize
import lxml.html
import re
import urllib
import time
import string


# RUNTIME INFO SETUP
'''
alphabet = list(string.ascii_lowercase) + list(string.digits) + ['"',"'",'.']
scraperwiki.sqlite.execute("drop table if exists runtime_info")
letters = ['"', "'", '.','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
count = 1
for letter in letters:
    record = {}
    record ['letter'] = letter
    record ['value'] = count
    record ['done'] = '0'
    print record
    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info') 
    count = count + 1
exit()
'''
#select replace(' sd d ',' ','')
#all = scraperwiki.sqlite.select('replace("CompanyNumber"," ","") from malta_companies')

#for a in all:
#    print a
    
# - Definition til að extracta streng ef við vitum tákn til beggja hliða

def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

b = mechanize.Browser()
b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
l = range(21, 1000, 10)

def process_companies(response,letter,page):
    root = lxml.html.fromstring(response)
    #print lxml.html.tostring(root)
    results = root.xpath ('//tr[contains(@class,"rgRow")]/.| //tr[contains(@class,"rgAltRow")]/.')
    print 'Processing: ', letter, 'page: ', page
    if results:
        for tr in results:
            record = {}
            record['CompanyName'] = tr[0].text
            record['CompanyNumber'] = tr[1].text
            record['CompanyAddress'] = tr[2].text
            record['CompanyLocality'] = tr[3].text
            record['CompanyComment'] = tr[4].text
            record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())

            scraperwiki.sqlite.save(['CompanyNumber'], data=record, table_name='malta_companies')

        for link in b.links(url_regex ='javascript:'):          
            if re.search("rgCurrentPage", str(link.attrs)):
                next_page_to_do = int(link.text) + 1
        try:
            if next_page_to_do == 11:
                next_link_to_do = b.find_link(text_regex='\.\.\.', nr = 0)
            elif next_page_to_do in l:
                next_link_to_do = b.find_link(text_regex='\.\.\.', nr = 1)
            else:
                next_link_to_do = b.find_link(text=str(next_page_to_do))

            eventtarget = extract(next_link_to_do.url, "javascript:__doPostBack('","','')")
            b.select_form(name="aspnetForm")
            b.form.set_all_readonly(False)
            b.form['__EVENTTARGET'] = eventtarget
            b.form['__EVENTARGUMENT'] = ''
            response = b.submit().read()
            process_companies(response,letter,next_page_to_do)
        except:
            letter = letter.replace("\\",'')
            print "NO MORE PAGES FOR LETTER: ", letter
            if letter == "'":
                update_statement= 'update runtime_info SET done=1 WHERE letter='+ '"'+ letter + '"'
            else:
                update_statement= "update runtime_info SET done=1 WHERE letter="+ "'"+ letter + "'"
            scraperwiki.sqlite.execute(update_statement)
            scraperwiki.sqlite.commit()
            return
    else:
        letter = letter.replace("\\",'')
        print "No companies begin with the letter: ", letter
        if letter == "'":
            update_statement= 'update runtime_info SET done=1 WHERE letter='+ '"'+ letter + '"'
        else:
            update_statement= "update runtime_info SET done=1 WHERE letter="+ "'"+ letter + "'"
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        
def get_letter_start_page(letter,value):
    page = '1'
    print 'Processing first page of companies starting with letter: ', letter
    b.select_form(name="aspnetForm")
    b.form.set_all_readonly(False)
    b.form['__EVENTTARGET'] = 'ctl00$cphMain$RadComboBoxFirstLetter'
    b.form['ctl00$cphMain$RadComboBoxFirstLetter'] =  str(letter)
    b.form['__EVENTARGUMENT'] = '{"Command":"Select","Index":' + str(value) + '}'
    b.form['ctl00_cphMain_RadComboBoxFirstLetter_ClientState'] = '{"logEntries":[],"value":"' +  str(letter) +'","text":"' + str(letter) + '","enabled":true}'

    response = b.submit().read()

    root = lxml.html.fromstring(response)
    number_of_results = root.xpath ('//div[contains(@class,"rgWrap rgInfoPart")]/*/text()')
    #print number_of_results
    if number_of_results:
        b.select_form(name="aspnetForm")
        b.form.set_all_readonly(False)
        b.form['ctl00$cphMain$RadGrid1$ctl00$ctl03$ctl01$PageSizeComboBox'] = '50'
        b.form['ctl00_cphMain_RadGrid1_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState'] = '{"logEntries":[],"value":"50","text":"50","enabled":true}'
        b.form['__EVENTTARGET'] = 'ctl00$cphMain$RadGrid1'
        b.form['__EVENTARGUMENT'] = 'cFireCommand:ctl00$cphMain$RadGrid1$ctl00;PageSize;50'
        response = b.submit().read()
        #newroot = lxml.html.fromstring(response)
        #number_of_results = newroot.xpath ('//div[contains(@class,"rgWrap rgInfoPart")]/*/text()')
        #print 'There are ', number_of_results[0], ' companies in ', number_of_results[1], ' pages'
        process_companies(response,letter,page)
    else:
        print 'There is only one result page with companies starting with letter: ', letter
        process_companies(response,letter,page)

def do_big_run():
    # LIST OF PAGENUMBERS WHO NEED SPECIAL PROCESSING
    #l = range(21, 1000, 10)
#    b = mechanize.Browser()
#    b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
#    b.open("http://rocsupport.mfsa.com.mt/pages/SearchCompanyInformation.aspx")
    response = b.response().read()
    root = lxml.html.fromstring(response)

    # GET A DICTIONARY OF STARTING LETTERS TO ITERATE THROUGH
    selection_statement = '* from runtime_info where done=0'
    letters = scraperwiki.sqlite.select(selection_statement)
    if letters:
        for key in letters:
            letter = key['letter']
            value = key['value']
            # PROCESS EACH LETTER
            if letter == '"':
                letter = '\\'+letter
            get_letter_start_page(letter, value)
    else:
        print "All done - let's drop runtime_info table to start again next time"
        scraperwiki.sqlite.execute("drop table if exists runtime_info")
        letters = ['"', "'", '.','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        count = 1
        for letter in letters:
            record = {}
            record ['letter'] = letter
            record ['value'] = count
            record ['done'] = '0'
            print record
            scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info') 
            count = count + 1


b = mechanize.Browser()
b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
b.open("http://rocsupport.mfsa.com.mt/pages/SearchCompanyInformation.aspx")

do_big_run()
