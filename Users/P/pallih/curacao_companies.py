# opencorporate curacao

import scraperwiki
import urllib
import urllib2
import string
import lxml.html
import time
import re

#Runtime info setup:
#record = {}
#record ['searchstring'] = a
#scraperwiki.sqlite.save(['searchstring'], data=record, table_name='runtime_info')

#scraperwiki.sqlite.save(unique_keys=["search_blob"], data={"search_blob":'aa'},table_name="runtime_info")

#exit()

url = 'http://www.curacao-chamber.an/info/registry/companyselect.asp'

regex = re.compile("There is no company")

def succ(word=''):
    ''' Takes a string, and returns the next successive value. '''
    
    parts = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    last = ['']
    

    # if none of the characters are in 'A-Z', 'a-z', or '0-9',
    #   then also include symbols
    if not any(ch for ch in word for part in parts if ch in part):
        parts = [string.printable[
            string.printable.index('!'):string.printable.index(' ')+1]]
        
    for index, ch in enumerate(word[::-1]):
        for part in parts:
            if ch in part:
                last = part
                ndx = part.index(ch)+1
                complete = True
                # if there's not an overflow (9+1=overflow),
                #    immediately return
                if ndx >= len(part):
                    complete = False
                    ndx = 0
                word = word[:(index+1)*-1]+part[ndx]+word[len(word)-index:]
                if complete:
                    return word
    return last[0] + word

def process(html):
    no_results = regex.findall(html)
    if not no_results:
        root = lxml.html.fromstring(html)
        for td in root.xpath('//tr[@class="row"] | //tr[@class="altrow"]/.')[1:]:
            record = {}
            record['url'] = 'http://www.curacao-chamber.an/info/registry/' + td[0][0].get('href')
            record['tradename'] = td[0][0].text
            record['registration_number'] = td[1].text
            record['official_name'] = td[2].text
            record['address'] =  td[3].text
            record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
            scraperwiki.sqlite.save(['registration_number'], data=record, table_name='curacao-companies')
    else:
        print 'No results. Onwards!'

def do_punctuation():
    punctuation = ['"',"'",'.','#','0','1','2','3','4','5','6','7','8','9']
    for p in punctuation:
        get(p)
    scraperwiki.sqlite.execute("drop table if exists runtime_info")
    scraperwiki.sqlite.save(unique_keys=["search_blob"], data={"search_blob":'aa'},table_name="runtime_info")


def get(search_string):
    values = {'name' : '%'+str(search_string)+'%%','companyid' : '','source' : '0','languageabbrev' : 'ENG','searchbut' : 'Search'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    html = response.read()
    process(html)
    
selection_statement = '* from runtime_info'
searchstring = scraperwiki.sqlite.select(selection_statement)
search_string = searchstring[0]
search_string = search_string['search_blob']

#search_string = 'zx'

if search_string == 'aaa':
    print "Let's do punctuation and numbers"
    do_punctuation()

else:

    while (search_string != 'aaa'):
        print 'Processing string: ', search_string
        get(search_string)
        search_string = succ(search_string)
        # save search string
        update_statement= 'update runtime_info SET search_blob='+ '"' +search_string+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        



    
# opencorporate curacao

import scraperwiki
import urllib
import urllib2
import string
import lxml.html
import time
import re

#Runtime info setup:
#record = {}
#record ['searchstring'] = a
#scraperwiki.sqlite.save(['searchstring'], data=record, table_name='runtime_info')

#scraperwiki.sqlite.save(unique_keys=["search_blob"], data={"search_blob":'aa'},table_name="runtime_info")

#exit()

url = 'http://www.curacao-chamber.an/info/registry/companyselect.asp'

regex = re.compile("There is no company")

def succ(word=''):
    ''' Takes a string, and returns the next successive value. '''
    
    parts = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    last = ['']
    

    # if none of the characters are in 'A-Z', 'a-z', or '0-9',
    #   then also include symbols
    if not any(ch for ch in word for part in parts if ch in part):
        parts = [string.printable[
            string.printable.index('!'):string.printable.index(' ')+1]]
        
    for index, ch in enumerate(word[::-1]):
        for part in parts:
            if ch in part:
                last = part
                ndx = part.index(ch)+1
                complete = True
                # if there's not an overflow (9+1=overflow),
                #    immediately return
                if ndx >= len(part):
                    complete = False
                    ndx = 0
                word = word[:(index+1)*-1]+part[ndx]+word[len(word)-index:]
                if complete:
                    return word
    return last[0] + word

def process(html):
    no_results = regex.findall(html)
    if not no_results:
        root = lxml.html.fromstring(html)
        for td in root.xpath('//tr[@class="row"] | //tr[@class="altrow"]/.')[1:]:
            record = {}
            record['url'] = 'http://www.curacao-chamber.an/info/registry/' + td[0][0].get('href')
            record['tradename'] = td[0][0].text
            record['registration_number'] = td[1].text
            record['official_name'] = td[2].text
            record['address'] =  td[3].text
            record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
            scraperwiki.sqlite.save(['registration_number'], data=record, table_name='curacao-companies')
    else:
        print 'No results. Onwards!'

def do_punctuation():
    punctuation = ['"',"'",'.','#','0','1','2','3','4','5','6','7','8','9']
    for p in punctuation:
        get(p)
    scraperwiki.sqlite.execute("drop table if exists runtime_info")
    scraperwiki.sqlite.save(unique_keys=["search_blob"], data={"search_blob":'aa'},table_name="runtime_info")


def get(search_string):
    values = {'name' : '%'+str(search_string)+'%%','companyid' : '','source' : '0','languageabbrev' : 'ENG','searchbut' : 'Search'}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    html = response.read()
    process(html)
    
selection_statement = '* from runtime_info'
searchstring = scraperwiki.sqlite.select(selection_statement)
search_string = searchstring[0]
search_string = search_string['search_blob']

#search_string = 'zx'

if search_string == 'aaa':
    print "Let's do punctuation and numbers"
    do_punctuation()

else:

    while (search_string != 'aaa'):
        print 'Processing string: ', search_string
        get(search_string)
        search_string = succ(search_string)
        # save search string
        update_statement= 'update runtime_info SET search_blob='+ '"' +search_string+ '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
        



    
