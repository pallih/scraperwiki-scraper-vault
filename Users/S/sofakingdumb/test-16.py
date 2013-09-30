url = "http://www.interpol.int/Public/Wanted/Search/Form.asp"
baseurl = "http://www.interpol.int"
searchbase= "http://www.interpol.int/Public/Wanted/Search/"

import mechanize 
import lxml.etree, lxml.html
import re
from lxml.html.clean import Cleaner
import scraperwiki

count = 0

def performSearch():
    global url
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='form1')
    br['cboNbHitsPerPage'] = ['200']
    br['cboNbPages']=['50']
    countrycontrol = br.form.find_control('ArrestWarrantIssuedBy')
    #print [ item.name  for item in countrycontrol.items ]

    # should be a loop over each country
    # (good way to thin this down as there always is an issuing country)
    print 'Submitting:',countrycontrol.items[160].name
    br['ArrestWarrantIssuedBy'] = [ countrycontrol.items[160].name ]  # happens to be NIGERIA

    response = br.submit()  # like a file handle object
    return response

######################################
#
# Main
#
######################################

def main():
    #print 
    parsepage(performSearch())
    #getlinks(url)


def getsusdata(url):
    global count
    data = {}
    #debug to track the url to visit
    print "get the links from "+url
    #call the retrieve function to try to get the url
    returl = retrieve(url)
    #check if data was returned
    if returl:
        #parse the address passed in
        root = lxml.html.parse(returl).getroot()
        #select the table elements
        sustable = root.cssselect('table')
        #get the interesting tables in a list
        instable=[sustable[3],sustable[5],sustable[7]]
        #create an empty list for clean tables
        cleantable=[]
        for i in instable:
            cleantable.append(cleanup(lxml.etree.tostring(i),['td','thead','font','strong']))
        
        for tr in cleantable[0].cssselect('tr'):
            if tr is not None:
                temp= tr.text
                if temp is not None:
                    temp = temp.replace("\n", "")
                    ele=temp.split(':')
                    data[ele[0]] = ele[1]
                    data['Count']=count
                    
        scraperwiki.datastore.save(["Count"],data)
        count +=1
    else:
        print "unable to get the links"

def retrieve(url):
    check = False
    try:
        html=mechanize.Browser()
        html.set_handle_robots(False)
        html.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7')]
        data=html.open(url)
        check=True
    except:
        print "unable to retrieve page"
    if check:
        return data
    else:
        return check

def cleanup(data,tags):
    cleaner= Cleaner(remove_tags=tags)
    clean=cleaner.clean_html(data)
    root = lxml.html.fromstring(clean)
    return root

def parsepage(response):
    root = lxml.html.parse(response).getroot()
    tables = root.cssselect('table')

    # the elements are not given classes or ids, so we have to find them by index ("the 4th table in the page")

    # extract result numbers (to verify matching rest of data is consistent)
    print [ b.text  for b in tables[3].cssselect('tr td font b') ]

    #SFD:additions to get suspect links
    susurls=[]
    #SFD:additions to get suspect links

    for susimage in tables[4].cssselect('table table img'):
        #print "--", lxml.etree.tostring(susimage)
        susdata = susimage
    #SFD:additions to get suspect links
        suslinks = susdata.getparent()
    
        susurls.append([a.get('href') for a in suslinks.cssselect('a')])

        for i,url in enumerate(susurls):
            getsusdata(baseurl+url[0])

    nexturl = [a.get('href') for a in root.cssselect('a')if re.search(r"Next", lxml.etree.tostring(a))]
    if nexturl:
        print baseurl+nexturl[0]
        ret=retrieve(searchbase+nexturl[0])
        if ret:
            parsepage(ret)
        

main()

'''
countrycontrol = br.form.find_control('ArrestWarrantIssuedBy')
print [ item.name  for item in countrycontrol.items ]

# should be a loop over each country
# (good way to thin this down as there always is an issuing country)
br['ArrestWarrantIssuedBy'] = [ countrycontrol.items[160].name ]  # happens to be NIGERIA

response = br.submit()  # like a file handle object

# lxml not the most friendly library, but good when you use cssselect; and it 
# handles all the string character escaping issues

root = lxml.html.parse(response).getroot()
tables = root.cssselect('table')

# the elements are not given classes or ids, so we have to find them by index ("the 4th table in the page")

# extract result numbers (to verify matching rest of data is consistent)
print [ b.text  for b in tables[3].cssselect('tr td font b') ]

for susimage in tables[4].cssselect('table table img'):
    print "--", lxml.etree.tostring(susimage)
    susdata = susimage
    for i in range(7):
        susdata = susdata.getparent()

    # print out the unstructured data from the fields
    print "\n\n".join([ lxml.etree.tostring(td)  for td in susdata.cssselect('td') ])

    # To do:
    # (1) get the structured fields out of this table and structure it
    # (2) step into each page per suspect and parse the data out of that
    # (3) save the data to the datastore
    # (4) worry about how we improve the datastore so as to monitor changes to what appears on the interpol webpage


'''
url = "http://www.interpol.int/Public/Wanted/Search/Form.asp"
baseurl = "http://www.interpol.int"
searchbase= "http://www.interpol.int/Public/Wanted/Search/"

import mechanize 
import lxml.etree, lxml.html
import re
from lxml.html.clean import Cleaner
import scraperwiki

count = 0

def performSearch():
    global url
    br = mechanize.Browser()
    br.open(url)
    br.select_form(name='form1')
    br['cboNbHitsPerPage'] = ['200']
    br['cboNbPages']=['50']
    countrycontrol = br.form.find_control('ArrestWarrantIssuedBy')
    #print [ item.name  for item in countrycontrol.items ]

    # should be a loop over each country
    # (good way to thin this down as there always is an issuing country)
    print 'Submitting:',countrycontrol.items[160].name
    br['ArrestWarrantIssuedBy'] = [ countrycontrol.items[160].name ]  # happens to be NIGERIA

    response = br.submit()  # like a file handle object
    return response

######################################
#
# Main
#
######################################

def main():
    #print 
    parsepage(performSearch())
    #getlinks(url)


def getsusdata(url):
    global count
    data = {}
    #debug to track the url to visit
    print "get the links from "+url
    #call the retrieve function to try to get the url
    returl = retrieve(url)
    #check if data was returned
    if returl:
        #parse the address passed in
        root = lxml.html.parse(returl).getroot()
        #select the table elements
        sustable = root.cssselect('table')
        #get the interesting tables in a list
        instable=[sustable[3],sustable[5],sustable[7]]
        #create an empty list for clean tables
        cleantable=[]
        for i in instable:
            cleantable.append(cleanup(lxml.etree.tostring(i),['td','thead','font','strong']))
        
        for tr in cleantable[0].cssselect('tr'):
            if tr is not None:
                temp= tr.text
                if temp is not None:
                    temp = temp.replace("\n", "")
                    ele=temp.split(':')
                    data[ele[0]] = ele[1]
                    data['Count']=count
                    
        scraperwiki.datastore.save(["Count"],data)
        count +=1
    else:
        print "unable to get the links"

def retrieve(url):
    check = False
    try:
        html=mechanize.Browser()
        html.set_handle_robots(False)
        html.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.44 Safari/534.7')]
        data=html.open(url)
        check=True
    except:
        print "unable to retrieve page"
    if check:
        return data
    else:
        return check

def cleanup(data,tags):
    cleaner= Cleaner(remove_tags=tags)
    clean=cleaner.clean_html(data)
    root = lxml.html.fromstring(clean)
    return root

def parsepage(response):
    root = lxml.html.parse(response).getroot()
    tables = root.cssselect('table')

    # the elements are not given classes or ids, so we have to find them by index ("the 4th table in the page")

    # extract result numbers (to verify matching rest of data is consistent)
    print [ b.text  for b in tables[3].cssselect('tr td font b') ]

    #SFD:additions to get suspect links
    susurls=[]
    #SFD:additions to get suspect links

    for susimage in tables[4].cssselect('table table img'):
        #print "--", lxml.etree.tostring(susimage)
        susdata = susimage
    #SFD:additions to get suspect links
        suslinks = susdata.getparent()
    
        susurls.append([a.get('href') for a in suslinks.cssselect('a')])

        for i,url in enumerate(susurls):
            getsusdata(baseurl+url[0])

    nexturl = [a.get('href') for a in root.cssselect('a')if re.search(r"Next", lxml.etree.tostring(a))]
    if nexturl:
        print baseurl+nexturl[0]
        ret=retrieve(searchbase+nexturl[0])
        if ret:
            parsepage(ret)
        

main()

'''
countrycontrol = br.form.find_control('ArrestWarrantIssuedBy')
print [ item.name  for item in countrycontrol.items ]

# should be a loop over each country
# (good way to thin this down as there always is an issuing country)
br['ArrestWarrantIssuedBy'] = [ countrycontrol.items[160].name ]  # happens to be NIGERIA

response = br.submit()  # like a file handle object

# lxml not the most friendly library, but good when you use cssselect; and it 
# handles all the string character escaping issues

root = lxml.html.parse(response).getroot()
tables = root.cssselect('table')

# the elements are not given classes or ids, so we have to find them by index ("the 4th table in the page")

# extract result numbers (to verify matching rest of data is consistent)
print [ b.text  for b in tables[3].cssselect('tr td font b') ]

for susimage in tables[4].cssselect('table table img'):
    print "--", lxml.etree.tostring(susimage)
    susdata = susimage
    for i in range(7):
        susdata = susdata.getparent()

    # print out the unstructured data from the fields
    print "\n\n".join([ lxml.etree.tostring(td)  for td in susdata.cssselect('td') ])

    # To do:
    # (1) get the structured fields out of this table and structure it
    # (2) step into each page per suspect and parse the data out of that
    # (3) save the data to the datastore
    # (4) worry about how we improve the datastore so as to monitor changes to what appears on the interpol webpage


'''
