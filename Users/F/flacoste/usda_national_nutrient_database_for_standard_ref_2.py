import lxml.html, re
from base64 import b64decode, b64encode
from collections import deque
from functools import reduce
from hashlib import sha512
from itertools import chain, ifilter, imap, izip, product, repeat
from operator import add, and_, eq
from scraperwiki import datastore, sqlite
from urllib2 import URLError, urlopen
from urlparse import urlunsplit


scheme='http'
host = 'www.ars.usda.gov'
path = '/Services/docs.htm'
query = 'docid=8964'
links_url = urlunsplit((scheme, host, path, query, '')) 
file_suffix = '.txt'
newline = '\r\n'
cell_delimiter = '^'
string_quotes = '~'

# http://www.ars.usda.gov/SP2UserFiles/Place/12354500/Data/SR24/sr24_doc.pdf
files = {
#         'DATA_SRC' : (('DataSrc_ID',),                          ('Authors',     'Title',        'Year',         'Journal',      'Vol_City',
#                                                                 'Issue_State',  'Start_Page',   'End_Page')),
         'DATA_SRC' : ((),                                       ('DataSrc_ID',  'Authors',      'Title',        'Year',         'Journal',
                                                                  'Vol_City',    'Issue_State',  'Start_Page',   'End_Page')),
         'DATSRCLN' : (('NDB_No',    'Nutr_No',  'DataSrc_ID'),  ()),
         'DERIV_CD' : (('Deriv_Cd',),                            ('Deriv_Desc',)),
         'FD_GROUP' : (('FdGrp_Cd',),                            ('FdGrp_Desc',)),
         'FOOD_DES' : (('NDB_No',),                              ('FdGrp_Cd',    'Long_Desc',    'Shrt_Desc',    'ComName',      'ManufacName',
                                                                  'Survey',      'Ref_desc',     'Refuse',       'SciName',      'N_Factor',     
                                                                  'Pro_Factor',  'Fat_Factor',   'CHO_Factor')),                                                        
         'FOOTNOTE' : ((),                                       ('NDB_No',      'Footnt_No',    'Footnt_Typ',   'Nutr_No',      'Footnt_Txt')),
         'LANGDESC' : (('Factor_Code',),                         ('Description',)),
#        'LANGUAL'  : (('NDB_No',),                              ('Factor_Code',)),
         'LANGUAL'  : ((),                                       ('NDB_No',      'Factor_Code',)), 
         'NUTR_DEF' : (('Nutr_No',),                             ('Units',       'Tagname',      'NutrDesc',     'Num_Dec',      'SR_Order')),
         'NUT_DATA' : (('NDB_No',    'Nutr_No'),                 ('Nutr_Val',    'Num_Data_Pts', 'Std_Error',    'Src_Cd',       'Deriv_Cd',
                                                                  'Ref_NDB_No',  'Add_Nutr_Mark','Num_Studies',  'Min',          'Max',
                                                                  'DF',          'Low_EB',       'Up_EB',        'Stat_cmt',     'AddMod_Date',
                                                                  'CC')),
         'SRC_CD'   : (('Src_Cd',),                              ('SrcCd_Desc',)),
         'WEIGHT'   : (('NDB_No',    'Seq'),                     ('Amount',      'Msre_Desc',    'Gm_Wgt',       'Num_Data_Pts', 'Std_Dev'))
        }

class DataError(Exception):
    pass

class LinkError(Exception):
    pass

def join(items):
    return ','.join(items)

def columns(name):
    return files[name][0] + files[name][1]

def primary_key(name):
    return files[name][0]

sqlite.execute('CREATE TABLE IF NOT EXISTS swvariables (file TEXT PRIMARY KEY, position INTEGER, length INTEGER, hash TEXT)')
for name in files:
    sqlite.execute('INSERT OR IGNORE INTO swvariables (file,position) VALUES (?,0)', name)
    cols = join(columns(name))
    if primary_key(name):
        cols = join((cols, ' PRIMARY KEY (%s)' % join(primary_key(name))))
    sqlite.execute('CREATE TABLE IF NOT EXISTS %s (%s)' % (name, cols))


def isquoted(s, q):
    return len(s) >= 2 * len(q) and s.startswith(q) and s.endswith(q)

#def rmap(value, functions):
#    return (function(value) for function in functions)
   
def process_cell(cell):
    cell = unicode(cell, errors='replace')
    return cell[1:-1] if isquoted(cell, string_quotes) else cell
    #return cell[1:-1] if reduce(and_, rmap(string_quotes, cell.startswith, cell.endswith)) else cell

def save_row(name, row):
    try:
        row = tuple(row)
        sqlite.execute('INSERT INTO %s VALUES (%s)' % (name, join(repeat('?', len(columns(name))))), row, verbose=0)
    except sqlite.SqliteError, e:
        print e
        print row
        raise DataError

def delete_table(name):
    sqlite.execute('UPDATE swvariables SET position=0,length=NULL,hash=NULL WHERE file=?', name)
    #sqlite.execute('DELETE FROM ' + name)
    sqlite.execute('DROP TABLE ' + name)
    sqlite.commit()

def replay_hash(data, hash):
    hash_object = sha512()
    for line in data:
        hash_object.update(line)
    if hash != hash_object.digest():
        raise DataError
    return hash_object

def save_line(name, line, hash):
    hash.update(line)
    save_row(name, imap(process_cell, line[:-2].split(cell_delimiter)))
    sqlite.execute('UPDATE swvariables SET position=position+?,hash=? WHERE file=?', (len(line), b64encode(hash.digest()), name), verbose=0)
    sqlite.commit()

def star(f):
    return lambda x: f(*x)

class links(object):
    links = {}
    def __init__(self, file_names, file_suffix, url):
        self.url = url
        self.file_names = file_names
        self.file_suffix = file_suffix
    def __iter__(self):
        return self.filter_links(self.find_links(self.url))
    def find_links(self, url):
        return (a.attrib['href'] for a in lxml.html.parse(urlopen(url)).iterfind('.//a[@href]'))
    def filter_links(self, links):
        return (link for name, link in ifilter(star(self.check_link), product(self.file_names,  links)))
    def check_link(self, name, link):
        if link.endswith(name + self.file_suffix):
            if name in self.links:
                if self.links[name] == link:
                    return False
                elif self.links[name] != link:
                    raise LinkError
            self.links[name] = link
            return True

def readlines(f, newline, size=None):
    if size:
        for line in readlines(f, newline):
            size -= len(line)         
            if size < 0:
                print "Size < 0"
                raise DataError
            yield line
            if size == 0:
                break
    else:
        line = ''
        for s in f:
            line += s
            while line:
                head, sep, tail = line.partition(newline)
                if tail:
                    yield head + sep
                    line = tail
                else:
                    if sep:
                        yield line
                        line = ''
                    else:
                        line = head
                    break
        if line:
            yield line    

"""
        def mend_broken_lines(f):
            partitions = tuple(((newline[:i], newline[i:]) for i in xrange(-1, -len(newline), -1)))
            line = []
            for s in f:
                
                    
"""
"""
import errno, socket
    def __init__(self):
        self.socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
    def connect(host, port):
        ret = socket.connect_ex((host, port))
        if ret == errno.EALREADY:
            select
            yield
        elif ret != 0  
            raise socket.error(ret)
    def send(s)
        while i:
            select
            sent = self.socket.send(s)
            i -= sent
    def recv()
        self.socket.recv_into_into(buffer)
        while i:
            select
            sent = self.socket.send(s)
            i -= sent

    def GET(host, path):
        s = 'GET %s HTTP/1.1\r\nHost: %s\r\n\r\n'
        send(s)
        i = len(s)
               
"""
def save_files():
    file_info = sqlite.execute('SELECT file,position,length,hash FROM swvariables ORDER BY position==length,position,RANDOM()')['data']
    file_links = links(imap(lambda x: x[0], file_info), file_suffix, links_url)
    for link, info in izip(file_links, file_info):
        name, position, length, hash = info
        print link, name, position, length, hash
        try:
            save_file(link, name, position, length, hash)
        except URLError:
            pass

def save_file(link, name, position, length, hash):
    f = urlopen(urlunsplit((scheme, host, link, '', '')))
    content_length = long(f.headers['Content-Length'])
    try:
        if position and length and hash and length == content_length and position <= length:
            print 'Checking hash'
            hash_object = replay_hash(readlines(f, newline, position), b64decode(hash))
            print 'Hash OK'
            if position == length:
                print 'File OK'
                return
        elif position == 0 and length == hash == None:
            print 'Starting fresh'
            position, length, hash_object = (0, content_length, sha512())
            sqlite.execute('UPDATE swvariables SET length=? WHERE file=?', (length, name))
        else:
            print "Save error"
            raise DataError
        for line in readlines(f, newline, content_length - position):
            save_line(name, line, hash_object)
        sqlite.commit()
        print 'All OK'
    except DataError:
        delete_table(name)
        print 'DataError'

try:
    save_files()  
except URLError:
    pass
except Exception, e:
    print e
    sqlite.commit()