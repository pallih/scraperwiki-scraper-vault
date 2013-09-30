import scraperwiki
import json
from lxml import etree
import random
import requests
import sys

requests.defaults.defaults['max_retries'] = 5
swutils=scraperwiki.utils.swimport('swutils')

user_agent =  swutils.get_user_agent()

def get_proxy():
    proxies = []
    ''' Returns a list with number of proxies
    format: {'http':ip:port '''
    apikey= '8811f365d8194c949c61f6d7f8e9f36760dc8bb9'
    proxieslist = scraperwiki.scrape('http://www.getproxy.jp/proxyapi?ApiKey=%s&area=US&sort=updatetime&orderby=asc' % apikey)
    doc = etree.XML(proxieslist.strip())
    messages = doc.findall("item/ip")
    for x in messages:
        proxies.append(x.text)
    return {'http':str(random.choice(proxies))}
#proxies = get_proxy()
proxies = {'http':'216.244.71.143:3128'}

print 'User agent'
print user_agent
print

print 'Local ip:'
print requests.get('http://httpbin.org/ip').text
response =  requests.get('http://httpbin.org/ip',proxies=proxies,headers=user_agent,verify=False)
print
print 'Proxy ip'
print response.text
print response.request.headers
print response.historyimport scraperwiki
import json
from lxml import etree
import random
import requests
import sys

requests.defaults.defaults['max_retries'] = 5
swutils=scraperwiki.utils.swimport('swutils')

user_agent =  swutils.get_user_agent()

def get_proxy():
    proxies = []
    ''' Returns a list with number of proxies
    format: {'http':ip:port '''
    apikey= '8811f365d8194c949c61f6d7f8e9f36760dc8bb9'
    proxieslist = scraperwiki.scrape('http://www.getproxy.jp/proxyapi?ApiKey=%s&area=US&sort=updatetime&orderby=asc' % apikey)
    doc = etree.XML(proxieslist.strip())
    messages = doc.findall("item/ip")
    for x in messages:
        proxies.append(x.text)
    return {'http':str(random.choice(proxies))}
#proxies = get_proxy()
proxies = {'http':'216.244.71.143:3128'}

print 'User agent'
print user_agent
print

print 'Local ip:'
print requests.get('http://httpbin.org/ip').text
response =  requests.get('http://httpbin.org/ip',proxies=proxies,headers=user_agent,verify=False)
print
print 'Proxy ip'
print response.text
print response.request.headers
print response.history