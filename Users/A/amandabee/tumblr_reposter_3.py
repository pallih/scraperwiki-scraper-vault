""" 
I have a bunch of tumblrs. I'd like to aggregate them on my own 
(horribly neglected) WordPress blog. 

"""

import scraperwiki
import json
import datetime
import pprint

import urllib

handles = {'amandabees','raizes','cs101','keepyoungandbeautiful','jour72312','pickledcarrots','nomadly','newsgamery','craft-ii','moreia'}


def iterate(set):
    for each in handles:
        url = 'http://'+ each + '.tumblr.com/api/read/json'
        pp = pprint.PrettyPrinter(indent=2)
        #data = json.loads(urllib.urlopen(url).read())
        data = urllib.urlopen(url).read()
        jdata = json.loads(data)
        pp.pprint(jdata)
        try:
            data = json.loads(urllib.urlopen(url).read())
            pp.pprint(data)
        except:
            print url
        # json 


iterate(handles)

""" 
I have a bunch of tumblrs. I'd like to aggregate them on my own 
(horribly neglected) WordPress blog. 

"""

import scraperwiki
import json
import datetime
import pprint

import urllib

handles = {'amandabees','raizes','cs101','keepyoungandbeautiful','jour72312','pickledcarrots','nomadly','newsgamery','craft-ii','moreia'}


def iterate(set):
    for each in handles:
        url = 'http://'+ each + '.tumblr.com/api/read/json'
        pp = pprint.PrettyPrinter(indent=2)
        #data = json.loads(urllib.urlopen(url).read())
        data = urllib.urlopen(url).read()
        jdata = json.loads(data)
        pp.pprint(jdata)
        try:
            data = json.loads(urllib.urlopen(url).read())
            pp.pprint(data)
        except:
            print url
        # json 


iterate(handles)

