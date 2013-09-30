import scraperwiki
import lxml.html

def parseMG(url,council):
    html = scraperwiki.scrape(url + "mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=")
    root = lxml.html.fromstring(html)
    members = list()
    for tr in root.cssselect("table[class='mgStatsTable'] tr")[1:]:
        tds = tr.cssselect("td")
        data = dict()
        data['photo'] = url + tds[0].cssselect("img")[0].attrib['src']
        data['name'] = tds[1].cssselect("a")[0].text_content()
        if data['name'][0:10] == 'Councillor': data['name'] = data['name'][11:]
        data['party'] = tds[2].text_content()
        data['constituency'] = tds[3].text_content()
        data['council'] = council
        members.append(data)
    return members

def parseCouncil(council):
    data = parseMG(council['url'],council['name'])
    scraperwiki.sqlite.save(unique_keys=['name','council'], data=data)

scrapes =  [{'url': 'http://www.harrow.gov.uk/www2/', 'name': 'London Borough of Harrow'},
{'url': 'http://council.southglos.gov.uk/', 'name': 'South Gloucestershire District Council'}]

for council in scrapes:
    parseCouncil(council)


import scraperwiki
import lxml.html

def parseMG(url,council):
    html = scraperwiki.scrape(url + "mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=")
    root = lxml.html.fromstring(html)
    members = list()
    for tr in root.cssselect("table[class='mgStatsTable'] tr")[1:]:
        tds = tr.cssselect("td")
        data = dict()
        data['photo'] = url + tds[0].cssselect("img")[0].attrib['src']
        data['name'] = tds[1].cssselect("a")[0].text_content()
        if data['name'][0:10] == 'Councillor': data['name'] = data['name'][11:]
        data['party'] = tds[2].text_content()
        data['constituency'] = tds[3].text_content()
        data['council'] = council
        members.append(data)
    return members

def parseCouncil(council):
    data = parseMG(council['url'],council['name'])
    scraperwiki.sqlite.save(unique_keys=['name','council'], data=data)

scrapes =  [{'url': 'http://www.harrow.gov.uk/www2/', 'name': 'London Borough of Harrow'},
{'url': 'http://council.southglos.gov.uk/', 'name': 'South Gloucestershire District Council'}]

for council in scrapes:
    parseCouncil(council)


