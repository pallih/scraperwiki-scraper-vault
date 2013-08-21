###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import simplejson, urllib, re
from BeautifulSoup import BeautifulSoup
from geopy import geocoders  


def get_category(category_name, cmstart=''):
    url = 'http://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:%s&cmstart=%s&cmsort=timestamp&cmdir=desc&cmlimit=100&format=json' % (urllib.quote(category_name), cmstart)
    
    json = scraperwiki.scrape(url)
    print json
    return simplejson.loads(json)

def get_page(page_id):
    url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&pageids=%s&rvprop=content&indexpageids&format=json' % page_id
    json = scraperwiki.scrape(url)
    content = simplejson.loads(json)
    id = content['query']['pageids'][0]
    actual_content = content['query']['pages'][id]['revisions'][0]['*']
    actual_content = re.sub("{{cite[^}]+}}","",actual_content)
    match = re.search('{{Infobox ([^}]*)}}', actual_content)
    g = geocoders.Google('ABQIAAAAD0swA2fCWr4WHfJT0hFApRQFh6EL7AzOjwKglJFzgjH9brlzARTFAkwWGlSkuzv9Tq_kKMoInlVlcA')
    
    if match != None:
        # there is an info box GOOD
        

        infobox =  match.group(1)
        details = infobox.split('|')
        info_dict = {}
        for pair in details:
            try:
                (key, val) = pair.split('=')
                key = key.strip()
                val = val.replace('[','').replace(']','')
                if key == 'Genre' or key=='Current_members':
                    val = val.split('<br>')
                    if len(val) == 1:
                        val = val[0].split('<br />')
                    if len(val) == 1:
                        val = val[0].split('<br/>')
                    if len(val) == 1:
                        val = val[0].split(',')
                    val = [re.sub(r'<[^>]*?>', '',e).strip() for e in val]

                info_dict[key] = val
            except ValueError:
                pass
    
        if info_dict.get('Origin',None) != None:
            # skip page without origin
            try:
                place, (lat, lng) = g.geocode(info_dict['Origin'].encode('utf8'))
            except:
                return None
            ret = {
                'pageids':id,
                'Name':info_dict.get('Name',None),
                'Origin':info_dict.get('Origin',None),
            }
            if info_dict.get('Genre',False):
                i=1
                for genre in info_dict['Genre']:
                    ret['Genre%s'%i] = genre
                    i=i+1
        else:
            return None
    else:
        #manage where there is not an info box
        return None
    return {'data':ret,'latlng':(lat,lng)}

def get_info(info, content):
    #FIX this to get multiple genre
    match = re.search('%s[\s]*=[\s]*([^|]*?)[\s]*[\||<|{]'%info, content)
    if match != None:
        return match.group(1).replace('[','').replace(']','')


def is_category(page_title):
    return page_title.startswith("Category:")


def scan_category(category):
    
    cat_list = get_category(category)
    has_page = True
    while has_page:
        #loop delle pagine
        
        for page in cat_list['query']['categorymembers']:
            if page['title'].startswith(("Talk:","List of")):
                pass
            elif is_category(page['title']):                
                cat = page['title'].split(":")
                print "--- category parsing %s" % cat[1]
                scan_category(cat[1])
            else:
                record = get_page(page['pageid'])
                if record != None:
                    if record['data']['Name'] == None:
                        record['data']['Name'] = page['title']
                    print record['data']['Name'] + record['data']['Origin']
                    scraperwiki.datastore.save(["Name"], record['data'], latlng=record['latlng'])
        if cat_list.has_key('query-continue'):
            cat_list = get_category(start_category, cat_list['query-continue']['categorymembers']['cmstart'])
        else:
            has_page = False
# retrieve a page
start_category = "Heavy metal musical groups by genre"
scan_category(start_category)




# save records to the datastore
#scraperwiki.datastore.save(["name"], record) 
    


#def get_page():