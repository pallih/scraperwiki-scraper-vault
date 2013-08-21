import requests
import scraperwiki
import lxml.html
import re
import json
import tarfile
import time
import StringIO
import os
import collections
import datetime

START_URL = 'https://classic.scraperwiki.com/browse/scrapers/?page=%s'
JSON_URL = 'https://api.scraperwiki.com/api/1.0/scraper/getuserinfo?format=jsondict&username=%s'
BASEDIR = os.path.dirname(os.path.abspath(__file__))
username_regex = re.compile("\/profiles\/(.*)\/")

s = requests.Session()

def scrape_usernames(page):
    print 'Doing page', page
    batch = []
    html = s.get(START_URL % page).text
    root = lxml.html.fromstring(html)
    owners = root.xpath('//a[@class="owner"]')
    for owner in owners:
        usernames = {}
        usernames['username'] = ( username_regex.findall(owner.attrib['href'])[0] )
        usernames['done'] = 0
        usernames['scrapercount'] = 0
        batch.append(usernames)
    scraperwiki.sqlite.save(["username"], batch, table_name="usernames")

#Collect usernames:
'''
for i in range(1,750):
    scrape_usernames(i)

'''

def scrape_user_scrapers(username):
    print 'Scraping user:', username
    mtime = time.time()
    alphachar = username[:1].upper()
    if not os.path.exists(BASEDIR+'/Users/'+ alphachar + '/' + username):
        os.makedirs(BASEDIR+'/Users/'+ alphachar + '/' + username)
    USERDIR = BASEDIR+'/Users/' + alphachar + '/' +username
    tarfilename = USERDIR+ '/'+username+'-scrapers.tar'
    tar = tarfile.open(tarfilename, 'w:gz')
    user_json = json.loads(s.get(JSON_URL % username).text)
    scrapers = []
    for d in user_json:
        for scraper_name in d['coderoles']['owner']:
            scrapers.append(scraper_name)
    scrapercount = len(scrapers)
    print '  Saving', scrapercount, 'scraper(s)'
    try:
        for scraper_name in scrapers:

            scraper = 'https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name='+scraper_name+'&version=-1&quietfields=runevents%7Cdatasummary%7Cuserroles%7Chistory'
            scraper_json = json.loads(s.get(scraper).text)
            for scrapers in scraper_json:
                code = scrapers['code'].encode('utf-8')
                language = scrapers['language']
                if language == 'python':
                    ending = '.py'
                elif language == 'php':
                    ending = '.php'
                elif language == 'ruby':
                    ending = '.rb'
                elif language == 'html':
                    ending = '.html'
                else:
                    ending = '.txt'
                tarinfo = tarfile.TarInfo(scraper_name+ending)
                tarinfo.size = len(code)
                tarinfo.mtime = mtime
                tar.addfile(tarinfo, StringIO.StringIO(str(code)))
                with open(USERDIR+'/'+scraper_name+ending, 'a') as the_file:
                    the_file.write(code)
        tar.close()
        update_statement= 'update usernames SET done=1 WHERE username ='+ '"' + username + '"'
        scraperwiki.sqlite.execute(update_statement)
        update_statement= 'update usernames SET scrapercount='+ '"' + str(scrapercount) + '" WHERE username ='+ '"' + username + '"'
        scraperwiki.sqlite.execute(update_statement)
        scraperwiki.sqlite.commit()
    except:
        print 'Oooops, something went wrong - must investigate'
        pass

def write_readme_file():
    stat_string = 'Count of file extensions<br>'
    extensions = collections.defaultdict(int)
    for path, dirs, files in os.walk(BASEDIR+'/Users/'):
        for filename in files:
            extensions[os.path.splitext(filename)[1].lower()] += 1

    for key,value in extensions.items():
        stat_string = stat_string + 'Extension: ' + str(key) + ' ' + str(value) + '<br>' #+ ' ' + value, +' items'
    return stat_string

todo = scraperwiki.sqlite.select('* from usernames where done=0')

print len(todo), 'users left to scrape'

for username in todo:
    scrape_user_scrapers(username['username'])

print 'All done'

intro = 'This repository contains code for all public scrapers at scraperwiki.com, as of <br>'\
        + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")\
        + '<br><br>'\
        + 'It was created by pallih @ gogn.in / twitter.com/pallih' \
        + '<br><br>'\
        + 'Some statistics: <br><br>'

file_stats = write_readme_file()
users = scraperwiki.sqlite.select('* from usernames')
over_100 = scraperwiki.sqlite.select('username,scrapercount from usernames WHERE CAST(scrapercount AS integer)>100 order by scrapercount DESC')
failed = scraperwiki.sqlite.select('* from usernames where done = 0')
usercount = len(users)

print 'Writing readme'

with open(BASEDIR+'/readme.md', 'w') as the_file:
    the_file.write(intro)
    the_file.write(file_stats)
    the_file.write('<br><br>')
    the_file.write('User stats:')
    the_file.write('<br><br>')
    the_file.write('Number of users: ' + str(usercount))
    the_file.write('<br><br>')
    the_file.write('Users with over 100 scrapers:<br>')
    for user in over_100:
        the_file.write(user['username'] +' ' + user['scrapercount'] + '<br>')
    the_file.write('<br><br>')
    the_file.write('Usernames that retrieval failed for:<br>')
    for user in failed:
        the_file.write(user['username'] + '<br>')