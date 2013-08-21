import scraperwiki
import lxml.html
import sys

urls=[]
for i in range(1,58):
    url = "http://apps.webofknowledge.com/summary.do?product=WOS&search_mode=CitationReport&qid=18&SID=R1D1A6aFJJHBDkcC1am&&page=" + str(i);
    urls.append(url)

for url in urls:
    html = scraperwiki.scrape(url)   
    root = lxml.html.fromstring(html)
    trs = root.cssselect("tr ")
    for tr in trs:
        tds = tr.cssselect("td [class='summary_data']")
        for td in tds:
            papername = td.cssselect("value")
            name = papername[0].text_content()        
            paperlinks = td.cssselect("a")
            p = paperlinks[0]
            plink = "http://apps.webofknowledge.com" + p.attrib.get('href')
            data = { 'papername' : name, 'link' : plink}
            scraperwiki.sqlite.save(unique_keys=['papername'], data=data,  table_name="webofknowledge2")
            





