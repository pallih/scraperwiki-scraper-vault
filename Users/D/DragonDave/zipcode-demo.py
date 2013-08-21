import scraperwiki,urllib2,lxml.html,unicodedata,csv
# Blank Python

# url='https://tools.usps.com/go/ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=1483+trotters+cv&address2=&city=atlanta&state=ga&urbanCode=&postalCode=&zip='

data = scraperwiki.scrape("https://sites.google.com/site/mlhdatadump/addresslookup/AddrTest.csv")
reader = csv.read(data.splitlines())
for row in reader:
    

url='https://tools.usps.com/go/ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=' LookupAddr '&address2=&city=' LookupCity '&state=' LookupState'&urbanCode=&postalCode=&zip='

html=urllib2.urlopen(url).read()
print html
root = lxml.html.fromstring(html).get_element_by_id('result-list')
for cdata in root.cssselect("[class='data']"):
    data={}
    for addressbit in cdata.cssselect("[class='std-addrss'] span"):
        bitname=addressbit.attrib['class']
        bittext=addressbit.text_content()
        bitname=unicodedata.normalize('NFKD', unicode(bitname)).encode('ascii','ignore').replace('/','-')
        data[bitname]=bittext
    for hiddenbit in cdata.cssselect("dl[class='details'] dt"):
        bitname=hiddenbit.text_content()
        bittext=hiddenbit.getnext().text_content()
        bitname=unicodedata.normalize('NFKD', unicode(bitname)).encode('ascii','ignore').replace('/','-')
        data[bitname]=bittext
    print data
    scraperwiki.sqlite.save(table_name='address',data=data,unique_keys=[])
