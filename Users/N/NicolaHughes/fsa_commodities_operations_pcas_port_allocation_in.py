import scraperwiki
import unicodedata
import os, re, sys


scraperwiki.sqlite.attach("fsa_commodities_operations_pcas_content")

contents = scraperwiki.sqlite.select("Content from fsa_commodities_operations_pcas_content.swdata")
#print len(contents)

def parse_port_allocation( info ):
    paragraphs = re.split('\r\n\r\n', info)
    #print paragraphs

    date = ' '.join(paragraphs[1].split(' ')[-3:])
    #print date

    contract = paragraphs[4].split(' ')[0]
    #print contract
    
    vendor_and_item = [line.strip() for line in paragraphs[4][len(contract):].strip().split('\n')]
    vendor = vendor_and_item[0]
    #print vendor
    
    address = ', '.join(vendor_and_item[1:-1])
    #print address
    
    item = vendor_and_item[len(vendor_and_item) - 1].strip()
    #print item

    item_details = paragraphs[5]
    #print item_details
    item_splits = [re.split(' +', x) for x in item_details.strip().replace('$','').split('\n')]
    
    for item_detail in item_splits:
        if item_detail[0] != 'October':
        #print item_detail
            bag = item_detail[0]
            quantity = item_detail[1].replace(',','')
            port = item_detail[2]
            price = item_detail[3].replace(',','')
            destination = item_detail[4]
            agency = item_detail[5]
            requisition = item_detail[-1].strip()
            data = {"contract_code": contract, "vendor": vendor, "address": address, "item": item, "bag": bag, "quantity": quantity, "port": port, "price": price, "destination": destination, "agency": agency, "requisition": requisition, "date": date}
            #print data
            scraperwiki.sqlite.save(["requisition", "contract_code", "quantity"], data)


for content in contents:
    info = unicodedata.normalize('NFKD', content["Content"]).encode('ascii','ignore')
    if 'Notice of Export Purchase and Port Allocation' in info:
        #print info
        parse_port_allocation(info)

import scraperwiki
import unicodedata
import os, re, sys


scraperwiki.sqlite.attach("fsa_commodities_operations_pcas_content")

contents = scraperwiki.sqlite.select("Content from fsa_commodities_operations_pcas_content.swdata")
#print len(contents)

def parse_port_allocation( info ):
    paragraphs = re.split('\r\n\r\n', info)
    #print paragraphs

    date = ' '.join(paragraphs[1].split(' ')[-3:])
    #print date

    contract = paragraphs[4].split(' ')[0]
    #print contract
    
    vendor_and_item = [line.strip() for line in paragraphs[4][len(contract):].strip().split('\n')]
    vendor = vendor_and_item[0]
    #print vendor
    
    address = ', '.join(vendor_and_item[1:-1])
    #print address
    
    item = vendor_and_item[len(vendor_and_item) - 1].strip()
    #print item

    item_details = paragraphs[5]
    #print item_details
    item_splits = [re.split(' +', x) for x in item_details.strip().replace('$','').split('\n')]
    
    for item_detail in item_splits:
        if item_detail[0] != 'October':
        #print item_detail
            bag = item_detail[0]
            quantity = item_detail[1].replace(',','')
            port = item_detail[2]
            price = item_detail[3].replace(',','')
            destination = item_detail[4]
            agency = item_detail[5]
            requisition = item_detail[-1].strip()
            data = {"contract_code": contract, "vendor": vendor, "address": address, "item": item, "bag": bag, "quantity": quantity, "port": port, "price": price, "destination": destination, "agency": agency, "requisition": requisition, "date": date}
            #print data
            scraperwiki.sqlite.save(["requisition", "contract_code", "quantity"], data)


for content in contents:
    info = unicodedata.normalize('NFKD', content["Content"]).encode('ascii','ignore')
    if 'Notice of Export Purchase and Port Allocation' in info:
        #print info
        parse_port_allocation(info)

