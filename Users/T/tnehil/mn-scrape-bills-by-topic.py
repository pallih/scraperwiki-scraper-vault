import scraperwiki
import re
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

schema = {}
try:
    currentdata = scraperwiki.sqlite.select("* from `swdata`")
    for i in currentdata:
        topicno = i['topicno']
        topiccnt = i['topiccnt']
        schema[topicno] = topiccnt
except:
    pass

chambers = ['Senate','House']

for chamber in chambers:
    topics = get_topics_list(chamber)
    for topic in topics:
        #print topic[0]
        #print type(schema[topic[0]])
        #print type(topic[2])
        #print schema[topic[0]]
        if topic[0] in schema and schema[topic[0]] == topic[2]:
            pass
        else:
            bills = scrape_bill_nums(chamber,topic[0])
            #for bill in bills:
            #osformat = open_states_format(bill)
            data = {'bills': bills,
                    'topicno': topic[0],
                    'topiccnt': int(topic[2]),
                    'topic': topic[1]}
            scraperwiki.sqlite.save(unique_keys=['topicno'], data=data)