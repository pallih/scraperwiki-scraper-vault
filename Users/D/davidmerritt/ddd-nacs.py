import scraperwiki
import datetime
import time
import re

BASE_URL_TEMPLATE=u"http://www.nacsonline.com/NACSShow/Expo/Pages/ExhibitorDirectory.aspx?vw=detail&eid=%d"

START_ID=22001
#STOP_ID=22020
STOP_ID=26488


from bs4 import BeautifulSoup
import re

REMAP={'categories':'Categories','website':'Website','dba':'Brands','maincategory':'Categories','address':'Address','boothnum':'Booth','phonenumber':'Phone','faxnumber':'Fax','description':'Description','companyname':'Name'};
FIELDS=['datescraped','companyname','dba','website','categories','maincategory','address','sourceurl','phonenumber','faxnumber' ,'description']


def scrape_one_page(id):
    return scraperwiki.scrape(BASE_URL_TEMPLATE % id)

def remap(data_dict):
    
    newdict={}
    
    for key in REMAP.keys():
        newdict [key] = data_dict[REMAP[key]].encode('utf-8')
    
    return newdict

def span_parse(parsed_element,element_name):
    return u",".join([span.text for span in parsed_element.find_all('span') if span.text != element_name])

def parse_company_page(raw_page):
    parsed_page=BeautifulSoup(raw_page)

    subheaders=dict([(subheader.text,subheader.parent) for subheader in parsed_page.find_all(attrs={'class':'subheader'})])

    subheaders.pop('Booth Location')

    categories=[link.text for link in subheaders.pop('Categories').find_all('a')]

    booth_span_select=parsed_page.find_all(lambda tag: tag.attrs['id'].find('Booth') >0 if 'id' in tag.attrs.keys() else False )

    booth_number=re.findall('Booth[^0-9]*([0-9]*)',booth_span_select[0].text)[0]

    rest_dict=dict([(key,span_parse(subheaders.pop(key),key)) for key in subheaders.keys()])
    
    cname_span_select=parsed_page.find_all(lambda tag: tag.attrs['id'].find('CompanyName') >0 if 'id' in tag.attrs.keys() else False )
    rest_dict['Name']=cname_span_select[0].text
    
    if 'Overview' in rest_dict.keys():
        rest_dict['Description']=rest_dict['Overview']
    else:
        rest_dict['Description']=''
    
    if not ('Brands' in rest_dict.keys()):
        rest_dict['Brands']=''

    if not ('Website' in rest_dict.keys()):
        rest_dict['Website']=''

    rest_dict['Categories']=u",".join(categories)
    rest_dict['Booth']=booth_number
    rest_dict['Phone'], rest_dict['Fax']=re.findall('([ 0-9()-]*)[^0-9()-]*p[^0-9()-]*([ 0-9()-]*)[^0-9()-]f', rest_dict['Contact'])[0]

    return rest_dict

def main():
    scraperwiki.sqlite.save_var("source", "www.nacsonline.com")
    scraperwiki.sqlite.save_var("author", "Lyubimov Denis")

    for id in range(START_ID,STOP_ID+1):
        time.sleep(1)

        try:
            raw=scrape_one_page(id)
            data_dict=remap(parse_company_page(raw))
            data_dict['sourceurl']=BASE_URL_TEMPLATE % id
            data_dict['datescraped']=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
            data_dict['address']=re.sub("[^ 0-9A-Za-z_()'-]"," ",data_dict['address'])
            
            scraperwiki.sqlite.save(FIELDS,data_dict)
        except Exception,e:
            print "Fail to scrape or parse id = %d " % id
            print e


main()import scraperwiki
import datetime
import time
import re

BASE_URL_TEMPLATE=u"http://www.nacsonline.com/NACSShow/Expo/Pages/ExhibitorDirectory.aspx?vw=detail&eid=%d"

START_ID=22001
#STOP_ID=22020
STOP_ID=26488


from bs4 import BeautifulSoup
import re

REMAP={'categories':'Categories','website':'Website','dba':'Brands','maincategory':'Categories','address':'Address','boothnum':'Booth','phonenumber':'Phone','faxnumber':'Fax','description':'Description','companyname':'Name'};
FIELDS=['datescraped','companyname','dba','website','categories','maincategory','address','sourceurl','phonenumber','faxnumber' ,'description']


def scrape_one_page(id):
    return scraperwiki.scrape(BASE_URL_TEMPLATE % id)

def remap(data_dict):
    
    newdict={}
    
    for key in REMAP.keys():
        newdict [key] = data_dict[REMAP[key]].encode('utf-8')
    
    return newdict

def span_parse(parsed_element,element_name):
    return u",".join([span.text for span in parsed_element.find_all('span') if span.text != element_name])

def parse_company_page(raw_page):
    parsed_page=BeautifulSoup(raw_page)

    subheaders=dict([(subheader.text,subheader.parent) for subheader in parsed_page.find_all(attrs={'class':'subheader'})])

    subheaders.pop('Booth Location')

    categories=[link.text for link in subheaders.pop('Categories').find_all('a')]

    booth_span_select=parsed_page.find_all(lambda tag: tag.attrs['id'].find('Booth') >0 if 'id' in tag.attrs.keys() else False )

    booth_number=re.findall('Booth[^0-9]*([0-9]*)',booth_span_select[0].text)[0]

    rest_dict=dict([(key,span_parse(subheaders.pop(key),key)) for key in subheaders.keys()])
    
    cname_span_select=parsed_page.find_all(lambda tag: tag.attrs['id'].find('CompanyName') >0 if 'id' in tag.attrs.keys() else False )
    rest_dict['Name']=cname_span_select[0].text
    
    if 'Overview' in rest_dict.keys():
        rest_dict['Description']=rest_dict['Overview']
    else:
        rest_dict['Description']=''
    
    if not ('Brands' in rest_dict.keys()):
        rest_dict['Brands']=''

    if not ('Website' in rest_dict.keys()):
        rest_dict['Website']=''

    rest_dict['Categories']=u",".join(categories)
    rest_dict['Booth']=booth_number
    rest_dict['Phone'], rest_dict['Fax']=re.findall('([ 0-9()-]*)[^0-9()-]*p[^0-9()-]*([ 0-9()-]*)[^0-9()-]f', rest_dict['Contact'])[0]

    return rest_dict

def main():
    scraperwiki.sqlite.save_var("source", "www.nacsonline.com")
    scraperwiki.sqlite.save_var("author", "Lyubimov Denis")

    for id in range(START_ID,STOP_ID+1):
        time.sleep(1)

        try:
            raw=scrape_one_page(id)
            data_dict=remap(parse_company_page(raw))
            data_dict['sourceurl']=BASE_URL_TEMPLATE % id
            data_dict['datescraped']=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
            data_dict['address']=re.sub("[^ 0-9A-Za-z_()'-]"," ",data_dict['address'])
            
            scraperwiki.sqlite.save(FIELDS,data_dict)
        except Exception,e:
            print "Fail to scrape or parse id = %d " % id
            print e


main()