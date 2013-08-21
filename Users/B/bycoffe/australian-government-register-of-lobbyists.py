###############################################################################
# Basic scraper
###############################################################################

import scraperwiki

import re


def get_ids():
    url = 'http://lobbyists.pmc.gov.au/who_register.cfm'
    page = scraperwiki.scrape(url)
    return set(re.findall(r'\?id=(?P<id>\d+)', page))


def get_data(id):
    url = 'http://lobbyists.pmc.gov.au/register/view_agency.cfm?id=%s' % id
    #page = urllib2.urlopen(url).read()
    print url
    page = scraperwiki.scrape(url)

    business_entity_name = re.search(r'Business Entity Name:<\/strong>(.*?)<\/li>', page).groups()[0].strip()
    last_updated = re.search(r'The information above was last updated on (.*?)\.<\/p>', page).groups()[0].strip()

    abn = re.search(r'A.B.N:<\/strong>(.*?)<\/li>', page).groups()[0].strip()
    trading_name = re.search(r'Trading Name:<\/strong>(.*?)<\/li>', page).groups()[0].strip()

    lobby = re.search(r'<table border="0" cellpadding="4" cellspacing="1" id="lobbyistDetails"  class="tablesorter">(.*?)<\/table>', page, re.S)
    if lobby != None:
        lobbyist_table = lobby.groups()[0]
        lobbyist_list = [dict(zip(['num', 'name', 'title', 'formergovrep', 'govrepceasedate'], row)) for row in re.findall(r'<td>(\d+)<\/td>\s+<td>(.*?)<\/td>\s+<td>(.*?)<\/td>\s+<td align="center">(.*?)<\/td>\s+<td align="center">(.*?)<\/td>', lobbyist_table)]
    else:
        lobbyist_list = []

    clients = re.search(r'<table border="0" cellpadding="4" cellspacing="1" id="clientDetails"  class="tablesorter">(.*?)<\/table>', page, re.S)
    if clients != None:
        clients_table = clients.groups()[0]
        for row in re.findall(r'<td>(\d+)<\/td>\s+<td>(.*?)<\/td>', clients_table):
            (rownum,client_name) = row
            client = {'lobbyist_name': business_entity_name, 'lobbyist_abn': abn, 'client_name':client_name}
            scraperwiki.sqlite.save(unique_keys=["lobbyist_abn","client_name"], data=client, table_name="lobbyist_clients") 

    owner_ul = re.search(r'<h2>Owner Details</h2>\s+<ul>(.*?)<\/ul>', page, re.S).groups()[0]
    owners = re.findall(r'<li>(.*?)<\/li>', owner_ul, re.S)

    return {'business_entity_name': business_entity_name,
            'abn': abn,
            'last_updated': last_updated,
            'trading_name': trading_name,
            'lobbyists': lobbyist_list,
            'owner_details': owners, 
            }

for id in get_ids():
    data = get_data(id)
    scraperwiki.sqlite.save(unique_keys=["abn"], data=data, table_name="lobbyists")