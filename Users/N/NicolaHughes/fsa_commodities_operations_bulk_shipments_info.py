import scraperwiki
import unicodedata
import os, re, sys


scraperwiki.sqlite.attach("fsa_commodities_operations_bulk_shipments_content")

contents = scraperwiki.sqlite.select("Content from fsa_commodities_operations_bulk_shipments_content.swdata")

def parse_bulk(info):
    paragraphs = re.split('\r\n\r\n', info)
    #print paragraphs

    date = ' '.join(paragraphs[1].replace('\r\n', ' ').split(' ')[-3:])
    if date == 'AS  AMENDED':
        date = ' '.join(paragraphs[2].replace('\t', ' ').split(' ')[-3:])
    #print date

    for paragraph in paragraphs:
        if "VEPK" in paragraph:
            r = re.findall(r'\bVEPK\w+', paragraph)
            vendor_and_item = paragraph
            #print vendor_and_item
            splits = vendor_and_item.split('\r\n')
            splits_strip = [i.strip() for i in splits]
            if splits_strip[0] == "Offer #1" or splits_strip[0] == "Offer #2" or splits_strip[0] == "Offer #3" or splits_strip[0] == "Offer #4":
                splits_strip = splits_strip[1:]
            if splits_strip[1] == "Offer #3" or splits_strip[1] == "Offer #4":
                splits_strip = splits_strip[2:]
            if splits_strip[0] == '':
                splits_strip = splits_strip[5:]
            #print splits_strip
            
            contract_code = splits_strip[0].replace('\t',' ').split(' ')[0]
            print contract_code
            vendor = ' '.join(splits_strip[0].replace('\t',' ').split(' ')[1:])
            #print vendor
            address = splits_strip[1]

            item_details = [x.strip().replace(',','').replace('$','') for x in splits_strip[2].replace(' ,',',').replace('\t',' ').split(' ') if len(x)]
            #print item_details
            item = item_details[0]
            quantity = item_details[1]
            port = ', '.join(item_details[2:4])
            if port == 'Myrtle, Grove':
                port = 'Myrtle Grove, LA'
            price = item_details[4]
            if len(item_details) == 10:
                destination = item_details[5]
                agency = item_details[6]
                requisition = item_details[7]
            else:
                destination = ', '.join(item_details[5:7])
                agency = item_details[7]
                requisition = item_details[8]
            data = {"contract_code": contract_code, "vendor": vendor, "address": address, "item": item, "bag": "bulk", "quantity": quantity, "port": port, "price": price, "destination": destination, "agency": agency, "requisition": requisition, "date": date}
            #print data
            #scraperwiki.sqlite.save(["requisition", "contract_code", "quantity"], data)


for content in contents:
    info = unicodedata.normalize('NFKD', content["Content"]).encode('ascii','ignore')
    print info
    parse_bulk(info)

