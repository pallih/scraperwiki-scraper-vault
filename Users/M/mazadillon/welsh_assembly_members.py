import scraperwiki
import lxml.html

def parseMG(url):
    html = scraperwiki.scrape(url + "mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=")
    root = lxml.html.fromstring(html)
    members = list()
    for tr in root.cssselect("table[class='mgStatsTable'] tr")[1:]:
        tds = tr.cssselect("td")
        data = dict()
        data['photo'] = url + tds[0].cssselect("img")[0].attrib['src']
        data['name'] = tds[1].cssselect("a")[0].text_content()
        data['party'] = tds[2].text_content()
        data['constituency'] = tds[3].text_content()
        data['region'] = tds[4].text_content()
        if(data['constituency'] == u'\xa0'): data['constituency'] = ''
        if(data['region'] == u'\xa0'): data['region'] = ''
        members.append(data)
    return members

data = parseMG('http://www.senedd.assemblywales.org/')
scraperwiki.sqlite.save(unique_keys=['name'], data=data)

import scraperwiki
import lxml.html

def parseMG(url):
    html = scraperwiki.scrape(url + "mgMemberIndex.aspx?VW=TABLE&PIC=1&FN=")
    root = lxml.html.fromstring(html)
    members = list()
    for tr in root.cssselect("table[class='mgStatsTable'] tr")[1:]:
        tds = tr.cssselect("td")
        data = dict()
        data['photo'] = url + tds[0].cssselect("img")[0].attrib['src']
        data['name'] = tds[1].cssselect("a")[0].text_content()
        data['party'] = tds[2].text_content()
        data['constituency'] = tds[3].text_content()
        data['region'] = tds[4].text_content()
        if(data['constituency'] == u'\xa0'): data['constituency'] = ''
        if(data['region'] == u'\xa0'): data['region'] = ''
        members.append(data)
    return members

data = parseMG('http://www.senedd.assemblywales.org/')
scraperwiki.sqlite.save(unique_keys=['name'], data=data)

