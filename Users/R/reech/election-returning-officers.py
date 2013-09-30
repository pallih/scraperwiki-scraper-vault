import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import re
from scraperwiki import datastore

def main():
    br = mechanize.Browser()
    print 'h'
    la_form = 'http://www.aboutmyvote.co.uk/make_it_local/search_for_a_local_authority.aspx?returnURL=0'
    br.open(la_form)
    br.form = list(br.forms())[0]
    br['Template$ctl25$selectLocation$laTermTextBox'] = '%' # wildcard search for all LA's
    html = br.submit(name='Template$ctl25$selectLocation$searchButton') # submit the location button!

    for id in get_ids(html): # fetch each LA ERO
        br.form = list(br.forms())[0]
        br['Template$ctl25$selectLocation$laRadioButtonList'] = [str(id),]
        html = br.submit(name='Template$ctl25$selectLocation$selectButton')
        parse_page(html, id)
        br.back()


def parse_page(html, id): # parse LA specific page
    la_page = BeautifulSoup(html.read())
    eo_det = la_page.find('div',{'class':'yourOffice'})
    eo={}
    eo['id'] = id
    address = [a.strip() for a in str(eo_det.find('p')).strip().split('<br />')]
    address = address[1:-2]
    eo['address1'] = address[0]
    eo['address2'] = address[1]
    eo['address3'] = address[2]
    eo['address4'] = address[3]
    eo['postcode'] = address[4]
    try:
        eo['phone'] = address[5]
    except:
        pass
    # latlng = scraperwiki.geo.gb_postcode_to_latlng(eo['postcode']) # seems broke for now :[
    # print latlng
    h = eo_det.findAll('a')
    eo['local_authority'] = h[0].text
    eo['url'] = h[0]['href']
    if len(h) > 1:
        eo['email'] = re.match('^mailto:(.*)',h[1]['href']).groups()[0]
    # save
    datastore.save(unique_keys=['id'], data=eo)
    print eo

def get_ids(html):
    list_page = BeautifulSoup(html.read())
    list_data = list_page.find('div',{'id':'Template_ctl25_selectLocation_searchResultsPanel',}).findAll('input', {'type':'radio'})
    return  [l['value'] for l in list_data]

main()
import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import re
from scraperwiki import datastore

def main():
    br = mechanize.Browser()
    print 'h'
    la_form = 'http://www.aboutmyvote.co.uk/make_it_local/search_for_a_local_authority.aspx?returnURL=0'
    br.open(la_form)
    br.form = list(br.forms())[0]
    br['Template$ctl25$selectLocation$laTermTextBox'] = '%' # wildcard search for all LA's
    html = br.submit(name='Template$ctl25$selectLocation$searchButton') # submit the location button!

    for id in get_ids(html): # fetch each LA ERO
        br.form = list(br.forms())[0]
        br['Template$ctl25$selectLocation$laRadioButtonList'] = [str(id),]
        html = br.submit(name='Template$ctl25$selectLocation$selectButton')
        parse_page(html, id)
        br.back()


def parse_page(html, id): # parse LA specific page
    la_page = BeautifulSoup(html.read())
    eo_det = la_page.find('div',{'class':'yourOffice'})
    eo={}
    eo['id'] = id
    address = [a.strip() for a in str(eo_det.find('p')).strip().split('<br />')]
    address = address[1:-2]
    eo['address1'] = address[0]
    eo['address2'] = address[1]
    eo['address3'] = address[2]
    eo['address4'] = address[3]
    eo['postcode'] = address[4]
    try:
        eo['phone'] = address[5]
    except:
        pass
    # latlng = scraperwiki.geo.gb_postcode_to_latlng(eo['postcode']) # seems broke for now :[
    # print latlng
    h = eo_det.findAll('a')
    eo['local_authority'] = h[0].text
    eo['url'] = h[0]['href']
    if len(h) > 1:
        eo['email'] = re.match('^mailto:(.*)',h[1]['href']).groups()[0]
    # save
    datastore.save(unique_keys=['id'], data=eo)
    print eo

def get_ids(html):
    list_page = BeautifulSoup(html.read())
    list_data = list_page.find('div',{'id':'Template_ctl25_selectLocation_searchResultsPanel',}).findAll('input', {'type':'radio'})
    return  [l['value'] for l in list_data]

main()
