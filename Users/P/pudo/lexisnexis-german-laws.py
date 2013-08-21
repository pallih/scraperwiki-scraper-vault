from urlparse import urlparse, parse_qs
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup, NavigableString, BeautifulStoneSoup, Comment
import json 

import scraperwiki

class Section(object):
    
    def __init__(self, doc, section_id):
        self.doc = doc
        self.section_id = section_id
        
    
    def load(self):
        print "Section", self.section_id
        soup = self.doc.url_soup(part=self.section_id)
        self.title = soup.findAll('meta', {'name': 'keywords'})[0].get('content')
        self.short_title = soup.findAll('span', {'class': 'ev_zaehlung'})[0].string
        self.type = soup.findAll('span', {'class': 'gesetz_type'})[0].string
        self.type = self.type.replace('(', '').replace(')', '').strip()
        self.path = soup.findAll('a', {'name': 'hidden_gliederung_pfad'})[0].string
        path_parts = self.path.split('/', 4)
        if len(path_parts) > 3:
            self.chapter = path_parts[4]
        else: 
            self.chapter = None
        self.chapter = self.chapter.strip('/ ')
        
        titles = soup.findAll('span', {'class': 'ev_ueberschrift'})
        if len(titles):
            self.section_title = titles[0].string
        else: 
            self.section_title = None
                    
        if (not self.title) or (not len(self.title)):
            self.title = self.short_title
        self.body = self.doc.clean_body(soup.findAll('div', {'class': 'gesetz_body'})[0])
        #print self.path.split('/')
        # _, _, self.level, self.short_title, self.chapter_title, self.norm_title, _ = self.path.split('/', 5)
        #print self.section_title
        #print len(self.short_title), "BODY", len(self.body)
    
    def to_dict(self):
        d = {'title': self.title, 
             'short_title': self.short_title,
             'section_title': self.section_title,
             'chapters': self.chapter.split('/'),
             'path': [p for p in self.path.split('/') if len(p)],
             'body': self.body,
             'type': self.type,
             'doc_id': self.doc.doc_id,
             'section_id': self.section_id}
        return d
    

class Document(object):
        
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.parts = dict()
        self.sections = None
        self.is_loaded = False
    
    def take_tag(self, body, tag):
        for _tag in body.findAll(tag):
            index = _tag.parent.contents.index(_tag)
            for child in _tag.contents:
                child.extract()
                _tag.parent.insert(index, child)
            _tag.extract()
    
    def del_tag(self, body, tag):
        for _tag in body.findAll(tag):
            _tag.extract()
    
    def clean_body(self, body):
        cs = body.findAll(text=lambda t:isinstance(t, Comment))
        [c.extract() for c in cs]
        self.take_tag(body, 'a')         
        self.del_tag(body, 'table')
        self.del_tag(body, 'sup')
        return unicode(body)
       
    def url_for(self, part=1, version=None, full=False):
        xid = str(self.doc_id)
        if part is not None:
            xid += ',' + str(part)
        if version is not None:
            xid += ',' + str(version)
        url = "http://www.lexsoft.de/lexisnexis/justizportal_nrw.cgi?templateID=document&xid=%s" % xid
        if full:
            url += "&task=chose_fliesstext"
        return url
        
    def url_text(self, part=1, version=None, full=False):
        #cache_dir = "out/html/lexisnexis-%s" % self.doc_id
        #if not os.path.isdir(cache_dir):
        #    os.makedirs(cache_dir)
        #cache_name = os.path.join(cache_dir, "c-%s-%s-%s.html" % (part, version, full))
        #if os.path.exists(cache_name):
        #    statinfo = os.stat(cache_name)
        #    cache_mintime = time() - (14 * 84600)
        #    if statinfo.st_mtime > cache_mintime:
        #        print "Reading cache", cache_name
        #        fp = file(cache_name, 'r')
        #        text = fp.read()
        #        fp.close()
        #        return text
        return scraperwiki.scrape(self.url_for(part=part, version=version, full=full))
        #fh = urlopen()
        #text = fh.read()
        #fh.close()
        #fc = file(cache_name, 'w')
        #fc.write(text)
        #fc.close()
        #return text 
        
    def url_soup(self, part=1, version=None, full=False):
        text = self.url_text(part=part, version=version, full=full)
        #soup = BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        soup = BeautifulSoup(text, convertEntities=BeautifulSoup.HTML_ENTITIES)
        return soup
        
    def find_parts(self, soup):
        #doc_table = soup.findAll('table', {'class': 'doc_table gesetz_tfe_table'})[0]
        for tree_doc in soup.findAll('li', {'class': 'tree_doc'}):
            doklink = tree_doc.findAll('a')[0]
            href = doklink.get('href')
            path, query = href.split('?')
            query = parse_qs(query)
            doc_id, part = query.get('xid')[0].split(',')
            part = part.split('#')
            if int(doc_id) == self.doc_id:
                self.parts[int(part[0])] = None
                
    def load_sections(self):
        if self.sections is None:
            self.sections = []
            section_ids = sorted(self.parts.keys())
            if 1 in section_ids:
                section_ids.remove(1)
            for section_id in section_ids:
                section = Section(self, section_id)
                section.load()
                self.sections.append(section)
        
    def load(self):
        if self.is_loaded:
            return
        print "-" * 72
        soup = self.url_soup()
        self.find_parts(soup)
        self.title = soup.findAll('meta', {'name': 'keywords'})[0].get('content')
        self.copyright = soup.findAll('meta', {'name': 'copyright'})[0].get('content')
        self.language = soup.findAll('meta', {'name': 'Content-Language'})[0].get('content')
        cs = soup.findAll('span', {'class': 'gesetz_normueberschrift'})[0].contents
        cs = [c for c in cs if isinstance(c, NavigableString) and len(c.strip())]
        self.path = soup.findAll('a', {'name': 'hidden_gliederung_pfad'})[0].string
        _, _, self.level, self.short_title, _ = self.path.split('/', 4)
        self.full_title = u" ".join(cs)
        self.body = self.clean_body(soup.findAll('div', {'class': 'gesetz_body'})[0])
        print self.full_title.encode('utf-8')
        #if len(cs) > 1:
        #    self.abbr = cs[1].replace('(', '').replace(')', '').strip()
        #else:
        #    self.abbr = self.short_title
        self.abbr = self.title.split(' - ')[0].strip()
        print self.abbr.encode('utf-8')
        print self.level.encode('utf-8')
        print self.doc_id, sorted(self.parts.keys())
        self.load_sections()
        self.is_loaded = True
        
    def to_dict(self):
        if not self.is_loaded:
            self.load()
        d = {'short_title': self.short_title,
             'title': self.title,
             'abbr': self.abbr,
             'level': self.level,
             'doc_id': self.doc_id,
             'full_title': self.full_title,
             'path': [p for p in self.path.split('/') if len(p)],
             'body': self.body,
             'copyright': self.copyright,
             'language': self.language,
             'parts': self.parts,
             'sections': [s.to_dict() for s in self.sections]}
        return d
        
        
    @classmethod
    def from_xid(cls, xid):
        xid_parts = xid.split(",")
        if not len(xid_parts): 
            return None
        doc_id = int(xid_parts[0])
        doc = cls(doc_id)
        if len(xid_parts) > 1:
            part = int(xid_parts[1])
            if len(xid_parts) > 2:
                version = int(xid_parts[2])
                doc.parts[part] = version
            else:
                doc.parts[part] = None
        return doc
    

def parse_search_pages():
    page = 0
    step = 10
    seen = []
    search_url = "http://www.lexsoft.de/lexisnexis/justizportal_nrw.cgi?templateID=suche&hitRangeBegin=%s&hitRangeEnd=%s"
    while True:
        range_begin = page * step
        range_end = range_begin + (step - 1)
        url = search_url % (range_begin, range_end)
        conn = urlopen(url)
        soup = BeautifulSoup(conn.read())
        results = soup.findAll('h3', {'class': 'hit_title'})
        for result in results:
            href = result.contents[1].get('href')
            path, query = href.split('?')
            query = parse_qs(query)
            xid = query.get('xid')[0]
            doc_id, rest = xid.split(',', 1)
            if doc_id in seen: 
                continue
            seen.append(doc_id)
            doc = Document.from_xid(xid)
            doc.load()
            scraperwiki.datastore.save(unique_keys=['doc_id'], data=doc.to_dict())
            #fh = codecs.open("out/lexisnexis-%s.js" % doc_id, 'w', 'utf-8')
            #_json = json.dumps(doc.to_dict(),  ensure_ascii=False, indent=2, encoding='utf-8')
            #fh.write(_json)
            #fh.close()
        conn.close()
        page += 1

parse_search_pages()

