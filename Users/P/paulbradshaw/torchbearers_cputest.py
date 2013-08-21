import scraperwiki
import lxml.html
import requests


# Global settings

base_url = 'http://www.london2012.com'
headers_dict = {'user-agent': 'Mozilla/5.0'}


# Helper functions

def get_dates():
    dates = []
    print '-- Scraping the list of dates'
    url = base_url + '/torch-relay/torchbearers/'
    html = requests.get(url, headers=headers_dict)
    dom = lxml.html.fromstring(html.text)
    for option in dom.cssselect('#communityByRegionfilterDayTorch option'):
        if option.get('value'):
            dates.append({'url': base_url + option.get('value'), 'date': option.text})
    print '-- Saving the list of dates'
    scraperwiki.sqlite.save(['url'], dates, 'dates')

def get_torchbearers():
    dates = scraperwiki.sqlite.select('* from dates')
    for d in dates:
        torchbearers2 = []
        print '-- Scraping torch bearers on ' + d['url']
        html = requests.get(d['url'], headers=headers_dict)
        dom = lxml.html.fromstring(html.text)
    
        for box in dom.cssselect('.torchBearerInfo'):
            temp = {
                'name': box.cssselect('.torchBearersName span')[0].text,
                'photo_url': base_url + box.cssselect('.torchBearerPhoto img')[0].get('src'),
                'date': d['date'],
                'date_url': d['url'],
                'location': box.cssselect('.tb-community a')[0].text,
                'location_url': base_url + box.cssselect('.tb-community a')[0].get('href'),
                'age': int(box.cssselect('.tb-age')[0].text.strip().replace('Age: ','')),
                'hometown': box.cssselect('.tb-hometown')[0].text.strip().replace('Hometown: ',''),
                'story': ''
            }
            try:
                temp['url'] = base_url + box.cssselect('.torchBearersName a')[0].get('href')
            except IndexError:
                temp['url'] = None
    
            torchbearers2.append(temp)
    
        print '-- Saving torch bearers on ' + d['url']
        scraperwiki.sqlite.save(['name', 'age'], torchbearers2, 'torchbearers')

def get_stories():
    torchbearers = scraperwiki.sqlite.select('* from torchbearers where url is not null and story == ""')
    for torchbearer in torchbearers:
        html = requests.get(torchbearer['url'], headers=headers_dict)
        dom = lxml.html.fromstring(html.text)
        try:    
            if dom.cssselect('.torchBearerBioText p')[0].text:
                story = dom.cssselect('.torchBearerBioText p')[0].text.strip('"')
                name = torchbearer['name']
                print "-- Saving " + name + "'s story"
                scraperwiki.sqlite.execute('update torchbearers set story=? where url=?', (story, torchbearer['url']))
                scraperwiki.sqlite.commit()
                scraperwiki.sqlite.save_var('name', name)
        except scraperwiki.CPUTimeExceededError:
            print "CPU exception caught"
        except:
            print "Error, unexpected exception"
            raise


try:
    # Do we have a list of dates?
    print scraperwiki.sqlite.select('count(*) as count from dates')[0]['count'], 'dates found'
except:
    # No we don't. So get them…
    get_dates()

try:
    # Great, we have a list of dates. Do we have a list of torchbearers?
    print scraperwiki.sqlite.select('count(*) as count from torchbearers')[0]['count'], 'torchbearers found'
except:
    # No we don't. So get them…
    get_torchbearers()

# Great, we have a list of torchbearers. Do we have their stories?
t = scraperwiki.sqlite.select("count(*) as count from torchbearers where url is not null")[0]['count']
s = scraperwiki.sqlite.select('count(*) as count from torchbearers where url is not null and story != ""')[0]['count']
if s < t:
    print t - s, 'torchbearers lack a story'
get_stories()
print 'all torchbearers have a story'


import scraperwiki
import lxml.html
import requests


# Global settings

base_url = 'http://www.london2012.com'
headers_dict = {'user-agent': 'Mozilla/5.0'}


# Helper functions

def get_dates():
    dates = []
    print '-- Scraping the list of dates'
    url = base_url + '/torch-relay/torchbearers/'
    html = requests.get(url, headers=headers_dict)
    dom = lxml.html.fromstring(html.text)
    for option in dom.cssselect('#communityByRegionfilterDayTorch option'):
        if option.get('value'):
            dates.append({'url': base_url + option.get('value'), 'date': option.text})
    print '-- Saving the list of dates'
    scraperwiki.sqlite.save(['url'], dates, 'dates')

def get_torchbearers():
    dates = scraperwiki.sqlite.select('* from dates')
    for d in dates:
        torchbearers2 = []
        print '-- Scraping torch bearers on ' + d['url']
        html = requests.get(d['url'], headers=headers_dict)
        dom = lxml.html.fromstring(html.text)
    
        for box in dom.cssselect('.torchBearerInfo'):
            temp = {
                'name': box.cssselect('.torchBearersName span')[0].text,
                'photo_url': base_url + box.cssselect('.torchBearerPhoto img')[0].get('src'),
                'date': d['date'],
                'date_url': d['url'],
                'location': box.cssselect('.tb-community a')[0].text,
                'location_url': base_url + box.cssselect('.tb-community a')[0].get('href'),
                'age': int(box.cssselect('.tb-age')[0].text.strip().replace('Age: ','')),
                'hometown': box.cssselect('.tb-hometown')[0].text.strip().replace('Hometown: ',''),
                'story': ''
            }
            try:
                temp['url'] = base_url + box.cssselect('.torchBearersName a')[0].get('href')
            except IndexError:
                temp['url'] = None
    
            torchbearers2.append(temp)
    
        print '-- Saving torch bearers on ' + d['url']
        scraperwiki.sqlite.save(['name', 'age'], torchbearers2, 'torchbearers')

def get_stories():
    torchbearers = scraperwiki.sqlite.select('* from torchbearers where url is not null and story == ""')
    for torchbearer in torchbearers:
        html = requests.get(torchbearer['url'], headers=headers_dict)
        dom = lxml.html.fromstring(html.text)
        try:    
            if dom.cssselect('.torchBearerBioText p')[0].text:
                story = dom.cssselect('.torchBearerBioText p')[0].text.strip('"')
                name = torchbearer['name']
                print "-- Saving " + name + "'s story"
                scraperwiki.sqlite.execute('update torchbearers set story=? where url=?', (story, torchbearer['url']))
                scraperwiki.sqlite.commit()
                scraperwiki.sqlite.save_var('name', name)
        except scraperwiki.CPUTimeExceededError:
            print "CPU exception caught"
        except:
            print "Error, unexpected exception"
            raise


try:
    # Do we have a list of dates?
    print scraperwiki.sqlite.select('count(*) as count from dates')[0]['count'], 'dates found'
except:
    # No we don't. So get them…
    get_dates()

try:
    # Great, we have a list of dates. Do we have a list of torchbearers?
    print scraperwiki.sqlite.select('count(*) as count from torchbearers')[0]['count'], 'torchbearers found'
except:
    # No we don't. So get them…
    get_torchbearers()

# Great, we have a list of torchbearers. Do we have their stories?
t = scraperwiki.sqlite.select("count(*) as count from torchbearers where url is not null")[0]['count']
s = scraperwiki.sqlite.select('count(*) as count from torchbearers where url is not null and story != ""')[0]['count']
if s < t:
    print t - s, 'torchbearers lack a story'
get_stories()
print 'all torchbearers have a story'


