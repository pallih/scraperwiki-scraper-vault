import scraperwiki
import cgi
import os
import lxml.etree as etree
import lxml.html
from lxml import html
import re
import itertools
import json
import urllib

scraperwiki.utils.httpresponseheader("Content-Type", "text/html")

print '<h1>FOIwiki ScraperSync</h1>'

args = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

if 'mode' not in args:
    print """
        <form>
            <select name="mode">
                <option value="update" selected="selected">Update</option>
                <option value="new">Create new</option>
            </select>
            <input name="page" value="Whole of Government Accounts" />
            from
            <input name="name" value="thing" />
            <input type="submit" />
        </form>
    """
    exit(0)

mode = args['mode']
destpage = args['page']
destpage = re.sub(r' ', '_', destpage)
sourcescraper = None

def header():
    if mode == 'update':
        p = etree.Element('p')
        p.text = "Synching from scraper to FOIwiki page "
        a2 = etree.SubElement(p, 'a', href = "http://foiwiki.com/foiwiki/index.php/%s" % urllib.quote(destpage))
        a2.text = re.sub('_', ' ', destpage)
        a2.tail = '.'
    else:
        p = etree.Element('p')
        p.text = "Constructing a new page from scraper "
        a1 = etree.SubElement(p, 'a', href = "http://scraperwiki.com/scrapers/%s/" % sourcescraper)
        a1.text = sourcescraper
        a1.tail = '.'
    return p

class ItemParseError(Exception):
    pass

class item(object):
    """
    Abstract class for items in all kinds of list (and potentially tables too).
    """
    def __init__(self, line=None, name=None):
        self.deleted = False; self.defunct = False; self.wdtklink = None
        self.wdtkreq = False; self.notes = None
        if line != None: self.parse(line)
        if name != None: self.name = name
    def __str__(self):
        ret = self.name
        if self.wdtklink != None: ret = "{{WDTK|%s|%s}}" % (ret, self.wdtklink)
        elif self.wdtkreq and not self.defunct: ret = "{{WDTKreq|%s}}" % (ret)
        if self.deleted: ret = "<strike>%s</strike>" % (ret)
        elif self.defunct: ret = "{{gone|%s}}" % (ret)
        return ret
    def parsewithnotes(self, t):
        # The presence of notes is really a part of the specific format,
        # but tweaking the parser to allow for it is tricky.
        while True:
            m = re.match(r"<strike>(.*)</strike> *(.*)", t)
            if m:
                self.deleted = True
                t = m.group(1)
                if m.group(2) != "": self.notes = m.group(2)
                continue
            m = re.match(r"{{(gone|WDTKreq|WDTKreq_listed)\|([^|}]*)}} *(.*)", t)
            if m:
                if m.group(1) == "gone":
                    self.defunct = True
                else:
                    self.wdtkreq = True
                t = m.group(2)
                if m.group(3) != "": self.notes = m.group(3)
                continue
            m = re.match(r"{{WDTK\|([^|}]*)\|([^|}]*)}} *(.*)", t)
            if m:
                self.wdtklink = m.group(2)
                t = m.group(1)
                if m.group(3) != "": self.notes = m.group(2)
                continue
            break
        m = re.match(r"(.*?)  (.*)", t)
        if m:
            t = m.group(1)
            self.notes = m.group(2)
        self.name = t
    def WDTKtagp(self, tag):
        """ Does this body have the specified tag in WDTK? """
        if self.wdtklink == None: return False
        if scraperwiki.sqlite.select('1 FROM wdtk.tags WHERE `URL name` = ? AND `tag` = ?',
             (self.wdtklink, tag)):
            return True
        return False        
    def WDTKguess(self):
        '''
        Try to find the WhatDoTheyKnow body corresponding to a particular name.
        '''
        name = self.name
        # Try looking for a precise name match and a match for the url_name.
        # Also try either adding or removing "The" from the start.
        url_name = name.lower()
        url_name = re.sub(r'[^a-z0-9_ -]','',url_name)
        url_name = re.sub(r'[^a-z0-9]+','_',url_name)
        the_url_name = url_name[4:] if url_name.startswith('the_') else 'the_' + url_name
        the_name = name[4:] if name.startswith('The ') else 'The ' + name
        result = scraperwiki.sqlite.select('`URL name` FROM wdtk.swdata WHERE `URL name` IN (?, ?) OR `Name` IN (?, ?)',
            (url_name, the_url_name, name, the_name))
        if result:
            self.wdtklink = result[0]['URL name']
    def WDTKsync(self):
        """ Update object with WDTK data. """
        if self.wdtklink == None: self.WDTKguess()
        if self.wdtklink != None:
            self.defunct = self.WDTKtagp('defunct')

class listitem(item):
    """A listitem represents an item in a simple list on FOIwiki."""
    def __repr__(self):
        return "listitem(" + repr(unicode(self)) + ")"
    def __str__(self):
        # The canonical format of a list item is "* ", followed
        # by the name of the body possibly wrapped in structure,
        # followed by two spaces and then free text.
        ret = item.__str__(self)
        if self.notes != None: ret = "%s  %s" % (ret, self.notes)
        return "* " + ret
    def parse(self, t):
        (t, n) = re.subn(r"^\* *", "", t);
        if n == 0: raise ItemParseError()
        self.parsewithnotes(t)

class taglistitem(item):
    """A taglistitem represents an item in a list where the first word of
    each item is a tag of some sort."""
    def __repr__(self):
        return "listitem(" + repr(unicode(self)) + ")"
    def __init__(self, *pos, **kw):
        self.tag = None
        item.__init__(self, *pos, **kw)
    def __str__(self):
        # The canonical format of a list item is "* ", followed
        # by the tag, followed by the name of the body possibly wrapped in structure,
        # followed by two spaces and then free text.
        ret = item.__str__(self)
        if self.notes != None: ret = "%s  %s" % (ret, self.notes)
        return "* %s %s" % (self.tag, ret)
    def parse(self, t):
        (t, n) = re.subn(r"^\* *", "", t);
        if n == 0: raise ItemParseError()
        m = re.match(r"([^ ]+) +(.*)", t)
        if m == None: raise ItemParseError()
        self.tag = m.group(1)
        self.parsewithnotes(m.group(2))

formats = { 'list': listitem, 'taglist': taglistitem }
formatitem = listitem

scraperwiki.sqlite.attach('whatdotheyknow_bodies', 'wdtk')

if mode == 'new' and 'name' in args:
    sourcescraper = args['name']
    scraperwiki.sqlite.attach(sourcescraper, 'scraper')

print lxml.html.tostring(header())

seen = set()

if mode == 'update':
    # FOIwiki claims to be producing XHTML, but it lies to us.
    page = scraperwiki.scrape('http://foiwiki.com/foiwiki/index.php?title=%s&action=edit' % urllib.quote(destpage))
    doc = html.fromstring(page)
    text = doc.xpath('string(//textarea)')
    print '<h1>Proposed amendments</h1>'
    # Make an iterator ourselves so we can use it for several loops
    wikilines = iter(text.split("\n"))
else:
    print '<h1>Proposed new list</h1>'
    wikilines = []

out = etree.Element('pre')
out.text = ''

# Search for ScraperSync start line
for l in wikilines:
    match = re.match(r'<!-- *ScraperSync +start(.*)-->', l)
    out.text += l + "\n"
    if match:
        params = json.loads(match.group(1))
        if 'scraper' in params:
            sourcescraper = params['scraper']
            scraperwiki.sqlite.attach(sourcescraper, 'scraper')
        if 'format' in params:
            formatitem = formats[params['format']]
        break
else:
    if mode == 'update':
        print '<h1>No ScraperSync start line found</h1>'
        exit(0)

items = []
# Process lines in the list itself
for l in wikilines:
    match = re.match(r'<!-- *ScraperSync +end(.*)-->', l)
    if match:
        wikilines = itertools.chain([l], wikilines)
        break
    try:
        obj = formatitem(l)
        obj.WDTKsync()
        if sourcescraper != None:
            if scraperwiki.sqlite.select('1 FROM scraper.swdata WHERE name = ?', obj.name):
                seen.add(obj.name)
            else:
                obj.deleted = True
        items.append(obj)
    except:
        items.append(l)

# Add missing items
if sourcescraper != None:
    data = scraperwiki.sqlite.select('name FROM scraper.swdata')
    for i in data:
        if i['name'] not in seen:
            obj = formatitem(name = i['name'])
            obj.WDTKsync()
            items.append(obj)

if params.get('sort') == 'name':
    items.sort(key = lambda x: x.name.lower())

for i in items:
    out.text += "%s\n" % (i)

# Copy through any lines from after the list
for l in wikilines:
    out.text += l + "\n"

print lxml.html.tostring(out)
