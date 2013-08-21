# Blank Python

import scraperwiki
import lxml.html
import urllib2

base_url = "http://www.nationalhistoricships.org.uk/ships_register.php?action=search&page=%d"

for i in range(74): # hack, work out proper number of pages
    url = base_url % i

    print url
    response = urllib2.urlopen(url)
    tree = lxml.html.parse(response, base_url=url)

    for tr in tree.xpath('//table[@id="regsearch_results"]/tr'):
        tds = tr.xpath('td')
        if len(tds) != 5:
            continue
        
        result_id = int(tds[0].text)
        vessel_a = tds[1].xpath('a')[0]
        vessel_name = vessel_a.text_content()
        vessel_url_stub = vessel_a.attrib['href']
        vessel_url = "http://www.nationalhistoricships.org.uk/ships_register.php" + vessel_url_stub
        builder = tds[2].text_content()
        try:
            build_year = int(tds[3].text)
        except TypeError:
            build_year = None
        image_url = "http://www.nationalhistoricships.org.uk" + tds[4].xpath('.//img')[0].attrib['src']
        vessel_id = int(vessel_url_stub[len("?action=ship&id="):])

        scraperwiki.sqlite.save(unique_keys=['vessel_id'],
                                data={'result_id': result_id, 'vessel_id': vessel_id, 
                                      'vessel_name': vessel_name, 'vessel_url': vessel_url,
                                      'builder': builder, 'build_year': build_year, 'image_url': image_url,},
                                table_name='ships')

# TODO scrape individual ship pages
for ship in scraperwiki.sqlite.select('* from ships'):
    print ship['vessel_url']
    response = urllib2.urlopen(ship['vessel_url'])
    tree = lxml.html.parse(response, base_url=ship['vessel_url'])

    second_detail = zip([x.text_content().replace(':', '').lower() for x in tree.xpath('//table[@class="vesseldetail_secondlevel"]//th')], [x.text_content() for x in tree.xpath('//table[@class="vesseldetail_secondlevel"]//td')])

    third_detail = zip([x.text_content().replace(':', '').lower() for x in tree.xpath('//dl[@class="vesseldetail_thirdlevel"]/dt')], [x.text_content() for x in tree.xpath('//dl[@class="vesseldetail_thirdlevel"]/dd')])
    
    try:
        history = tree.xpath('//div[@id="history_tab"]')[0].text_content().strip()
    except IndexError:
        history = None

    try:
        development = tree.xpath('//div[@id="development_tab"]')[0].text_content().strip()
    except IndexError:
        development = None

    try:
        bibliography = tree.xpath('//div[@id="bibliography_tab"]')[0].text_content().strip()
    except IndexError:
        bibliography = None

    print second_detail 
    print third_detail
    print history
    print development
    print bibliography

    for k,v in second_detail:
        ship[k] = v
    for k,v in third_detail:
        ship[k] = v

    ship['history'] = history
    ship['development'] = development
    ship['bibliography'] = bibliography

    scraperwiki.sqlite.save(unique_keys=['vessel_id'], data=ship, table_name="ships")

