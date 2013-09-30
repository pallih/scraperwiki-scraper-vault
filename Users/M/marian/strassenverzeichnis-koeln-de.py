# coding: utf-8

import scraperwiki
import urllib2
from scrapemark import scrape
import time
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]


strassen = []
strasse_zu_bezirk = {}
strasse_zu_veedel = {}

baseurl = 'http://www.koeln.de/apps/strassen/'
html = urllib2.urlopen(baseurl).read()

veedels = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/veedel/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/bezirk/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = shuffle(bezirke)
for bezirk in bezirke:
    strassen = scrape("""
    <ul class="streets">
    {*
        <li><a href="/apps/strassen/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </ul>
    """, url=baseurl+'bezirk/'+ bezirk['url'])
    rows = []
    for strasse in strassen:
        strasse_zu_bezirk[strasse['name']] = bezirk['name']
        rows.append({'strasse': strasse['name'], 'bezirk': bezirk['name']})
    scraperwiki.sqlite.save(['strasse', 'bezirk'], rows, table_name="swdata")
    time.sleep(3)
# coding: utf-8

import scraperwiki
import urllib2
from scrapemark import scrape
import time
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]


strassen = []
strasse_zu_bezirk = {}
strasse_zu_veedel = {}

baseurl = 'http://www.koeln.de/apps/strassen/'
html = urllib2.urlopen(baseurl).read()

veedels = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/veedel/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/bezirk/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = shuffle(bezirke)
for bezirk in bezirke:
    strassen = scrape("""
    <ul class="streets">
    {*
        <li><a href="/apps/strassen/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </ul>
    """, url=baseurl+'bezirk/'+ bezirk['url'])
    rows = []
    for strasse in strassen:
        strasse_zu_bezirk[strasse['name']] = bezirk['name']
        rows.append({'strasse': strasse['name'], 'bezirk': bezirk['name']})
    scraperwiki.sqlite.save(['strasse', 'bezirk'], rows, table_name="swdata")
    time.sleep(3)
# coding: utf-8

import scraperwiki
import urllib2
from scrapemark import scrape
import time
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]


strassen = []
strasse_zu_bezirk = {}
strasse_zu_veedel = {}

baseurl = 'http://www.koeln.de/apps/strassen/'
html = urllib2.urlopen(baseurl).read()

veedels = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/veedel/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/bezirk/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = shuffle(bezirke)
for bezirk in bezirke:
    strassen = scrape("""
    <ul class="streets">
    {*
        <li><a href="/apps/strassen/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </ul>
    """, url=baseurl+'bezirk/'+ bezirk['url'])
    rows = []
    for strasse in strassen:
        strasse_zu_bezirk[strasse['name']] = bezirk['name']
        rows.append({'strasse': strasse['name'], 'bezirk': bezirk['name']})
    scraperwiki.sqlite.save(['strasse', 'bezirk'], rows, table_name="swdata")
    time.sleep(3)
# coding: utf-8

import scraperwiki
import urllib2
from scrapemark import scrape
import time
import random

def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]


strassen = []
strasse_zu_bezirk = {}
strasse_zu_veedel = {}

baseurl = 'http://www.koeln.de/apps/strassen/'
html = urllib2.urlopen(baseurl).read()

veedels = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/veedel/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = scrape("""
    <table id="navi-bottom">
    {*
        <li><a href="/apps/strassen/bezirk/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </table>
    """, html)

bezirke = shuffle(bezirke)
for bezirk in bezirke:
    strassen = scrape("""
    <ul class="streets">
    {*
        <li><a href="/apps/strassen/{{ [].url }}">{{ [].name }}</a></li>
    *}
    </ul>
    """, url=baseurl+'bezirk/'+ bezirk['url'])
    rows = []
    for strasse in strassen:
        strasse_zu_bezirk[strasse['name']] = bezirk['name']
        rows.append({'strasse': strasse['name'], 'bezirk': bezirk['name']})
    scraperwiki.sqlite.save(['strasse', 'bezirk'], rows, table_name="swdata")
    time.sleep(3)
