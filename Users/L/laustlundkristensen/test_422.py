import scraperwiki
import lxml.html

for num in range(1,202): 
    html = scraperwiki.scrape("http://www.yellowpages.co.za/hearing_aid_service/hearing_aid_service/" + str(num))
    list = lxml.html.fromstring(html).cssselect("div#results-list > div")
#    print list
    i = 0
    for el in list:
        data = {}
        i = i + 1
        data['id'] = str(num) + " - " + el.attrib['id']
        d = el.cssselect("div.resultAddressbar h2")
        if len(d) == 1:
            try: 
                data['name'] = lxml.etree.tostring(d[0], method="text", encoding=unicode)
            except UnicodeEncodeError:
                print lxml.etree.tostring(d[0])
        d = el.cssselect("div.resultAddressbar div.where")
        if len(d) == 1:
            data['address'] = lxml.etree.tostring(d[0], method="text")
        d = el.cssselect("div.details h3")
        if len(d) == 1:
            data['tel'] = lxml.etree.tostring(d[0], method="text")
        d = el.cssselect("div.details div.resultFaxBar")
        if len(d) == 1:
            data['fax'] = lxml.etree.tostring(d[0], method="text")
        d = el.cssselect("div.details div.resultEmailBar")
        if len(d) == 1:
            data['email'] = lxml.etree.tostring(d[0])
        d = el.cssselect("div.details div.resultWebsiteBar")
        if len(d) == 1:
            data['website'] = lxml.etree.tostring(d[0])
        d = el.cssselect("div.resultAddressbar > div.resultDirectionBar > a")
        if len(d) == 1:
            data['latlong'] = d[0].attrib["href"]

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

