# FromSebacon_energyshare top 100
import scraperwiki
from pyquery import PyQuery as pq
data = []
p = 1
count = 1
while count <= 100:
#    url = "http://www.energyshare.com/groups/followers/p:%d" % p

    url = "http://www.50hertz-transmission.net/cps/rde/papp/SID-B9786E3A-E692AA5F/apc_nextgen_inter_trm-prod/http://miniapp-internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=-1&bundesland.id=&pagingDescriptor.currentPage=%d" + "&spannungsebene.id=" % p


# print url

    html = scraperwiki.scrape(url)
    doc = pq(html)
    items = doc("div.new-group-listing div.column")
    for item in items:
        link = pq(item)('h6 a')[0]
#        title = link.attrib['title']
#        href = link.attrib['href']
#        supporters = int(pq(item)("p.color-silver:first").text().replace("Supporters ", ""))
#        data = {'rank': count,
#                'project':title,
#                'url':href,
#                'supporters': supporters}
#        count += 1
#        scraperwiki.sqlite.save(unique_keys=data.keys(), data=data)
    p += 1# FromSebacon_energyshare top 100
import scraperwiki
from pyquery import PyQuery as pq
data = []
p = 1
count = 1
while count <= 100:
#    url = "http://www.energyshare.com/groups/followers/p:%d" % p

    url = "http://www.50hertz-transmission.net/cps/rde/papp/SID-B9786E3A-E692AA5F/apc_nextgen_inter_trm-prod/http://miniapp-internet.corp.transmission-it.de:8081/ma-trm-eegdata/Report.action?prepare=&_sourcePage=%2FWEB-INF%2Fpages%2Freport.jsp&reportType=masterDataEEG&eegYear=&filter.allEnergySources=true&kunde.id=-1&bundesland.id=&pagingDescriptor.currentPage=%d" + "&spannungsebene.id=" % p


# print url

    html = scraperwiki.scrape(url)
    doc = pq(html)
    items = doc("div.new-group-listing div.column")
    for item in items:
        link = pq(item)('h6 a')[0]
#        title = link.attrib['title']
#        href = link.attrib['href']
#        supporters = int(pq(item)("p.color-silver:first").text().replace("Supporters ", ""))
#        data = {'rank': count,
#                'project':title,
#                'url':href,
#                'supporters': supporters}
#        count += 1
#        scraperwiki.sqlite.save(unique_keys=data.keys(), data=data)
    p += 1