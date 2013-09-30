import scraperwiki
import lxml.html
import re
import base64
import random
import sys
import dateutil.parser
import htmlentitydefs
import unicodedata

import json

from pprint import pprint



# output fields:
#
# 'complaint' - description of complaint
# 'clauses_noted' - which PCC clauses were violated
# 'publication' - who the complaint was against
# 'url' - URL of case on PCC site
# 'complainant_name' - who was complaining
# 'decision' - eg "Upheld", "Not Upheld"
# 'adjudication' -
# 'date_published'
# 'report' - which pcc report the descision was published in
# 'resolution'
# 'id' - article id of case on the pcc CMS


valid_fields = set(['complainant_name','publication','url','decision','complaint','adjudication','date_published','clauses_noted','report','resolution','id'])


##
# Removes HTML or XML character references and entities from a text string.
# (from http://effbot.org/zone/re-sub.htm#unescape-html )
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
#
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)



# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""


    # kill comments
    comment_pat = re.compile( r"<!--(.*?)-->", re.DOTALL )
    html = comment_pat.sub( u'', html )

    # An internal "helper for the helper" function: only keep <br> and <p> tags
    def replace_tag(match):
        tag = match.group()
        tagname = tag[1:].lstrip().lower()
        if tagname.startswith('br') or tagname.startswith('p'):
            return tag  # don't replace it
        else:
            return ''   # replace it with nothing, i.e. remove it

    # Remove tags except <br> and <p> tags
    text = re.sub('<.*?>', replace_tag, html)

    # Collapse whitespace to single spaces
    text = ' '.join(text.split())

    # Replace one or more <br|p> tags and any surrounding spaces
    # with two newlines
    text = re.sub('\s*(<.*?>\s*)+', '\n\n', text)

    # convert html entities
    text = unescape( text )

    # Remove whitespace from either end
    text = text.strip()


    return text



def normalise_fieldname(n):
    n = n.lower()
    parts = re.compile('[^\w]+').split(n)
    n = '_'.join(parts)
    assert len(n) < 32
    return n

def extract_article_id(url):
    """ the PCC CMS encodes the article id in the url. Extract it. """
    id_pat = re.compile(r'article=(.*)$')
    m = id_pat.search( url )
    encoded_id = m.group(1)
    article_id = int( base64.urlsafe_b64decode( encoded_id ) )
    return article_id


def scrape( url ):
    """ Scrape an individual case from a page on the PCC Content Management System"""
    #print url

    article_id = extract_article_id(url)
 
    page = scraperwiki.scrape(url)
    
    # Convert to Unicode (handles funny characters like euro signs)
    #page = page.decode('latin-1')
    page = page.decode('windows-1252')


    # grrr... stupid cms...
    if 'OXYBOX - [News System Error]' in page:
        print "SKIP %s (blank page: 'OXYBOX - [News System Error]')" % url
        return None

    # Store the scraping results in data, including the article ID.
    # We'll add fields as we find them.
    data = {'id': article_id}



    # slightly evil regex to make sure we pick up all the text we want...
    # Use <span class="GreyTitle"> to delimit the fields, but that
    # doesn't work for the last field, so we need to use the "Go Back" link instead.
    # (Note the non-consuming (?=....) for the end marker. Without it findall()
    # won't work because the matches will overlap)
    pat = re.compile( '<span class="GreyTitle">(.*?)(?=(?:<span class="GreyTitle">)|(?:<br/><br/><a href="/.*[.]html"><b><< Go Back</b></a>))', re.DOTALL )
        
    for value in pat.findall( page ):
        #print value              
        # fieldname and value always seem to be separated by "</span>"
        fieldname, value = value.split('</span>', 1)

        # Extract the text from the fieldname and value.
        # Discard the colon separator from whichever it ends up in.
        fieldname = gettext(fieldname).rstrip(':')
        value = gettext(value.lstrip(':'))

        fieldname = normalise_fieldname(fieldname)

        # Convert things that look like numbers into numbers
        #if value.isdigit():
        #    value = int(value)


        # Store the data
        data[fieldname] = value
        #print fieldname, ": ", value
  
    data['url'] = url

    pubdate = None

    if "date_published" in data:
        pubdate = extract_pubdate( data['date_published'] )

    if "report" in data:
        if pubdate is None:
            pubdate = extract_pubdate( data['report'] )

        m = re.compile( r'^\s*(\d+)' ).search( data['report'] )
        data['report'] = m.group(1)

    data['date_published'] = pubdate.strftime( '%Y-%m-%d' )

    # name is often a little borked (at least when it first appears on the site)
    data['complainant_name'] = tidy_complainant_name(data['complainant_name'],data['publication'])

    return data


def find_cases():
    case_urls = []
    
    # the "num" field lets us grab links to all cases in one go. Yay!
    num = '20000'
    page = '1'
    search_url = "http://www.pcc.org.uk/advanced_search.html?page=" + page + "&num=" + num + "&publication=x&decision=x&keywords=&cases=on"
    html = scraperwiki.scrape(search_url)
    doc = lxml.html.document_fromstring( html )
    doc.make_links_absolute( search_url )
 
    rows = doc.cssselect( '#content table tr' )[3:]
    for row in rows:
        a = row.cssselect( 'a' )[0]
        case_urls.append( a.get('href') )
    return case_urls


def tidy_complainant_name(name,publication):
    """ handle cases where complainant name has whole case title

    eg http://www.pcc.org.uk/news/index.html?article=NzE3OQ==
    complainant name is: "Resolved - Full Fact v Daily Mail"
    """

    oldname = name

    name = name.replace(u' v ' + publication, u'')
    borkpat =  re.compile( r'^\s*(Resolved|Adjudication|Adjudicated)\s*-\s*', re.IGNORECASE )
    name = borkpat.sub( u'', name )

    if name != oldname:
        print( "TIDY complainant name '%s' => '%s'" % (oldname, name) )
    return name


def sanity_check(data):
    """ make sure don't have any silly unexpected fields creeping in """
    for field,val in data.iteritems():
        assert field in valid_fields


# ----- START -----


TESTING = False

if TESTING:
    case_urls = find_cases()
    case_urls = random.sample(case_urls,30)
    #case_urls = case_urls[0:50]


    # first url is a "OXYBOX News System Error" at time of writing
    #case_urls = [ "http://www.pcc.org.uk/news/index.html?article=MzUwOA==",
    #    "http://www.pcc.org.uk/news/index.html?article=NjY4MA==",
    #    "http://www.pcc.org.uk/cases/adjudicated.html?article=NjYzNQ==",
    #    "http://www.pcc.org.uk/news/index.html?article=NzE3OQ==" ]
    print "TESTING!"
else:
    print "fetching list of cases..."
    case_urls = find_cases()


print "found %d cases" % ( len(case_urls), )

all_fields = set()



errcnt = 0
for case_url in case_urls:
    article_id = extract_article_id(case_url)
    rows = scraperwiki.sqlite.select("id from swdata WHERE id=?", (article_id,), verbose=0)
    if len(rows)>0:
        print "got ", case_url, " already"
        continue

    print "scrape ", case_url, "..."
    try:
        data = scrape( case_url )
        if data is not None:
            sanity_check(data)
            if not TESTING:
                scraperwiki.sqlite.save(['id'], data)
            for f in data.keys():
                all_fields.add(f)
        #pprint(data)

    except Exception, e:
        print "ERROR scraping %s: %s" %( case_url, e.message )
        errcnt = errcnt + 1
        if errcnt>50:
            print "BAILING OUT - too many errors."
            raise

print "all fields: ", all_fields




import scraperwiki
import lxml.html
import re
import base64
import random
import sys
import dateutil.parser
import htmlentitydefs
import unicodedata

import json

from pprint import pprint



# output fields:
#
# 'complaint' - description of complaint
# 'clauses_noted' - which PCC clauses were violated
# 'publication' - who the complaint was against
# 'url' - URL of case on PCC site
# 'complainant_name' - who was complaining
# 'decision' - eg "Upheld", "Not Upheld"
# 'adjudication' -
# 'date_published'
# 'report' - which pcc report the descision was published in
# 'resolution'
# 'id' - article id of case on the pcc CMS


valid_fields = set(['complainant_name','publication','url','decision','complaint','adjudication','date_published','clauses_noted','report','resolution','id'])


##
# Removes HTML or XML character references and entities from a text string.
# (from http://effbot.org/zone/re-sub.htm#unescape-html )
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
#
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)



# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""


    # kill comments
    comment_pat = re.compile( r"<!--(.*?)-->", re.DOTALL )
    html = comment_pat.sub( u'', html )

    # An internal "helper for the helper" function: only keep <br> and <p> tags
    def replace_tag(match):
        tag = match.group()
        tagname = tag[1:].lstrip().lower()
        if tagname.startswith('br') or tagname.startswith('p'):
            return tag  # don't replace it
        else:
            return ''   # replace it with nothing, i.e. remove it

    # Remove tags except <br> and <p> tags
    text = re.sub('<.*?>', replace_tag, html)

    # Collapse whitespace to single spaces
    text = ' '.join(text.split())

    # Replace one or more <br|p> tags and any surrounding spaces
    # with two newlines
    text = re.sub('\s*(<.*?>\s*)+', '\n\n', text)

    # convert html entities
    text = unescape( text )

    # Remove whitespace from either end
    text = text.strip()


    return text



def normalise_fieldname(n):
    n = n.lower()
    parts = re.compile('[^\w]+').split(n)
    n = '_'.join(parts)
    assert len(n) < 32
    return n

def extract_article_id(url):
    """ the PCC CMS encodes the article id in the url. Extract it. """
    id_pat = re.compile(r'article=(.*)$')
    m = id_pat.search( url )
    encoded_id = m.group(1)
    article_id = int( base64.urlsafe_b64decode( encoded_id ) )
    return article_id


def scrape( url ):
    """ Scrape an individual case from a page on the PCC Content Management System"""
    #print url

    article_id = extract_article_id(url)
 
    page = scraperwiki.scrape(url)
    
    # Convert to Unicode (handles funny characters like euro signs)
    #page = page.decode('latin-1')
    page = page.decode('windows-1252')


    # grrr... stupid cms...
    if 'OXYBOX - [News System Error]' in page:
        print "SKIP %s (blank page: 'OXYBOX - [News System Error]')" % url
        return None

    # Store the scraping results in data, including the article ID.
    # We'll add fields as we find them.
    data = {'id': article_id}



    # slightly evil regex to make sure we pick up all the text we want...
    # Use <span class="GreyTitle"> to delimit the fields, but that
    # doesn't work for the last field, so we need to use the "Go Back" link instead.
    # (Note the non-consuming (?=....) for the end marker. Without it findall()
    # won't work because the matches will overlap)
    pat = re.compile( '<span class="GreyTitle">(.*?)(?=(?:<span class="GreyTitle">)|(?:<br/><br/><a href="/.*[.]html"><b><< Go Back</b></a>))', re.DOTALL )
        
    for value in pat.findall( page ):
        #print value              
        # fieldname and value always seem to be separated by "</span>"
        fieldname, value = value.split('</span>', 1)

        # Extract the text from the fieldname and value.
        # Discard the colon separator from whichever it ends up in.
        fieldname = gettext(fieldname).rstrip(':')
        value = gettext(value.lstrip(':'))

        fieldname = normalise_fieldname(fieldname)

        # Convert things that look like numbers into numbers
        #if value.isdigit():
        #    value = int(value)


        # Store the data
        data[fieldname] = value
        #print fieldname, ": ", value
  
    data['url'] = url

    pubdate = None

    if "date_published" in data:
        pubdate = extract_pubdate( data['date_published'] )

    if "report" in data:
        if pubdate is None:
            pubdate = extract_pubdate( data['report'] )

        m = re.compile( r'^\s*(\d+)' ).search( data['report'] )
        data['report'] = m.group(1)

    data['date_published'] = pubdate.strftime( '%Y-%m-%d' )

    # name is often a little borked (at least when it first appears on the site)
    data['complainant_name'] = tidy_complainant_name(data['complainant_name'],data['publication'])

    return data


def find_cases():
    case_urls = []
    
    # the "num" field lets us grab links to all cases in one go. Yay!
    num = '20000'
    page = '1'
    search_url = "http://www.pcc.org.uk/advanced_search.html?page=" + page + "&num=" + num + "&publication=x&decision=x&keywords=&cases=on"
    html = scraperwiki.scrape(search_url)
    doc = lxml.html.document_fromstring( html )
    doc.make_links_absolute( search_url )
 
    rows = doc.cssselect( '#content table tr' )[3:]
    for row in rows:
        a = row.cssselect( 'a' )[0]
        case_urls.append( a.get('href') )
    return case_urls


def tidy_complainant_name(name,publication):
    """ handle cases where complainant name has whole case title

    eg http://www.pcc.org.uk/news/index.html?article=NzE3OQ==
    complainant name is: "Resolved - Full Fact v Daily Mail"
    """

    oldname = name

    name = name.replace(u' v ' + publication, u'')
    borkpat =  re.compile( r'^\s*(Resolved|Adjudication|Adjudicated)\s*-\s*', re.IGNORECASE )
    name = borkpat.sub( u'', name )

    if name != oldname:
        print( "TIDY complainant name '%s' => '%s'" % (oldname, name) )
    return name


def sanity_check(data):
    """ make sure don't have any silly unexpected fields creeping in """
    for field,val in data.iteritems():
        assert field in valid_fields


# ----- START -----


TESTING = False

if TESTING:
    case_urls = find_cases()
    case_urls = random.sample(case_urls,30)
    #case_urls = case_urls[0:50]


    # first url is a "OXYBOX News System Error" at time of writing
    #case_urls = [ "http://www.pcc.org.uk/news/index.html?article=MzUwOA==",
    #    "http://www.pcc.org.uk/news/index.html?article=NjY4MA==",
    #    "http://www.pcc.org.uk/cases/adjudicated.html?article=NjYzNQ==",
    #    "http://www.pcc.org.uk/news/index.html?article=NzE3OQ==" ]
    print "TESTING!"
else:
    print "fetching list of cases..."
    case_urls = find_cases()


print "found %d cases" % ( len(case_urls), )

all_fields = set()



errcnt = 0
for case_url in case_urls:
    article_id = extract_article_id(case_url)
    rows = scraperwiki.sqlite.select("id from swdata WHERE id=?", (article_id,), verbose=0)
    if len(rows)>0:
        print "got ", case_url, " already"
        continue

    print "scrape ", case_url, "..."
    try:
        data = scrape( case_url )
        if data is not None:
            sanity_check(data)
            if not TESTING:
                scraperwiki.sqlite.save(['id'], data)
            for f in data.keys():
                all_fields.add(f)
        #pprint(data)

    except Exception, e:
        print "ERROR scraping %s: %s" %( case_url, e.message )
        errcnt = errcnt + 1
        if errcnt>50:
            print "BAILING OUT - too many errors."
            raise

print "all fields: ", all_fields




