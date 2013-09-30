import scraperwiki
from lxml import html

base_url = "http://fbinter.stadt-berlin.de/rbs/rbs-lookup.jsp"
#streets_url = "http://fbinter.stadt-berlin.de/rbs/rbs-lookup.jsp?beznr=&otnr=%s"
#streets_url = "http://fbinter.stadt-berlin.de/rbs/rbs-slct-str.jsp?beznr=&otnr=%s&strnr=&strname=&hausnr=&go=&mapLabel=&targetUrl="
streets_url = "http://fbinter.stadt-berlin.de/rbs/rbs-slct-str-liste.jsp?beznr=&targetUrl=&strname=&strnr=&mapLabel=&hausnr=&go=&otnr=%s"
houses_url = "http://fbinter.stadt-berlin.de/rbs/rbs-slct-hnr-liste.jsp?hausnr=&go=&targetUrl=&mapLabel=&strnr=%s&count=&singlestranr="
data_url = "http://fbinter.stadt-berlin.de/rbs/rbs-show-data-text.jsp?strnr=%s&hausnr=%s&targetUrl=&go=&mapLabel="

def get_data(street, house):
    url = data_url % (street, house)
    print url
    doc = html.parse(url)
    data = {'strnr': street, 'hausnr': house}
    for row in doc.findall('//table[@class="hnrresult"]//tr'):
        name, value = row.findall('./td')
        name = str(name.text_content().encode('ascii', 'ignore'))
        name = name.replace(':', '_').replace('.', '-').replace(' ', '_')
        value = value.xpath('string()').strip()
        data[name] = value
    print data
    #scraperwiki.sqlite.save(unique_keys=["strnr", "hausnr"], 
    #    data=data)
        

doc = html.parse(base_url)
for option in doc.findall('//select[@name="otnr"]/option'):
    sdoc = html.parse(streets_url % option.get('value'))
    for street in sdoc.findall('//input[@name="strnr"]'):
        hdoc = html.parse(houses_url % street.get('value'))
        for house in hdoc.findall('//input[@name="hausnr"]'):
            print house.items()
            print dir(house)
            #get_data(street.get('value'), house.get('value'))

import scraperwiki
from lxml import html

base_url = "http://fbinter.stadt-berlin.de/rbs/rbs-lookup.jsp"
#streets_url = "http://fbinter.stadt-berlin.de/rbs/rbs-lookup.jsp?beznr=&otnr=%s"
#streets_url = "http://fbinter.stadt-berlin.de/rbs/rbs-slct-str.jsp?beznr=&otnr=%s&strnr=&strname=&hausnr=&go=&mapLabel=&targetUrl="
streets_url = "http://fbinter.stadt-berlin.de/rbs/rbs-slct-str-liste.jsp?beznr=&targetUrl=&strname=&strnr=&mapLabel=&hausnr=&go=&otnr=%s"
houses_url = "http://fbinter.stadt-berlin.de/rbs/rbs-slct-hnr-liste.jsp?hausnr=&go=&targetUrl=&mapLabel=&strnr=%s&count=&singlestranr="
data_url = "http://fbinter.stadt-berlin.de/rbs/rbs-show-data-text.jsp?strnr=%s&hausnr=%s&targetUrl=&go=&mapLabel="

def get_data(street, house):
    url = data_url % (street, house)
    print url
    doc = html.parse(url)
    data = {'strnr': street, 'hausnr': house}
    for row in doc.findall('//table[@class="hnrresult"]//tr'):
        name, value = row.findall('./td')
        name = str(name.text_content().encode('ascii', 'ignore'))
        name = name.replace(':', '_').replace('.', '-').replace(' ', '_')
        value = value.xpath('string()').strip()
        data[name] = value
    print data
    #scraperwiki.sqlite.save(unique_keys=["strnr", "hausnr"], 
    #    data=data)
        

doc = html.parse(base_url)
for option in doc.findall('//select[@name="otnr"]/option'):
    sdoc = html.parse(streets_url % option.get('value'))
    for street in sdoc.findall('//input[@name="strnr"]'):
        hdoc = html.parse(houses_url % street.get('value'))
        for house in hdoc.findall('//input[@name="hausnr"]'):
            print house.items()
            print dir(house)
            #get_data(street.get('value'), house.get('value'))

