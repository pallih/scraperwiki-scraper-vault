import scraperwiki
import mechanize
import lxml.html


'''http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python'''


base_url = 'https://healthri.mylicense.com/'
url = 'https://healthri.mylicense.com/Verification/Search.aspx'
headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br = mechanize.Browser()
br2 = mechanize.Browser()
br.addheaders = headers
br2.addheaders = headers

br.open(url)


print url

'''function for parsing a record when we get a proper page of results'''
def pageParser(stuff): #when to use 'self'
    '''this is the test parser for each page of results, put this in a function'''
    for el in stuff.cssselect("table.rgMasterTable tbody tr td"):
        for guy in el.cssselect("a"):
            desc = guy.text
            linky = guy.attrib['href']
            #print linky
            '''go into each record and scrape a smoke signal'''
            br2.open(base_url+linky)
            html = br2.response().read()
            dom = lxml.html.fromstring(html)
            dumps = dom.cssselect('#ctl00_ContentPlaceHolder1_hypInControlOf2')
            for i in dumps:
                print i.text


'''Mechanize patch till fixed: https://bitbucket.org/ScraperWiki/scraperwiki/issue/963/mechanize-library-breaks-on-known'''
html = br.response().read()
dom = lxml.html.fromstring(html)

bad_form = dom.cssselect('#aspnetForm')[0]
bad_inputs = bad_form.cssselect('input')

#for el in bad_inputs:
print el

bad_inputs[0].set('value', '1')

'''disable the disabled button - so we can advance'''
bad_inputs[8].getparent().remove(bad_inputs[8])

good_form = lxml.html.tostring(bad_form)
print good_form

mech_form = mechanize._form.ParseString(good_form, br.geturl())

br.form = mech_form[1]

#req = br.submit()


req = br.click(type="submit", nr=0)
res = br.open(req)
#data = res.read()


'''go to the next page and repeat (probably going to need to modularize things),
   or just check out https://github.com/fgregg/legistar-scrape/blob/master/legistar/scraper.py : lines 84 - 112.
   loop the pages and get it all'''

got_all = False

while got_all is False:
    
    data = res.read()
    '''parse data for one page only'''

    root = lxml.html.fromstring(data)

    '''get form post request data'''
    viewstate = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    event_arg = root.xpath('//input[@name="__EVENTARGUMENT"]')[0].attrib['value']
    vstate = root.xpath('//input[@name="__VSTATE"]')[0].attrib['value']
    
    #pageParser(root)
    
    current_scrape = root.cssselect("a.rgCurrentPage") #get current page link at a.rgCurrentPage    
    
    next_scrape = current_scrape[1].getnext()

    if current_scrape: 
        
        current_scrape = current_scrape[0]
        
        print 'page: ',  current_scrape.text

        

    else:
        next_scrape = None

    if next_scrape is not None:
        '''next scrape should open up the next link as a response and head back to the top of the loop to scrape that via pageParser()
           trickiest part here because you have to send data from the next_scrape back as post information to the form, not as a link to click'''


        event_target = next_scrape.attrib['href'].split("'")[1]
        print "Hi, my name is: ", event_target


        '''send the event target with the form and submit to get next page'''
        br.select_form('aspnetForm')        
        br.set_all_readonly(False)
        br['__EVENTTARGET'] = event_target
        br['__EVENTARGUMENT'] = event_arg
        br['__VIEWSTATE'] = viewstate
        br['__VSTATE'] = vstate
               
        '''disable submit buttons'''
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch2').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear2').disabled = True
        
        
        '''Keeps scraping the same page: see - http://stackoverflow.com/questions/13114977/why-does-this-scraperwiki-for-an-aspx-site-return-only-the-same-page-of-search-r
        http://stackoverflow.com/questions/6116023/screenscaping-aspx-with-python-mechanize-javascript-form-submission'''
        res = br.submit()

        #got_all = True #only for testing
        print "And we're out"        
            
    else:
        got_all = True #if there are no other links to follow, we are done, exit the loop
        print "I got everything, I got nothing!"


'''Save rows to a scraperwiki (we will figure out a better way of storing later)'''import scraperwiki
import mechanize
import lxml.html


'''http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python'''


base_url = 'https://healthri.mylicense.com/'
url = 'https://healthri.mylicense.com/Verification/Search.aspx'
headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br = mechanize.Browser()
br2 = mechanize.Browser()
br.addheaders = headers
br2.addheaders = headers

br.open(url)


print url

'''function for parsing a record when we get a proper page of results'''
def pageParser(stuff): #when to use 'self'
    '''this is the test parser for each page of results, put this in a function'''
    for el in stuff.cssselect("table.rgMasterTable tbody tr td"):
        for guy in el.cssselect("a"):
            desc = guy.text
            linky = guy.attrib['href']
            #print linky
            '''go into each record and scrape a smoke signal'''
            br2.open(base_url+linky)
            html = br2.response().read()
            dom = lxml.html.fromstring(html)
            dumps = dom.cssselect('#ctl00_ContentPlaceHolder1_hypInControlOf2')
            for i in dumps:
                print i.text


'''Mechanize patch till fixed: https://bitbucket.org/ScraperWiki/scraperwiki/issue/963/mechanize-library-breaks-on-known'''
html = br.response().read()
dom = lxml.html.fromstring(html)

bad_form = dom.cssselect('#aspnetForm')[0]
bad_inputs = bad_form.cssselect('input')

#for el in bad_inputs:
print el

bad_inputs[0].set('value', '1')

'''disable the disabled button - so we can advance'''
bad_inputs[8].getparent().remove(bad_inputs[8])

good_form = lxml.html.tostring(bad_form)
print good_form

mech_form = mechanize._form.ParseString(good_form, br.geturl())

br.form = mech_form[1]

#req = br.submit()


req = br.click(type="submit", nr=0)
res = br.open(req)
#data = res.read()


'''go to the next page and repeat (probably going to need to modularize things),
   or just check out https://github.com/fgregg/legistar-scrape/blob/master/legistar/scraper.py : lines 84 - 112.
   loop the pages and get it all'''

got_all = False

while got_all is False:
    
    data = res.read()
    '''parse data for one page only'''

    root = lxml.html.fromstring(data)

    '''get form post request data'''
    viewstate = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    event_arg = root.xpath('//input[@name="__EVENTARGUMENT"]')[0].attrib['value']
    vstate = root.xpath('//input[@name="__VSTATE"]')[0].attrib['value']
    
    #pageParser(root)
    
    current_scrape = root.cssselect("a.rgCurrentPage") #get current page link at a.rgCurrentPage    
    
    next_scrape = current_scrape[1].getnext()

    if current_scrape: 
        
        current_scrape = current_scrape[0]
        
        print 'page: ',  current_scrape.text

        

    else:
        next_scrape = None

    if next_scrape is not None:
        '''next scrape should open up the next link as a response and head back to the top of the loop to scrape that via pageParser()
           trickiest part here because you have to send data from the next_scrape back as post information to the form, not as a link to click'''


        event_target = next_scrape.attrib['href'].split("'")[1]
        print "Hi, my name is: ", event_target


        '''send the event target with the form and submit to get next page'''
        br.select_form('aspnetForm')        
        br.set_all_readonly(False)
        br['__EVENTTARGET'] = event_target
        br['__EVENTARGUMENT'] = event_arg
        br['__VIEWSTATE'] = viewstate
        br['__VSTATE'] = vstate
               
        '''disable submit buttons'''
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch2').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear2').disabled = True
        
        
        '''Keeps scraping the same page: see - http://stackoverflow.com/questions/13114977/why-does-this-scraperwiki-for-an-aspx-site-return-only-the-same-page-of-search-r
        http://stackoverflow.com/questions/6116023/screenscaping-aspx-with-python-mechanize-javascript-form-submission'''
        res = br.submit()

        #got_all = True #only for testing
        print "And we're out"        
            
    else:
        got_all = True #if there are no other links to follow, we are done, exit the loop
        print "I got everything, I got nothing!"


'''Save rows to a scraperwiki (we will figure out a better way of storing later)'''import scraperwiki
import mechanize
import lxml.html


'''http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python'''


base_url = 'https://healthri.mylicense.com/'
url = 'https://healthri.mylicense.com/Verification/Search.aspx'
headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br = mechanize.Browser()
br2 = mechanize.Browser()
br.addheaders = headers
br2.addheaders = headers

br.open(url)


print url

'''function for parsing a record when we get a proper page of results'''
def pageParser(stuff): #when to use 'self'
    '''this is the test parser for each page of results, put this in a function'''
    for el in stuff.cssselect("table.rgMasterTable tbody tr td"):
        for guy in el.cssselect("a"):
            desc = guy.text
            linky = guy.attrib['href']
            #print linky
            '''go into each record and scrape a smoke signal'''
            br2.open(base_url+linky)
            html = br2.response().read()
            dom = lxml.html.fromstring(html)
            dumps = dom.cssselect('#ctl00_ContentPlaceHolder1_hypInControlOf2')
            for i in dumps:
                print i.text


'''Mechanize patch till fixed: https://bitbucket.org/ScraperWiki/scraperwiki/issue/963/mechanize-library-breaks-on-known'''
html = br.response().read()
dom = lxml.html.fromstring(html)

bad_form = dom.cssselect('#aspnetForm')[0]
bad_inputs = bad_form.cssselect('input')

#for el in bad_inputs:
print el

bad_inputs[0].set('value', '1')

'''disable the disabled button - so we can advance'''
bad_inputs[8].getparent().remove(bad_inputs[8])

good_form = lxml.html.tostring(bad_form)
print good_form

mech_form = mechanize._form.ParseString(good_form, br.geturl())

br.form = mech_form[1]

#req = br.submit()


req = br.click(type="submit", nr=0)
res = br.open(req)
#data = res.read()


'''go to the next page and repeat (probably going to need to modularize things),
   or just check out https://github.com/fgregg/legistar-scrape/blob/master/legistar/scraper.py : lines 84 - 112.
   loop the pages and get it all'''

got_all = False

while got_all is False:
    
    data = res.read()
    '''parse data for one page only'''

    root = lxml.html.fromstring(data)

    '''get form post request data'''
    viewstate = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    event_arg = root.xpath('//input[@name="__EVENTARGUMENT"]')[0].attrib['value']
    vstate = root.xpath('//input[@name="__VSTATE"]')[0].attrib['value']
    
    #pageParser(root)
    
    current_scrape = root.cssselect("a.rgCurrentPage") #get current page link at a.rgCurrentPage    
    
    next_scrape = current_scrape[1].getnext()

    if current_scrape: 
        
        current_scrape = current_scrape[0]
        
        print 'page: ',  current_scrape.text

        

    else:
        next_scrape = None

    if next_scrape is not None:
        '''next scrape should open up the next link as a response and head back to the top of the loop to scrape that via pageParser()
           trickiest part here because you have to send data from the next_scrape back as post information to the form, not as a link to click'''


        event_target = next_scrape.attrib['href'].split("'")[1]
        print "Hi, my name is: ", event_target


        '''send the event target with the form and submit to get next page'''
        br.select_form('aspnetForm')        
        br.set_all_readonly(False)
        br['__EVENTTARGET'] = event_target
        br['__EVENTARGUMENT'] = event_arg
        br['__VIEWSTATE'] = viewstate
        br['__VSTATE'] = vstate
               
        '''disable submit buttons'''
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch2').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear2').disabled = True
        
        
        '''Keeps scraping the same page: see - http://stackoverflow.com/questions/13114977/why-does-this-scraperwiki-for-an-aspx-site-return-only-the-same-page-of-search-r
        http://stackoverflow.com/questions/6116023/screenscaping-aspx-with-python-mechanize-javascript-form-submission'''
        res = br.submit()

        #got_all = True #only for testing
        print "And we're out"        
            
    else:
        got_all = True #if there are no other links to follow, we are done, exit the loop
        print "I got everything, I got nothing!"


'''Save rows to a scraperwiki (we will figure out a better way of storing later)'''import scraperwiki
import mechanize
import lxml.html


'''http://stackoverflow.com/questions/1480356/how-to-submit-query-to-aspx-page-in-python'''


base_url = 'https://healthri.mylicense.com/'
url = 'https://healthri.mylicense.com/Verification/Search.aspx'
headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br = mechanize.Browser()
br2 = mechanize.Browser()
br.addheaders = headers
br2.addheaders = headers

br.open(url)


print url

'''function for parsing a record when we get a proper page of results'''
def pageParser(stuff): #when to use 'self'
    '''this is the test parser for each page of results, put this in a function'''
    for el in stuff.cssselect("table.rgMasterTable tbody tr td"):
        for guy in el.cssselect("a"):
            desc = guy.text
            linky = guy.attrib['href']
            #print linky
            '''go into each record and scrape a smoke signal'''
            br2.open(base_url+linky)
            html = br2.response().read()
            dom = lxml.html.fromstring(html)
            dumps = dom.cssselect('#ctl00_ContentPlaceHolder1_hypInControlOf2')
            for i in dumps:
                print i.text


'''Mechanize patch till fixed: https://bitbucket.org/ScraperWiki/scraperwiki/issue/963/mechanize-library-breaks-on-known'''
html = br.response().read()
dom = lxml.html.fromstring(html)

bad_form = dom.cssselect('#aspnetForm')[0]
bad_inputs = bad_form.cssselect('input')

#for el in bad_inputs:
print el

bad_inputs[0].set('value', '1')

'''disable the disabled button - so we can advance'''
bad_inputs[8].getparent().remove(bad_inputs[8])

good_form = lxml.html.tostring(bad_form)
print good_form

mech_form = mechanize._form.ParseString(good_form, br.geturl())

br.form = mech_form[1]

#req = br.submit()


req = br.click(type="submit", nr=0)
res = br.open(req)
#data = res.read()


'''go to the next page and repeat (probably going to need to modularize things),
   or just check out https://github.com/fgregg/legistar-scrape/blob/master/legistar/scraper.py : lines 84 - 112.
   loop the pages and get it all'''

got_all = False

while got_all is False:
    
    data = res.read()
    '''parse data for one page only'''

    root = lxml.html.fromstring(data)

    '''get form post request data'''
    viewstate = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']
    event_arg = root.xpath('//input[@name="__EVENTARGUMENT"]')[0].attrib['value']
    vstate = root.xpath('//input[@name="__VSTATE"]')[0].attrib['value']
    
    #pageParser(root)
    
    current_scrape = root.cssselect("a.rgCurrentPage") #get current page link at a.rgCurrentPage    
    
    next_scrape = current_scrape[1].getnext()

    if current_scrape: 
        
        current_scrape = current_scrape[0]
        
        print 'page: ',  current_scrape.text

        

    else:
        next_scrape = None

    if next_scrape is not None:
        '''next scrape should open up the next link as a response and head back to the top of the loop to scrape that via pageParser()
           trickiest part here because you have to send data from the next_scrape back as post information to the form, not as a link to click'''


        event_target = next_scrape.attrib['href'].split("'")[1]
        print "Hi, my name is: ", event_target


        '''send the event target with the form and submit to get next page'''
        br.select_form('aspnetForm')        
        br.set_all_readonly(False)
        br['__EVENTTARGET'] = event_target
        br['__EVENTARGUMENT'] = event_arg
        br['__VIEWSTATE'] = viewstate
        br['__VSTATE'] = vstate
               
        '''disable submit buttons'''
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnSearch2').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear').disabled = True
        br.find_control('ctl00$ContentPlaceHolder1$btnClear2').disabled = True
        
        
        '''Keeps scraping the same page: see - http://stackoverflow.com/questions/13114977/why-does-this-scraperwiki-for-an-aspx-site-return-only-the-same-page-of-search-r
        http://stackoverflow.com/questions/6116023/screenscaping-aspx-with-python-mechanize-javascript-form-submission'''
        res = br.submit()

        #got_all = True #only for testing
        print "And we're out"        
            
    else:
        got_all = True #if there are no other links to follow, we are done, exit the loop
        print "I got everything, I got nothing!"


'''Save rows to a scraperwiki (we will figure out a better way of storing later)'''