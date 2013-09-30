import scraperwiki, csv

API_KEY = 'testkey12'
START_DATE = '1996-01-01'
END_DATE = '2007-01-03'
SEARCH_PHRASES = """

# add the phrases you want to test below here, one per line. blank lines and ones prefaced by '#' will be skipped.
firearm
concealed carry

"""
INCLUDE_SENATE = True
INCLUDE_HOUSE = True

BASE_URL = 'http://capitolwords.org/api/dates.json?phrase=[phrase]&start_date=%s&end_date=%s&chamber=Senate' % (START_DATE, END_DATE)
LEGISLATOR_CSV = 'https://raw.github.com/sunlightlabs/apidata/master/legislators/legislators.csv'






def tally(r):
    total = 0
    j = json.loads(r)
    for i in j['results']:
        total += int(i['count'])
    return total

legislators = {}
data = scraperwiki.scrape(LEGISLATOR_CSV)
reader = csv.reader(data.splitlines())
for (i,row) in enumerate(reader):
    if i>0:
        if row[0].upper()=='SEN' and INCLUDE_SENATE:
            legislators[row[16]] = [row[0], row[1], row[2], row[3], row[4], {}]


search_phrases = []
for line in map(lambda x: x.strip(), SEARCH_PHRASES.split("\n")):
    if (line[0] is not '#') and (len(line)>0):
        search_phrases.append(line)


for term in search_phrases:
    term = term.strip()
    bioguide_counts = {}

    url = ('%s&apikey=%s' % (BASE_URL, API_KEY)).replace('[phrase]', term)

    for leg in legislators:   
        url_target = '%s&bioguide_id=%s' % (url, BIOGUIDE_ID)
        data = scraperwiki.scrape(url_target)

    target_count = tally(r_target.content)
    total_count = tally(r_all.content)

    writer.writerow( (term, target_count, total_count) )import scraperwiki, csv

API_KEY = 'testkey12'
START_DATE = '1996-01-01'
END_DATE = '2007-01-03'
SEARCH_PHRASES = """

# add the phrases you want to test below here, one per line. blank lines and ones prefaced by '#' will be skipped.
firearm
concealed carry

"""
INCLUDE_SENATE = True
INCLUDE_HOUSE = True

BASE_URL = 'http://capitolwords.org/api/dates.json?phrase=[phrase]&start_date=%s&end_date=%s&chamber=Senate' % (START_DATE, END_DATE)
LEGISLATOR_CSV = 'https://raw.github.com/sunlightlabs/apidata/master/legislators/legislators.csv'






def tally(r):
    total = 0
    j = json.loads(r)
    for i in j['results']:
        total += int(i['count'])
    return total

legislators = {}
data = scraperwiki.scrape(LEGISLATOR_CSV)
reader = csv.reader(data.splitlines())
for (i,row) in enumerate(reader):
    if i>0:
        if row[0].upper()=='SEN' and INCLUDE_SENATE:
            legislators[row[16]] = [row[0], row[1], row[2], row[3], row[4], {}]


search_phrases = []
for line in map(lambda x: x.strip(), SEARCH_PHRASES.split("\n")):
    if (line[0] is not '#') and (len(line)>0):
        search_phrases.append(line)


for term in search_phrases:
    term = term.strip()
    bioguide_counts = {}

    url = ('%s&apikey=%s' % (BASE_URL, API_KEY)).replace('[phrase]', term)

    for leg in legislators:   
        url_target = '%s&bioguide_id=%s' % (url, BIOGUIDE_ID)
        data = scraperwiki.scrape(url_target)

    target_count = tally(r_target.content)
    total_count = tally(r_all.content)

    writer.writerow( (term, target_count, total_count) )