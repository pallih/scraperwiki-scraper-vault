import scraperwiki
import time


# Blank Python

import scraperwiki,urllib2,lxml.html,unicodedata
#data = scraperwiki.scrape("https://sites.google.com/site/mlhdatadump/addresslookup/AddrTest.csv")
data = scraperwiki.scrape("https://sites.google.com/site/mlhdatadump/addresslookup/NoVALookup2ToValidate6-22-2012.csv")

import csv           
reader = csv.reader(data.splitlines())

for row in reader:           
    LookupAddr = row[0]
    LookupCity = row[1]
    LookupState = row[2]
    LookupZip = row[3]
#print LookupAddr, LookupCity, LookupState
    
    url='https://tools.usps.com/go/ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1='+LookupAddr+'&address2=&city='+LookupCity+'&state='+LookupState+'&urbanCode=&postalCode=&zip='+LookupZip+''

    def load(url):
        retries = 10
        for i in range(retries):
            try:
                handle = urllib2.urlopen(url)
                return handle.read()
            except urllib2.URLError:
                if i + 1 == retries:
                    raise
                else:
                    time.sleep(42)

    print load(url)


#For typo'd addresses
    html=load(url)
    print html
    noresults = False
    valid = True
    apt = False
    typo = html.find("Unfortunately, this address wasn't found")
    if typo != -1:
        noresults=True
        data={1:"Unfortunately, this address wasn't found"}
        print "*"
    if typo == -1:
        nondel = html.find('The address you provided is not recognized')
        if nondel != -1:
            valid=False
            data={1:'The address you entered is invalid,'}
            print "*"
        if nondel == -1:
            multi = html.find('Several addresses matched the information you provided')
            if multi != -1:
                apt=True
                data={1:'The address you entered has n-deliverable addresses,'}
                print "*"

    if typo != -1:
        data={'noresults':noresults}
        print data
        scraperwiki.sqlite.save(table_name='address',data=data,unique_keys=[])




    else:
        root = lxml.html.fromstring(html).get_element_by_id('result-list')
        for cdata in root.cssselect("[class='data']"):
            #data={'valid':valid,'apt':apt,'error':error}
            data={'valid':valid,'apt':apt,'noresults':noresults}
            for addressbit in cdata.cssselect("[class='std-address'] span"): # the assertion that these are unique is FALSE; erases names.
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

