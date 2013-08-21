import scraperwiki, requests, lxml.html, re

# Blank Python
baseurl='http://myneta.info/up2012/'

def getlist():
    html=requests.get(baseurl).content
    root=lxml.html.fromstring(html)
    for a in root.cssselect("table[width='100%'][align='center'][border='1'] tr td a"):
        yield (baseurl+a.attrib['href'],a.text_content().strip())

for con in getlist():
    print con
    buildup=[]
    data={}
    url=con[0]
    html=requests.get(url).content
    root=lxml.html.fromstring(html)
    dist=root.cssselect('title')[0].text_content().partition(':')[2].strip()
    for tr in root.cssselect("""table[border='1'][width='100%'] table[width='100%'] tr[onmouseover="this.style.backgroundColor='skyblue'"]"""):
        data={'dist':dist, 'cons':con[1]}
        tds=tr.cssselect('td')
        data['name']=tds[0].cssselect('a')[0].text_content()
        data['candurl']=baseurl+tds[0].cssselect('a')[0].attrib['href']
        data['winner']='Winner' in unicode(tds[0].text_content())
        data['party']=tds[1].text_content()
        data['crimcases']=int(tds[2].text_content())
        data['education']=tds[3].text_content()
        data['age']=int(tds[4].text_content())
        assets=unicode(tds[5].text_content()).replace(',','')
        try:
            data['assets']=int(re.match('Rs(.*)~',assets).group(1).strip())
        except:
            if 'Nil' in assets or 'nil' in assets:
                data['assets']=0
            else:
                print assets
                raise
        liab=unicode(tds[6].text_content()).replace(',','')
        data['liab']=int(re.match('Rs(.*)~',liab).group(1).strip())
        buildup.append(data)
        scraperwiki.sqlite.save(table_name='cand',data=data,unique_keys=[])

    