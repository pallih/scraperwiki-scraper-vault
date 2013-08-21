import scraperwiki


# Blank Python

import scraperwiki,urllib2,lxml.html,unicodedata
#data = scraperwiki.scrape("https://sites.google.com/site/mlhdatadump/addresslookup/AddrTest.csv")
data = scraperwiki.scrape("https://sites.google.com/site/mlhdatadump/addresslookup/GivenAddressesForValidation6-11-2012.csv")

import csv           
reader = csv.reader(data.splitlines())

for row in reader:           
    LookupAddr = row[0]
    LookupCity = row[1]
    LookupState = row[2]
#print LookupAddr, LookupCity, LookupState
    
    url='https://tools.usps.com/go/ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1='+LookupAddr+'&address2=&city='+LookupCity+'&state='+LookupState+'&urbanCode=&postalCode=&zip='


# Below is my attempt at searching for the string that indicates a non-deliverable address. If the string is found, nondel != -1 and a message indicating that the address is not valid should be printed to the results. If the invalid address string is not found, the address from the results page should be printed.
    html=urllib2.urlopen(url).read()
    print html
    nondel = html.find('The address you provided is not recognized')
    valid=True
    apt = False
    if nondel != -1:
        valid=False
        data={1:'The address you entered is invalid,'}
        print "*"

#For typo'd addresses
    html=urllib2.urlopen(url).read()
    print html
    typo = html.find("Unfortunately, this address wasn't found")
    noresults = False
    valid = valid
    apt = apt
    if typo != -1:
        noresults=True
        data={1:"Unfortunately, this address wasn't found"}
        print "*"


#Finding addresses with multiple mailboxes
    html=urllib2.urlopen(url).read()
    print html
    multi = html.find('Several addresses matched the information you provided')
    apt = False
    if multi != -1:
        apt=True
        data={1:'The address you entered has n-deliverable addresses,'}
        print "*"

    if typo == -1:    
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
    
    else:
        #root = lxml.html.fromstring(html).get_element_by_class('noresults-container')
        #for cdata in root.cssselect("[class='error']"):
            #data={'noresults':noresults}
            #print data
        data={'noresults':noresults}
        print data
        scraperwiki.sqlite.save(table_name='address',data=data,unique_keys=[])
