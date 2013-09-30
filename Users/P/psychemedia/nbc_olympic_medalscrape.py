import scraperwiki
from lxml import etree


rooturl='http://www.nbcolympics.com/medals/library/2012-standings/tabs/medals/_overall.html'

xmldata=etree.parse(rooturl)
xmlRoot = xmldata.getroot()
tb=xmlRoot.find('.//tbody')

def flatten(el):
    if el != None:
        result = [ (el.text or "") ]
        for sel in el:
            result.append(flatten(sel))
            result.append(sel.tail or "")
        return "".join(result)
    return ''


countries={}
rows=tb.findall('.//tr')
for row in rows:
    cells=row.findall('.//td')
    #for cell in cells:
    #    print cell.text
    if cells[0].get('class')!='nbc-ruler':
        #print flatten(cells[0])
        cd=cells[0].find('.//a')
        countries[cells[0].find('.//img').get('alt')]=cd.get("href")
        #print cd.get("href"),cd.text.strip(), cells[0].find('.//img').get('alt'),cells[3].text,cells[4].text,cells[4].text
    else: break

def parseCountryPage(url,cc):
    xmldata=etree.parse(url)
    xmlRoot = xmldata.getroot()
    tb=xmlRoot.find('.//tbody')
    rows=tb.findall('.//tr')
    for row in rows[1:]:
        #<tr class="or-even"><td class="athlete-sport"><a href="/archery/index.html" title="Archery">Archery </a></td><td class="or-gold or-c">0</td><td class="or-silver or-c">1</td><td class="or-bronze or-c">0</td><td class="or-total or-c">1</td></tr>
        cells=row.findall('.//td')
        event=flatten(cells[0]).strip()
        print flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3])
        data = { 'ccevent':cc+'_'+flatten(cells[0]).strip(),'cc':cc, 'Event':event,'Gold':int(flatten(cells[1])), 'Silver':int(flatten(cells[2])), 'Bronze':int(flatten(cells[3] ))}
        print data
        scraperwiki.sqlite.save(unique_keys=['ccevent'],table_name='medalStandings', data=data)
        m=1
        for medal in ['Gold','Silver','Bronze']:
            haul=int(flatten(cells[m]))
            if haul > 0:
                data = {'ccem':cc+'_'+event+'_'+medal,'cc':cc, 'Event':event,'Medal':medal,'Haul':haul}
                scraperwiki.sqlite.save(unique_keys=['ccem'],table_name='medalAllocation', data=data)
            m=m+1

#returns /nations/nation=china/index.html?etx=medals&etx2=2012-medals
#http://www.nbcolympics.com/nations/nation=united-states/medals/tabs/_2012-medals.html
#scraperwiki.sqlite.execute("drop table if exists 'medalAllocation'")

urlstub='http://www.nbcolympics.com/nations/nation='
for country in countries:
    cStub=countries[country].split('=')[1]
    cStub=cStub.split('/')[0]
    if country=='USA': cStub='united-states'
    url=urlstub+cStub+'/medals/tabs/_2012-medals.html'
    parseCountryPage(url,country)

import scraperwiki
from lxml import etree


rooturl='http://www.nbcolympics.com/medals/library/2012-standings/tabs/medals/_overall.html'

xmldata=etree.parse(rooturl)
xmlRoot = xmldata.getroot()
tb=xmlRoot.find('.//tbody')

def flatten(el):
    if el != None:
        result = [ (el.text or "") ]
        for sel in el:
            result.append(flatten(sel))
            result.append(sel.tail or "")
        return "".join(result)
    return ''


countries={}
rows=tb.findall('.//tr')
for row in rows:
    cells=row.findall('.//td')
    #for cell in cells:
    #    print cell.text
    if cells[0].get('class')!='nbc-ruler':
        #print flatten(cells[0])
        cd=cells[0].find('.//a')
        countries[cells[0].find('.//img').get('alt')]=cd.get("href")
        #print cd.get("href"),cd.text.strip(), cells[0].find('.//img').get('alt'),cells[3].text,cells[4].text,cells[4].text
    else: break

def parseCountryPage(url,cc):
    xmldata=etree.parse(url)
    xmlRoot = xmldata.getroot()
    tb=xmlRoot.find('.//tbody')
    rows=tb.findall('.//tr')
    for row in rows[1:]:
        #<tr class="or-even"><td class="athlete-sport"><a href="/archery/index.html" title="Archery">Archery </a></td><td class="or-gold or-c">0</td><td class="or-silver or-c">1</td><td class="or-bronze or-c">0</td><td class="or-total or-c">1</td></tr>
        cells=row.findall('.//td')
        event=flatten(cells[0]).strip()
        print flatten(cells[0]),flatten(cells[1]),flatten(cells[2]),flatten(cells[3])
        data = { 'ccevent':cc+'_'+flatten(cells[0]).strip(),'cc':cc, 'Event':event,'Gold':int(flatten(cells[1])), 'Silver':int(flatten(cells[2])), 'Bronze':int(flatten(cells[3] ))}
        print data
        scraperwiki.sqlite.save(unique_keys=['ccevent'],table_name='medalStandings', data=data)
        m=1
        for medal in ['Gold','Silver','Bronze']:
            haul=int(flatten(cells[m]))
            if haul > 0:
                data = {'ccem':cc+'_'+event+'_'+medal,'cc':cc, 'Event':event,'Medal':medal,'Haul':haul}
                scraperwiki.sqlite.save(unique_keys=['ccem'],table_name='medalAllocation', data=data)
            m=m+1

#returns /nations/nation=china/index.html?etx=medals&etx2=2012-medals
#http://www.nbcolympics.com/nations/nation=united-states/medals/tabs/_2012-medals.html
#scraperwiki.sqlite.execute("drop table if exists 'medalAllocation'")

urlstub='http://www.nbcolympics.com/nations/nation='
for country in countries:
    cStub=countries[country].split('=')[1]
    cStub=cStub.split('/')[0]
    if country=='USA': cStub='united-states'
    url=urlstub+cStub+'/medals/tabs/_2012-medals.html'
    parseCountryPage(url,country)

