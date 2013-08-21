import scraperwiki
import xml.dom.minidom
import datetime

xml_string = scraperwiki.scrape('http://api.intrade.com/jsp/XML/MarketData/xml.jsp')
contract_dom = xml.dom.minidom.parseString(xml_string)

def get_contract_list(dom):
    contracts = []
    contract_doms = dom.getElementsByTagName('contract')
    for contract in contract_doms:
        contracts.append({'name':contract.getElementsByTagName('name')[0].firstChild.data,
                           'symbol':contract.getElementsByTagName('symbol')[0].firstChild.data,
                           'id':contract.getAttribute('id'),
                           'event':contract.parentNode.getElementsByTagName('name')[0].firstChild.data,
                           'even_id':contract.parentNode.getAttribute('id'),
                           'event_start':contract.parentNode.getAttribute('StartDate'),
                           'event_end':contract.parentNode.getAttribute('EndDate'),
                           'event_group':contract.parentNode.parentNode.getElementsByTagName('name')[0].firstChild.data,
                           'event_group_id':contract.parentNode.parentNode.getAttribute('id'),
                           'event_class':contract.parentNode.parentNode.parentNode.getElementsByTagName('name')[0].firstChild.data,
                           'event_class_id':contract.parentNode.parentNode.parentNode.getAttribute('id'),
                          })
    scraperwiki.sqlite.save(unique_keys = ['id'], data=contracts, table_name='contract_info')

def get_contract_volume(dom):
    contracts = []
    contract_doms = dom.getElementsByTagName('contract')
    for contract in contract_doms:
        contracts.append({'id':contract.getAttribute('id'),
                          'volume':int(contract.getElementsByTagName('totalVolume')[0].firstChild.data),
                          'date':datetime.date.today()
                         })
    scraperwiki.sqlite.save(unique_keys=['date', 'id'], data=contracts, table_name='contract_volume')

get_contract_list(contract_dom)
get_contract_volume(contract_dom)