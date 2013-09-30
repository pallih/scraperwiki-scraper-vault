import scraperwiki
import urlparse
import lxml.html

cnt = 0
for page in range(1,5):
    url = "http://www.harrynorman.com/AgentResult.aspx?RecordType=3&0605=1&0040=1&0535=&AgoraPage={0}&AgoraItems=48&0520_order=ascending".format(page)
    html = scraperwiki.scrape(url)
    #print html
    tree = lxml.html.parse(url)
    data = {}
    for i in range(1,48):
        cnt = cnt+1
        data['slno'] = cnt
        data['name'] = tree.xpath("//div[@id='arItems']/div[{0}]/h2/text()".format(i))
        data['mail'] = tree.xpath("//div[@id='arItems']/div[{0}]/p[2]/a[1]/text()".format(i))
        #print data['name']
        scraperwiki.sqlite.save(['slno'], data)import scraperwiki
import urlparse
import lxml.html

cnt = 0
for page in range(1,5):
    url = "http://www.harrynorman.com/AgentResult.aspx?RecordType=3&0605=1&0040=1&0535=&AgoraPage={0}&AgoraItems=48&0520_order=ascending".format(page)
    html = scraperwiki.scrape(url)
    #print html
    tree = lxml.html.parse(url)
    data = {}
    for i in range(1,48):
        cnt = cnt+1
        data['slno'] = cnt
        data['name'] = tree.xpath("//div[@id='arItems']/div[{0}]/h2/text()".format(i))
        data['mail'] = tree.xpath("//div[@id='arItems']/div[{0}]/p[2]/a[1]/text()".format(i))
        #print data['name']
        scraperwiki.sqlite.save(['slno'], data)