import scraperwiki
import lxml.html


def flatten(el):          
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

def ascii(s): return "".join(i for i in s if ord(i)<128)

urlStub="http://www.parliament.uk/business/publications/business-papers/commons/deposited-papers/"
#http://www.parliament.uk/business/publications/business-papers/commons/deposited-papers/?max=10&page=2#toggle-1035

scraping=1
num=1000
page=1
tn='depositedPapers'
bigdata=[]
while (scraping):
    data={}
    url=urlStub+'?max='+str(num)+"&page="+str(page)
    page=page+1
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    if root.cssselect("div.no-results")!=[]:
        scraping=0
    else:
        rows=root.cssselect("div#results table tbody tr")
        for row in rows:
            data['ref']= row.cssselect('div.number')[0].text.strip()
            attachments=row.cssselect('ul.attachments li a')
            data['date']=row.cssselect('td.date')[0].text.strip()
            data['house']=row.cssselect('td.chamber span')[0].text.strip()
            data['by']=row.cssselect('td.deposited-by span')[0].text.strip()
            data['summary']=flatten(row.cssselect('div.notes')[0]).strip()
            for d in data: data[d]=ascii(data[d])
            for item in attachments:
                data['attachmentURL']=item.attrib['href']
                data['attachmentDesc']=ascii(item.text.strip())
                #scraperwiki.sqlite.save(unique_keys=['attachmentURL'], table_name=tn, data=data,verbose=0)
                bigdata.append(data.copy())
                if len(bigdata)>100:
                    scraperwiki.sqlite.save(unique_keys=['attachmentURL'], table_name=tn, data=bigdata,verbose=0)
                    bigdata=[]
scraperwiki.sqlite.save(unique_keys=['attachmentURL'], table_name=tn, data=bigdata,verbose=0)
