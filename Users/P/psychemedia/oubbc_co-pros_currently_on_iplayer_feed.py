import scraperwiki
from lxml import etree
from datetime import datetime

scraperwiki.sqlite.attach( 'ou_bbc_co-pros_on_iplayer' )
q = '* FROM "bbcOUcoPros" WHERE strftime("%s",`expires`)>strftime("%s","now")'
data = scraperwiki.sqlite.select(q)

description = {"seriesTitle": ("string", "Series"),"progID": ("string", "Episode"),"short_synopsis":("string","About"),"title": ("string", "View episode on iPlayer"), "availability":("string","Availability"),"expires": ("string", "Expires"), "ouTitle":("string","OU title"),"ouURI": ("string", "OU URI"),"ouContent": ("string", "OU description"),"ouLinkTitle": ("string", "OU Link"),"seriesID":("string","Series ID")}


#hacked out of https://scraperwiki.com/editor/raw/utility_library
#I really should lern how to use that library properly
import time
from pytz import timezone

RFC3339_DATE = "%Y-%m-%dT%H:%M:%SZ"
RFC822_DATE = "%a, %d %b %Y %H:%M:%S %z"
TZ = timezone('Europe/London')

all_atom_fields = { # default map from data fields to ATOM, to be overridden
        'title': 'title',
        'subtitle': 'description',
        'link': 'link',
        'id': 'id',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'content': 'description',
            'link': 'link',
            'id': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }

all_rss_fields = { # default map from data fields to RSS, to be overridden
        'title': 'title',
        'description': 'description',
        'link': 'link',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'description': 'description',
            'link': 'link',
            'guid': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }
# return valid string/unicode if not null, otherwise empty string
def vstr(s):
    if s:
        try:
            return unicode(s)
        except UnicodeDecodeError:
            return str(s)
    else:
        return u''


def toAtom(data):
    exit(-1)
    #still working on this
    scraperwiki.utils.httpresponseheader("Content-Type", "application/atom+xml")
    ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
    NSMAP = { None: ATOM_NAMESPACE }
    feed_type = 'atom'
    root = etree.Element('feed', nsmap=NSMAP)
    pubdate = datetime.now(TZ).strftime(RFC3339_DATE)
    branch = etree.SubElement(root, 'updated')
    branch.text = vstr(pubdate)
    branch = etree.SubElement(root, 'title')
    branch.text = "OU/BBC Co-Pros Currently on iPlayer"
    branch = etree.SubElement(root, 'title')
    branch.text = "OU/BBC Co-Pros Currently on iPlayer"
    branch = etree.SubElement(root, 'link')
    branch.set("href", vstr('http://www.open.ac.uk/openlearn/whats-on'))
    branch.set("rel", "self")

    for row in data:
        branch = etree.SubElement(root, "entry")
        no_date = True
        if no_date:
            leaf = etree.SubElement(branch, 'updated')
            leaf.text = vstr(pubdate)
        leaf = etree.SubElement(branch, 'title')
        leaf.text = vstr(data['seriesTitle']+': '+data['title'])
        leaf = etree.SubElement(branch, 'link')
        leaf.set("href", vstr('http://www.bbc.co.uk/programmes/'+data['progID']))
        if k == 'summary' or k == 'content':
            leaf.set("type", "html")
        leaf = etree.SubElement(branch, 'author')

def toRSS(data):
    feed_type = 'rss'
    root = etree.Element('rss')
    root.set("version", "2.0")
    branch = etree.SubElement(root, "channel")
    twig = etree.SubElement(branch, 'title')
    twig.text = vstr('OU/BBC Co-Pros Currently on iPlayer')
    twig = etree.SubElement(branch, 'link')
    twig.text = vstr('http://www.open.ac.uk/openlearn/whats-on')
    twig = etree.SubElement(branch, 'description')
    twig.text = vstr('Feed of programmes co-produced by The Open University and the BBC currently on iPlayer')
    pubdate = datetime.now(TZ).strftime(RFC822_DATE)
    twig = etree.SubElement(branch, 'pubDate')
    twig.text = vstr(pubdate)
    for row in data:
        twig = etree.SubElement(branch, "item")
        leaf = etree.SubElement(twig, 'title')
        leaf.text =vstr(row['seriesTitle']+': '+row['title'])
        leaf = etree.SubElement(twig, 'link')
        leaf.text = vstr('http://www.bbc.co.uk/programmes/'+row['progID'])
        leaf = etree.SubElement(twig, 'description')
        leaf.text = vstr('<div>Avaiability: '+row['availability']+'</div><div>Expires: '+row['expires']+'</div><div>'+row['short_synopsis']+'</div>')
        leaf = etree.SubElement(twig, 'pubDate')
        leaf.text = vstr(pubdate)
    return root

#print data
root = toRSS(data)
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
#scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
print etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)import scraperwiki
from lxml import etree
from datetime import datetime

scraperwiki.sqlite.attach( 'ou_bbc_co-pros_on_iplayer' )
q = '* FROM "bbcOUcoPros" WHERE strftime("%s",`expires`)>strftime("%s","now")'
data = scraperwiki.sqlite.select(q)

description = {"seriesTitle": ("string", "Series"),"progID": ("string", "Episode"),"short_synopsis":("string","About"),"title": ("string", "View episode on iPlayer"), "availability":("string","Availability"),"expires": ("string", "Expires"), "ouTitle":("string","OU title"),"ouURI": ("string", "OU URI"),"ouContent": ("string", "OU description"),"ouLinkTitle": ("string", "OU Link"),"seriesID":("string","Series ID")}


#hacked out of https://scraperwiki.com/editor/raw/utility_library
#I really should lern how to use that library properly
import time
from pytz import timezone

RFC3339_DATE = "%Y-%m-%dT%H:%M:%SZ"
RFC822_DATE = "%a, %d %b %Y %H:%M:%S %z"
TZ = timezone('Europe/London')

all_atom_fields = { # default map from data fields to ATOM, to be overridden
        'title': 'title',
        'subtitle': 'description',
        'link': 'link',
        'id': 'id',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'content': 'description',
            'link': 'link',
            'id': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }

all_rss_fields = { # default map from data fields to RSS, to be overridden
        'title': 'title',
        'description': 'description',
        'link': 'link',
        'items': 'items',
        'item': 'item',
        'sub_item': {
            'title': 'title',
            'description': 'description',
            'link': 'link',
            'guid': 'id',
            },
        'geo_item': {
            'point': 'point'
            }
        }
# return valid string/unicode if not null, otherwise empty string
def vstr(s):
    if s:
        try:
            return unicode(s)
        except UnicodeDecodeError:
            return str(s)
    else:
        return u''


def toAtom(data):
    exit(-1)
    #still working on this
    scraperwiki.utils.httpresponseheader("Content-Type", "application/atom+xml")
    ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
    NSMAP = { None: ATOM_NAMESPACE }
    feed_type = 'atom'
    root = etree.Element('feed', nsmap=NSMAP)
    pubdate = datetime.now(TZ).strftime(RFC3339_DATE)
    branch = etree.SubElement(root, 'updated')
    branch.text = vstr(pubdate)
    branch = etree.SubElement(root, 'title')
    branch.text = "OU/BBC Co-Pros Currently on iPlayer"
    branch = etree.SubElement(root, 'title')
    branch.text = "OU/BBC Co-Pros Currently on iPlayer"
    branch = etree.SubElement(root, 'link')
    branch.set("href", vstr('http://www.open.ac.uk/openlearn/whats-on'))
    branch.set("rel", "self")

    for row in data:
        branch = etree.SubElement(root, "entry")
        no_date = True
        if no_date:
            leaf = etree.SubElement(branch, 'updated')
            leaf.text = vstr(pubdate)
        leaf = etree.SubElement(branch, 'title')
        leaf.text = vstr(data['seriesTitle']+': '+data['title'])
        leaf = etree.SubElement(branch, 'link')
        leaf.set("href", vstr('http://www.bbc.co.uk/programmes/'+data['progID']))
        if k == 'summary' or k == 'content':
            leaf.set("type", "html")
        leaf = etree.SubElement(branch, 'author')

def toRSS(data):
    feed_type = 'rss'
    root = etree.Element('rss')
    root.set("version", "2.0")
    branch = etree.SubElement(root, "channel")
    twig = etree.SubElement(branch, 'title')
    twig.text = vstr('OU/BBC Co-Pros Currently on iPlayer')
    twig = etree.SubElement(branch, 'link')
    twig.text = vstr('http://www.open.ac.uk/openlearn/whats-on')
    twig = etree.SubElement(branch, 'description')
    twig.text = vstr('Feed of programmes co-produced by The Open University and the BBC currently on iPlayer')
    pubdate = datetime.now(TZ).strftime(RFC822_DATE)
    twig = etree.SubElement(branch, 'pubDate')
    twig.text = vstr(pubdate)
    for row in data:
        twig = etree.SubElement(branch, "item")
        leaf = etree.SubElement(twig, 'title')
        leaf.text =vstr(row['seriesTitle']+': '+row['title'])
        leaf = etree.SubElement(twig, 'link')
        leaf.text = vstr('http://www.bbc.co.uk/programmes/'+row['progID'])
        leaf = etree.SubElement(twig, 'description')
        leaf.text = vstr('<div>Avaiability: '+row['availability']+'</div><div>Expires: '+row['expires']+'</div><div>'+row['short_synopsis']+'</div>')
        leaf = etree.SubElement(twig, 'pubDate')
        leaf.text = vstr(pubdate)
    return root

#print data
root = toRSS(data)
scraperwiki.utils.httpresponseheader("Content-Type", "application/rss+xml")
#scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
print etree.tostring(root, encoding="utf-8", xml_declaration=True, pretty_print=True)