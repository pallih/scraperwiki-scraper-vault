import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
from xml.dom import minidom
import sys
import urllib
from scraperwiki import datastore

base_url = 'http://risk.english-heritage.org.uk/'
search_base = base_url + '2010.aspx?rs=1&rt=0&st=a&ctype=all&crit=&pn='


def main():
    for i in range(1,522):  # somewhat rough'n ready :[
        try:
            result_page = BeautifulSoup(scraperwiki.scrape(search_base+str(i)))
        except:
            print "End of pages"
            return
        
        print search_base+str(i)
        parse_results(result_page)
    
    
def locate(location_string):
    
    url = "http://maps.google.com/maps?%s" % urllib.urlencode({ 'output':'kml','q':location_string })
    # print 'locating : ' + url
    try:
        kml = minidom.parse(urllib.urlopen(url))
        lat = kml.getElementsByTagName('latitude')[0].childNodes[0].data
        lng = kml.getElementsByTagName('longitude')[0].childNodes[0].data
        return (float(lat),float(lng))
    except:
        print 'error: geolocation' # , sys.exc_info()
        return None

def locate_by_monument_number(n):
    url = 'http://www.pastscape.org.uk/maps.aspx?a=0&hob_id=%s' % n
    #try:
    print url
    result_page = scraperwiki.scrape(url)
    print result_page
    #except:
    #    print 'error: monument_location'
    #    return None
        
# grab detail url
def parse_results(page):
                                                      
    results = page.find('div', {'class':'searchResults'}).findAll('a')
    
    for r in results:
        print((base_url + '/' + str(r['href'])))
        parse_detail(base_url + '/' + str(r['href']))

# parse details, save        
def parse_detail(detail_url):
    
    latlng=None
    
    conditions = {
        'Extensive significant problems i.e. under plough, collapse':'Significant problems',
        'Generally unsatisfactory with major localised problems':'Unsatisfactory',
        'Generally unsatisfactory with major localised problems':'Unsatisfactory',
        'Extensive significant problems':'Significant problems',
        'Significant extensive problems':'Significant problems',
        'Generally satisfactory but with localised significant problems':'Satisfactory',
        'Generally satisfactory but with minor localised problems':'Satisfactory',
        'Generally satisfactory but with significant localised problems':'Satisfactory',
        'Generally unsatisfactory with major localised problems':'Unsatisfactory ',
        'Optimal ie the best we can realistically expect to achieve':'Optimal',
    }
    
    try:
        detail = BeautifulSoup(scraperwiki.scrape(detail_url)).find('div',{'class':'HARDetail'})
        r=detail.findAll('td', {'class':'label'})
        
        labels = [str(d.contents[0]).lower().strip().replace(':','').replace(' ','_').replace('<strong>','').replace('</strong>','') for d in detail.findAll('td', {'class':'label'})]                         
              
        values = [str(d.contents[0]).strip().replace('<strong>','').replace('</strong>','') for d in detail.findAll('td', {'class':'text'})]
        
        site = dict(zip(labels, values))
        print site                                              
        
        try:
            site['image'] = detail.find('a', {'id':'ctl00_ContentPlaceHolder1_aThumb'})
            site['image_thumb'] = base_url + '/' + str(site['image']['href'].replace('.jpg','_160.jpg'))
            site['image_url'] = base_url + '/' + str(site['image']['href'])
        except:
            pass

        site['description'] = detail.findAll('table')[1].find('table').find('td').contents[0].strip()
        site['id'] = int(re.match('.*?id=([0-9]*?)&.*',detail_url).groups()[0])
        site['url'] = unicode(detail_url)
        # site['contact'] = site['contact'].split(' 0')
        site['contact'] = re.match('^(.*?) ([0-9 ]*$)',site['contact']).groups()
        site['condition_simple'] = site['condition']      

        for k,v in conditions.iteritems():
            if str(site['condition']) == str(k):
                site['condition_simple'] = unicode(v)
                
        site['contact_name'] = site['contact'][0]
        site['contact_phone'] = site['contact'][1]
        
        # remove N/A's
        for k,v in site.items():
            if type(v) == unicode:
                site[k] = v.replace('N/A','')
        
        try:
        # retrieve actual location
            if site.has_key('monument_number'):
                latlng = locate_by_monument_number(site['monument_number'])
                print 'geolocated'
        except:
            print 'ex'
            pass                                         
        
        
        del(site['contact']) 
        del(site['image'])
        datastore.save(unique_keys=['id',], data=site, latlng=latlng)
        
        
    except:
        print 'failed at ' + str(detail_url)
        print 'error: ', sys.exc_info()

main()
import scraperwiki
from BeautifulSoup import BeautifulSoup
import re
from xml.dom import minidom
import sys
import urllib
from scraperwiki import datastore

base_url = 'http://risk.english-heritage.org.uk/'
search_base = base_url + '2010.aspx?rs=1&rt=0&st=a&ctype=all&crit=&pn='


def main():
    for i in range(1,522):  # somewhat rough'n ready :[
        try:
            result_page = BeautifulSoup(scraperwiki.scrape(search_base+str(i)))
        except:
            print "End of pages"
            return
        
        print search_base+str(i)
        parse_results(result_page)
    
    
def locate(location_string):
    
    url = "http://maps.google.com/maps?%s" % urllib.urlencode({ 'output':'kml','q':location_string })
    # print 'locating : ' + url
    try:
        kml = minidom.parse(urllib.urlopen(url))
        lat = kml.getElementsByTagName('latitude')[0].childNodes[0].data
        lng = kml.getElementsByTagName('longitude')[0].childNodes[0].data
        return (float(lat),float(lng))
    except:
        print 'error: geolocation' # , sys.exc_info()
        return None

def locate_by_monument_number(n):
    url = 'http://www.pastscape.org.uk/maps.aspx?a=0&hob_id=%s' % n
    #try:
    print url
    result_page = scraperwiki.scrape(url)
    print result_page
    #except:
    #    print 'error: monument_location'
    #    return None
        
# grab detail url
def parse_results(page):
                                                      
    results = page.find('div', {'class':'searchResults'}).findAll('a')
    
    for r in results:
        print((base_url + '/' + str(r['href'])))
        parse_detail(base_url + '/' + str(r['href']))

# parse details, save        
def parse_detail(detail_url):
    
    latlng=None
    
    conditions = {
        'Extensive significant problems i.e. under plough, collapse':'Significant problems',
        'Generally unsatisfactory with major localised problems':'Unsatisfactory',
        'Generally unsatisfactory with major localised problems':'Unsatisfactory',
        'Extensive significant problems':'Significant problems',
        'Significant extensive problems':'Significant problems',
        'Generally satisfactory but with localised significant problems':'Satisfactory',
        'Generally satisfactory but with minor localised problems':'Satisfactory',
        'Generally satisfactory but with significant localised problems':'Satisfactory',
        'Generally unsatisfactory with major localised problems':'Unsatisfactory ',
        'Optimal ie the best we can realistically expect to achieve':'Optimal',
    }
    
    try:
        detail = BeautifulSoup(scraperwiki.scrape(detail_url)).find('div',{'class':'HARDetail'})
        r=detail.findAll('td', {'class':'label'})
        
        labels = [str(d.contents[0]).lower().strip().replace(':','').replace(' ','_').replace('<strong>','').replace('</strong>','') for d in detail.findAll('td', {'class':'label'})]                         
              
        values = [str(d.contents[0]).strip().replace('<strong>','').replace('</strong>','') for d in detail.findAll('td', {'class':'text'})]
        
        site = dict(zip(labels, values))
        print site                                              
        
        try:
            site['image'] = detail.find('a', {'id':'ctl00_ContentPlaceHolder1_aThumb'})
            site['image_thumb'] = base_url + '/' + str(site['image']['href'].replace('.jpg','_160.jpg'))
            site['image_url'] = base_url + '/' + str(site['image']['href'])
        except:
            pass

        site['description'] = detail.findAll('table')[1].find('table').find('td').contents[0].strip()
        site['id'] = int(re.match('.*?id=([0-9]*?)&.*',detail_url).groups()[0])
        site['url'] = unicode(detail_url)
        # site['contact'] = site['contact'].split(' 0')
        site['contact'] = re.match('^(.*?) ([0-9 ]*$)',site['contact']).groups()
        site['condition_simple'] = site['condition']      

        for k,v in conditions.iteritems():
            if str(site['condition']) == str(k):
                site['condition_simple'] = unicode(v)
                
        site['contact_name'] = site['contact'][0]
        site['contact_phone'] = site['contact'][1]
        
        # remove N/A's
        for k,v in site.items():
            if type(v) == unicode:
                site[k] = v.replace('N/A','')
        
        try:
        # retrieve actual location
            if site.has_key('monument_number'):
                latlng = locate_by_monument_number(site['monument_number'])
                print 'geolocated'
        except:
            print 'ex'
            pass                                         
        
        
        del(site['contact']) 
        del(site['image'])
        datastore.save(unique_keys=['id',], data=site, latlng=latlng)
        
        
    except:
        print 'failed at ' + str(detail_url)
        print 'error: ', sys.exc_info()

main()
