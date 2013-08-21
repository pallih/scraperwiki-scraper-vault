# -*- coding: latin-1 -*-

import scraperwiki
import lxml.html
import mechanize
import datetime
import string

# common lib

def get_var(var):
    return scraperwiki.sqlite.get_var(var)

def save_var(var, val):
    scraperwiki.sqlite.save_var(var, val)

def get_date(): 
    return datetime.date.today().strftime('%Y-%m-%d')

def save_data(data):
    scraperwiki.sqlite.save(unique_keys=['site_phys_id'], data=data)

def load_page(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

# mechanize methods
br = None
def br_init():
    global br
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)   # no robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br

# backwords compatible alias
def br_get():
    return br_init()

def br_load_page(url):
    if br == None:
        br_init()
    resp = br.open(url)
    html = resp.read()
    return lxml.html.fromstring(html)

def br_submit_form(form, ctrl_dic):
    if br == None:
        br_init()
    if type(form) is int:
        br.select_form(nr=form)
    else:
        br.select_form(form)
    br.set_all_readonly(False)    # allow everything to be written to
    for ctrl in ctrl_dic:
        br[ctrl] = ctrl_dic[ctrl]
    resp = br.submit()
    html = resp.read()
    #print html
    return lxml.html.fromstring(html)

def br_back():
    br.back()

# single node text
def get_node_text(node, css, index=0):
    nodes = node.cssselect(css)
    if index >= len(nodes):
        return ''
    vals = nodes[index] \
                .text_content() \
                .encode('utf-8') \
                .replace("’", "'") \
                .strip() \
                .split('\n')
    vals = [x.strip() for x in vals]
    return string.join(vals, '|')

def log_complete():
    scraperwiki.sqlite.save_var('done', datetime.datetime.now())
