#!/usr/bin/python
# @sopier
# 7 September 2012

"""
variasi email:
    someemail@domain.com
    some_email@domain.com
    some.email@domain.com
    someemail[at]domain.com
    someemail(at)domain.com
    someemail @ domain.com
    someemail @ domain . com
    someemail [at] domain.com
"""

import requests
import re
import time


"""Step by step logics:
    1. get url from keyword, i.e.: bike forums
    2. for each unique url, get_data()
"""


class EmailScraper(object):

    counter = 0    

    def __init__(self, forums):
        self.forums = forums

    def get_url(self, keyword):
        headers = {'User-agent': 'Mozilla/5.0'}
        url = 'http://www.google.com/search?q=' + keyword + '+forums'
        html = requests.get(url, headers=headers).content
        url_data = re.findall(re.compile(r"<cite>(.*)</cite>", re.DOTALL), url)
        return url_data
        
    def get_data(self):
        headers = {'User-agent': 'Mozilla/5.0'}
        base_url = 'http://www.google.com/search?q=site:' + self.forums + '+email+@yahoo.com+OR+@gmail.com+OR+@ymail.com+OR+@hotmail.com&num=100&start='
        
        email_container = []

        count = 1

        for i in range(2):
            url = base_url + str(self.counter)
            html = requests.get(url, headers=headers).content
            clean_html = html.replace('<b>', '').replace('</b>', '').lower()
            
            self.counter += 100
            print 'getting the data ' + str(count)
            count += 1
            time.sleep(15)

            email_data = re.findall(re.compile(r"\w+[_.]?\w+@\w+\.[a-zA-Z]+", re.I), clean_html)
            email_container.append(email_data)

        return email_container



e = EmailScraper('forums.roadbikereview.com')
print e.get_data()