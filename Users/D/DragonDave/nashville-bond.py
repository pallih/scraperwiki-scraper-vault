import scraperwiki,lxml.html,datetime

import urllib
# Blank Python

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(n)

def scrapeday(date):
    # get data
    url='http://ccc.nashville.gov/portal/pls/portal/PORTAL.RPT_DEF_BOND_MAIL_ADD_NAME.show'
    datetext=date.strftime('%m-%d-%Y')
    print "Scraping %s"%datetext
    data=''.join(["p_reference_path=&p_exec_mode=&p_action=RUN&p_page_url=&p_redirect_url=",
                 "&p_mode=1&p_arg_names=date_bond_posted&p_arg_values=ARRAYSTART&p_arg_values=%s&p_arg_values=ARRAYEND"% datetext])
    html=urllib.urlopen(url, data=data).read()
    
    # parse data
    root=lxml.html.fromstring(html)
    records=root.cssselect("table[summary='Printing Table Headers'] tr")[3:]
    print "%d records found"%len(records)
    for tr in records:
        # each record
        data={'date':date}
        tds=map(lxml.html.HtmlElement.text_content, tr.cssselect("td"))
        if len(tds)==1:
            continue # skip posted dates
        tds=map(unicode,tds)
        tds=map(unicode.strip, tds)
        (data['defendant'],skip,skip,data['oca'],skip,data['address'],data['case'],data['company'],data['tca'],data['description'])=tds
        try:
            if int(data['address'][-5:]):
                data['zip']=data['address'][-5:]
        except:
            pass
        scraperwiki.sqlite.save(data=data, unique_keys=[], table_name='bond')

scrapeday(datetime.date.today()-datetime.timedelta(days=1)) # scrape yesterday, today might not be ready.import scraperwiki,lxml.html,datetime

import urllib
# Blank Python

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(n)

def scrapeday(date):
    # get data
    url='http://ccc.nashville.gov/portal/pls/portal/PORTAL.RPT_DEF_BOND_MAIL_ADD_NAME.show'
    datetext=date.strftime('%m-%d-%Y')
    print "Scraping %s"%datetext
    data=''.join(["p_reference_path=&p_exec_mode=&p_action=RUN&p_page_url=&p_redirect_url=",
                 "&p_mode=1&p_arg_names=date_bond_posted&p_arg_values=ARRAYSTART&p_arg_values=%s&p_arg_values=ARRAYEND"% datetext])
    html=urllib.urlopen(url, data=data).read()
    
    # parse data
    root=lxml.html.fromstring(html)
    records=root.cssselect("table[summary='Printing Table Headers'] tr")[3:]
    print "%d records found"%len(records)
    for tr in records:
        # each record
        data={'date':date}
        tds=map(lxml.html.HtmlElement.text_content, tr.cssselect("td"))
        if len(tds)==1:
            continue # skip posted dates
        tds=map(unicode,tds)
        tds=map(unicode.strip, tds)
        (data['defendant'],skip,skip,data['oca'],skip,data['address'],data['case'],data['company'],data['tca'],data['description'])=tds
        try:
            if int(data['address'][-5:]):
                data['zip']=data['address'][-5:]
        except:
            pass
        scraperwiki.sqlite.save(data=data, unique_keys=[], table_name='bond')

scrapeday(datetime.date.today()-datetime.timedelta(days=1)) # scrape yesterday, today might not be ready.