import scraperwiki
import mechanize
import lxml.html
import urllib
import urllib2
import re
import string

# Convert key name into something that SQLite can cope with
re_sqlite_key = re.compile ('[a-zA-Z0-9_\- ]+$')
def key_sanitise (raw):
    out = list()
    for c in raw:
        if re_sqlite_key.match (c):
            out.append (c)
        #elif c == ' ':
            #out.append ('_')
    return ''.join(out)

def val_sanitise (raw):
    return raw

# Scrape one school
def scrape_urn (urn):
    base = 'http://www.education.gov.uk/edubase/establishment/'
    pages = ['general', 'school-characterisics', 'links', 'sen', 'pru', 'quality-indicators', 'communications', 'census-data', 'regional-indicators']
    # NB typo in "characteristics" is Edubase's!

    # Scrape one page (recursive)
    # The thinking behind this is that all data are presented as <th>var</th><td>val</td> type blocks 
    def scrape_urn_tags (tree, out):
        if (tree.tag == 'th') or (tree.tag == 'td'):
            if not (tree.text is None):
                return (tree.tag, tree.text)
        var = ''
        val = ''
        for el in tree:
            (d_tag, d_text) = scrape_urn_tags (el, out)
            if (d_tag == 'th'):
                var = key_sanitise(d_text)
                if (val != ''):
                    out[var] = val
                    var = ''
                    val = ''
            elif (d_tag == 'td'):
                val = val_sanitise(d_text)
                if (var != ''):
                    out[var] = val 
                    var = ''
                    val = ''
        return (None, None)

    for page in pages:
        outdict = {}
        data = scraperwiki.scrape (base+page+'.xhtml?urn='+str(urn))
        root = lxml.html.fromstring (data)
        scrape_urn_tags (root, outdict)
        if ('Local Authority' in outdict):
            # Process to extract 3 digit DfE LA code
            outdict['DfE LA Code'] = outdict['Local Authority'][:3]
            outdict['Local Authority'] = outdict['Local Authority'][4:]
        outdict['Unique Reference Number'] = urn # Needed to tie all the tables together (URN is given only in general.xml)
        scraperwiki.sqlite.save (unique_keys=['Unique Reference Number'], data=outdict, table_name=page, verbose=0)

def checkpoint_get ():
    global state, point, runs
    state = scraperwiki.sqlite.get_var ('state', 'Start', verbose=0)
    point = scraperwiki.sqlite.get_var ('point', 0, verbose=0)
    runs = scraperwiki.sqlite.get_var ('runs', 0, verbose=0)

def checkpoint_set (newstate, newpoint):
    global state, point
    scraperwiki.sqlite.save_var ('state', newstate, verbose=0)
    scraperwiki.sqlite.save_var ('point', newpoint, verbose=0)
    state = newstate
    point = newpoint

checkpoint_get()
scraperwiki.sqlite.save_var ('runs', runs+1, verbose=0)
print 'Scraper state is %s (%d)' % (state, point)

if (state == 'Start'):
    # (1) Set up the initial search
    # AIUI, mechanize is robots aware and Edubase don't seem to have an objection
    url = 'http://www.education.gov.uk/edubase/search.xhtml?clear=true'
    br = mechanize.Browser(factory=mechanize.RobustFactory()) 
    br.open (url)
    br.select_form (nr=0)
    br.form['changes.townLocalityPostcode.value'] = ''
    br.form['changes.type.codes'] = ['1', '2', '3', '4', '5', '6', '9', '10', '11'] # Academies -> Welsh Schools
    br.form['changes.status.codes'] = ['1', '2', '3', '4'] # Closed, Open, Proposed to Close, Proposed to Open
    #br.form['changeLASubset'] = ['All'] #FIXME: England and Wales
    br.submit()

    # (2) Build database of URNs
    try:
        if point > 0:
            br.select_form (nr=1)
            br.form['integerValue'] = str(point)
            br.submit()
        while True:
            print "Processing page %d" % (point)
            for l in br.links(url_regex="summary.xhtml.urn="):
                if (l.url[-6:].isdigit()):
                    scraperwiki.sqlite.save (unique_keys=['Unique Reference Number'], data={'Unique Reference Number':l.url[-6:]}, table_name='edubase2', verbose=0)
    
            try:
                br.follow_link (text_regex='Next')
                url = br.geturl()
                point = int(url[url.rfind('=')+1:])
                checkpoint_set ('Start', point)
            except Exception: #FIXME: is there a more specific exception for br.follow_link()?
                break
    
        checkpoint_set ('Fetch', 0)
    except scraperwiki.CPUTimeExceededError:
        checkpoint_set ('Start', point)

#if (state == 'Fetch'):

# (3) Scrape all search results
if (state == 'Fetch'):
    # Must be ordered and must be >= (not >), to ensure total retrieval of whatever last URN was
    res = scraperwiki.sqlite.select ('* FROM edubase2 WHERE [Unique Reference Number] >= %d ORDER BY [Unique Reference Number] ASC' % (point), verbose=0)
    try:
        for row in res:
            urn = int(row['Unique Reference Number'])
            scrape_urn (urn)
            checkpoint_set ('Fetch', urn)
        checkpoint_set ('Postproc', 0)
    except scraperwiki.CPUTimeExceededError:
        checkpoint_set ('Fetch', urn)

# (4) Postprocessing
if (state == 'Postproc'):
    #FIXME: update DfE number/ESTAB in edubase2 table
    checkpoint_set ('Postproc', 0)
    #checkpoint_set ('Start', 0)

