# Blank Python

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request
from time import sleep
import simplejson
import scraperwiki

"""This is the address of the advanced search"""
site = "http://www.saa.gov.uk"
search = site + "/search.php?SEARCHED=1&ST=advanced&SEARCH_TABLE=valuation_roll&TYPE_FLAG=C&x=11&y=6&AS_UARN=&DISPLAY_COUNT=100&POSTCODE="

# find the BoundaryLine geometry for Edinburgh
# ( http://unlock.edina.ac.uk/ws/search?name=City%20of%20Edinburgh - Edinburgh is ID 13323656 )
# find all the postcodes in Edinburgh's bounding box

def find_postcodes():
    postcode_search = "http://unlock.edina.ac.uk/ws/search?spatialMask=13323656&realSpatial=no&name=EH*&format=json&maxRows=200"
    res = simplejson.loads(urlopen(postcode_search).read())
    list_postcodes(res,0)

def crosscheck_postcodes():
    # we missed some, possibly due to a bug now fixed in Unlock search.
    # however some 200+ really don't exist in CodePoint, the mystery of the Bad Postcodes
    scraperwiki.sqlite.execute("delete from badpostcodes")
    codes = scraperwiki.sqlite.select("distinct postcode from properties")
    postcodes = list(p['postcode'] for p in codes)
    for p in postcodes:
         encoded = p.replace(' ','%20')
         got = scraperwiki.sqlite.select("* from postcodes where postcode = '"+p+"'")
         if got == []:
#             print "missing"
             try:
             #    possjson = urlopen("http://unlock.edina.ac.uk/ws/search?format=json&name="+encoded).read()
             #print possjson
                 res = simplejson.loads(urlopen("http://unlock.edina.ac.uk/ws/search?format=json&name="+p).read())
                 f = res['features'][0]
                 lonlat = f['properties']['centroid']
                 scraperwiki.sqlite.save(['postcode'],{'postcode':p,'lonlat':lonlat,'unlock_id':f['id']})
                 
#                 print res
             except:
#                 print "failed for "+p
                 scraperwiki.sqlite.save(['postcode'], {'postcode':p} ,table_name='badpostcodes')

def list_postcodes(res,startRow):

    total = res['totalResults']

    for f in res['features']:

        p = f['properties']['name']
        # Add a space - may be fragile. An issue for Unlock, postcodes should come out in their native forms
        chars = list(p)
        chars.insert(-3,' ')
        postcode = ''.join(chars)

        data = { 'postcode' : postcode, 'lonlat': f['properties']['centroid'],'unlock_id':f['id'] }

        scraperwiki.sqlite.save(['postcode'], data, table_name="postcodes")

    if startRow < total:
         startRow = startRow + 200
         try:
             find_postcodes(simplejson.loads(urlopen(postcode_search+'&startRow='+str(startRow)).read()),startRow)
         except:
             pass


def read_more(more):
    # extra metadata. currently only saving the proprietor info.
    soup = BeautifulSoup(urlopen(site+more).read())
    row = soup.find('tr',{'class':'bgdarkgrey'})
    data = {}
    # err happened? but why?
    try:
        cols = row.findAll('td')
        prop = cols[3]
        proprietor = "\n".join(list(c for c in prop.contents if c.string is not None))
        data['proprietor'] = proprietor
    except: pass

    return data 

def extract_data(row):
    # read the rows, look up links, save the data to the scraperwiki store
    data = {}
    cols = row.findAll('td')

    labels = { 0: 'ref_no',1:'description',2:'address',3:'occupier',4:'rateable',5:'more' }

    for n in labels.keys():
        if labels[n] == 'more':
            item = cols[n].find('a')['href']
        elif labels[n] == 'rateable':
            item = cols[n].contents[0]
            item = item.replace('&pound;','')
            item = item.replace(',','')
        elif labels[n] == 'address':
            item = "\n".join(list(c for c in cols[n].contents if c.string is not None))
            data['postcode'] = cols[n].contents[-1]
        elif cols[n].find('a') is not None:
            item = cols[n].find('a').text
        else: 
            item = "\n".join(list(c for c in cols[n].contents if c.string is not None))
        
        try: item.replace('<br />',' ')
        except: pass

        data[labels[n]] = item

    # commented out for now, as we want the core data 
    # and this will bring Scraperwiki down every few 2 or 3K requests - and there may easily be 100K
    #more = read_more(data['more'])
    # gesture of politeness? will ScraperWiki be cautious + storage save lag compensate?
    # sleep(1)

    #for k in more.keys(): data[k] = more[k]
    #data.pop('more')
    # instead
    data['proprietor'] = ''
    #print data
    scraperwiki.sqlite.save(['ref_no'], data,table_name='properties')

    return data

def read_page(raw):
    # page through looking for rows of data 
    soup = BeautifulSoup(raw)

    soup.find('br').replaceWith(' ')
    # fish out the table rows with light or dark grey CSS
    rows = soup.findAll('tr',{'class':'bglightgrey'})
    rows2 = soup.findAll('tr',{'class':'bgdarkgrey'})

    for row in rows: extract_data(row)
    for row in rows2: extract_data(row)

    # If there are results there will be a page count which may be > 1
    counter = soup.find('div',{'class':'pagecounter'})
    try: 
        pages = counter.findAll('li')
        count = len(pages)
        
        if count > 1:
            # follow the link after the current page
            search = None
            next = None
            for p in pages:
                a = p.find('a')
                 
                if next == 1:
                    search = a['href']
                    print search
                    break

                if a is None:
                    next = 1 
                
            print site+search
            read_page(urlopen(site+search).read())
    except:
        pass


# uncomment this to reload the Edinburgh postcode open data from Unlock
#find_postcodes()
    
# uncomment this to search ALL THE POSTCODES
#codes = scraperwiki.sqlite.select("postcode from postcodes")
#postcodes = list(p['postcode'] for p in codes)

# uncomment this just to test
# postcodes = ['EH9','EH27 8DF']
#postcodes = ['EH27 8DF']

# in an attempt to break through the rate limit to start with,
# lets try by postcode outcode, it'll paginate may count as one search


def search_request(postcode):
    request = Request(search+postcode)
    #print request.get_full_url()
    request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
    return urlopen(request).read()
    

def postcode_outcodes():

    nums = range(1,52) # there are up to 95 but
    postcodes = list( 'EH'+str(n) for n in nums)
    for p in postcodes:
        raw = search_request(p)
        soup = BeautifulSoup(raw)
        if soup.find('p',{'id':'results'}) is not None:

            incodes = list( p+'%20'+str(n) for n in range(1,9))
            for i in incodes: 
                print i
                read_page(search_request(i))

        else:
            read_page(raw)
            
            
#postcode_outcodes()    
def type_rateables():
    # if we force type to int we get integer column type?
    properties = scraperwiki.sqlite.select("* from properties")
    for p in properties:
        p['rates'] = int(p['rateable'])
        scraperwiki.sqlite.save(['ref_no'], p,table_name='properties')

def central_proprietors():
    # look up ownership info on vacant properties of suitable rateable value in central-ish areas
    # should have left out the commas for easy sort 
    postcodes = (1,2,3,6,7,8,9,10,11,16)
    for c in postcodes:
        code = 'EH'+str(c)+' %'
        print "* from properties where rates < 10000 and rates > 2000 and occupier = 'Vacant' and postcode like '"+code+"'"
        properties = scraperwiki.sqlite.select("* from properties where rates < 10000 and rates > 2000 and occupier = 'Vacant' and postcode like '"+code+"'")

        for p in properties:
            print p['postcode']
            print 'X'+p['proprietor']+'X'
            if p['proprietor'] is None:
                
                data = read_more(p['more'])
                p['proprietor'] = data['proprietor']

                scraperwiki.sqlite.save(['ref_no'], p,table_name='properties')

#type_rateables()
#central_proprietors()

def clean_postcodes():
    codes = scraperwiki.sqlite.select("* from postcodes where postcode like '%  %'")
    for p in codes:
        p['postcode'] = p['postcode'].replace('  ',' ')
        scraperwiki.sqlite.save(['postcode'], p, table_name="postcodes")
        
#clean_postcodes()

def split_lonlats(p):
    # yet again i was  trying to be too clever 
    lon,lat = p['lonlat'].split(',')
    p['lon'] = lon
    p['lat'] = lat 
    scraperwiki.sqlite.save(['ref_no'], p,table_name='properties')
    pass 

def append_lonlats():
    # for easier import into other services that expect geodata
    properties = scraperwiki.sqlite.select("* from properties where lonlat is null")
    failed = 0
    for p in properties:
        s = "* from postcodes where postcode = '"+p['postcode']+"'"
        #print s
        ll = scraperwiki.sqlite.select(s)
        try:
            lonlat = ll[0]['lonlat']
            p['lon'],p['lat'] = lonlat.split(',')
            scraperwiki.sqlite.save(['ref_no'], p,table_name='properties')

        except:
            failed = failed + 1
    print str(failed) + " postcodes failed"

  

def search_by_postcode():
    for p in postcodes:

    # don't duplicate requests
        found = scraperwiki.sqlite.select("* from properties where postcode is ? limit 1",[p])
        if len(found) != 0:
           continue

        p = p.replace(' ','%20')
        print p
        request = Request(search+p)
        #print request.get_full_url()
        request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
        raw=urlopen(request).read()
        #print raw
        read_page(raw)



crosscheck_postcodes()

append_lonlats()
