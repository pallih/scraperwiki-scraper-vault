import scraperwiki
import mechanize
import string
import re
import itertools
import lxml.etree, lxml.html

pattern = re.compile("dgPublicRegistry[^']*")

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'
br = mechanize.Browser()
            # without this header the __EVENTTARGET and __EVENTARGUMENT will be missing
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br1 = mechanize.Browser()

def singleteacher(response):
    root = lxml.html.parse(response).getroot()
    div = root.cssselect('div#divSearchDetail')[0]
    #print lxml.etree.tostring(div)
    data = { }
    data['lastname'] = div.cssselect('span#lblLastName')[0].text.strip()
    data['givenname'] = div.cssselect('span#lblGivenName')[0].text.strip()
    data['certstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblHelpCertStatus')[0].text.strip() 
    data['pracstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblPracStatus')[0].text.strip() 

    vdate = div.cssselect('span#ctrlMemCurrCertStatus_lblCertStatus')[0].text.strip() 
    mdate = re.match('VALID To (\w\w\w) (\d+), (\d\d\d\d)$', vdate)
    if mdate:
        data['validity'] = 'VALID'
            # Convert this date properly!
        data['validdate'] = "%s-%s-%02d" % (mdate.group(3), mdate.group(1), int(mdate.group(2)))

    elif vdate == 'Cancelled - Non Payment of Fees':
        data['validity'] = 'CANCELLED'

    elif vdate == 'Expired Certificate':
        data['validity'] = 'EXPIRED'

    else:
        print vdate
        print data
        assert False


    scraperwiki.datastore.save(unique_keys=["lastname", "givenname"], data=data)



def scrape_page(br):
    root =lxml.html.parse(br.response()).getroot()
    #print lxml.etree.tostring(root)

    br.select_form('Form1')
    br.form.set_all_readonly(False)
    br.form.find_control('nav:top_search_submit').disabled=True

    trs = root.cssselect('table#dgPublicRegistry tr')
    for i, tr in enumerate(trs):
        me = re.search("__doPostBack\('(dgPublicRegistry:.*?)',''\)", lxml.etree.tostring(tr))
        if not me:
            assert i == 0 or i == len(trs) - 1
            #print lxml.etree.tostring(tr) #[td.text  for td in tr ]
            continue
        br['__EVENTTARGET'] = me.group(1)
        br['__EVENTARGUMENT'] = ''
        request = br.click()
        response = br1.open(request)
        singleteacher(response)


def scrapeletter(l):
    br.open(url)
    br.select_form(name='Form1')
    br.form['txtboxSurname'] = l

    br.submit('btnSearch')
    scrape_page(br)
    
    n = 2
    while True:
        try:
            link = br.find_link(text=str(n))
        except:
            try:
                link = br.find_link(text="[Next]")
            except:
                break

        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        br.form.find_control('nav:top_search_submit').disabled=True
        br['__EVENTTARGET'] = re.search("(dgPublicRegistry[^']*)", link.url).group(1)
        br['__EVENTARGUMENT'] = ''
        br.submit()
        print "page", n
        scrape_page(br)
        n += 1


#completed_letters = scraperwiki.metadata.get('completed_letters',[])
#print completed_letters
#for l in string.lowercase:
#    if l in completed_letters:
#        continue
#    scrapeletter(l)
#    completed_letters.append(l)
#    scraperwiki.metadata.save('completed_letters', completed_letters)
scrapeletter('a')

#scraperwiki.metadata.save('completed_letters', []) # Let's start again :)
import scraperwiki
import mechanize
import string
import re
import itertools
import lxml.etree, lxml.html

pattern = re.compile("dgPublicRegistry[^']*")

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'
br = mechanize.Browser()
            # without this header the __EVENTTARGET and __EVENTARGUMENT will be missing
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br1 = mechanize.Browser()

def singleteacher(response):
    root = lxml.html.parse(response).getroot()
    div = root.cssselect('div#divSearchDetail')[0]
    #print lxml.etree.tostring(div)
    data = { }
    data['lastname'] = div.cssselect('span#lblLastName')[0].text.strip()
    data['givenname'] = div.cssselect('span#lblGivenName')[0].text.strip()
    data['certstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblHelpCertStatus')[0].text.strip() 
    data['pracstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblPracStatus')[0].text.strip() 

    vdate = div.cssselect('span#ctrlMemCurrCertStatus_lblCertStatus')[0].text.strip() 
    mdate = re.match('VALID To (\w\w\w) (\d+), (\d\d\d\d)$', vdate)
    if mdate:
        data['validity'] = 'VALID'
            # Convert this date properly!
        data['validdate'] = "%s-%s-%02d" % (mdate.group(3), mdate.group(1), int(mdate.group(2)))

    elif vdate == 'Cancelled - Non Payment of Fees':
        data['validity'] = 'CANCELLED'

    elif vdate == 'Expired Certificate':
        data['validity'] = 'EXPIRED'

    else:
        print vdate
        print data
        assert False


    scraperwiki.datastore.save(unique_keys=["lastname", "givenname"], data=data)



def scrape_page(br):
    root =lxml.html.parse(br.response()).getroot()
    #print lxml.etree.tostring(root)

    br.select_form('Form1')
    br.form.set_all_readonly(False)
    br.form.find_control('nav:top_search_submit').disabled=True

    trs = root.cssselect('table#dgPublicRegistry tr')
    for i, tr in enumerate(trs):
        me = re.search("__doPostBack\('(dgPublicRegistry:.*?)',''\)", lxml.etree.tostring(tr))
        if not me:
            assert i == 0 or i == len(trs) - 1
            #print lxml.etree.tostring(tr) #[td.text  for td in tr ]
            continue
        br['__EVENTTARGET'] = me.group(1)
        br['__EVENTARGUMENT'] = ''
        request = br.click()
        response = br1.open(request)
        singleteacher(response)


def scrapeletter(l):
    br.open(url)
    br.select_form(name='Form1')
    br.form['txtboxSurname'] = l

    br.submit('btnSearch')
    scrape_page(br)
    
    n = 2
    while True:
        try:
            link = br.find_link(text=str(n))
        except:
            try:
                link = br.find_link(text="[Next]")
            except:
                break

        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        br.form.find_control('nav:top_search_submit').disabled=True
        br['__EVENTTARGET'] = re.search("(dgPublicRegistry[^']*)", link.url).group(1)
        br['__EVENTARGUMENT'] = ''
        br.submit()
        print "page", n
        scrape_page(br)
        n += 1


#completed_letters = scraperwiki.metadata.get('completed_letters',[])
#print completed_letters
#for l in string.lowercase:
#    if l in completed_letters:
#        continue
#    scrapeletter(l)
#    completed_letters.append(l)
#    scraperwiki.metadata.save('completed_letters', completed_letters)
scrapeletter('a')

#scraperwiki.metadata.save('completed_letters', []) # Let's start again :)
import scraperwiki
import mechanize
import string
import re
import itertools
import lxml.etree, lxml.html

pattern = re.compile("dgPublicRegistry[^']*")

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'
br = mechanize.Browser()
            # without this header the __EVENTTARGET and __EVENTARGUMENT will be missing
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br1 = mechanize.Browser()

def singleteacher(response):
    root = lxml.html.parse(response).getroot()
    div = root.cssselect('div#divSearchDetail')[0]
    #print lxml.etree.tostring(div)
    data = { }
    data['lastname'] = div.cssselect('span#lblLastName')[0].text.strip()
    data['givenname'] = div.cssselect('span#lblGivenName')[0].text.strip()
    data['certstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblHelpCertStatus')[0].text.strip() 
    data['pracstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblPracStatus')[0].text.strip() 

    vdate = div.cssselect('span#ctrlMemCurrCertStatus_lblCertStatus')[0].text.strip() 
    mdate = re.match('VALID To (\w\w\w) (\d+), (\d\d\d\d)$', vdate)
    if mdate:
        data['validity'] = 'VALID'
            # Convert this date properly!
        data['validdate'] = "%s-%s-%02d" % (mdate.group(3), mdate.group(1), int(mdate.group(2)))

    elif vdate == 'Cancelled - Non Payment of Fees':
        data['validity'] = 'CANCELLED'

    elif vdate == 'Expired Certificate':
        data['validity'] = 'EXPIRED'

    else:
        print vdate
        print data
        assert False


    scraperwiki.datastore.save(unique_keys=["lastname", "givenname"], data=data)



def scrape_page(br):
    root =lxml.html.parse(br.response()).getroot()
    #print lxml.etree.tostring(root)

    br.select_form('Form1')
    br.form.set_all_readonly(False)
    br.form.find_control('nav:top_search_submit').disabled=True

    trs = root.cssselect('table#dgPublicRegistry tr')
    for i, tr in enumerate(trs):
        me = re.search("__doPostBack\('(dgPublicRegistry:.*?)',''\)", lxml.etree.tostring(tr))
        if not me:
            assert i == 0 or i == len(trs) - 1
            #print lxml.etree.tostring(tr) #[td.text  for td in tr ]
            continue
        br['__EVENTTARGET'] = me.group(1)
        br['__EVENTARGUMENT'] = ''
        request = br.click()
        response = br1.open(request)
        singleteacher(response)


def scrapeletter(l):
    br.open(url)
    br.select_form(name='Form1')
    br.form['txtboxSurname'] = l

    br.submit('btnSearch')
    scrape_page(br)
    
    n = 2
    while True:
        try:
            link = br.find_link(text=str(n))
        except:
            try:
                link = br.find_link(text="[Next]")
            except:
                break

        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        br.form.find_control('nav:top_search_submit').disabled=True
        br['__EVENTTARGET'] = re.search("(dgPublicRegistry[^']*)", link.url).group(1)
        br['__EVENTARGUMENT'] = ''
        br.submit()
        print "page", n
        scrape_page(br)
        n += 1


#completed_letters = scraperwiki.metadata.get('completed_letters',[])
#print completed_letters
#for l in string.lowercase:
#    if l in completed_letters:
#        continue
#    scrapeletter(l)
#    completed_letters.append(l)
#    scraperwiki.metadata.save('completed_letters', completed_letters)
scrapeletter('a')

#scraperwiki.metadata.save('completed_letters', []) # Let's start again :)
import scraperwiki
import mechanize
import string
import re
import itertools
import lxml.etree, lxml.html

pattern = re.compile("dgPublicRegistry[^']*")

url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'
br = mechanize.Browser()
            # without this header the __EVENTTARGET and __EVENTARGUMENT will be missing
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br1 = mechanize.Browser()

def singleteacher(response):
    root = lxml.html.parse(response).getroot()
    div = root.cssselect('div#divSearchDetail')[0]
    #print lxml.etree.tostring(div)
    data = { }
    data['lastname'] = div.cssselect('span#lblLastName')[0].text.strip()
    data['givenname'] = div.cssselect('span#lblGivenName')[0].text.strip()
    data['certstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblHelpCertStatus')[0].text.strip() 
    data['pracstatus'] = div.cssselect('span#ctrlMemCurrCertStatus_lblPracStatus')[0].text.strip() 

    vdate = div.cssselect('span#ctrlMemCurrCertStatus_lblCertStatus')[0].text.strip() 
    mdate = re.match('VALID To (\w\w\w) (\d+), (\d\d\d\d)$', vdate)
    if mdate:
        data['validity'] = 'VALID'
            # Convert this date properly!
        data['validdate'] = "%s-%s-%02d" % (mdate.group(3), mdate.group(1), int(mdate.group(2)))

    elif vdate == 'Cancelled - Non Payment of Fees':
        data['validity'] = 'CANCELLED'

    elif vdate == 'Expired Certificate':
        data['validity'] = 'EXPIRED'

    else:
        print vdate
        print data
        assert False


    scraperwiki.datastore.save(unique_keys=["lastname", "givenname"], data=data)



def scrape_page(br):
    root =lxml.html.parse(br.response()).getroot()
    #print lxml.etree.tostring(root)

    br.select_form('Form1')
    br.form.set_all_readonly(False)
    br.form.find_control('nav:top_search_submit').disabled=True

    trs = root.cssselect('table#dgPublicRegistry tr')
    for i, tr in enumerate(trs):
        me = re.search("__doPostBack\('(dgPublicRegistry:.*?)',''\)", lxml.etree.tostring(tr))
        if not me:
            assert i == 0 or i == len(trs) - 1
            #print lxml.etree.tostring(tr) #[td.text  for td in tr ]
            continue
        br['__EVENTTARGET'] = me.group(1)
        br['__EVENTARGUMENT'] = ''
        request = br.click()
        response = br1.open(request)
        singleteacher(response)


def scrapeletter(l):
    br.open(url)
    br.select_form(name='Form1')
    br.form['txtboxSurname'] = l

    br.submit('btnSearch')
    scrape_page(br)
    
    n = 2
    while True:
        try:
            link = br.find_link(text=str(n))
        except:
            try:
                link = br.find_link(text="[Next]")
            except:
                break

        br.select_form(name='Form1')
        br.form.set_all_readonly(False)
        br.form.find_control('nav:top_search_submit').disabled=True
        br['__EVENTTARGET'] = re.search("(dgPublicRegistry[^']*)", link.url).group(1)
        br['__EVENTARGUMENT'] = ''
        br.submit()
        print "page", n
        scrape_page(br)
        n += 1


#completed_letters = scraperwiki.metadata.get('completed_letters',[])
#print completed_letters
#for l in string.lowercase:
#    if l in completed_letters:
#        continue
#    scrapeletter(l)
#    completed_letters.append(l)
#    scraperwiki.metadata.save('completed_letters', completed_letters)
scrapeletter('a')

#scraperwiki.metadata.save('completed_letters', []) # Let's start again :)
