import sgmllib
import urllib2
import time
import urllib

import os
r =0
class get_usproxy(sgmllib.SGMLParser):
    def parse(self, s):
        self.feed(s)
        self.close()
    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.inside_item = 0
        self.inside_title = 0
        self.inside_port = 0
        self.inside_proxy = 0
        self.inside_guid = 0
        self.US = 0
        self.proxy_list = []
        self.proxy = ""
        self.ip = ""
        self.port = ""
    def handle_data(self, data):
        if self.inside_item:
            if self.inside_guid:
                #if data.__contains__('http//www.proxylists.net/us_0.html'):
                if data.__contains__('http//www.proxylists.net/3128_0.html'):
                    self.US = 1
                else:
                    self.US = 0
        if self.US:
            if self.inside_proxy ==1:
                self.ip = data
                
            elif self.inside_port ==1:
                self.port=data
    def start_item(self, attributes):
        self.inside_item = 1
    def end_item(self):
        self.inside_item = 0
    def start_title(self, attributes):
        self.inside_title = 1
    def end_title(self):
        self.inside_title = 0
    def start_guid(self, attributes):
        self.inside_guid = 1
    def end_guid(self): 
        self.inside_guid = 0
    def start_prxproxy(self, attributes):
        if self.US:
            self.proxy = ""
    def end_prxproxy(self):
        if self.US:
            self.proxy = self.ip + ":" + self.port
            self.proxy_list.append(self.proxy)
    def start_prxip(self, attributes):
        self.inside_proxy = 1
    def end_prxip(self):
        self.inside_proxy = 0
    def start_prxport(self, attributes):
        self.inside_port = 1
    def end_prxport(self): 
        self.inside_port = 0
############ end of class get_usproxy


k = urllib2.urlopen("http://www.proxylists.net/proxylists.xml").read()
proxyparser = get_usproxy()
k = k.replace(":","")
proxyparser.parse(k)
proxy_list = proxyparser.proxy_list
for l in proxy_list:
    print l