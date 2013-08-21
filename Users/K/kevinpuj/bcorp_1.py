import scraperwiki,requests,re,lxml.html

# Blank Python
page=0
while True:
    page=page+1
    print "Page %d"%page


    url='http://www.bcorporation.net/index.cfm/fuseaction/company.getResults?page=%d'%page
    jsondata=requests.get(url).content
    print jsondata
    # json doesn't work :(
    # data=json.loads(jsondata)
    names=re.findall(r'"url": "(.*?)"',jsondata)
    if len(names)==0:
        exit()

    for item in names:
        print item
        try:
            data={'id':item}
            url='http://www.bcorporation.net/'+item
            html=requests.get(url).content
            #print html
            root = lxml.html.fromstring(html)
            for tr in root.cssselect("tr[class='category']"):
                try:
                    area=tr.cssselect("a[class='modal ']")[0].text_content()[:-2]
                except:
                    area=tr.cssselect("a[class='modal area-excellence']")[0].text_content()[:-2]
                try:
                    data[area]=float(tr.cssselect("td[class='points']")[0].text_content())
                except ValueError,e:
                    print "Badvalue in %s: %s - continuing."%(data['id'],e)
                    

            for tr in root.cssselect("tr[class='total']"):
                data['total']=float(tr.cssselect("td[class='points']")[0].text_content())
            for statitem in root.cssselect("ul[class='stats'] li"):
                if "Location:" in statitem.text_content():
                    data['location']=statitem.cssselect('span')[0].text_content()
            col1=root.get_element_by_id('col1').text_content().partition(u"The Change We Seek")
            data['change']=col1[2][1:].strip()
            (name,sep,about)=col1[0].strip().partition('\r\n')
            data['about']=about
            data['name']=name.partition('About ')[2]
            #print data
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        except:
            print "Something went wrong with id %s"%(data['id'])
            raise
            
        

#print data

"""  <ul class="stats">

        

            <li><strong>Product/Services:</strong> <span>Investment Management Service</span></li>

        

            <li><strong>Location:</strong> <span>Philadelphia, PA</span></li>

        

            <li><strong></span><a href="http://www.3sistersinvest.com" target="_blank">http://www.3sistersinvest.com</a></strong></li>

        

    </ul>"""
