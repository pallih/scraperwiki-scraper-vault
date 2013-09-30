import scraperwiki
import json
import requests
import hmac
import hashlib
appid = 'appid=KEA74001'
appsecret = '584850749014014780c282529462e689'

# Blank Python
def get_token():
    key = hmac.new(appsecret, appid, hashlib.sha256).hexdigest()
    payload = {'key': key,'appid': 'KEA74001'}
    r = requests.get("http://api.iebc.or.ke/token/",params=payload)
    token_dict = json.loads(r.content)
    return token_dict['token']
def post_api(url):
    token = get_token()
    print token
    filter=''
    keyString = "%stoken=%s" % (filter, token)
    key = hmac.new(appsecret,keyString, hashlib.sha256).hexdigest()
    print key
    payload = {'token': token,'key':key}
    headers = {'content-type': 'application/json',"Content-Length": "0",}
    r = requests.get(url,params=payload)
    return r.content
def serialize(content):
    const_dict = json.loads(content)
    return const_dict

station_request = post_api("http://api.iebc.or.ke/pollingstation/")
station_dict = serialize(station_request)
stations = station_dict['polling_stations']

report_request = post_api('http://api.iebc.or.ke/reporting/')
print report_request
samplereport = post_api('http://api.iebc.or.ke/reporting/code/EBAC7ECA-DAE0-48FD-BF5A-7CD3AC5C74A9/')
print samplereport
#for station in stations:
#    print station['name']
    #url = 'http://api.iebc.or.ke/reporting/' + station['code'] + '/'
#    reported = post_api('http://api.iebc.or.ke/reporting/')
#    print reported
    


    

    



import scraperwiki
import json
import requests
import hmac
import hashlib
appid = 'appid=KEA74001'
appsecret = '584850749014014780c282529462e689'

# Blank Python
def get_token():
    key = hmac.new(appsecret, appid, hashlib.sha256).hexdigest()
    payload = {'key': key,'appid': 'KEA74001'}
    r = requests.get("http://api.iebc.or.ke/token/",params=payload)
    token_dict = json.loads(r.content)
    return token_dict['token']
def post_api(url):
    token = get_token()
    print token
    filter=''
    keyString = "%stoken=%s" % (filter, token)
    key = hmac.new(appsecret,keyString, hashlib.sha256).hexdigest()
    print key
    payload = {'token': token,'key':key}
    headers = {'content-type': 'application/json',"Content-Length": "0",}
    r = requests.get(url,params=payload)
    return r.content
def serialize(content):
    const_dict = json.loads(content)
    return const_dict

station_request = post_api("http://api.iebc.or.ke/pollingstation/")
station_dict = serialize(station_request)
stations = station_dict['polling_stations']

report_request = post_api('http://api.iebc.or.ke/reporting/')
print report_request
samplereport = post_api('http://api.iebc.or.ke/reporting/code/EBAC7ECA-DAE0-48FD-BF5A-7CD3AC5C74A9/')
print samplereport
#for station in stations:
#    print station['name']
    #url = 'http://api.iebc.or.ke/reporting/' + station['code'] + '/'
#    reported = post_api('http://api.iebc.or.ke/reporting/')
#    print reported
    


    

    



