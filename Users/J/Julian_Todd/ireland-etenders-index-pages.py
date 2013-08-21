import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

import mechanize
import re
import datetime
import lxml.etree
import lxml.html
import urlparse

# This one has defeated me.  I cannot make this follow the pagination
# We keep getting page 1 each time

url = 'http://etenders.gov.ie/search/Search_MainPageAdv.aspx'



def scrapepage(br, request):
    print "rrr", request.get_data()
    f0 = br.open(request)
    print "ttt", f0.read()
    br.select_form(name='aspnetForm')
    print [ c.name  for c in br.form.controls ]

    # the page selected (and the list from)
    pageselect = br.find_control('ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList')
    pageitems = [ item.name  for item in pageselect.items ]
    print pageitems
    print br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList']

    # select page 9
    br['ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'] = ['9']

    # implement the javascript that is called which notifies which nav bar is used
    br.find_control('__EVENTTARGET').readonly = False
    br['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$NavBar1$PageNoDropDownList'
    br.find_control('__EVENTARGUMENT').readonly = False
    br['__EVENTARGUMENT'] = ''

    request1 = br.form.click()
    return request1


def scrapedaterange(datefrom, dateto):
    # main lookup
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/3.0')]
    br.open(url)
    br.select_form(name='aspnetForm')
    sday = "%02d/%02d/%d" % (date.day, date.month, date.year)
    br['ctl00$ContentPlaceHolder1$txtDateAfter'] = "%02d/%02d/%d" % (datefrom.day, datefrom.month, datefrom.year)
    br['ctl00$ContentPlaceHolder1$txtDateBefore'] = "%02d/%02d/%d" % (dateto.day, dateto.month, dateto.year)
    br.find_control('ctl00$ContentPlaceHolder1$chkExpired').toggle('on')
    request0 = br.form.click('ctl00$ContentPlaceHolder1$cmdSearch')

    request1 = scrapepage(br, request0)

    # this should print page 9
    scrapepage(br, request1)
    return

    # call parser when this is done
    #root = lxml.html.parse(f0).getroot()
    #for tr in root.cssselect('tr.GridItem'):
    #    parserow(tr)


def parserecord(yurl):
    print yurl


def parserow(tr):
    data = { }

    v = lxml.etree.tostring(tr)
    assert len(tr) == 2, v
    td0, td1 = list(tr)

    imgs = list(td0)
    div = imgs.pop(0)

    data['date'] = div.text

    assert div.tag == 'div', v
    for img in imgs:
        assert img.tag == 'img', v
        timg = img.get('title')
        if timg == 'This image represents publication in the European Journal':
            data['OJEU'] = True
        elif timg == 'There are additional documents attached to this notice.':
            data['Attachments'] = True
        elif timg == 'This is a low value notice below the EU thresholds':
            data['OJEU'] = False
        else:
            assert timg == 'The Tender Submission Postbox can be used for this notice.', [timg]

    
    assert len(list(td1)) == 5, v
    a, br1, strong, br2, br3 = list(td1)
    assert a.tag == 'a', v
    assert (br1.tag, br2.tag, br3.tag) == ('br', 'br', 'br'), v

    data['url'] = urlparse.urljoin(url, a.get('href'))
    data['title'] = a.text

    mref = re.match("\s*Ref:\s*(\S*?),\s*", br1.tail)
    assert mref, br1.tail
    data['ref'] = mref.group(1)

    mby = re.match("\s*By\s*(.*)", br2.tail)
    assert mby, br2.tail
    data['by'] = mby.group(1)

    # unparsed
    #strong <strong>Deadline</strong>:&#13; 19-may-09&#13;
    #br3 <br />&#13; By&#13; Mercy University Hospital&#13;...more

    print data
    parserecord(data['url'])


date = datetime.datetime(2009, 5, 5)
scrapedaterange(date, date+datetime.timedelta(60))
#scrapeday(date+datetime.timedelta(1))

