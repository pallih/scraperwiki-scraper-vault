import urllib2 
"""
An extensible library for opening URLs
Reference: http://docs.python.org/2/library/urllib2.html
"""

import simplejson
"""
An extensible library for encoding and decoding JSON 
Reference: https://pypi.python.org/pypi/simplejson/
"""

import scraperwiki 
"""
A simple built in ScraperWiki library providead by scraperwiki.com
Reference: https://scraperwiki.com/docs/python/python_intro_tutorial/
"""

from scraperwiki import swimport
"""
Import the program code from another crawler
Reference: https://scraperwiki.com/docs/python/python_help_documentation/
"""

followers = []
# initialize an array to store the followers of a specified account

following = 'justinbieber' 
"""
The specified account that we want to crawl the data from his/her followers
Example:
justinbieber
"""

json_url = 'https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=' + following 
"""
The ids of the followers
Example:
https://api.twitter.com/1/followers/ids.json?cursor=-1&screen_name=justinbieber
"""

json_results = simplejson.loads(scraperwiki.scrape(json_url))
""" 
Download HTML from the specified website (scraperwiki.scrape(json_url))
and then Convert JSON into Python object (simplejson.loads(scraperwiki.scrape(json_url)))
Note that all strings in JSON must be included by double quotes
Reference: http://stackoverflow.com/questions/9524691/unable-to-use-simplejson-loads-on-a-string
"""

followers = json_results['ids']
"""
Put all the ids into the array "followers"
Reference: http://simplejson.readthedocs.org/en/latest/
http://hi.baidu.com/leejun_2005/item/fc688affc196f8723c198b7c
"""

followers_str = map(str, followers) 
"""
Convert the ids into String type
Reference: http://pydoing.blogspot.hk/2011/02/python-strbui.html
"""

swimport('compfyp1213b.emailer').lookup(followers_str)
# the second part of the program

