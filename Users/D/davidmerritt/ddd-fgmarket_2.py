import scraperwiki
import datetime
import time
import re
from bs4.element import Tag


MAIN_URL=u"http://www.fgmarket.com/"

CATEGORY_URL_TEMPLATE="http://www.fgmarket.com/%s%s"
PROFILE_URL_TEMPLATE='http://www.fgmarket.com%s'
FIELDS=['datescraped','emails','companyname','dba','website','categories','maincategory','city','state','zip','country','address','sourceurl','phonenumber','faxnumber' ,'description','contactlink']

from bs4 import BeautifulSoup
import re

def scrape_main():
    return scraperwiki.scrape(MAIN_URL)



def scrape_one_page(id):
    return scraperwiki.scrape(BASE_URL_TEMPLATE % id)


def get_categories_url(main_page):
    return [c.attrs['href'] for c in BeautifulSoup(main_page).find_all(attrs={'class','home-category-main'})]

def parse_profile_page(profile_page,profile_page_link_suffix):
    
    pp=BeautifulSoup(profile_page)

    temp=dict((k,pp.find_all(attrs={'itemprop':k})[0].attrs['content']) for k in ['name','streetAddress','postalCode','addressLocality','telephone','email'])

    
    result={}
    
    for key in FIELDS:
        result[key]=''

    #dict(zip(FIELDS,['',]*len(FIELDS)))

    try:    
        result['maincategory'] = ', '.join([ ll.contents[0].contents[0] if type(ll.contents[0])==Tag else ll.contents[0] for ll in   pp.find(attrs={'class':'profile-categories'}).find_all(lambda tag: tag.name==u'li' and tag.parent.parent.name==u'div')])

        result['city'],result['state']=temp['addressLocality'].split(',')

        result['sourceurl']  = PROFILE_URL_TEMPLATE % (profile_page_link_suffix,)
        result['contactlink'] = PROFILE_URL_TEMPLATE % (profile_page_link_suffix+"#contact_form",)

        result['address']=temp['streetAddress']
    
    
        result['emails']=temp['email']

        result['phonenumber']=temp['telephone']
    
        result['description']=pp.find(attrs={'class':'tagLine'}).text
        
        result['zip']=temp['postalCode']

        result['country']='USA'
    
        result['companyname']=temp['name']
    except:
        print 'Failed to parse',profile_page
    try:
        result['website']=pp.find(attrs={'class':'website-link'}).find('a').text
    except:
        print 'Failed to parse',profile_page
    
    try: 
        faxselect=pp.find(attrs={'class':'Fax'})
        result['faxnumber']=faxselect.contents[0] if faxselect else ''
    except:
        print 'Failed to parse',profile_page

    return result

def save_scrapped_profile(scrapped_dict):

    scrapped_dict['datescraped']= datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    
    
    scraperwiki.sqlite.save(FIELDS, data=scrapped_dict)

def parse_category_page_number(category,n):

    sn= '' if n==0 else '?page=%s' % (n,)

    curl=CATEGORY_URL_TEMPLATE % (category,sn)


    
    
    profile_links=[(a.attrs['href'] ) for  a in BeautifulSoup(scraperwiki.scrape(curl)).find_all(attrs={'class','vendorInfo'}) if a.attrs['href'].find('#contact_form')==-1 ]

    return profile_links

def get_tinlistings(category,n):

    sn= '' if n==0 else '?page=%s' % (n,)

    curl=CATEGORY_URL_TEMPLATE % (category,sn)

    #print curl

    scraped=scraperwiki.scrape(curl)

    #print scraped

    return BeautifulSoup(scraped).find_all(attrs={'class':'tinlisting'})   

def parse_tin_listing(tinlisting):
    

    try:

        result={}

        for key in FIELDS:
            result[key]=''
        #result=dict(zip(FIELDS,['',]*len(FIELDS)))

        left=tinlisting.find(attrs={'class':'listing-left'})

        result['companyname']=left.find('span').text

        
        left.find('span').decompose()
        
        children=[c for c in left.children]

        result['city'],remainder=children[4].split(',')
    
        result['state'],result['zip']=remainder.lstrip().split(' ',1)

        print remainder,children[4],'s',result['state'],'z',result['zip']

        result['address']=children[2]

        result['country']='USA'

        result['description']=''

        result['contactlink']=''

        

        phones=dict(
[(tr.find('td',attrs={'class','phonenumbertype'}).text,tr.find('td',attrs={'class','phonenumber'}).text) for tr in tinlisting.find_all('tr')])

        result['faxnumber']= phones['Fax:'] if  'Fax:' in phones.keys() else ''
    
        result['phonenumber']= phones['Local:'] if 'Local:' in phones.keys() else ''

        return result
    except Exception,e:
        print 'Failed to parse', tinlisting ,e 
        
        return {}
        



scraperwiki.sqlite.save_var("source", "fgmarket.com")
scraperwiki.sqlite.save_var("author", "Lyubimov Denis")


# As one run can't finish in time this variable saves where it should start next time. If you want to scrape all from beginning set it to 0.
cnn=scraperwiki.sqlite.get_var("parsedcategoryn")

categs=get_categories_url(scrape_main())[cnn:]



for can,categ in enumerate(categs):
    
    scraperwiki.sqlite.save_var("parsedcategoryn", can+cnn)    
    n=0
    parsed_cat_page=parse_category_page_number(categ,n)
    while parsed_cat_page:

        n+=1
        
        for suffix in parsed_cat_page:
            save_scrapped_profile(parse_profile_page(scraperwiki.scrape("http://fgmarket.com"+suffix),suffix))        
        
        parsed_cat_page=parse_category_page_number(categ,n)        
    
    tinlist=get_tinlistings(categ,n)

    print tinlist

    while tinlist:
        

        categ_url=CATEGORY_URL_TEMPLATE % (categ,'' if n==0 else '?page=%s' % (n,))
        n+=1
        for tinl in tinlist:
             res= parse_tin_listing(tinl)

             if res:  
                 res['sourceurl']=categ_url
                 save_scrapped_profile(res)
    
        tinlist=get_tinlistings(categ,n)
      import scraperwiki
import datetime
import time
import re
from bs4.element import Tag


MAIN_URL=u"http://www.fgmarket.com/"

CATEGORY_URL_TEMPLATE="http://www.fgmarket.com/%s%s"
PROFILE_URL_TEMPLATE='http://www.fgmarket.com%s'
FIELDS=['datescraped','emails','companyname','dba','website','categories','maincategory','city','state','zip','country','address','sourceurl','phonenumber','faxnumber' ,'description','contactlink']

from bs4 import BeautifulSoup
import re

def scrape_main():
    return scraperwiki.scrape(MAIN_URL)



def scrape_one_page(id):
    return scraperwiki.scrape(BASE_URL_TEMPLATE % id)


def get_categories_url(main_page):
    return [c.attrs['href'] for c in BeautifulSoup(main_page).find_all(attrs={'class','home-category-main'})]

def parse_profile_page(profile_page,profile_page_link_suffix):
    
    pp=BeautifulSoup(profile_page)

    temp=dict((k,pp.find_all(attrs={'itemprop':k})[0].attrs['content']) for k in ['name','streetAddress','postalCode','addressLocality','telephone','email'])

    
    result={}
    
    for key in FIELDS:
        result[key]=''

    #dict(zip(FIELDS,['',]*len(FIELDS)))

    try:    
        result['maincategory'] = ', '.join([ ll.contents[0].contents[0] if type(ll.contents[0])==Tag else ll.contents[0] for ll in   pp.find(attrs={'class':'profile-categories'}).find_all(lambda tag: tag.name==u'li' and tag.parent.parent.name==u'div')])

        result['city'],result['state']=temp['addressLocality'].split(',')

        result['sourceurl']  = PROFILE_URL_TEMPLATE % (profile_page_link_suffix,)
        result['contactlink'] = PROFILE_URL_TEMPLATE % (profile_page_link_suffix+"#contact_form",)

        result['address']=temp['streetAddress']
    
    
        result['emails']=temp['email']

        result['phonenumber']=temp['telephone']
    
        result['description']=pp.find(attrs={'class':'tagLine'}).text
        
        result['zip']=temp['postalCode']

        result['country']='USA'
    
        result['companyname']=temp['name']
    except:
        print 'Failed to parse',profile_page
    try:
        result['website']=pp.find(attrs={'class':'website-link'}).find('a').text
    except:
        print 'Failed to parse',profile_page
    
    try: 
        faxselect=pp.find(attrs={'class':'Fax'})
        result['faxnumber']=faxselect.contents[0] if faxselect else ''
    except:
        print 'Failed to parse',profile_page

    return result

def save_scrapped_profile(scrapped_dict):

    scrapped_dict['datescraped']= datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    
    
    scraperwiki.sqlite.save(FIELDS, data=scrapped_dict)

def parse_category_page_number(category,n):

    sn= '' if n==0 else '?page=%s' % (n,)

    curl=CATEGORY_URL_TEMPLATE % (category,sn)


    
    
    profile_links=[(a.attrs['href'] ) for  a in BeautifulSoup(scraperwiki.scrape(curl)).find_all(attrs={'class','vendorInfo'}) if a.attrs['href'].find('#contact_form')==-1 ]

    return profile_links

def get_tinlistings(category,n):

    sn= '' if n==0 else '?page=%s' % (n,)

    curl=CATEGORY_URL_TEMPLATE % (category,sn)

    #print curl

    scraped=scraperwiki.scrape(curl)

    #print scraped

    return BeautifulSoup(scraped).find_all(attrs={'class':'tinlisting'})   

def parse_tin_listing(tinlisting):
    

    try:

        result={}

        for key in FIELDS:
            result[key]=''
        #result=dict(zip(FIELDS,['',]*len(FIELDS)))

        left=tinlisting.find(attrs={'class':'listing-left'})

        result['companyname']=left.find('span').text

        
        left.find('span').decompose()
        
        children=[c for c in left.children]

        result['city'],remainder=children[4].split(',')
    
        result['state'],result['zip']=remainder.lstrip().split(' ',1)

        print remainder,children[4],'s',result['state'],'z',result['zip']

        result['address']=children[2]

        result['country']='USA'

        result['description']=''

        result['contactlink']=''

        

        phones=dict(
[(tr.find('td',attrs={'class','phonenumbertype'}).text,tr.find('td',attrs={'class','phonenumber'}).text) for tr in tinlisting.find_all('tr')])

        result['faxnumber']= phones['Fax:'] if  'Fax:' in phones.keys() else ''
    
        result['phonenumber']= phones['Local:'] if 'Local:' in phones.keys() else ''

        return result
    except Exception,e:
        print 'Failed to parse', tinlisting ,e 
        
        return {}
        



scraperwiki.sqlite.save_var("source", "fgmarket.com")
scraperwiki.sqlite.save_var("author", "Lyubimov Denis")


# As one run can't finish in time this variable saves where it should start next time. If you want to scrape all from beginning set it to 0.
cnn=scraperwiki.sqlite.get_var("parsedcategoryn")

categs=get_categories_url(scrape_main())[cnn:]



for can,categ in enumerate(categs):
    
    scraperwiki.sqlite.save_var("parsedcategoryn", can+cnn)    
    n=0
    parsed_cat_page=parse_category_page_number(categ,n)
    while parsed_cat_page:

        n+=1
        
        for suffix in parsed_cat_page:
            save_scrapped_profile(parse_profile_page(scraperwiki.scrape("http://fgmarket.com"+suffix),suffix))        
        
        parsed_cat_page=parse_category_page_number(categ,n)        
    
    tinlist=get_tinlistings(categ,n)

    print tinlist

    while tinlist:
        

        categ_url=CATEGORY_URL_TEMPLATE % (categ,'' if n==0 else '?page=%s' % (n,))
        n+=1
        for tinl in tinlist:
             res= parse_tin_listing(tinl)

             if res:  
                 res['sourceurl']=categ_url
                 save_scrapped_profile(res)
    
        tinlist=get_tinlistings(categ,n)
      