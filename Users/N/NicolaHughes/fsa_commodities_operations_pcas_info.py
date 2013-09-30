import scraperwiki
import unicodedata
import os, re, sys

"""
Notice has a header_id and a code, both from first row and used as identifiers

item is an order item, it has an item code, and it have 'belongs_to' which points
to the header_id (see Notice above) where it belongs. Also has address details

orderline is an individual entry which has 'belongs_to' which points to the item's
item_code (see above). It also has 'belongs_in' which contains the header_id so
it can tied into the single export notice.
"""

scraperwiki.sqlite.attach("fsa_commodities_operations_pcas_content")

contents = scraperwiki.sqlite.select("Content from fsa_commodities_operations_pcas_content.swdata")

def parse_export_notice( lines ):
    """ Pass in a list of lines, and it will parse them into the relevant
    notice object and orderlines, which will be associated by the header_id
    of the notice """
    # Matches the end of an address line
    r = re.compile('^(.*)([A-ZA-Z]\S \d{9}|\d{5}-\d{4})$')

    notice = {}
    header = lines.pop(0)
    parts = header.split(' ')
    notice['header_id'] = parts[0]
    notice['code'] = parts[3]

    for l in lines:
        if 'NOTICE OF EXPORT PURCHASES' in l:
            notice['notice_date'] = ' '.join(l.replace('\t','').split(' ')[-3:])
            continue

    item = None
    address_lines = []
    orderline = {}
    in_address = False
    for line in lines:
        if line.startswith('VEP'):
            if item:
                scraperwiki.sqlite.save( ['item_code','belongs_to'], item, table_name='orders')
            item = { 'belongs_to': notice['header_id'], 'item_code': line.split(' ')[0] }
            item['vendor'] = line[len(item['item_code']):].strip() # get to end of line
            #notice['item_code'] = item['item_code']
            in_address = True
            continue

        if in_address:
            m = r.match(line)
            if m:
                # End of address segment
                item['address'] = ', '.join(address_lines)
                address_lines = []

                in_address = False
                continue
            else:
                address_lines.append(line.strip())
                continue

        # Still here? Then we're probably on an actual order line
        # If it is an end order line, save order otherwise create a new order
        # and save it.
        if line.strip().startswith('TOTAL QUANTITY'):
            # Last line was scheme, not order
            if orderline:
                scheme = orderline['item']
            orderline = None
            continue

        if item:
            if not orderline:
                orderline = { 'belongs_to': item['item_code'], 'belongs_in': notice['header_id']}
                orderline['item'] = line.strip()
            else:
                parts = re.sub('\s{2,}', '\t', line).split('\t')
                if len(parts) == 3:
                    orderline['bag'] = parts[0]
                    orderline['quantity'] = parts[1].split(' ')[0].replace(',','')
                    orderline['port'] = parts[1].split(' ')[1]
                    orderline['price'] = parts[2].replace(',','')
                    scraperwiki.sqlite.save( ['item','bag', 'quantity', 'port', 'price'], orderline, table_name='orderline')
                    orderline = None

        if line.startswith('********************'):
            break

    if item:
        scraperwiki.sqlite.save( ['item_code','belongs_to'], item, table_name='orders')

    # save notice
    print 'Saving notice', notice
    scraperwiki.sqlite.save( ['header_id', 'code'], notice, table_name='notices')

one = False
for content in contents:
    info = unicodedata.normalize('NFKD', content["Content"]).encode('ascii','ignore')
    if 'Notice of Export Purchase and Port Allocation' in info:
        print '*' * 30 
        print 'This is a port allocation file, need a parser for it'
        continue
    parse_export_notice([x.strip() for x in info.split('\n')])
import scraperwiki
import unicodedata
import os, re, sys

"""
Notice has a header_id and a code, both from first row and used as identifiers

item is an order item, it has an item code, and it have 'belongs_to' which points
to the header_id (see Notice above) where it belongs. Also has address details

orderline is an individual entry which has 'belongs_to' which points to the item's
item_code (see above). It also has 'belongs_in' which contains the header_id so
it can tied into the single export notice.
"""

scraperwiki.sqlite.attach("fsa_commodities_operations_pcas_content")

contents = scraperwiki.sqlite.select("Content from fsa_commodities_operations_pcas_content.swdata")

def parse_export_notice( lines ):
    """ Pass in a list of lines, and it will parse them into the relevant
    notice object and orderlines, which will be associated by the header_id
    of the notice """
    # Matches the end of an address line
    r = re.compile('^(.*)([A-ZA-Z]\S \d{9}|\d{5}-\d{4})$')

    notice = {}
    header = lines.pop(0)
    parts = header.split(' ')
    notice['header_id'] = parts[0]
    notice['code'] = parts[3]

    for l in lines:
        if 'NOTICE OF EXPORT PURCHASES' in l:
            notice['notice_date'] = ' '.join(l.replace('\t','').split(' ')[-3:])
            continue

    item = None
    address_lines = []
    orderline = {}
    in_address = False
    for line in lines:
        if line.startswith('VEP'):
            if item:
                scraperwiki.sqlite.save( ['item_code','belongs_to'], item, table_name='orders')
            item = { 'belongs_to': notice['header_id'], 'item_code': line.split(' ')[0] }
            item['vendor'] = line[len(item['item_code']):].strip() # get to end of line
            #notice['item_code'] = item['item_code']
            in_address = True
            continue

        if in_address:
            m = r.match(line)
            if m:
                # End of address segment
                item['address'] = ', '.join(address_lines)
                address_lines = []

                in_address = False
                continue
            else:
                address_lines.append(line.strip())
                continue

        # Still here? Then we're probably on an actual order line
        # If it is an end order line, save order otherwise create a new order
        # and save it.
        if line.strip().startswith('TOTAL QUANTITY'):
            # Last line was scheme, not order
            if orderline:
                scheme = orderline['item']
            orderline = None
            continue

        if item:
            if not orderline:
                orderline = { 'belongs_to': item['item_code'], 'belongs_in': notice['header_id']}
                orderline['item'] = line.strip()
            else:
                parts = re.sub('\s{2,}', '\t', line).split('\t')
                if len(parts) == 3:
                    orderline['bag'] = parts[0]
                    orderline['quantity'] = parts[1].split(' ')[0].replace(',','')
                    orderline['port'] = parts[1].split(' ')[1]
                    orderline['price'] = parts[2].replace(',','')
                    scraperwiki.sqlite.save( ['item','bag', 'quantity', 'port', 'price'], orderline, table_name='orderline')
                    orderline = None

        if line.startswith('********************'):
            break

    if item:
        scraperwiki.sqlite.save( ['item_code','belongs_to'], item, table_name='orders')

    # save notice
    print 'Saving notice', notice
    scraperwiki.sqlite.save( ['header_id', 'code'], notice, table_name='notices')

one = False
for content in contents:
    info = unicodedata.normalize('NFKD', content["Content"]).encode('ascii','ignore')
    if 'Notice of Export Purchase and Port Allocation' in info:
        print '*' * 30 
        print 'This is a port allocation file, need a parser for it'
        continue
    parse_export_notice([x.strip() for x in info.split('\n')])
