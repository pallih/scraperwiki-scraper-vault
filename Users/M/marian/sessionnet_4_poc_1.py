# encoding: utf-8

import scraperwiki
import mechanize
import re
import time
import hashlib
import pprint

"""
Proof of concept for SessionNet 4.4.3 attachment scraping
"""

BASE_URL = "https://secure.stadt-witten.de/session/bis/"
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'scrape-a-ris/0.1')]

START_SESSION_ID = 1270
END_SESSION_ID = 1271

def get_sitzung(id):
    url = BASE_URL + "to0040.asp?__ksinr=%d" % id
    print url
    br.open(url)
    for link in br.links(url_regex=".*kvonr.*"):
        print link.url
        get_vorlage(id, BASE_URL + link.url)
        time.sleep(0.3)

def get_vorlage(session_id, url):
    try:
        response = mechanize.urlopen(mechanize.Request(url))
        #pprint.pprint(response)
    except URLError:
        return
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    for form in forms:
        # All forms are iterated. Might not all be attachment-related.
        for control in form.controls:
            if control.name == 'DT':
                print "Attachment found:", control.value
                request2 = form.click()
                try:
                    response2 = mechanize.urlopen(request2)
                    form_url = response2.geturl()
                    if "getfile.asp" in form_url or 'ydocstart.asp' in form_url:
                        data = response2.read()
                        md5 = hashlib.md5(data).hexdigest()
                        scraperwiki.sqlite.save(
                            unique_keys=['session_id', 'dt', 'md5', 'size'],
                            data={'session_id': session_id, 'dt': control.value, 'md5': md5, 'size': len(data)})
                        continue
                except mechanize.HTTPError, response2:
                    print "HTTP-FEHLER :("
                except URLError:
                    pass

for si in range(START_SESSION_ID, END_SESSION_ID):
    print "Getting Sitzung %d" % si
    get_sitzung(si)
    time.sleep(1)
# encoding: utf-8

import scraperwiki
import mechanize
import re
import time
import hashlib
import pprint

"""
Proof of concept for SessionNet 4.4.3 attachment scraping
"""

BASE_URL = "https://secure.stadt-witten.de/session/bis/"
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'scrape-a-ris/0.1')]

START_SESSION_ID = 1270
END_SESSION_ID = 1271

def get_sitzung(id):
    url = BASE_URL + "to0040.asp?__ksinr=%d" % id
    print url
    br.open(url)
    for link in br.links(url_regex=".*kvonr.*"):
        print link.url
        get_vorlage(id, BASE_URL + link.url)
        time.sleep(0.3)

def get_vorlage(session_id, url):
    try:
        response = mechanize.urlopen(mechanize.Request(url))
        #pprint.pprint(response)
    except URLError:
        return
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    for form in forms:
        # All forms are iterated. Might not all be attachment-related.
        for control in form.controls:
            if control.name == 'DT':
                print "Attachment found:", control.value
                request2 = form.click()
                try:
                    response2 = mechanize.urlopen(request2)
                    form_url = response2.geturl()
                    if "getfile.asp" in form_url or 'ydocstart.asp' in form_url:
                        data = response2.read()
                        md5 = hashlib.md5(data).hexdigest()
                        scraperwiki.sqlite.save(
                            unique_keys=['session_id', 'dt', 'md5', 'size'],
                            data={'session_id': session_id, 'dt': control.value, 'md5': md5, 'size': len(data)})
                        continue
                except mechanize.HTTPError, response2:
                    print "HTTP-FEHLER :("
                except URLError:
                    pass

for si in range(START_SESSION_ID, END_SESSION_ID):
    print "Getting Sitzung %d" % si
    get_sitzung(si)
    time.sleep(1)
# encoding: utf-8

import scraperwiki
import mechanize
import re
import time
import hashlib
import pprint

"""
Proof of concept for SessionNet 4.4.3 attachment scraping
"""

BASE_URL = "https://secure.stadt-witten.de/session/bis/"
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'scrape-a-ris/0.1')]

START_SESSION_ID = 1270
END_SESSION_ID = 1271

def get_sitzung(id):
    url = BASE_URL + "to0040.asp?__ksinr=%d" % id
    print url
    br.open(url)
    for link in br.links(url_regex=".*kvonr.*"):
        print link.url
        get_vorlage(id, BASE_URL + link.url)
        time.sleep(0.3)

def get_vorlage(session_id, url):
    try:
        response = mechanize.urlopen(mechanize.Request(url))
        #pprint.pprint(response)
    except URLError:
        return
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    for form in forms:
        # All forms are iterated. Might not all be attachment-related.
        for control in form.controls:
            if control.name == 'DT':
                print "Attachment found:", control.value
                request2 = form.click()
                try:
                    response2 = mechanize.urlopen(request2)
                    form_url = response2.geturl()
                    if "getfile.asp" in form_url or 'ydocstart.asp' in form_url:
                        data = response2.read()
                        md5 = hashlib.md5(data).hexdigest()
                        scraperwiki.sqlite.save(
                            unique_keys=['session_id', 'dt', 'md5', 'size'],
                            data={'session_id': session_id, 'dt': control.value, 'md5': md5, 'size': len(data)})
                        continue
                except mechanize.HTTPError, response2:
                    print "HTTP-FEHLER :("
                except URLError:
                    pass

for si in range(START_SESSION_ID, END_SESSION_ID):
    print "Getting Sitzung %d" % si
    get_sitzung(si)
    time.sleep(1)
# encoding: utf-8

import scraperwiki
import mechanize
import re
import time
import hashlib
import pprint

"""
Proof of concept for SessionNet 4.4.3 attachment scraping
"""

BASE_URL = "https://secure.stadt-witten.de/session/bis/"
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'scrape-a-ris/0.1')]

START_SESSION_ID = 1270
END_SESSION_ID = 1271

def get_sitzung(id):
    url = BASE_URL + "to0040.asp?__ksinr=%d" % id
    print url
    br.open(url)
    for link in br.links(url_regex=".*kvonr.*"):
        print link.url
        get_vorlage(id, BASE_URL + link.url)
        time.sleep(0.3)

def get_vorlage(session_id, url):
    try:
        response = mechanize.urlopen(mechanize.Request(url))
        #pprint.pprint(response)
    except URLError:
        return
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    for form in forms:
        # All forms are iterated. Might not all be attachment-related.
        for control in form.controls:
            if control.name == 'DT':
                print "Attachment found:", control.value
                request2 = form.click()
                try:
                    response2 = mechanize.urlopen(request2)
                    form_url = response2.geturl()
                    if "getfile.asp" in form_url or 'ydocstart.asp' in form_url:
                        data = response2.read()
                        md5 = hashlib.md5(data).hexdigest()
                        scraperwiki.sqlite.save(
                            unique_keys=['session_id', 'dt', 'md5', 'size'],
                            data={'session_id': session_id, 'dt': control.value, 'md5': md5, 'size': len(data)})
                        continue
                except mechanize.HTTPError, response2:
                    print "HTTP-FEHLER :("
                except URLError:
                    pass

for si in range(START_SESSION_ID, END_SESSION_ID):
    print "Getting Sitzung %d" % si
    get_sitzung(si)
    time.sleep(1)
