# -*- coding: utf-8 -*
#opencorporates Utah - usa

import scraperwiki,re
import string
import lxml.html
import urllib2
import time


########## - stolen from here: http://www.python-forum.org/pythonforum/viewtopic.php?f=2&t=21333
def succ(word=''):
    ''' Takes a string, and returns the next successive value. '''
    parts = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
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
#################

id_number_regex = re.compile(".*=(\d.*)")



#first page with all results (% wildcard):
#starturl = 'https://secure.utah.gov/bes/action/searchresults?name=%25&type=beginning&pageNo='
starturl = 'https://secure.utah.gov/bes/action/searchresults?name='


# https://secure.utah.gov/bes/action/searchresults?track=3&name=%25&pageNo=100
#https://secure.utah.gov/bes/action/searchresults?name=%25&pageNo=300

#Runtime info setup:
#record = {}
#record ['lastPageNo'] = '0'
#record ['lastSequence'] = 'aaa'
#scraperwiki.sqlite.save(['lastSequence'], data=record, table_name='runtime_info')
#exit()

def scrape(lastSeq,lastPageNo):
    print '*** Now doing sequence: ' + lastSeq + ' and result page: ' + str(lastPageNo)
    try:
        resp = urllib2.urlopen(starturl + str(lastSeq)+'&type=beginning&pageNo='+str(lastPageNo),'20')
        html = resp.read()
    except urllib2.HTTPError, error:
        print 'The server could  not fulfill the request.'
        print 'Error code: ', error.code
    except URLError, error:
        print 'We failed to reach a server.'
        print 'Reason: ', error.reason
    root = lxml.html.fromstring(html)
    #results = root.xpath('//div[@class="entities"]/.')    
    #print root.cssselect("div.entityRow")
    #print len(results)
    #print results
    data = []
    for tr in root.cssselect("div.entityRow"):
        record = {}
        record['name'] = tr[0].text_content()
        record['status'] = tr[1][0].text_content()
        record['type'] = tr[1][1].text_content()
        record['city'] = tr[1][2].text_content()
        detail_url = tr[2][0].get('href')
        record['detail_url'] = 'https://secure.utah.gov' + detail_url
        id_number = id_number_regex.findall(detail_url)
        record['id_number'] = id_number[0]
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        data.append(record)
    scraperwiki.sqlite.save(['name', 'id_number'], data=data, table_name='us_utah_corporate_entities')
    print 'processed resultpage for sequence: ',lastSeq,' and result page ', str(lastPageNo)
    update_statement= 'update runtime_info SET lastPageNo=' + str(lastPageNo) + ' WHERE lastsequence='+ '"' + lastSeq+ '"'
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    if root.xpath('/html/body/div/div/form/div/div/a[contains(text(), ">>")]'): #avoid the expensive // xpath operator
        #print 'there is a next page to do'
        next_int = int(lastPageNo)+1
        #print 'get results: ', next_int, '-', next_int+50
        #time.sleep(2) #sleep for 2 sec - a desperate attempt to avoid 500 errors from the server
        
        scrape(lastSeq,str(next_int))  


selection_statement = '* from runtime_info'
last_sequence = scraperwiki.sqlite.select(selection_statement)
for last in last_sequence:
    last_seq = last['lastSequence']
    last_PageNo = last['lastPageNo']
print 'Last sequence done: "',last_seq, '" and last result page done ', last_PageNo
#scrape(str(next_int))

while (last_seq != 'aaaa'):
    #print 'ekki enn', last_seq
    scrape(str(last_seq),int(last_PageNo)+1)
    update_statement= 'update runtime_info SET lastPageNo=0 AND lastsequence='+ '"' + last_seq + '"'
    scraperwiki.sqlite.execute(update_statement)
    scraperwiki.sqlite.commit()
    lastPageNo = 0

    last_seq = succ(last_seq)

#restart when done with all sequences
#update_statement= 'update runtime_info SET lastPageNo=0 AND lastsequence="aaa"'
#scraperwiki.sqlite.execute(update_statement)
#scraperwiki.sqlite.commit()



