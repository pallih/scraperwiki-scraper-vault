import scraperwiki, urllib2, lxml.html, re

# Blank Python


scraperwiki.sqlite.attach('rasff_portal')



try:
    details=scraperwiki.sqlite.select('detail_url from rasff_portal.swdata except select url from detail')
except:
    details=scraperwiki.sqlite.select('detail_url from rasff_portal.swdata')
urls = [x['detail_url'] for x in details]

print 'Left: ', len(urls)


for url in urls:
    #print url
    data={'url':url}
    html=urllib2.urlopen(url).read()
    root=lxml.html.fromstring(html).cssselect("div[class='BoxA']")[0]

    data['title']=root.cssselect('h2')[0].text_content()

    for th in root.cssselect("th[scope='row']"):
        cat=th.text_content()[:-3]
        if cat=='': continue
        info=th.getnext().cssselect('input')[0].attrib['value']
        data[cat]=info

    for legend in root.cssselect("fieldset legend"):
        cat=legend.text_content()[:-2]
        #print cat
        trs=legend.getnext().cssselect('tr')
        header=[item.text_content() for item in trs[0].cssselect('th')]
        #print header
        if header: #followup/hazards
            builder=[]
            for tr in trs[1:]: # ignore header
                haz={'Reference':data['Reference']} # populate row
                info=[item.attrib['value'] for item in tr.cssselect('input')]
                for item in zip(header,info):
                    haz[item[0].replace('/','-')]=item[1]
                builder.append(haz)

            # spew this data, line by line, tallying with headers elsewhere
                #print info
            data[cat+'_num']=len(trs)-1
            #print builder
            scraperwiki.sqlite.save(table_name=cat, data=builder, unique_keys=[],verbose=1)
            
        else: # distributed to / origin
            data[cat+'_text']=re.sub('[\n\t| ]','',trs[0].text_content()).strip().replace(u'\xa0',' ')
            #print data[cat+'_text']
    scraperwiki.sqlite.save(table_name='detail', data=data, unique_keys=['Reference'], verbose=1)
        
    import scraperwiki, lxml.html, re
import requests
# Blank Python

s = requests.session()

pick_up_cookies_url = 'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=searchResultList'

s.get(pick_up_cookies_url, verify=False)

scraperwiki.sqlite.attach('rasff_portal')

try:
    details=scraperwiki.sqlite.select('detail_url from rasff_portal.swdata except select url from detail')
except:
    details=scraperwiki.sqlite.select('detail_url from rasff_portal.swdata')
urls = [x['detail_url'] for x in details]

print 'Left: ', len(urls)


for url in urls:
    data={'url':url}
    #html=opener.open(url).read()
    html = s.get(url, verify=False).text
    root=lxml.html.fromstring(html).cssselect("div[class='BoxA']")[0]

    data['title']=root.cssselect('h2')[0].text_content()

    for th in root.cssselect("th[scope='row']"):
        cat=th.text_content()[:-3]
        if cat=='': continue
        info=th.getnext().cssselect('input')[0].attrib['value']
        data[cat]=info

    for legend in root.cssselect("fieldset legend"):
        cat=legend.text_content()[:-2]
        trs=legend.getnext().cssselect('tr')
        header=[item.text_content() for item in trs[0].cssselect('th')]
        if header: #followup/hazards
            builder=[]
            for tr in trs[1:]: # ignore header
                haz={'Reference':data['Reference']} # populate row
                info=[item.attrib['value'] for item in tr.cssselect('input')]
                for item in zip(header,info):
                    haz[item[0].replace('/','-')]=item[1]
                builder.append(haz)

            # spew this data, line by line, tallying with headers elsewhere
                #print info
            data[cat+'_num']=len(trs)-1
            #print builder
            scraperwiki.sqlite.save(table_name=cat, data=builder, unique_keys=[], verbose=1)
            
        else: # distributed to / origin
            data[cat+'_text']=re.sub('[\n\t| ]','',trs[0].text_content()).strip().replace(u'\xa0',' ')
            #print data[cat+'_text']
    scraperwiki.sqlite.save(table_name='detail', data=data, unique_keys=['Reference'], verbose=1)
        
    