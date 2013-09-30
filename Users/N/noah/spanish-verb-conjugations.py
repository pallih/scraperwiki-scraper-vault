###############################################################################
# Scrape verb conjugations from SpanishDict.com
###############################################################################

import urllib2

import lxml.etree
import lxml.html

has_scraper_wiki = False
try:
    import scraperwiki
    scraperwiki.metadata.save('data_columns', ['Lemma', 'Form', 'Tense', 'Irregular'])
    has_scraper_wiki = True
except ImportError:
    has_scraper_wiki = False

class Conjugation(object):
    def __init__(self, lemma, form, tense=None, irregular=False):
        self.lemma = lemma
        self.form = form
        self.tense = tense
        self.irregular = irregular
    
    def to_tsv(self):
        return '\t'.join([self.lemma, self.form, self.tense or '', str(self.irregular)])
    
    def save(self):
        if has_scraper_wiki:
            scraperwiki.datastore.save(["Lemma", "Form", "Tense"], {
                'Lemma': self.lemma,
                'Form': self.form,
                'Tense': self.tense,
                'Irregular': self.irregular
            })
        else:
            print self.to_tsv()

def read_response(url, retries=3):
    response = None
    for r in range(retries):
        try:
            if has_scraper_wiki:
                response = scraperwiki.scrape(url)
            else:
                response = urllib2.urlopen(url).read()
            break
        except: # No idea what scraperwiki may or may not raise here
            continue
    
    if response is None:
        raise ValueError(
            'No response from "%s" after %d tries' % (url, retries))
    
    return response

def get_tense(e):
    """The tense is in the TR above the current conjugation"""
    # Find the current TR
    parent = e.getparent()
    while parent.tag != 'tr':
        parent = parent.getparent()
    
    # Find the tense in the previous TR
    previous = parent.getprevious()
    tense = previous.cssselect('.conj_subheader')[0].text_content()
    
    return tense

def get_conjugations(lemma):
    url = "http://www.spanishdict.com/conjugate/" + lemma.encode('utf-8')
    html = read_response(url).decode('utf-8')
    root = lxml.html.fromstring(html)
    
    # Get irregular forms
    irregular_forms = set()
    for e in root.cssselect('.conjugations li em'):
        form = e.text_content().strip()
        irregular_forms.add(form)
    
    # Build conjugations list
    conjugations = []
    for e in root.cssselect('.conjugations li'):
        form = e.text_content().strip()
        if form == '-':
            continue
        tense = get_tense(e)
        irregular = form in irregular_forms
        conj = Conjugation(lemma, form, tense, irregular)
        conjugations.append(conj)
    
    # Get gerund and past participle
    for e in root.cssselect('ul.conjugate span.green'):
        tense = e.cssselect('a')[0].text_content().strip()
        form = e.getparent().text_content().replace(tense, '').strip(': ')
        # No indication of irregularity here
        conj = Conjugation(lemma, form, tense, False) 
        conjugations.append(conj)
    
    return conjugations

def get_es_verbs():
    url = 'http://pastebin.com/download.php?i=d0Mrpzbs'
    txt = read_response(url).decode('utf-8')
    return txt.split('\r\n')

def main():
    verbs = get_es_verbs()
    
    # Retrieve current verb from metadata
    current_verb = None
    if has_scraper_wiki:
        current_verb = scraperwiki.metadata.get('current_verb', None)
    
    # Start from current verb
    start = 0
    if current_verb:
        start = verbs.index(current_verb)
    
    print 'scraping conjugations for %d verbs...' % (len(verbs))
    for v in verbs[start:]:
        if has_scraper_wiki:
            scraperwiki.metadata.save('current_verb', v)
        for c in get_conjugations(v):
            c.save()
    
    # Remove current verb from metadata after complete run
    if has_scraper_wiki:
        scraperwiki.metadata.save('current_verb', None)

if __name__ in ('__main__', 'scraper'):
    main()
###############################################################################
# Scrape verb conjugations from SpanishDict.com
###############################################################################

import urllib2

import lxml.etree
import lxml.html

has_scraper_wiki = False
try:
    import scraperwiki
    scraperwiki.metadata.save('data_columns', ['Lemma', 'Form', 'Tense', 'Irregular'])
    has_scraper_wiki = True
except ImportError:
    has_scraper_wiki = False

class Conjugation(object):
    def __init__(self, lemma, form, tense=None, irregular=False):
        self.lemma = lemma
        self.form = form
        self.tense = tense
        self.irregular = irregular
    
    def to_tsv(self):
        return '\t'.join([self.lemma, self.form, self.tense or '', str(self.irregular)])
    
    def save(self):
        if has_scraper_wiki:
            scraperwiki.datastore.save(["Lemma", "Form", "Tense"], {
                'Lemma': self.lemma,
                'Form': self.form,
                'Tense': self.tense,
                'Irregular': self.irregular
            })
        else:
            print self.to_tsv()

def read_response(url, retries=3):
    response = None
    for r in range(retries):
        try:
            if has_scraper_wiki:
                response = scraperwiki.scrape(url)
            else:
                response = urllib2.urlopen(url).read()
            break
        except: # No idea what scraperwiki may or may not raise here
            continue
    
    if response is None:
        raise ValueError(
            'No response from "%s" after %d tries' % (url, retries))
    
    return response

def get_tense(e):
    """The tense is in the TR above the current conjugation"""
    # Find the current TR
    parent = e.getparent()
    while parent.tag != 'tr':
        parent = parent.getparent()
    
    # Find the tense in the previous TR
    previous = parent.getprevious()
    tense = previous.cssselect('.conj_subheader')[0].text_content()
    
    return tense

def get_conjugations(lemma):
    url = "http://www.spanishdict.com/conjugate/" + lemma.encode('utf-8')
    html = read_response(url).decode('utf-8')
    root = lxml.html.fromstring(html)
    
    # Get irregular forms
    irregular_forms = set()
    for e in root.cssselect('.conjugations li em'):
        form = e.text_content().strip()
        irregular_forms.add(form)
    
    # Build conjugations list
    conjugations = []
    for e in root.cssselect('.conjugations li'):
        form = e.text_content().strip()
        if form == '-':
            continue
        tense = get_tense(e)
        irregular = form in irregular_forms
        conj = Conjugation(lemma, form, tense, irregular)
        conjugations.append(conj)
    
    # Get gerund and past participle
    for e in root.cssselect('ul.conjugate span.green'):
        tense = e.cssselect('a')[0].text_content().strip()
        form = e.getparent().text_content().replace(tense, '').strip(': ')
        # No indication of irregularity here
        conj = Conjugation(lemma, form, tense, False) 
        conjugations.append(conj)
    
    return conjugations

def get_es_verbs():
    url = 'http://pastebin.com/download.php?i=d0Mrpzbs'
    txt = read_response(url).decode('utf-8')
    return txt.split('\r\n')

def main():
    verbs = get_es_verbs()
    
    # Retrieve current verb from metadata
    current_verb = None
    if has_scraper_wiki:
        current_verb = scraperwiki.metadata.get('current_verb', None)
    
    # Start from current verb
    start = 0
    if current_verb:
        start = verbs.index(current_verb)
    
    print 'scraping conjugations for %d verbs...' % (len(verbs))
    for v in verbs[start:]:
        if has_scraper_wiki:
            scraperwiki.metadata.save('current_verb', v)
        for c in get_conjugations(v):
            c.save()
    
    # Remove current verb from metadata after complete run
    if has_scraper_wiki:
        scraperwiki.metadata.save('current_verb', None)

if __name__ in ('__main__', 'scraper'):
    main()
