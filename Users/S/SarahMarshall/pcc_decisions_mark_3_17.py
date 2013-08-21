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



def extract_pubdate( pubdate_str ):

    # a lot of (older) pcc cases have no date, only the number of
    # the pcc report in which they were published, which covers a
    # particular time period.
    pcc_reports = {
        # reportnumber: (start_date, end_date),
        1: ( "1/11/1987", "31/1/1988" ),
        2: ( "1/2/1988", "30/4/1988" ),
        3: ( "1/5/1988", "31/7/1988" ),
        4: ( "1/8/1988", "31/10/1988" ),
        5: ( "1/11/1988", "31/1/1989" ),
        6: ( "1/2/1989", "30/4/1989" ),
        7: ( "1/5/1989", "31/7/1989" ),
        8: ( "1/8/1989", "31/10/1989" ),
        9: ( "1/11/1989", "31/1/1990" ),
        10: ( "1/2/1990", "30/4/1990" ),
        11: ( "1/5/1990", "31/7/1990" ),
        12: ( "1/8/1990", "31/10/1990" ),
        13: ( "1/11/1990", "31/1/1991" ),
        14: ( "1/2/1991", "30/4/1991" ),
        15: ( "1/5/1991", "31/7/1991" ),
        16: ( "1/8/1991", "31/10/1991" ),
        17: ( "1/11/1991", "31/1/1992" ),
        18: ( "1/2/1992", "30/4/1992" ),
        19: ( "1/5/1992", "31/7/1992" ),
        20: ( "1/8/1992", "31/10/1992" ),
        21: ( "1/11/1992", "31/1/1993" ),
        22: ( "1/2/1993", "30/4/1993" ),
        23: ( "1/5/1993", "31/7/1993" ),
        24: ( "1/8/1993", "31/10/1993" ),
        25: ( "1/11/1993", "31/1/1994" ),
        26: ( "1/2/1994", "30/4/1994" ),
        27: ( "1/5/1994", "31/7/1994" ),
        28: ( "1/8/1994", "31/10/1994" ),
        29: ( "1/11/1994", "31/1/1995" ),
        30: ( "1/2/1995", "30/4/1995" ),
        31: ( "1/5/1995", "31/7/1995" ),
        32: ( "1/8/1995", "31/10/1995" ),
        33: ( "1/11/1995", "31/1/1996" ),
        34: ( "1/2/1996", "30/4/1996" ),
        35: ( "1/5/1996", "31/7/1996" ),
        36: ( "1/8/1996", "31/10/1996" ),
        37: ( "1/11/1996", "31/1/1997" ),
        38: ( "1/2/1997", "30/4/1997" ),
        39: ( "1/5/1997", "31/7/1997" ),
        40: ( "1/8/1997", "31/10/1997" ),
        41: ( "1/11/1997", "31/1/1998" ),
        42: ( "1/2/1998", "30/4/1998" ),
        43: ( "1/5/1998", "31/7/1998" ),
        44: ( "1/8/1998", "31/10/1998" ),
        45: ( "1/11/1998", "31/1/1999" ),
        46: ( "1/2/1999", "30/4/1999" ),
        47: ( "1/5/1999", "31/7/1999" ),
        48: ( "1/8/1999", "31/10/1999" ),
        49: ( "1/11/1999", "31/1/2000" ),
        50: ( "1/2/2000", "30/4/2000" ),
        51: ( "1/5/2000", "31/7/2000" ),
        52: ( "1/8/2000", "31/10/2000" ),
        53: ( "1/11/2000", "31/1/2001" ),
        54: ( "1/2/2001", "30/4/2001" ),
        55: ( "1/5/2001", "31/7/2001" ),
        56: ( "1/8/2001", "31/10/2001" ),
        57: ( "1/11/2001", "31/1/2002" ),
        58: ( "1/2/2002", "30/4/2002" ),
        59: ( "1/5/2002", "31/7/2002" ),
        60: ( "1/8/2002", "31/10/2002" ),
        61: ( "1/11/2002", "31/1/2003" ),
        62: ( "1/2/2003", "30/4/2003" ),
        63: ( "1/5/2003", "31/7/2003" ),
        64: ( "1/8/2003", "31/10/2003" ),
        65: ( "1/11/2003", "31/1/2004" ),
        66: ( "1/2/2004", "30/4/2004" ),
        67: ( "1/5/2004", "31/7/2004" ),
        68: ( "1/8/2004", "31/10/2004" ),
        69: ( "1/11/2004", "31/1/2005" ),
        70: ( "1/2/2005", "30/4/2005" ),
        71: ( "1/5/2005", "31/10/2005" ),
        72: ( "1/11/2005", "30/4/2006" ),
        73: ( "1/5/2006", "31/10/2006" ),
        74: ( "1/11/2006", "30/4/2007" ),
        75: ( "1/5/2007", "30/9/2007" ),
        76: ( "1/10/2007", "31/3/2008" ),
        77: ( "1/4/2008", "30/9/2008" ),
        78: ( "1/10/2008", "31/3/2009" ),
        79: ( "1/4/2009", "30/9/2009" ),
        80: ( "1/10/2009", "31/12/2009" ),
    }

    # sometimes just a report number eg "75"
    if pubdate_str.isdigit():
        # if case has only a report number, set the publication date to
        # the end of the report period.
        # cheesy, but more useful than no date.
        reportnum = int( pubdate_str )
        pubdate_str = pcc_reports[reportnum][1]
    else:
        # sometimes a report number and an adjudication date, or just some cruft text...
        # eg:
        # '80 Adjudication issued 23/12/09' => "23/12/09"
        # '80 Adjudication issed 18/12/09' => "18/12/09"
        # 'Date published 27/09/2010'
        pat = re.compile( r'(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})', re.IGNORECASE )
        m = pat.search( pubdate_str )
        if m:
            pubdate_str = m.group(1)

    dt = dateutil.parser.parse( pubdate_str, dayfirst=True )  # fuzzy=True
    if dt is None:
        print "BAD: ", pubdate_str 

    return dt

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



