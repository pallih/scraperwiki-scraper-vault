import BeautifulSoup
import urllib2
import scraperwiki
import time
from hashlib import md5

row_keys = ('Date', 'Purpose of meeting', 'Department', 'Minister', 'Title', 'date_scraped')

def runonce():
    depts_page = urllib2.urlopen('http://whoslobbying.com/uk/departments')
    s = BeautifulSoup.BeautifulSoup(depts_page)
    depts = [(li.a.string, li.a['href']) for li in s.findAll('li', {'class': 'department'})]
    return depts

def ministers(url):
    mins_page = urllib2.urlopen(url)
    s = BeautifulSoup.BeautifulSoup(mins_page)
    n = s.findAll('span', {'class': 'person'})
    names = [name.a['href'] for name in n if name.a['href']]
    return names

def parsealicious(dept, url):
    mins = ministers(url)
    for minister in mins:
        uri = minister
        try:
            page = urllib2.urlopen(uri)
        except urllib2.HTTPError:
            print 'http error, skipped: ', uri
            continue
        soup = BeautifulSoup.BeautifulSoup(page)
        months = soup.findAll('div', {'class': 'span4'})
        mn = soup.find('h1', {'class': 'fn'})
        minister_name = mn.string
        mr = soup.find('span', {'class': 'role_title'})
        minister_role = (mr.string).strip()
        if minister_name == None:
            minister_name = minister_role
        else:
            minister_name = (mn.string).strip()
        months = soup.findAll('div', {'class': 'span4'})
        for month in months:
            meetings = month.findAll('p', {'class': 'vevent meeting'})
            d = month.find('h3', {'class': 'period'})
            if d != None:
                date = d.string
            for meeting in meetings:
                    attendee_spans = meeting.findAll('span', {'class': 'attendee'})
                    attendees = [attendee.a.contents[0] for attendee in attendee_spans]
                    purp = meeting.find('span', {'class': 'purpose'})
                    if purp:
                        purpose = purp.string
                    else:
                        purp = attendee_spans[-1]
                        purpose = purp.next_sibling
                    date_scraped = time.time()
                    output = dict(zip(row_keys, (date, purpose, dept, minister_name, minister_role, date_scraped)))
                    hasher = md5()
                    hasher.update(str(output))
                    output['meeting_hash'] = hasher.hexdigest()
                    scraperwiki.sqlite.save(data=output, unique_keys=['meeting_hash'])
                    for attendee in attendees:
                        scraperwiki.sqlite.execute('INSERT INTO lobbies VALUES (?, ?)', [(output['meeting_hash']), attendee])
                    scraperwiki.sqlite.commit()

ranonce = scraperwiki.sqlite.get_var('ranonce', 'no')

if ranonce == 'no':
    depts = runonce()
    for department in depts:
        d = {}
        d.update(dept=(department[0]), uri=(department[1]))
        print d['dept']
        scraperwiki.sqlite.save(data=d, unique_keys=['dept'], table_name='uris')
    scraperwiki.sqlite.save_var('ranonce', 'yes')
    scraperwiki.sqlite.execute('''CREATE TABLE lobbies ('meeting_hash' TEXT, 'lobby' TEXT, UNIQUE('meeting_hash', 'lobby') ON CONFLICT IGNORE);''')

else:
    depts = scraperwiki.sqlite.select("* from uris")
for dept in depts:
    parsealicious(dept["dept"], dept["uri"])
