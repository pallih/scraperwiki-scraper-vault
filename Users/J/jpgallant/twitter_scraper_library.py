import scraperwiki
import simplejson
import urllib2
import dateutil.parser

# This scraper works with timeline in a more efficient way than the deprecated
# paging version that is used on scraperwiki
# https://dev.twitter.com/docs/working-with-timelines

# TODO: write support for storing entities

COUNT    = 200
MAX_RUNS = 8

num_runs = 0
VERBOSE = False

def get_db_max_id():
    max_db_id = 0

    try:
        query_result = scraperwiki.sqlite.select("id from swdata order by id desc limit 1")
    
        if query_result:
            max_db_id = query_result[0]['id']
    except:
        pass
    
    return max_db_id

def get_db_min_id():
    min_db_id = 0

    try:
        query_result = scraperwiki.sqlite.select("id from swdata order by id limit 1")

        if query_result:
            min_db_id = query_result[0]['id']
    except:
        pass

    return min_db_id  

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

def get_num_rows():
    num_rows = 0
    try:
        result = scraperwiki.sqlite.select("count(id) as n from swdata")
        if result:
            num_rows = result[0]['n']
    except:
        pass

    return num_rows

def fetch_statuses(max_id, since_id, username, list):
    base_url = 'https://api.twitter.com/1/%s/lists/%s/statuses.json?include_entities=false&include_rts=true&per_page=%s' \
         % (urllib2.quote(username), urllib2.quote(list), COUNT)
    
    if max_id > 0:
        base_url += "&max_id=%s" % max_id

    if since_id > 0:
        base_url += "&since_id=%s" % since_id

    json = fetch_url(base_url)
    results_json = simplejson.loads(json)
    
    return results_json
    
def fetch_user_timeline(max_id, since_id, username):
    base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=false&include_rts=true&screen_name=%s&count=%s' \
         % (urllib2.quote(username), COUNT)
    
    if max_id > 0:
        base_url += "&max_id=%s" % max_id

    if since_id > 0:
        base_url += "&since_id=%s" % since_id

    json = fetch_url(base_url)
    results_json = simplejson.loads(json)
    
    return results_json
 
def add_results(results_json, max_id):
    new_max_id = num_saved = 0
    for result in results_json:    
        data = {}
        data['id'] = result['id']
        data['text'] = result['text']
        data['from_user_id'] = result['user']['id']
        data['from_user'] = result['user']['name']
        data['created_at'] = dateutil.parser.parse(result['created_at'])
    
        # print data['id']
        scraperwiki.sqlite.save(["id"], data)
        num_saved += 1
    
        if data['id'] < max_id or 0 == max_id:
            new_max_id = data['id']
            #print "New max_id: %s" % new_max_id    

    return (new_max_id, num_saved)

# fetches from the top of the timeline aka new messages
def fetch_from_top(since_id, fetcher, *args):
    global num_runs
    num_saved_lastrun = 1
    num_saved_total = 0
    max_id = 0 # first fetch without this
    while num_saved_lastrun > 0 and num_runs < MAX_RUNS:
        results_json = fetcher(max_id, since_id, *args)
        (new_max_id, num_saved_lastrun) = add_results(results_json, max_id)
        max_id = new_max_id-1 # decrease by 1 since max_id is always returned
        num_runs += 1
        num_saved_total += num_saved_lastrun

    if VERBOSE:
        print "Finished fetching from top. Found a total of %d" % num_saved_total

def fetch_from_bottom(max_id, fetcher, *args):
    global num_runs
    num_saved_lastrun = 1
    num_saved_total = 0
    while num_saved_lastrun > 0 and num_runs < MAX_RUNS:
        results_json = fetcher(max_id, 0, *args)
        (new_max_id, num_saved_lastrun) = add_results(results_json, max_id)
        max_id = new_max_id-1 # decrease by 1 since max_id is always returned
        num_runs += 1
        num_saved_total += num_saved_lastrun

    if VERBOSE:
        print "Finished fetching from bottom. Found a total of %d" % num_saved_total

def statuses(username, list, verbose=False):
    global VERBOSE
    VERBOSE = verbose
    # Fetch max_id from db
    max_db_id = get_db_max_id()

    # First fetch all new
    fetch_from_top(max_db_id, fetch_statuses, username, list)

    # Fetch min id from db
    min_db_id = get_db_min_id()

    num_rows = get_num_rows()
    # if we have more than 3200 rows we probably have nothing to fetch at the end of the timeline
    if num_rows < 3200:
        fetch_from_bottom(min_db_id - 1, fetch_statuses, username, list) # decrease by 1 since max_id is always returned and we got it'
    elif VERBOSE:
        print "Not fetching from bottom. Got it all"

def user_timeline(username, verbose=False):
    global VERBOSE
    VERBOSE = verbose
    # Fetch max_id from db
    max_db_id = get_db_max_id()

    # First fetch all new
    fetch_from_top(max_db_id, fetch_user_timeline, username)

    # Fetch min id from db
    min_db_id = get_db_min_id()

    num_rows = get_num_rows()
    # if we have more than 3200 rows we probably have nothing to fetch at the end of the timeline
    if num_rows < 3200:
        fetch_from_bottom(min_db_id - 1, fetch_user_timeline, username) # decrease by 1 since max_id is always returned and we got it'
    elif VERBOSE:
        print "Not fetching from bottom. Got it all"import scraperwiki
import simplejson
import urllib2
import dateutil.parser

# This scraper works with timeline in a more efficient way than the deprecated
# paging version that is used on scraperwiki
# https://dev.twitter.com/docs/working-with-timelines

# TODO: write support for storing entities

COUNT    = 200
MAX_RUNS = 8

num_runs = 0
VERBOSE = False

def get_db_max_id():
    max_db_id = 0

    try:
        query_result = scraperwiki.sqlite.select("id from swdata order by id desc limit 1")
    
        if query_result:
            max_db_id = query_result[0]['id']
    except:
        pass
    
    return max_db_id

def get_db_min_id():
    min_db_id = 0

    try:
        query_result = scraperwiki.sqlite.select("id from swdata order by id limit 1")

        if query_result:
            min_db_id = query_result[0]['id']
    except:
        pass

    return min_db_id  

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

def get_num_rows():
    num_rows = 0
    try:
        result = scraperwiki.sqlite.select("count(id) as n from swdata")
        if result:
            num_rows = result[0]['n']
    except:
        pass

    return num_rows

def fetch_statuses(max_id, since_id, username, list):
    base_url = 'https://api.twitter.com/1/%s/lists/%s/statuses.json?include_entities=false&include_rts=true&per_page=%s' \
         % (urllib2.quote(username), urllib2.quote(list), COUNT)
    
    if max_id > 0:
        base_url += "&max_id=%s" % max_id

    if since_id > 0:
        base_url += "&since_id=%s" % since_id

    json = fetch_url(base_url)
    results_json = simplejson.loads(json)
    
    return results_json
    
def fetch_user_timeline(max_id, since_id, username):
    base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=false&include_rts=true&screen_name=%s&count=%s' \
         % (urllib2.quote(username), COUNT)
    
    if max_id > 0:
        base_url += "&max_id=%s" % max_id

    if since_id > 0:
        base_url += "&since_id=%s" % since_id

    json = fetch_url(base_url)
    results_json = simplejson.loads(json)
    
    return results_json
 
def add_results(results_json, max_id):
    new_max_id = num_saved = 0
    for result in results_json:    
        data = {}
        data['id'] = result['id']
        data['text'] = result['text']
        data['from_user_id'] = result['user']['id']
        data['from_user'] = result['user']['name']
        data['created_at'] = dateutil.parser.parse(result['created_at'])
    
        # print data['id']
        scraperwiki.sqlite.save(["id"], data)
        num_saved += 1
    
        if data['id'] < max_id or 0 == max_id:
            new_max_id = data['id']
            #print "New max_id: %s" % new_max_id    

    return (new_max_id, num_saved)

# fetches from the top of the timeline aka new messages
def fetch_from_top(since_id, fetcher, *args):
    global num_runs
    num_saved_lastrun = 1
    num_saved_total = 0
    max_id = 0 # first fetch without this
    while num_saved_lastrun > 0 and num_runs < MAX_RUNS:
        results_json = fetcher(max_id, since_id, *args)
        (new_max_id, num_saved_lastrun) = add_results(results_json, max_id)
        max_id = new_max_id-1 # decrease by 1 since max_id is always returned
        num_runs += 1
        num_saved_total += num_saved_lastrun

    if VERBOSE:
        print "Finished fetching from top. Found a total of %d" % num_saved_total

def fetch_from_bottom(max_id, fetcher, *args):
    global num_runs
    num_saved_lastrun = 1
    num_saved_total = 0
    while num_saved_lastrun > 0 and num_runs < MAX_RUNS:
        results_json = fetcher(max_id, 0, *args)
        (new_max_id, num_saved_lastrun) = add_results(results_json, max_id)
        max_id = new_max_id-1 # decrease by 1 since max_id is always returned
        num_runs += 1
        num_saved_total += num_saved_lastrun

    if VERBOSE:
        print "Finished fetching from bottom. Found a total of %d" % num_saved_total

def statuses(username, list, verbose=False):
    global VERBOSE
    VERBOSE = verbose
    # Fetch max_id from db
    max_db_id = get_db_max_id()

    # First fetch all new
    fetch_from_top(max_db_id, fetch_statuses, username, list)

    # Fetch min id from db
    min_db_id = get_db_min_id()

    num_rows = get_num_rows()
    # if we have more than 3200 rows we probably have nothing to fetch at the end of the timeline
    if num_rows < 3200:
        fetch_from_bottom(min_db_id - 1, fetch_statuses, username, list) # decrease by 1 since max_id is always returned and we got it'
    elif VERBOSE:
        print "Not fetching from bottom. Got it all"

def user_timeline(username, verbose=False):
    global VERBOSE
    VERBOSE = verbose
    # Fetch max_id from db
    max_db_id = get_db_max_id()

    # First fetch all new
    fetch_from_top(max_db_id, fetch_user_timeline, username)

    # Fetch min id from db
    min_db_id = get_db_min_id()

    num_rows = get_num_rows()
    # if we have more than 3200 rows we probably have nothing to fetch at the end of the timeline
    if num_rows < 3200:
        fetch_from_bottom(min_db_id - 1, fetch_user_timeline, username) # decrease by 1 since max_id is always returned and we got it'
    elif VERBOSE:
        print "Not fetching from bottom. Got it all"