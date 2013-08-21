# Need to compare scraped against http://www.nice.org.uk/guidance/cg/published/index.jsp?p=off 
# to make sure we have all of the data
import scraperwiki
import datetime
import lxml.html
import copy
import re
import time
import sys

cgonly = scraperwiki.sqlite.select("code,url,title,category,subcategory from cgonly")
for c in cgonly:
    scraperwiki.sqlite.save(['code','category'], c, table_name='data')    
    
sys.exit(0)

#scraperwiki.sqlite.execute('delete from data where code="CG127" and category is null')
#sys.exit(0)

#data = dict(code="CG127",url="http://www.nice.org.uk/nicemedia/live/13561/56015/56015.pdf",
#title="Hypertension",category="Cardiovascular",subcategory="")
#scraperwiki.sqlite.save(['code','category'], data, table_name='data')

#data = dict(code="CG150", url="http://www.nice.org.uk/nicemedia/live/13901/60854/60854.pdf",
#title="Headaches", category="Central nervous system", subcategory="")
#scraperwiki.sqlite.save(['code','category'], data, table_name='data')

def split_anchor(a):
    return a.text_content(), a.attrib.get('href')

def pages_count(page_obj):
    """ Return a list of all pages """
    div = page_obj.cssselect('.pagingBottomSearch div')
    if not div:
        return 0
    return len(div) - 1



def process_sub_categories(page, parent_name):
    links = page.cssselect('div#nptMainContentLeft ul li a')
    for link in links: 
        nm,url = split_anchor( link )
        nm = nm[0:nm.find('(')].strip()
        nm = '%s_%s' % (parent_name, nm, )
        if not nm in categories:
            categories[nm] = []
        process_category( nm, url,startat=1 )

def process_category(name, url,startat=2):
    data = scraperwiki.scrape( url )
    page = lxml.html.fromstring( data )
    cnt = pages_count( page )
    if cnt == 0:
        process_sub_categories( page, name )
        categories[name] = []
        return 
    # We'll risk 20 and then stop when we get 0 links
    for x in range(startat, 20): 
        categories[name].append( "%s&page=%d" % (url,x) )

def add_page( category, name, pageurl ):
    cat, subcat = category,""
    if '_' in category:
        cat,_,subcat = category.rpartition('_')
    print ' ---- Category',cat
    print ' ---- Subcategory', subcat
    try:
        data = scraperwiki.scrape( pageurl )
    except:
        print "++ A bad URL " + pageurl
        return False

    obj = lxml.html.fromstring( data )
    try:
        print pageurl
        print data
        name,url = split_anchor( obj.cssselect('#hyperlink')[0] )
    except:
        print '++ Could not find NICE Guidance, look for full?'
        return False

    print ' ----',name
    try:
        code, title = re.match('(CG\d+)\s(.*):', name).groups(0)
    except:
        title = name[0:name.find(':')]
        code = pageurl[28:]
        code = code[0:code.find('/')]
        print 'Alternate', code, title
    url = 'http://www.nice.org.uk%s' % url
    data = dict( code=code, category=cat, subcategory=subcat,title=title, url=url, when=datetime.datetime.now().isoformat() )
    scraperwiki.sqlite.save(['code','category'], data, table_name='data')
    return True

categories = {}
sub_categories = {}

content = scraperwiki.scrape( 'http://guidance.nice.org.uk/index.jsp?action=find' )
print content

page = lxml.html.fromstring( scraperwiki.scrape( 'http://guidance.nice.org.uk/index.jsp?action=find' ) )
ul = page.cssselect('ul.termsCloud')[0]
lks = ul.cssselect('li a')
for l in lks:
    nm,link = split_anchor(l)
    categories[nm] = [link]

tmp = copy.deepcopy(categories)
for k,v in tmp.iteritems():
    print 'Processing category', k
    process_category(k,  v[0] )


print 'Starting actual work now'
for k,v in categories.iteritems():
    print 'Processing category - ', k
    links = categories[k]
    print '-- There are %d pages to check' % len(links)
    print links
    pages_to_read = []
    found = []
    bail = False
    for link in links:
        if bail:
            break
        print '-- Checking page', link
        data = scraperwiki.scrape( link )
        p = lxml.html.fromstring( data )
        #anchors = p.cssselect(".formats ul li a")
        anchors = p.cssselect("a")

        print '-- Found %d anchors' % len(anchors)
        for a in anchors:
            nm,url = split_anchor( a )
            m = re.match(".*CG(\d+).*", nm )
            if m:
                nm = m.groups()[0]
                if nm in found:
                    bail = True
                    break
                found.append(nm)
                print "*", nm
                url = "http://guidance.nice.org.uk/CG%s/NICEGuidance/pdf/English" % nm
                if not add_page( k, nm, url ):
                    url = "http://guidance.nice.org.uk/CG%s/Guidance/pdf/English" % nm
                    add_page( k, nm, url )
                


# Need to compare scraped against http://www.nice.org.uk/guidance/cg/published/index.jsp?p=off 
# to make sure we have all of the data
import scraperwiki
import datetime
import lxml.html
import copy
import re
import time
import sys

cgonly = scraperwiki.sqlite.select("code,url,title,category,subcategory from cgonly")
for c in cgonly:
    scraperwiki.sqlite.save(['code','category'], c, table_name='data')    
    
sys.exit(0)

#scraperwiki.sqlite.execute('delete from data where code="CG127" and category is null')
#sys.exit(0)

#data = dict(code="CG127",url="http://www.nice.org.uk/nicemedia/live/13561/56015/56015.pdf",
#title="Hypertension",category="Cardiovascular",subcategory="")
#scraperwiki.sqlite.save(['code','category'], data, table_name='data')

#data = dict(code="CG150", url="http://www.nice.org.uk/nicemedia/live/13901/60854/60854.pdf",
#title="Headaches", category="Central nervous system", subcategory="")
#scraperwiki.sqlite.save(['code','category'], data, table_name='data')

def split_anchor(a):
    return a.text_content(), a.attrib.get('href')

def pages_count(page_obj):
    """ Return a list of all pages """
    div = page_obj.cssselect('.pagingBottomSearch div')
    if not div:
        return 0
    return len(div) - 1



def process_sub_categories(page, parent_name):
    links = page.cssselect('div#nptMainContentLeft ul li a')
    for link in links: 
        nm,url = split_anchor( link )
        nm = nm[0:nm.find('(')].strip()
        nm = '%s_%s' % (parent_name, nm, )
        if not nm in categories:
            categories[nm] = []
        process_category( nm, url,startat=1 )

def process_category(name, url,startat=2):
    data = scraperwiki.scrape( url )
    page = lxml.html.fromstring( data )
    cnt = pages_count( page )
    if cnt == 0:
        process_sub_categories( page, name )
        categories[name] = []
        return 
    # We'll risk 20 and then stop when we get 0 links
    for x in range(startat, 20): 
        categories[name].append( "%s&page=%d" % (url,x) )

def add_page( category, name, pageurl ):
    cat, subcat = category,""
    if '_' in category:
        cat,_,subcat = category.rpartition('_')
    print ' ---- Category',cat
    print ' ---- Subcategory', subcat
    try:
        data = scraperwiki.scrape( pageurl )
    except:
        print "++ A bad URL " + pageurl
        return False

    obj = lxml.html.fromstring( data )
    try:
        print pageurl
        print data
        name,url = split_anchor( obj.cssselect('#hyperlink')[0] )
    except:
        print '++ Could not find NICE Guidance, look for full?'
        return False

    print ' ----',name
    try:
        code, title = re.match('(CG\d+)\s(.*):', name).groups(0)
    except:
        title = name[0:name.find(':')]
        code = pageurl[28:]
        code = code[0:code.find('/')]
        print 'Alternate', code, title
    url = 'http://www.nice.org.uk%s' % url
    data = dict( code=code, category=cat, subcategory=subcat,title=title, url=url, when=datetime.datetime.now().isoformat() )
    scraperwiki.sqlite.save(['code','category'], data, table_name='data')
    return True

categories = {}
sub_categories = {}

content = scraperwiki.scrape( 'http://guidance.nice.org.uk/index.jsp?action=find' )
print content

page = lxml.html.fromstring( scraperwiki.scrape( 'http://guidance.nice.org.uk/index.jsp?action=find' ) )
ul = page.cssselect('ul.termsCloud')[0]
lks = ul.cssselect('li a')
for l in lks:
    nm,link = split_anchor(l)
    categories[nm] = [link]

tmp = copy.deepcopy(categories)
for k,v in tmp.iteritems():
    print 'Processing category', k
    process_category(k,  v[0] )


print 'Starting actual work now'
for k,v in categories.iteritems():
    print 'Processing category - ', k
    links = categories[k]
    print '-- There are %d pages to check' % len(links)
    print links
    pages_to_read = []
    found = []
    bail = False
    for link in links:
        if bail:
            break
        print '-- Checking page', link
        data = scraperwiki.scrape( link )
        p = lxml.html.fromstring( data )
        #anchors = p.cssselect(".formats ul li a")
        anchors = p.cssselect("a")

        print '-- Found %d anchors' % len(anchors)
        for a in anchors:
            nm,url = split_anchor( a )
            m = re.match(".*CG(\d+).*", nm )
            if m:
                nm = m.groups()[0]
                if nm in found:
                    bail = True
                    break
                found.append(nm)
                print "*", nm
                url = "http://guidance.nice.org.uk/CG%s/NICEGuidance/pdf/English" % nm
                if not add_page( k, nm, url ):
                    url = "http://guidance.nice.org.uk/CG%s/Guidance/pdf/English" % nm
                    add_page( k, nm, url )
                


