import scraperwiki
import string
import requests
import lxml.html
import re
import itertools
import time

list_url = 'http://hlaupastyrkur.is/godgerdafelog'


def scrape_felog():
    r = requests.get(list_url)
    content = r.content
    root = lxml.html.fromstring(content)
    results = root.xpath('//div[@class="item"]')
    for x in results:
        record = {}
        record['felag'] = x.text_content().strip()
        record['url'] = x[0][0].attrib['href']
        record['done'] = 0
        scraperwiki.sqlite.save(table_name='felog', data=record, unique_keys=['url'],verbose=1)

def scrape_upphaedir(todo):
    for x in todo:
        record = {}
        r = requests.get(x['url'])
        content = r.content
        root = lxml.html.fromstring(content)
        amounts = root.xpath('//div[@class="amount"]')
        print x['felag'],':'
        all_amounts = []
        for a in amounts[:-1]:
            amount = int(a[0].text)
            all_amounts.append(amount)            
        if len(all_amounts) != 0:
            record['Samtals'] = sum(all_amounts)
            record['Fjoldi'] = len(all_amounts)
            record['Haesti'] = max(all_amounts)
            record['Medaltal'] = sum(all_amounts)/len(all_amounts)
            record['Laegsti'] = min(all_amounts)
            record['upphaedir'] = all_amounts
            record['url'] = x['url']
            record['felag'] = x['felag']
            scraperwiki.sqlite.save(table_name='felog', data=record, unique_keys=['url'],verbose=1)
            update_statement1= 'update felog SET done= 1 WHERE url='+ '"' + x['url'] + '"'
            scraperwiki.sqlite.execute(update_statement1)
            scraperwiki.sqlite.commit()
        else:
            update_statement1= 'update felog SET done= 1 WHERE url='+ '"' + x['url'] + '"'
            scraperwiki.sqlite.execute(update_statement1)
            scraperwiki.sqlite.commit()
        

#scrape_felog()

#exit()

todo = scraperwiki.sqlite.select("* from felog where done='0'")


print "Eftir :", len(todo)

scrape_upphaedir(todo)
    import scraperwiki
import string
import requests
import lxml.html
import re
import itertools
import time

list_url = 'http://hlaupastyrkur.is/godgerdafelog'


def scrape_felog():
    r = requests.get(list_url)
    content = r.content
    root = lxml.html.fromstring(content)
    results = root.xpath('//div[@class="item"]')
    for x in results:
        record = {}
        record['felag'] = x.text_content().strip()
        record['url'] = x[0][0].attrib['href']
        record['done'] = 0
        scraperwiki.sqlite.save(table_name='felog', data=record, unique_keys=['url'],verbose=1)

def scrape_upphaedir(todo):
    for x in todo:
        record = {}
        r = requests.get(x['url'])
        content = r.content
        root = lxml.html.fromstring(content)
        amounts = root.xpath('//div[@class="amount"]')
        print x['felag'],':'
        all_amounts = []
        for a in amounts[:-1]:
            amount = int(a[0].text)
            all_amounts.append(amount)            
        if len(all_amounts) != 0:
            record['Samtals'] = sum(all_amounts)
            record['Fjoldi'] = len(all_amounts)
            record['Haesti'] = max(all_amounts)
            record['Medaltal'] = sum(all_amounts)/len(all_amounts)
            record['Laegsti'] = min(all_amounts)
            record['upphaedir'] = all_amounts
            record['url'] = x['url']
            record['felag'] = x['felag']
            scraperwiki.sqlite.save(table_name='felog', data=record, unique_keys=['url'],verbose=1)
            update_statement1= 'update felog SET done= 1 WHERE url='+ '"' + x['url'] + '"'
            scraperwiki.sqlite.execute(update_statement1)
            scraperwiki.sqlite.commit()
        else:
            update_statement1= 'update felog SET done= 1 WHERE url='+ '"' + x['url'] + '"'
            scraperwiki.sqlite.execute(update_statement1)
            scraperwiki.sqlite.commit()
        

#scrape_felog()

#exit()

todo = scraperwiki.sqlite.select("* from felog where done='0'")


print "Eftir :", len(todo)

scrape_upphaedir(todo)
    