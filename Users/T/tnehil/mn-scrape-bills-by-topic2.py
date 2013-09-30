import scraperwiki
import re
import json
from BeautifulSoup import BeautifulSoup

def scrape_bill_nums(chamber,topic):
    url = 'https://www.revisor.mn.gov/bills/status_result.php?body=' + chamber + '&search=basic&session=0882013&location=House&bill=&bill_type=bill&rev_number=&keyword_type=all&keyword=&keyword_field_text=1&topic%5B%5D='+topic+'&submit_topic=GO&titleword='
    
    soup = BeautifulSoup(scraperwiki.scrape(url))    
    bills = []    
    rows = soup('tr')
    for row in rows:
        contents = BeautifulSoup(str(row))
        try:
            bill = contents('td')[1].a.contents
            bills.append(str(bill[0]))
        except:
            pass
    return bills

def open_states_format(bill):
    if bill[2] == '0':
        if bill[3] == '0':
            if bill[4] == '0':
                append = " " + bill[5:]
            else:
                append = " " + bill[4:]
        else:
            append = " " + bill[3:]
        result = bill[0:2] + append
    else:
        result = bill
    return result

def get_topics_list(chamber):
    topics = []
    url = 'https://www.revisor.mn.gov/bills/status_search.php?body='+chamber
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    select = soup('select')[4] #lame, but that should be the categories select
    options = BeautifulSoup(str(select))
    for option in options('option'):
        billnumber = re.findall(r'\d+', option.contents[0])
        if billnumber == []:
            billnumber = 0
        else:
            billnumber = int(billnumber[0])
        paren1 = option.contents[0].find('(')
        topics.append([option['value'],option.contents[0][0:paren1-1],billnumber])
    return topics

#print get_topics_list('Senate')

def aggregate_the_data():
    print 'Aggregate'
    currentdata = scraperwiki.sqlite.select("* from swdata")
    for i in currentdata:
        topic = i['topic']
        topic_id_upper = i['topic_id_upper'].encode('ascii')
        topic_id_lower = i['topic_id_lower'].encode('ascii')
        bill_count_upper = i['bill_count_upper']
        bill_count_lower = i['bill_count_lower']
        bills_upper = i['bills_upper'].encode('ascii')
        bills_lower = i['bills_lower'].encode('ascii')
        
        if bill_count_upper == '':
            bill_count_upper = 0
        if bill_count_lower == '':
            bill_count_lower = 0
        bill_count = int(bill_count_upper) + int(bill_count_lower)
        bills = bills_upper + bills_lower
        data = {'topic':str(topic),
                'topic_id_upper':topic_id_upper,
                'topic_id_lower':topic_id_lower,
                'bill_count_upper':int(bill_count_upper),
                'bill_count_lower':int(bill_count_lower),
                'bill_count': bill_count,
                'bills_upper':bills_upper,
                'bills_lower':bills_lower,
                'bills':bills
                }
        scraperwiki.sqlite.save(unique_keys=['topic'], data=data)



#Start of live code
database = {}
try:
    currentdata = scraperwiki.sqlite.select("* from swdata")
except:
    currentdata = {}
for i in currentdata:
    database[i['topic']] = {}
    
    if 'topic_id_upper' in i and i['topic_id_upper'] != '':
        topic_id_upper = i['topic_id_upper']
        bill_count_upper = int(i['bill_count_upper'])
        bills_upper = i['bills_upper']
        database[i['topic']].update({'topic_id_upper':topic_id_upper,'bill_count_upper':bill_count_upper,'bills_upper':bills_upper})

    if 'topic_id_lower' in i and i['topic_id_lower'] != '':
        topic_id_lower = i['topic_id_lower']
        bill_count_lower = int(i['bill_count_lower'])
        bills_lower = i['bills_lower']
        database[i['topic']].update({'topic_id_lower':topic_id_lower,'bill_count_lower':bill_count_lower,'bills_lower':bills_lower})


chambers = ['Senate','House']

for chamber in chambers:
    print chamber
    topics = get_topics_list(chamber)
    for topic in topics:
        if chamber == 'Senate' and topic[1] in database and 'bill_count_upper' in database[topic[1]] and database[topic[1]]['bill_count_upper'] == topic[2]:
            pass
        elif chamber == 'House' and topic[1] in database and 'bill_count_lower' in database[topic[1]] and database[topic[1]]['bill_count_lower'] == topic[2]:
            pass
        else:
            bills = scrape_bill_nums(chamber,topic[0])
            for i in range(0,len(bills)):
                bills[i] = open_states_format(bills[i])
            if chamber == 'House':
                if topic[1] in database and 'bill_count_upper' in database[topic[1]]:
                    bill_count_upper = int(database[topic[1]]['bill_count_upper'])
                    topic_id_upper = database[topic[1]]['topic_id_upper'] 
                    bills_upper = database[topic[1]]['bills_upper']
                else:
                    bills_upper = ''
                    topic_id_upper = ''
                    bill_count_upper = ''
                            
                data = {'bills_lower': bills,
                        'topic_id_lower': topic[0],
                        'bill_count_lower': int(topic[2]),
                        'topic': topic[1],
                        'bills_upper':bills_upper,
                        'topic_id_upper':topic_id_upper,
                        'bill_count_upper':bill_count_upper
                        }
            if chamber == 'Senate':
                if topic[1] in database and 'bill_count_lower' in database[topic[1]]:
                    bill_count_lower = int(database[topic[1]]['bill_count_lower'])
                    topic_id_lower = database[topic[1]]['topic_id_lower']
                    bills_lower = database[topic[1]]['bills_lower'] 

                else:
                    bills_lower = ''
                    topic_id_lower = ''
                    bill_count_lower = ''
                            
                data = {'bills_upper': bills,
                        'topic_id_upper': topic[0],
                        'bill_count_upper': int(topic[2]),
                        'topic': topic[1],
                        'bills_lower':bills_lower,
                        'topic_id_lower':topic_id_lower,
                        'bill_count_lower':bill_count_lower                        
                        }                
            scraperwiki.sqlite.save(unique_keys=['topic'], data=data)



aggregate_the_data()import scraperwiki
import re
import json
from BeautifulSoup import BeautifulSoup

def scrape_bill_nums(chamber,topic):
    url = 'https://www.revisor.mn.gov/bills/status_result.php?body=' + chamber + '&search=basic&session=0882013&location=House&bill=&bill_type=bill&rev_number=&keyword_type=all&keyword=&keyword_field_text=1&topic%5B%5D='+topic+'&submit_topic=GO&titleword='
    
    soup = BeautifulSoup(scraperwiki.scrape(url))    
    bills = []    
    rows = soup('tr')
    for row in rows:
        contents = BeautifulSoup(str(row))
        try:
            bill = contents('td')[1].a.contents
            bills.append(str(bill[0]))
        except:
            pass
    return bills

def open_states_format(bill):
    if bill[2] == '0':
        if bill[3] == '0':
            if bill[4] == '0':
                append = " " + bill[5:]
            else:
                append = " " + bill[4:]
        else:
            append = " " + bill[3:]
        result = bill[0:2] + append
    else:
        result = bill
    return result

def get_topics_list(chamber):
    topics = []
    url = 'https://www.revisor.mn.gov/bills/status_search.php?body='+chamber
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    select = soup('select')[4] #lame, but that should be the categories select
    options = BeautifulSoup(str(select))
    for option in options('option'):
        billnumber = re.findall(r'\d+', option.contents[0])
        if billnumber == []:
            billnumber = 0
        else:
            billnumber = int(billnumber[0])
        paren1 = option.contents[0].find('(')
        topics.append([option['value'],option.contents[0][0:paren1-1],billnumber])
    return topics

#print get_topics_list('Senate')

def aggregate_the_data():
    print 'Aggregate'
    currentdata = scraperwiki.sqlite.select("* from swdata")
    for i in currentdata:
        topic = i['topic']
        topic_id_upper = i['topic_id_upper'].encode('ascii')
        topic_id_lower = i['topic_id_lower'].encode('ascii')
        bill_count_upper = i['bill_count_upper']
        bill_count_lower = i['bill_count_lower']
        bills_upper = i['bills_upper'].encode('ascii')
        bills_lower = i['bills_lower'].encode('ascii')
        
        if bill_count_upper == '':
            bill_count_upper = 0
        if bill_count_lower == '':
            bill_count_lower = 0
        bill_count = int(bill_count_upper) + int(bill_count_lower)
        bills = bills_upper + bills_lower
        data = {'topic':str(topic),
                'topic_id_upper':topic_id_upper,
                'topic_id_lower':topic_id_lower,
                'bill_count_upper':int(bill_count_upper),
                'bill_count_lower':int(bill_count_lower),
                'bill_count': bill_count,
                'bills_upper':bills_upper,
                'bills_lower':bills_lower,
                'bills':bills
                }
        scraperwiki.sqlite.save(unique_keys=['topic'], data=data)



#Start of live code
database = {}
try:
    currentdata = scraperwiki.sqlite.select("* from swdata")
except:
    currentdata = {}
for i in currentdata:
    database[i['topic']] = {}
    
    if 'topic_id_upper' in i and i['topic_id_upper'] != '':
        topic_id_upper = i['topic_id_upper']
        bill_count_upper = int(i['bill_count_upper'])
        bills_upper = i['bills_upper']
        database[i['topic']].update({'topic_id_upper':topic_id_upper,'bill_count_upper':bill_count_upper,'bills_upper':bills_upper})

    if 'topic_id_lower' in i and i['topic_id_lower'] != '':
        topic_id_lower = i['topic_id_lower']
        bill_count_lower = int(i['bill_count_lower'])
        bills_lower = i['bills_lower']
        database[i['topic']].update({'topic_id_lower':topic_id_lower,'bill_count_lower':bill_count_lower,'bills_lower':bills_lower})


chambers = ['Senate','House']

for chamber in chambers:
    print chamber
    topics = get_topics_list(chamber)
    for topic in topics:
        if chamber == 'Senate' and topic[1] in database and 'bill_count_upper' in database[topic[1]] and database[topic[1]]['bill_count_upper'] == topic[2]:
            pass
        elif chamber == 'House' and topic[1] in database and 'bill_count_lower' in database[topic[1]] and database[topic[1]]['bill_count_lower'] == topic[2]:
            pass
        else:
            bills = scrape_bill_nums(chamber,topic[0])
            for i in range(0,len(bills)):
                bills[i] = open_states_format(bills[i])
            if chamber == 'House':
                if topic[1] in database and 'bill_count_upper' in database[topic[1]]:
                    bill_count_upper = int(database[topic[1]]['bill_count_upper'])
                    topic_id_upper = database[topic[1]]['topic_id_upper'] 
                    bills_upper = database[topic[1]]['bills_upper']
                else:
                    bills_upper = ''
                    topic_id_upper = ''
                    bill_count_upper = ''
                            
                data = {'bills_lower': bills,
                        'topic_id_lower': topic[0],
                        'bill_count_lower': int(topic[2]),
                        'topic': topic[1],
                        'bills_upper':bills_upper,
                        'topic_id_upper':topic_id_upper,
                        'bill_count_upper':bill_count_upper
                        }
            if chamber == 'Senate':
                if topic[1] in database and 'bill_count_lower' in database[topic[1]]:
                    bill_count_lower = int(database[topic[1]]['bill_count_lower'])
                    topic_id_lower = database[topic[1]]['topic_id_lower']
                    bills_lower = database[topic[1]]['bills_lower'] 

                else:
                    bills_lower = ''
                    topic_id_lower = ''
                    bill_count_lower = ''
                            
                data = {'bills_upper': bills,
                        'topic_id_upper': topic[0],
                        'bill_count_upper': int(topic[2]),
                        'topic': topic[1],
                        'bills_lower':bills_lower,
                        'topic_id_lower':topic_id_lower,
                        'bill_count_lower':bill_count_lower                        
                        }                
            scraperwiki.sqlite.save(unique_keys=['topic'], data=data)



aggregate_the_data()