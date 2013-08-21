import scraperwiki
import string
import requests
import lxml.html
import re
import time

id_number_regex = re.compile(".*=(\d.*)")
total_number_regex = re.compile(".*Total Results: (\d+).*")
swutils = scraperwiki.utils.swimport('swutils')

#Runtime info setup:
'''
#letters
scraperwiki.sqlite.save_var('lastPageNo', 0)
scraperwiki.sqlite.save_var('lastSequence', 'aaa') 
#numbers
scraperwiki.sqlite.save_var('lastNumberPageNo', 0)
scraperwiki.sqlite.save_var('lastNumberSequence', '0')
#punctuation
scraperwiki.sqlite.save_var('lastPunctuationPageNo', 0)
scraperwiki.sqlite.save_var('lastPunctuationSequence', '?\\!?')
exit()
'''

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

starturl = 'https://secure.utah.gov/bes/action/searchresults?name='

def scrape(runtype,lastSeq,lastPageNo):
    if runtype == 'letters':
        scraperwiki.sqlite.save_var('lastSequence', lastSeq)
        scraperwiki.sqlite.save_var('lastPageNo', lastPageNo)
    if runtype == 'numbers':
        scraperwiki.sqlite.save_var('lastNumbersSequence', lastSeq)
        scraperwiki.sqlite.save_var('lastNumbersPageNo', lastPageNo)
    if runtype == 'punctuation':
        scraperwiki.sqlite.save_var('lastPunctuationSequence', lastSeq)
        scraperwiki.sqlite.save_var('lastPunctuationPageNo', lastPageNo)

    print '*** Now doing sequence: ' + lastSeq + ' and result page: ' + str(lastPageNo)
    response = requests.get(starturl + str(lastSeq)+'&type=beginning&pageNo='+str(lastPageNo),verify=False,headers=user_agent)
    html = response.text    
    root = lxml.html.fromstring(html)
    try:
        total_results = total_number_regex.findall(html)[0]
    except IndexError:
        return
    until = int(round(round(int(total_results)/float(50))/2))+1
    #print total_results
    #print until
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
        try:
            record['id_number'] = id_number[0]
        except:
            continue
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        data.append(record)
    scraperwiki.sqlite.save(['name', 'id_number'], data=data, table_name='us_utah_corporate_entities')
    #print 'processed resultpage for sequence: ',lastSeq,' and result page ', str(lastPageNo)
    
    if root.xpath('/html/body/div/div/form/div/div/a[contains(text(), ">>")]'): #avoid the expensive // xpath operator
        #print 'there is a next page to do'
        next_int = int(lastPageNo)+1
        #print 'get results: ', next_int, '-', next_int+50
        #time.sleep(2) #sleep for 2 sec - a desperate attempt to avoid 500 errors from the server
        if next_int == until:
            return()
        scrape(runtype,lastSeq,str(next_int))  

user_agent = swutils.get_user_agent(browser_type='mobile') # get a mobile user agent - less overhead

def letters():
    selection_statement = '* from runtime_info'
    last_seq = scraperwiki.sqlite.get_var('lastSequence')
    last_PageNo = scraperwiki.sqlite.get_var('lastPageNo')
    print 'Last sequence done: "',last_seq, '" and last result page done ', last_PageNo
    if len(succ(last_seq)) == 4:
        print 'Done with letters - resetting'
        done()
    
    while len(succ(last_seq)) !=4:
        scrape('letters',str(last_seq),int(last_PageNo))
        print 'Done with ', str(last_seq)   
        #scraperwiki.sqlite.save_var('lastSequence', last_seq)
        #scraperwiki.sqlite.save_var('lastPageNo', 0) 
        last_PageNo = 0
        last_seq = succ(last_seq)

def numbers(): 

    numbers = range(0,10)
    lastPageNoNumber = 0
    for n in numbers:
        scrape('numbers',str(n),int(lastPageNoNumber))
        print 'Done with ', str(n)   
        #scraperwiki.sqlite.save_var('lastSequence', last_seq) 
        lastPageNoNumber = 0
        #last_seq = succ(last_seq)


def punctuation():
    last_seq = scraperwiki.sqlite.get_var('lastPunctuationSequence')
    last_PageNo = scraperwiki.sqlite.get_var('lastPunctuationPageNo')
    print 'Last sequence done: "',last_seq, '" and last result page done ', last_PageNo
    # set up the strings
    parts = []
    #for x in string.punctuation:
    #    parts.append(x)
    parts = ['"!"','"-"','"="','"&"']
    print parts
    #newparts = []
    #for p in parts:
    #    app = '"'+p+'"'
    #    newparts.append(app)
    #if last_seq == '?\!?':
    #print newparts
    for n in parts:
        scrape('punctuation',str(n),int(last_PageNo))
        print n
        
        print 'Done with ', str(n)   
            #scraperwiki.sqlite.save_var('lastSequence', last_seq)
            #scraperwiki.sqlite.save_var('lastPageNo', 0) 
        last_PageNo = 0
            #last_seq = succ(last_seq)
            #scraperwiki.sqlite.save_var('lastPunctuationPageNo', 0)
            #scraperwiki.sqlite.save_var('lastPunctuationSequence', n)
        #print n[0]
        #last_seq = n
    #lastPageNoNumber = 0
    #for n in newparts:
        #try:
         #   scrape(str(n),int(lastPageNoNumber))
        #except:
        #    pass
        #print 'Done with ', str(n)   
        #scraperwiki.sqlite.save_var('lastSequence', last_seq) 
        #lastPageNoNumber = 0
        #last_seq = succ(last_seq)

def done():
    print 'all done'
    scraperwiki.sqlite.save_var('lastPageNo', 0)
    scraperwiki.sqlite.save_var('lastSequence', 'aaa') 

#punctuation()
#numbers()
letters()
numbers()
