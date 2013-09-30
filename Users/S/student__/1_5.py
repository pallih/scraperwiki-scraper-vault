import scraperwiki
import lxml.html
import lxml.etree
import mechanize
import time
import cStringIO
import re
url="http://www.ccof.org/cgi-bin/organicdirectory_search.cgi"  

def scrp():
    html_content = scraperwiki.scrape(url)
    i=0
    while re.search('Next 5 Results',html_content):
    #for i in range(480):
        print i
        ind=0
        root1 = lxml.html.fromstring(html_content)
        #if root1.cssselect("body table")[2]:
             #pass
        #else:
            #return
        tbl1 = root1.cssselect("body table")[2]
        step2 = tbl1.cssselect("tr table")
        step3 = step2[3].cssselect("tr")
        mydata=[]
        for tr in step3:
            tds = tr.cssselect("td")
            try:
                val = tds[1].text_content()
                key = tds[0].text_content()
                #print key, val
                if key.startswith('Business'):
                    if 'dba' in val:
                        spl=val.split(' ')
                        dba = spl[spl.index('dba')+1:]
                        mydata.append(((u'dba'),unicode(' '.join(dba))))
                        val=' '.join(spl[:spl.index('dba')])
                if key.startswith('Contact'):
                    spl = val.split()
                    for w in spl[:]:
                        if w.endswith('.') or len(w)==1:
                            mydata.append(
                                ((u'contact1title'),unicode(spl.pop(spl.index(w))))
                                )
                    if len(spl)==3:
                        mydata.append(
                            ((u'contact1last'),unicode('_'.join((spl[1],spl[2]))))
                            )
                        val=spl[0]
                        key='contact1first:'
                    if len(spl)%2==0:
                        for n in range(len(spl)):
                            if n%2!=0 and n!=0:
                                mydata.append(
                                    ((u'contact'+unicode((n/2)+1)+u'last'),unicode(spl[n]))
                                    )
                            elif n==0:
                                val=spl[0]
                                key='contact1first:'
                            else:
                                 mydata.append(
                                    ((u'contact'+unicode((n/2)+1)+u'first'),unicode(spl[n]))
                                    )
                if key.startswith('Email'):
                    #val = ','.join(val.split())
                    key = 'emails:'
                if key.startswith('Business'):
                    key = 'companyname:'
                if key.startswith('Product'):
                    key = 'categories:'
                if key.startswith('Sales'):
                    key = 'salesmethod:'
                if key.startswith('CCO'):
                    key = 'certifications'
                if key.startswith('County'):
                    key = 'country:'
                if key.startswith('Phone'):
                    key = 'phonenumber:'
                if key.startswith('Fax'):
                    key = 'faxnomber:'
                if key.startswith('Chapter') or key.startswith('Contact'):
                    pass
                else:
                    key = key.lower()
                    mydata.append((unicode(key[:-1]),unicode(val)))
                    mydata.append(('id', i*5+ind))                 
                #print ind
            except IndexError:
                #print dict(mydata)
                scraperwiki.sqlite.save(unique_keys=['id'], data=dict(mydata))
                mydata=[]
                ind+=1
            
        html_content=next_page(i)
        i+=1
def next_page(ind): 
    #time.sleep(4)
    br = mechanize.Browser()
    for attemt in range(5):
        try:
            response = br.open(url)
            break
        except:
            pass
    #br.select_form()
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    form = forms[0]
    form.set_all_readonly(False)
    form['startitem']=str(ind*5+5)
    form.set_all_readonly(True)
    response = form.click()
    #response1 = br.submit()
    #print response1
    #br.open(mechanize.urlopen(response).read()
    return mechanize.urlopen(response).read()
scrp()import scraperwiki
import lxml.html
import lxml.etree
import mechanize
import time
import cStringIO
import re
url="http://www.ccof.org/cgi-bin/organicdirectory_search.cgi"  

def scrp():
    html_content = scraperwiki.scrape(url)
    i=0
    while re.search('Next 5 Results',html_content):
    #for i in range(480):
        print i
        ind=0
        root1 = lxml.html.fromstring(html_content)
        #if root1.cssselect("body table")[2]:
             #pass
        #else:
            #return
        tbl1 = root1.cssselect("body table")[2]
        step2 = tbl1.cssselect("tr table")
        step3 = step2[3].cssselect("tr")
        mydata=[]
        for tr in step3:
            tds = tr.cssselect("td")
            try:
                val = tds[1].text_content()
                key = tds[0].text_content()
                #print key, val
                if key.startswith('Business'):
                    if 'dba' in val:
                        spl=val.split(' ')
                        dba = spl[spl.index('dba')+1:]
                        mydata.append(((u'dba'),unicode(' '.join(dba))))
                        val=' '.join(spl[:spl.index('dba')])
                if key.startswith('Contact'):
                    spl = val.split()
                    for w in spl[:]:
                        if w.endswith('.') or len(w)==1:
                            mydata.append(
                                ((u'contact1title'),unicode(spl.pop(spl.index(w))))
                                )
                    if len(spl)==3:
                        mydata.append(
                            ((u'contact1last'),unicode('_'.join((spl[1],spl[2]))))
                            )
                        val=spl[0]
                        key='contact1first:'
                    if len(spl)%2==0:
                        for n in range(len(spl)):
                            if n%2!=0 and n!=0:
                                mydata.append(
                                    ((u'contact'+unicode((n/2)+1)+u'last'),unicode(spl[n]))
                                    )
                            elif n==0:
                                val=spl[0]
                                key='contact1first:'
                            else:
                                 mydata.append(
                                    ((u'contact'+unicode((n/2)+1)+u'first'),unicode(spl[n]))
                                    )
                if key.startswith('Email'):
                    #val = ','.join(val.split())
                    key = 'emails:'
                if key.startswith('Business'):
                    key = 'companyname:'
                if key.startswith('Product'):
                    key = 'categories:'
                if key.startswith('Sales'):
                    key = 'salesmethod:'
                if key.startswith('CCO'):
                    key = 'certifications'
                if key.startswith('County'):
                    key = 'country:'
                if key.startswith('Phone'):
                    key = 'phonenumber:'
                if key.startswith('Fax'):
                    key = 'faxnomber:'
                if key.startswith('Chapter') or key.startswith('Contact'):
                    pass
                else:
                    key = key.lower()
                    mydata.append((unicode(key[:-1]),unicode(val)))
                    mydata.append(('id', i*5+ind))                 
                #print ind
            except IndexError:
                #print dict(mydata)
                scraperwiki.sqlite.save(unique_keys=['id'], data=dict(mydata))
                mydata=[]
                ind+=1
            
        html_content=next_page(i)
        i+=1
def next_page(ind): 
    #time.sleep(4)
    br = mechanize.Browser()
    for attemt in range(5):
        try:
            response = br.open(url)
            break
        except:
            pass
    #br.select_form()
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    form = forms[0]
    form.set_all_readonly(False)
    form['startitem']=str(ind*5+5)
    form.set_all_readonly(True)
    response = form.click()
    #response1 = br.submit()
    #print response1
    #br.open(mechanize.urlopen(response).read()
    return mechanize.urlopen(response).read()
scrp()