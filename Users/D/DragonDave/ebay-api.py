import os, sys, re
import string, StringIO, base64
import yaml, pycurl, urllib
from types import DictType, ListType

from xml.dom.minidom import parseString, Node
from BeautifulSoup import BeautifulStoneSoup
from types import DictType 

import xml.etree.ElementTree as ET

class object_dict(dict):
    """object view of dict, you can 
    >>> a = object_dict()
    >>> a.fish = 'fish'
    >>> a['fish']
    'fish'
    >>> a['water'] = 'water'
    >>> a.water
    'water'
    >>> a.test = {'value': 1}
    >>> a.test2 = object_dict({'name': 'test2', 'value': 2})
    >>> a.test, a.test2.name, a.test2.value
    (1, 'test2', 2)
    """
    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        
        d = self.__getitem__(item)
        
        if isinstance(d, dict) and 'value' in d and len(d) == 1:
            return d['value']
        else:
            return d
    
        # if value is the only key in object, you can omit it
            
    def __setattr__(self, item, value):
        self.__setitem__(item, value)

    def getvalue(self, item, value=None):
        return self.get(item, {}).get('value', value)

class xml2dict(object):

    def __init__(self):
        pass

    def _parse_node(self, node):
        node_tree = object_dict()
        # Save attrs and text, hope there will not be a child with same name
        if node.text:
            node_tree.value = node.text
        for (k,v) in node.attrib.items():
            k,v = self._namespace_split(k, object_dict({'value':v}))
            node_tree[k] = v
        #Save childrens
        for child in node.getchildren():
            tag, tree = self._namespace_split(child.tag, self._parse_node(child))
            if  tag not in node_tree: # the first time, so store it in dict
                node_tree[tag] = tree
                continue
            old = node_tree[tag]
            if not isinstance(old, list):
                node_tree.pop(tag)
                node_tree[tag] = [old] # multi times, so change old dict to a list       
            node_tree[tag].append(tree) # add the new one      

        return node_tree

    def _namespace_split(self, tag, value):
        """
           Split the tag  '{http://cs.sfsu.edu/csc867/myscheduler}patients'
             ns = http://cs.sfsu.edu/csc867/myscheduler
             name = patients
        """
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            value.namespace, tag = result.groups()    

        return (tag,value)

    def parse(self, file):
        """parse a xml file to a dict"""
        f = open(file, 'r')
        return self.fromstring(f.read()) 

    def fromstring(self, s):
        """parse a string"""
        t = ET.fromstring(s)
        root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
        return object_dict({root_tag: root_tree})


# Basic conversation goal here is converting a dict to an object allowing
# more comfortable access. `Struct()` and `make_struct()` are used to archive
# this goal.
# See http://stackoverflow.com/questions/1305532/convert-python-dict-to-object for the inital Idea
#
# The reasoning for this is the observation that we ferry arround hundreds of dicts via JSON
# and accessing them as `obj['key']` is tiresome after some time. `obj.key` is much nicer.
class Struct(object):
    """Emulate a cross over between a dict() and an object()."""
    def __init__(self, entries, default=None, nodefault=False):
        # ensure all keys are strings and nothing else
        entries = dict([(str(x), y) for x, y in entries.items()])
        self.__dict__.update(entries)
        self.__default = default
        self.__nodefault = nodefault

    def __getattr__(self, name):
        """Emulate Object access.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.a
        'b'
        >>> obj.foobar
        'c'

        `hasattr` results in strange behaviour if you give a default value. This might change in the future.
        >>> hasattr(obj, 'a')
        True
        >>> hasattr(obj, 'foobar')
        True
        """
        if name.startswith('_'):
            # copy expects __deepcopy__, __getnewargs__ to raise AttributeError
            # see http://groups.google.com/group/comp.lang.python/browse_thread/thread/6ac8a11de4e2526f/
            # e76b9fbb1b2ee171?#e76b9fbb1b2ee171
            raise AttributeError("'<Struct>' object has no attribute '%s'" % name)
        if self.__nodefault:
            raise AttributeError("'<Struct>' object has no attribute '%s'" % name)
        return self.__default

    def __getitem__(self, key):
        """Emulate dict like access.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj['a']
        'b'

        While the standard dict access via [key] uses the default given when creating the struct,
        access via get(), results in None for keys not set. This might be considered a bug and
        should change in the future.
        >>> obj['foobar']
        'c'
        >>> obj.get('foobar')
        'c'
        """
        # warnings.warn("dict_accss[foo] on a Struct, use object_access.foo instead",
        #                DeprecationWarning, stacklevel=2)
        if self.__nodefault:
            return self.__dict__[key]
        return self.__dict__.get(key, self.__default)

    def get(self, key, default=None):
        """Emulate dictionary access.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.get('a')
        'b'
        >>> obj.get('foobar')
        'c'
        """
        if key in self.__dict__:
            return self.__dict__[key]
        if not self.__nodefault:
            return self.__default
        return default

    def __contains__(self, item):
        """Emulate dict 'in' functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> 'a' in obj
        True
        >>> 'foobar' in obj
        False
        """
        return item in self.__dict__

    def __nonzero__(self):
        """Returns whether the instance evaluates to False"""
        return bool(self.items())

    def has_key(self, item):
        """Emulate dict.has_key() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.has_key('a')
        True
        >>> obj.has_key('foobar')
        False
        """
        return item in self

    def items(self):
        """Emulate dict.items() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.items()
        [('a', 'b')]
        """
        return [(k, v) for (k, v) in self.__dict__.items() if not k.startswith('_Struct__')]

    def keys(self):
        """Emulate dict.keys() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.keys()
        ['a']
        """
        return [k for (k, _v) in self.__dict__.items() if not k.startswith('_Struct__')]

    def values(self):
        """Emulate dict.values() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.values()
        ['b']
        """
        return [v for (k, v) in self.__dict__.items() if not k.startswith('_Struct__')]

    def __repr__(self):
        return "<Struct: %r>" % dict(self.items())

    def as_dict(self):
        """Return a dict representing the content of this struct."""
        return self.__dict__


def make_struct(obj, default=None, nodefault=False):
    """Converts a dict to an object, leaves objects untouched.

    Someting like obj.vars() = dict() - Read Only!

    >>> obj = make_struct(dict(foo='bar'))
    >>> obj.foo
    'bar'

    `make_struct` leaves objects alone.
    >>> class MyObj(object): pass
    >>> data = MyObj()
    >>> data.foo = 'bar'
    >>> obj = make_struct(data)
    >>> obj.foo
    'bar'

    `make_struct` also is idempotent
    >>> obj = make_struct(make_struct(dict(foo='bar')))
    >>> obj.foo
    'bar'

    `make_struct` recursively handles dicts and lists of dicts
    >>> obj = make_struct(dict(foo=dict(bar='baz')))
    >>> obj.foo.bar
    'baz'

    >>> obj = make_struct([dict(foo='baz')])
    >>> obj
    [<Struct: {'foo': 'baz'}>]
    >>> obj[0].foo
    'baz'

    >>> obj = make_struct(dict(foo=dict(bar=dict(baz='end'))))
    >>> obj.foo.bar.baz
    'end'

    >>> obj = make_struct(dict(foo=[dict(bar='baz')]))
    >>> obj.foo[0].bar
    'baz'
    >>> obj.items()
    [('foo', [<Struct: {'bar': 'baz'}>])]
    """
    if type(obj) == type(Struct):
        return obj
    if (not hasattr(obj, '__dict__')) and hasattr(obj, 'iterkeys'):
        # this should be a dict
        struc = Struct(obj, default, nodefault)
        # handle recursive sub-dicts
        for key, val in obj.items():
            setattr(struc, key, make_struct(val, default, nodefault))
        return struc
    elif hasattr(obj, '__delslice__') and hasattr(obj, '__getitem__'):
        #
        return [make_struct(v, default, nodefault) for v in obj]
    else:
        return obj


# Code is based on http://code.activestate.com/recipes/573463/
def _convert_dict_to_xml_recurse(parent, dictitem, listnames):
    """Helper Function for XML conversion."""
    # we can't convert bare lists
    assert not isinstance(dictitem, list)

    if isinstance(dictitem, dict):
        for (tag, child) in sorted(dictitem.iteritems()):
            if isinstance(child, list):
                # iterate through the array and convert
                listelem = ET.Element(None)
                listelem2 = ET.Element(tag)
                parent.append(listelem)
                for listchild in child:
                    elem = ET.Element(listnames.get(tag, listelem2.tag))
                    listelem.append(elem)
                    _convert_dict_to_xml_recurse(elem, listchild, listnames)
            else:
                elem = ET.Element(tag)
                parent.append(elem)
                _convert_dict_to_xml_recurse(elem, child, listnames)
    elif not dictitem is None:
        parent.text = unicode(dictitem)


def dict2et(xmldict, roottag='data', listnames=None):
    """Converts a dict to an ElementTree.

    Converts a dictionary to an XML ElementTree Element::
    """

    if not listnames:
        listnames = {}
    root = ET.Element(roottag)
    _convert_dict_to_xml_recurse(root, xmldict, listnames)
    return root


def list2et(xmllist, root, elementname):
    """Converts a list to an ElementTree.

        See also dict2et()
    """

    basexml = dict2et({root: xmllist}, 'xml', listnames={root: elementname})
    return basexml.find(root)


def dict2xml(datadict, roottag='TRASHME', listnames=None, pretty=False):
    """
    Converts a dictionary to an UTF-8 encoded XML string.
    See also dict2et()
    """
    root = dict2et(datadict, roottag, listnames)
    
    xml = to_string(root, pretty=pretty)
    return xml.replace('<%s>' % roottag, '').replace('</%s>' % roottag, '')
    
def list2xml(datalist, roottag, elementname, pretty=False):
    """Converts a list to an UTF-8 encoded XML string.

    See also dict2et()
    """
    root = list2et(datalist, roottag, elementname)
    return to_string(root, pretty=pretty)


def to_string(root, encoding='utf-8', pretty=False):
    """Converts an ElementTree to a string"""

    if pretty:
        indent(root)

    tree = ET.ElementTree(root)
    fileobj = StringIO.StringIO()
    #fileobj.write('<?xml version="1.0" encoding="%s"?>' % encoding)
    if pretty:
        fileobj.write('\n')
    tree.write(fileobj, 'utf-8')
    return fileobj.getvalue()


# From http://effbot.org/zone/element-lib.htm
# prettyprint: Prints a tree with each node indented according to its depth. This is
# done by first indenting the tree (see below), and then serializing it as usual.
# indent: Adds whitespace to the tree, so that saving it as usual results in a prettyprinted tree.
# in-place prettyprint formatter

def indent(elem, level=0):
    """XML prettyprint: Prints a tree with each node indented according to its depth."""
    i = "\n" + level * " "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent(child, level + 1)
        if child:
            if not child.tail or not child.tail.strip():
                child.tail = i
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def test():
    """Simple selftest."""

    data = {"guid": "3104247-7",
            "menge": 7,
            "artnr": "14695",
            "batchnr": "3104247"}
    xmlstr = dict2xml(data, roottag='warenzugang')
    assert xmlstr == ('<?xml version="1.0" encoding="utf-8"?><warenzugang><artnr>14695</artnr>'
                      '<batchnr>3104247</batchnr><guid>3104247-7</guid><menge>7</menge></warenzugang>')

    data = {"kommiauftragsnr": 2103839,
     "anliefertermin": "2009-11-25",
     "fixtermin": True,
     "prioritaet": 7,
     "info_kunde": "Besuch H. Gerlach",
     "auftragsnr": 1025575,
     "kundenname": "Ute Zweihaus 400424990",
     "kundennr": "21548",
     "name1": "Uwe Zweihaus",
     "name2": "400424990",
     "name3": "",
     u"strasse": u"Bahnhofstr. 2",
     "land": "DE",
     "plz": "42499",
     "ort": u"Hucksenwagen",
     "positionen": [{"menge": 12,
                     "artnr": "14640/XL",
                     "posnr": 1},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3}],
     "versandeinweisungen": [{"guid": "2103839-XalE",
                              "bezeichner": "avisierung48h",
                              "anweisung": "48h vor Anlieferung unter 0900-LOGISTIK avisieren"},
                             {"guid": "2103839-GuTi",
                              "bezeichner": "abpackern140",
                              "anweisung": u"Paletten hochstens auf 140 cm Packen"}]
    }

    xmlstr = dict2xml(data, roottag='kommiauftrag')

    data = {"kommiauftragsnr": 2103839,
     "positionen": [{"menge": 4,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "23455326543222553"},
                    {"menge": 8,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "43255634634653546"},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2,
                     "nve": "43255634634653546"},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3,
                     "nve": "23455326543222553"}],
     "nves": [{"nve": "23455326543222553",
               "gewicht": 28256,
               "art": "paket"},
              {"nve": "43255634634653546",
               "gewicht": 28256,
                "art": "paket"}]}

    xmlstr = dict2xml(data, roottag='rueckmeldung')
    print xmlstr


VERSION = (0, 1, 6)


def get_version():
    version = '%s.%s.%s' % (VERSION[0], VERSION[1], VERSION[2])
    return version

__version__ = get_version()       

def nodeText(node):
    rc = []

    if hasattr(node, 'childNodes'):
        for cn in node.childNodes:
            if cn.nodeType == cn.TEXT_NODE:
                rc.append(cn.data)
            elif cn.nodeType == cn.CDATA_SECTION_NODE:
                rc.append(cn.data)    
        
    return ''.join(rc)

def tag(name, value):
    return "<%s>%s</%s>" % ( name, value, name )

class ebaybase(object):
    
    def __init__(self, debug=False, method='GET', proxy_host=None, timeout=20, proxy_port=80, **kwargs):                
        self.verb       = None
        self.debug      = debug
        self.method     = method
        self.timeout    = timeout
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port 
        self.spooled_calls = [];
        self._reset()
     
    def debug_callback(self, debug_type, debug_message):
        sys.stderr.write('type: ' + str(debug_type) + ' message'+str(debug_message) + "\n")
    
    def v(self, *args, **kwargs):
        
        args_a = [w for w in args]
        first  = args_a[0]
        args_a.remove(first)

        h = kwargs.get('mydict', {})
        if h:
            h = h.get(first, {})
        else:
            h = self.response_dict().get(first, {})
        
        if len(args) == 1:
            try:
                return h.get('value', None)
            except:
                return h
                
        last = args_a.pop()
        
        for a in args_a:
            h = h.get(a, {})

        h = h.get(last, {})
        
        try:
            return h.get('value', None)
        except:
            return h    
        
    def load_yaml(self, config_file):
            
        dirs = [ '.', os.environ.get('HOME'), '/etc' ]

        for mydir in dirs:
            myfile = "%s/%s" % (mydir, config_file)
            
            if os.path.exists( myfile ):
                try:
                    f = open( myfile, "r" ) 
                except IOError, e:
                    print "unable to open file %s" % e

                #print "using file %s" % myfile
                
                yData  = yaml.load( f.read() )
                domain = self.api_config.get('domain', '')
                
                self.api_config_append( yData.get(domain, {}) )
                return
    
    def api_config_append(self, config):
        for c in config:
            self.api_config[c] = config[c] 
        
    def getNodeText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    def _reset(self):
        self._response_content = None
        self._response_dom     = None
        self._response_obj     = None
        self._response_soup    = None
        self._response_dict    = None
        self._response_error   = None
        
    def do(self, verb, call_data=dict()):
        return self.execute(verb, call_data)
                    
    def execute(self, verb, data):
        self.verb = verb

        if type(data) == DictType:
            self.call_xml = dict2xml(data, roottag='TRASHME')
        elif type(data) == ListType:
            self.call_xml = list2xml(data, roottag='TRASHME')
        else:    
            self.call_xml = data

        self._reset()    
        self._response_content = self._execute_http_request()

        # remove xml namespace
        regex = re.compile('xmlns="[^"]+"')
        self._response_content = regex.sub( '', self._response_content )

    def response_soup(self):
        if not self._response_soup:
            self._response_soup = BeautifulStoneSoup(unicode(self._response_content))
        
        return self._response_soup
        
    def response_obj(self):
        if not self._response_obj:
            self._response_obj = make_struct(self.response_dict())
        
        return self._response_obj
            
    def response_dom(self):
        if not self._response_dom:
            dom = parseString((self._response_content or ("<%sResponse></%sResponse>" % (self.verb, self.verb))) )
            self._response_dom = dom.getElementsByTagName(self.verb+'Response')[0]
        
        return self._response_dom

    def response_dict(self):
        if not self._response_dict:
            mydict = xml2dict().fromstring(self._response_content)
            self._response_dict = mydict.get(self.verb+'Response', mydict)
            
        return self._response_dict
        
    def api_init(self,config_items):
        for config in config_items:
            self.api_config[config[0]] = config[1]
 
    def _execute_http_request(self):
        "performs the http post and returns the XML response body"
        try:
            curl = pycurl.Curl()
            
            if self.proxy_host:
                curl.setopt(pycurl.PROXY, str('%s:%d' % (self.proxy_host, self.proxy_port)))
            else:
                curl.setopt(pycurl.PROXY, '')

            # construct headers
            request_headers = self._build_request_headers()
            curl.setopt( pycurl.HTTPHEADER, [
                str( '%s: %s' % ( k, v ) ) for k, v in request_headers.items()
            ] )

            # construct URL & post data
            request_url = self.api_config.get('domain', None)
            
            if self.api_config.get('uri', None):
                request_url = "%s%s" % ( request_url, self.api_config.get('uri', None) )
            
            if self.api_config.get('https', None):
                request_url = "https://%s" % request_url
            
            if self.method == 'POST':
                request_xml = self._build_request_xml()
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, str(request_xml))
            
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.URL, str(request_url))
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            
            response_header = StringIO.StringIO()
            response_body   = StringIO.StringIO()

            curl.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
            curl.setopt(pycurl.TIMEOUT, self.timeout)

            curl.setopt(pycurl.HEADERFUNCTION, response_header.write)
            curl.setopt(pycurl.WRITEFUNCTION, response_body.write)

            if self.debug:
                sys.stderr.write("CURL Request: %s\n" % request_url)
                curl.setopt(pycurl.VERBOSE, 1)
                curl.setopt(pycurl.DEBUGFUNCTION, self.debug_callback)

            curl.perform()
            
            response_code   = curl.getinfo(pycurl.HTTP_CODE)
            response_status = response_header.getvalue().splitlines()[0]
            response_reason = re.match( r'^HTTP.+? +\d+ +(.*) *$', response_status ).group(1)
            response_data   = response_body.getvalue()
        
            if response_code != 200:
                print response_data
                self._response_error = "Error: %s" % response_reason
                raise Exception('%s' % response_reason)
            else:
                return response_data
            
        except Exception, e:
            self._response_error = "Exception: %s" % e
            raise Exception("%s" % e)
        
    def error(self):
        "builds and returns the api error message"

        str = []

        if self._response_error:
            str.append(self._response_error)

        for e in self.response_dom().getElementsByTagName("Errors"):

            if e.getElementsByTagName('ErrorClassification'):
                str.append('- Class: %s' % nodeText(e.getElementsByTagName('ErrorClassification')[0]))

            if e.getElementsByTagName('SeverityCode'):
                str.append('- Severity: %s' % nodeText(e.getElementsByTagName('SeverityCode')[0]))

            if e.getElementsByTagName('ErrorCode'):
                str.append('- Code: %s' % nodeText(e.getElementsByTagName('ErrorCode')[0]))

            if e.getElementsByTagName('ShortMessage'):
                str.append('- %s ' % nodeText(e.getElementsByTagName('ShortMessage')[0]))

            if e.getElementsByTagName('LongMessage'):
                str.append('- %s ' % nodeText(e.getElementsByTagName('LongMessage')[0]))

        if (len(str) > 0):
            return "%s error:\n%s\n" % (self.verb, "\n".join(str))

        return "\n".join(str)
            
class shopping(ebaybase):
    """
    Shopping backend for ebaysdk.
    http://developer.ebay.com/products/shopping/

    shopping(debug=False, domain='open.api.ebay.com', uri='/shopping', method='POST', https=False, siteid=0, response_encoding='XML', request_encoding='XML', config_file='ebay.yaml')
    
    >>> s = shopping()
    >>> s.execute('FindItemsAdvanced', {'CharityID': 3897})
    >>> print s.response_obj().Ack
    Success
    >>> print s.error()
    <BLANKLINE>
    """
    
    def __init__(self, 
        domain='open.api.ebay.com', 
        uri='/shopping',
        https=False,
        siteid=0,
        response_encoding='XML',
        request_encoding='XML',
        config_file='ebay.yaml',
        **kwargs ):

        ebaybase.__init__(self, method='POST', **kwargs)

        self.api_config = {
            'domain' : domain,
            'uri' : uri,
            'https' : https,
            'siteid' : siteid,
            'response_encoding' : response_encoding,
            'request_encoding' : request_encoding,
        }    

        self.load_yaml(config_file)

    def _build_request_headers(self):
        return {
            "X-EBAY-API-VERSION": self.api_config.get('version', ''),
            "X-EBAY-API-APP-ID": self.api_config.get('appid', ''),
            "X-EBAY-API-SITEID": self.api_config.get('siteid', ''),
            "X-EBAY-API-CALL-NAME": self.verb,
            "X-EBAY-API-REQUEST-ENCODING": "XML",
            "Content-Type": "text/xml"
        }

    def _build_request_xml(self):
        xml = "<?xml version='1.0' encoding='utf-8'?>"
        xml += "<" + self.verb + "Request xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
        xml += self.call_xml
        xml += "</" + self.verb + "Request>"

        return xml

class html(ebaybase):
    """
    HTML backend for ebaysdk.
    
    (self, debug=False, method='GET', proxy_host=None, timeout=20, proxy_port=80)
    
    >>> h = html()
    >>> h.execute('http://shop.ebay.com/i.html?rt=nc&_nkw=mytouch+slide&_dmpt=PDA_Accessories&_rss=1')
    >>> print h.response_obj().rss.channel.ttl
    60
    >>> title = h.response_dom().getElementsByTagName('title')[0]
    >>> print nodeText( title )
    mytouch slide
    >>> print title.toxml()
    <title><![CDATA[mytouch slide]]></title>
    >>> print h.error()
    None
    """

    def __init__(self, **kwargs):
        ebaybase.__init__(self, method='GET', **kwargs)

    def response_dom(self):
        if not self._response_dom:
            self._response_dom = parseString(self._response_content)

        return self._response_dom

    def response_dict(self):
        if not self._response_dict:
            self._response_dict = xml2dict().fromstring(self._response_content)
            
        return self._response_dict

    def execute(self, url, call_data=dict()):
        "execute(self, url, call_data=dict())"
        
        self.url = url
        self.call_data = call_data
 
        self._reset()    
        self._response_content = self._execute_http_request()

        # remove xml namespace
        regex = re.compile( 'xmlns="[^"]+"' )
        self._response_content = regex.sub( '', self._response_content )

    def _execute_http_request(self):
        "performs the http post and returns the XML response body"
        
        try:
            curl = pycurl.Curl()
            
            if self.proxy_host:
                curl.setopt(pycurl.PROXY, str('%s:%d' % (self.proxy_host, self.proxy_port)))
            else:
                curl.setopt(pycurl.PROXY, '')
            
            request_url = self.url
            if self.call_data and self.method == 'GET':
                request_url = request_url + '?' + urllib.urlencode(self.call_data)

            if self.method == 'POST':
                request_xml = self._build_request_xml()
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, str(request_xml))
            
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.URL, str(request_url))
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            
            response_header = StringIO.StringIO()
            response_body   = StringIO.StringIO()

            curl.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
            curl.setopt(pycurl.TIMEOUT, self.timeout)

            curl.setopt(pycurl.HEADERFUNCTION, response_header.write)
            curl.setopt(pycurl.WRITEFUNCTION, response_body.write)

            if self.debug:
                sys.stderr.write("CURL Request: %s\n" % request_url)
                curl.setopt(pycurl.VERBOSE, 1)
                curl.setopt(pycurl.DEBUGFUNCTION, self.debug_callback)

            curl.perform()
            
            response_code   = curl.getinfo(pycurl.HTTP_CODE)
            response_status = response_header.getvalue().splitlines()[0]
            response_reason = re.match( r'^HTTP.+? +\d+ +(.*) *$', response_status ).group(1)
            response_data   = response_body.getvalue()
        
            if response_code != 200:
                self._response_error = "Error: %s" % response_reason
                raise Exception('%s' % response_reason)
            else:
                return response_data
            
        except Exception, e:
            self._response_error = "Exception: %s" % e
            raise Exception("%s" % e)
        
    def error(self):
         "builds and returns the api error message"     
         return self._response_error
         
class trading(ebaybase):
    """
    Trading backend for the ebaysdk
    http://developer.ebay.com/products/trading/
    
    >>> t = trading()
    >>> t.execute('GetCharities', { 'CharityID': 3897 }) 
    >>> charity_name = ''
    >>> if len( t.response_dom().getElementsByTagName('Name') ) > 0:
    ...   charity_name = nodeText(t.response_dom().getElementsByTagName('Name')[0])
    >>> print charity_name 
    Sunshine Kids Foundation
    >>> print t.error()
    <BLANKLINE>
    """

    def __init__(self, 
        domain=None,
        uri=None,
        https=None,
        siteid=None,
        response_encoding=None,
        request_encoding=None,
        proxy_host=None,
        proxy_port=None,
        username=None,
        password=None,
        token=None,
        iaf_token=None,
        appid=None,
        certid=None,
        devid=None,
        version=None,
        config_file='ebay.yaml',
        **kwargs ):
        
        ebaybase.__init__(self, method='POST', **kwargs)

        self.api_config = {
            'domain' : 'api.ebay.com',
            'uri' : '/ws/api.dll',
            'https' : False,
            'siteid' : '0',
            'response_encoding' : 'XML',
            'request_encoding' : 'XML',
            'version' : '648',
        }

        self.load_yaml(config_file)        

        self.api_config['domain']=domain or self.api_config.get('domain')
        self.api_config['uri']=uri or self.api_config.get('uri')
        self.api_config['https']=https or self.api_config.get('https')
        self.api_config['siteid']=siteid or self.api_config.get('siteid')
        self.api_config['response_encoding']=response_encoding or self.api_config.get('response_encoding')
        self.api_config['request_encoding']=request_encoding or self.api_config.get('request_encoding')
        self.api_config['username']=username or self.api_config.get('username')
        self.api_config['password']=password or self.api_config.get('password')
        self.api_config['token']=token or self.api_config.get('token')
        self.api_config['iaf_token']=iaf_token or self.api_config.get('iaf_token')
        self.api_config['appid']=appid or self.api_config.get('appid')
        self.api_config['certid']=certid or self.api_config.get('certid')
        self.api_config['devid']=devid or self.api_config.get('devid')
        self.api_config['version']=version or self.api_config.get('compatability') or self.api_config.get('version')

    def _build_request_headers(self):
        headers = {
            "X-EBAY-API-COMPATIBILITY-LEVEL": self.api_config.get('version', ''),
            "X-EBAY-API-DEV-NAME": self.api_config.get('devid', ''),
            "X-EBAY-API-APP-NAME": self.api_config.get('appid',''),
            "X-EBAY-API-CERT-NAME": self.api_config.get('certid',''),
            "X-EBAY-API-SITEID": self.api_config.get('siteid',''),
            "X-EBAY-API-CALL-NAME": self.verb,
            "Content-Type": "text/xml"
        }
        if self.api_config.get('iaf_token', None):
            headers["X-EBAY-API-IAF-TOKEN"] = self.api_config.get('iaf_token')
        return headers

    def _build_request_xml(self):
        xml = "<?xml version='1.0' encoding='utf-8'?>"
        xml += "<" + self.verb + "Request xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
        if not self.api_config.get('iaf_token', None):
            xml += "<RequesterCredentials>"
            if self.api_config.get('token', None):
                xml += "<eBayAuthToken>%s</eBayAuthToken>" % self.api_config.get('token')
            elif self.api_config.get('username', None):
                xml += "<Username>%s</Username>" % self.api_config.get('username', '')
                if self.api_config.get('password', None):
                    xml += "<Password>%s</Password>" % self.api_config.get('password', '')
            xml += "</RequesterCredentials>"
        xml += self.call_xml
        xml += "</" + self.verb + "Request>"
        return xml

class finding(ebaybase):
    """
    Finding backend for ebaysdk.
    http://developer.ebay.com/products/finding/
    
    >>> f = finding()
    >>> f.execute('findItemsAdvanced', {'keywords': 'shoes'})        
    >>> error = f.error()
    >>> print error
    <BLANKLINE>
    
    >>> if len( error ) <= 0:
    ...   print f.response_obj().itemSearchURL != ''
    ...   items = f.response_obj().searchResult.item    
    ...   print len(items)
    ...   print f.response_obj().ack
    True
    100
    Success
    
    """
    
    def __init__(self, 
        domain='svcs.ebay.com', 
        service='FindingService', 
        uri='/services/search/FindingService/v1',
        https=False,
        siteid='EBAY-US',
        response_encoding='XML',
        request_encoding='XML',
        config_file='ebay.yaml',
        **kwargs ):

        ebaybase.__init__(self, method='POST', **kwargs)

        self.api_config = {
            'domain'  : domain,
            'service' : service,
            'uri'     : uri,
            'https'   : https,
            'siteid'  : siteid,
            'response_encoding' : response_encoding,
            'request_encoding' : request_encoding,
        }    

        self.load_yaml(config_file)

    def _build_request_headers(self):
        return {
            "X-EBAY-SOA-SERVICE-NAME" : self.api_config.get('service',''),
            "X-EBAY-SOA-SERVICE-VERSION" : self.api_config.get('version',''),
            "X-EBAY-SOA-SECURITY-APPNAME"  : self.api_config.get('appid',''),
            "X-EBAY-SOA-GLOBAL-ID"  : self.api_config.get('siteid',''),
            "X-EBAY-SOA-OPERATION-NAME" : self.verb,
            "X-EBAY-SOA-REQUEST-DATA-FORMAT"  : self.api_config.get('request_encoding',''),
            "X-EBAY-SOA-RESPONSE-DATA-FORMAT" : self.api_config.get('response_encoding',''),
            "Content-Type" : "text/xml"
        }

    def _build_request_xml(self):
        xml = "<?xml version='1.0' encoding='utf-8'?>"
        xml += "<" + self.verb + "Request xmlns=\"http://www.ebay.com/marketplace/search/v1/services\">"
        xml += self.call_xml
        xml += "</" + self.verb + "Request>"

        return xml

import os, sys, re
import string, StringIO, base64
import yaml, pycurl, urllib
from types import DictType, ListType

from xml.dom.minidom import parseString, Node
from BeautifulSoup import BeautifulStoneSoup
from types import DictType 

import xml.etree.ElementTree as ET

class object_dict(dict):
    """object view of dict, you can 
    >>> a = object_dict()
    >>> a.fish = 'fish'
    >>> a['fish']
    'fish'
    >>> a['water'] = 'water'
    >>> a.water
    'water'
    >>> a.test = {'value': 1}
    >>> a.test2 = object_dict({'name': 'test2', 'value': 2})
    >>> a.test, a.test2.name, a.test2.value
    (1, 'test2', 2)
    """
    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        
        d = self.__getitem__(item)
        
        if isinstance(d, dict) and 'value' in d and len(d) == 1:
            return d['value']
        else:
            return d
    
        # if value is the only key in object, you can omit it
            
    def __setattr__(self, item, value):
        self.__setitem__(item, value)

    def getvalue(self, item, value=None):
        return self.get(item, {}).get('value', value)

class xml2dict(object):

    def __init__(self):
        pass

    def _parse_node(self, node):
        node_tree = object_dict()
        # Save attrs and text, hope there will not be a child with same name
        if node.text:
            node_tree.value = node.text
        for (k,v) in node.attrib.items():
            k,v = self._namespace_split(k, object_dict({'value':v}))
            node_tree[k] = v
        #Save childrens
        for child in node.getchildren():
            tag, tree = self._namespace_split(child.tag, self._parse_node(child))
            if  tag not in node_tree: # the first time, so store it in dict
                node_tree[tag] = tree
                continue
            old = node_tree[tag]
            if not isinstance(old, list):
                node_tree.pop(tag)
                node_tree[tag] = [old] # multi times, so change old dict to a list       
            node_tree[tag].append(tree) # add the new one      

        return node_tree

    def _namespace_split(self, tag, value):
        """
           Split the tag  '{http://cs.sfsu.edu/csc867/myscheduler}patients'
             ns = http://cs.sfsu.edu/csc867/myscheduler
             name = patients
        """
        result = re.compile("\{(.*)\}(.*)").search(tag)
        if result:
            value.namespace, tag = result.groups()    

        return (tag,value)

    def parse(self, file):
        """parse a xml file to a dict"""
        f = open(file, 'r')
        return self.fromstring(f.read()) 

    def fromstring(self, s):
        """parse a string"""
        t = ET.fromstring(s)
        root_tag, root_tree = self._namespace_split(t.tag, self._parse_node(t))
        return object_dict({root_tag: root_tree})


# Basic conversation goal here is converting a dict to an object allowing
# more comfortable access. `Struct()` and `make_struct()` are used to archive
# this goal.
# See http://stackoverflow.com/questions/1305532/convert-python-dict-to-object for the inital Idea
#
# The reasoning for this is the observation that we ferry arround hundreds of dicts via JSON
# and accessing them as `obj['key']` is tiresome after some time. `obj.key` is much nicer.
class Struct(object):
    """Emulate a cross over between a dict() and an object()."""
    def __init__(self, entries, default=None, nodefault=False):
        # ensure all keys are strings and nothing else
        entries = dict([(str(x), y) for x, y in entries.items()])
        self.__dict__.update(entries)
        self.__default = default
        self.__nodefault = nodefault

    def __getattr__(self, name):
        """Emulate Object access.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.a
        'b'
        >>> obj.foobar
        'c'

        `hasattr` results in strange behaviour if you give a default value. This might change in the future.
        >>> hasattr(obj, 'a')
        True
        >>> hasattr(obj, 'foobar')
        True
        """
        if name.startswith('_'):
            # copy expects __deepcopy__, __getnewargs__ to raise AttributeError
            # see http://groups.google.com/group/comp.lang.python/browse_thread/thread/6ac8a11de4e2526f/
            # e76b9fbb1b2ee171?#e76b9fbb1b2ee171
            raise AttributeError("'<Struct>' object has no attribute '%s'" % name)
        if self.__nodefault:
            raise AttributeError("'<Struct>' object has no attribute '%s'" % name)
        return self.__default

    def __getitem__(self, key):
        """Emulate dict like access.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj['a']
        'b'

        While the standard dict access via [key] uses the default given when creating the struct,
        access via get(), results in None for keys not set. This might be considered a bug and
        should change in the future.
        >>> obj['foobar']
        'c'
        >>> obj.get('foobar')
        'c'
        """
        # warnings.warn("dict_accss[foo] on a Struct, use object_access.foo instead",
        #                DeprecationWarning, stacklevel=2)
        if self.__nodefault:
            return self.__dict__[key]
        return self.__dict__.get(key, self.__default)

    def get(self, key, default=None):
        """Emulate dictionary access.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.get('a')
        'b'
        >>> obj.get('foobar')
        'c'
        """
        if key in self.__dict__:
            return self.__dict__[key]
        if not self.__nodefault:
            return self.__default
        return default

    def __contains__(self, item):
        """Emulate dict 'in' functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> 'a' in obj
        True
        >>> 'foobar' in obj
        False
        """
        return item in self.__dict__

    def __nonzero__(self):
        """Returns whether the instance evaluates to False"""
        return bool(self.items())

    def has_key(self, item):
        """Emulate dict.has_key() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.has_key('a')
        True
        >>> obj.has_key('foobar')
        False
        """
        return item in self

    def items(self):
        """Emulate dict.items() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.items()
        [('a', 'b')]
        """
        return [(k, v) for (k, v) in self.__dict__.items() if not k.startswith('_Struct__')]

    def keys(self):
        """Emulate dict.keys() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.keys()
        ['a']
        """
        return [k for (k, _v) in self.__dict__.items() if not k.startswith('_Struct__')]

    def values(self):
        """Emulate dict.values() functionality.

        >>> obj = Struct({'a': 'b'}, default='c')
        >>> obj.values()
        ['b']
        """
        return [v for (k, v) in self.__dict__.items() if not k.startswith('_Struct__')]

    def __repr__(self):
        return "<Struct: %r>" % dict(self.items())

    def as_dict(self):
        """Return a dict representing the content of this struct."""
        return self.__dict__


def make_struct(obj, default=None, nodefault=False):
    """Converts a dict to an object, leaves objects untouched.

    Someting like obj.vars() = dict() - Read Only!

    >>> obj = make_struct(dict(foo='bar'))
    >>> obj.foo
    'bar'

    `make_struct` leaves objects alone.
    >>> class MyObj(object): pass
    >>> data = MyObj()
    >>> data.foo = 'bar'
    >>> obj = make_struct(data)
    >>> obj.foo
    'bar'

    `make_struct` also is idempotent
    >>> obj = make_struct(make_struct(dict(foo='bar')))
    >>> obj.foo
    'bar'

    `make_struct` recursively handles dicts and lists of dicts
    >>> obj = make_struct(dict(foo=dict(bar='baz')))
    >>> obj.foo.bar
    'baz'

    >>> obj = make_struct([dict(foo='baz')])
    >>> obj
    [<Struct: {'foo': 'baz'}>]
    >>> obj[0].foo
    'baz'

    >>> obj = make_struct(dict(foo=dict(bar=dict(baz='end'))))
    >>> obj.foo.bar.baz
    'end'

    >>> obj = make_struct(dict(foo=[dict(bar='baz')]))
    >>> obj.foo[0].bar
    'baz'
    >>> obj.items()
    [('foo', [<Struct: {'bar': 'baz'}>])]
    """
    if type(obj) == type(Struct):
        return obj
    if (not hasattr(obj, '__dict__')) and hasattr(obj, 'iterkeys'):
        # this should be a dict
        struc = Struct(obj, default, nodefault)
        # handle recursive sub-dicts
        for key, val in obj.items():
            setattr(struc, key, make_struct(val, default, nodefault))
        return struc
    elif hasattr(obj, '__delslice__') and hasattr(obj, '__getitem__'):
        #
        return [make_struct(v, default, nodefault) for v in obj]
    else:
        return obj


# Code is based on http://code.activestate.com/recipes/573463/
def _convert_dict_to_xml_recurse(parent, dictitem, listnames):
    """Helper Function for XML conversion."""
    # we can't convert bare lists
    assert not isinstance(dictitem, list)

    if isinstance(dictitem, dict):
        for (tag, child) in sorted(dictitem.iteritems()):
            if isinstance(child, list):
                # iterate through the array and convert
                listelem = ET.Element(None)
                listelem2 = ET.Element(tag)
                parent.append(listelem)
                for listchild in child:
                    elem = ET.Element(listnames.get(tag, listelem2.tag))
                    listelem.append(elem)
                    _convert_dict_to_xml_recurse(elem, listchild, listnames)
            else:
                elem = ET.Element(tag)
                parent.append(elem)
                _convert_dict_to_xml_recurse(elem, child, listnames)
    elif not dictitem is None:
        parent.text = unicode(dictitem)


def dict2et(xmldict, roottag='data', listnames=None):
    """Converts a dict to an ElementTree.

    Converts a dictionary to an XML ElementTree Element::
    """

    if not listnames:
        listnames = {}
    root = ET.Element(roottag)
    _convert_dict_to_xml_recurse(root, xmldict, listnames)
    return root


def list2et(xmllist, root, elementname):
    """Converts a list to an ElementTree.

        See also dict2et()
    """

    basexml = dict2et({root: xmllist}, 'xml', listnames={root: elementname})
    return basexml.find(root)


def dict2xml(datadict, roottag='TRASHME', listnames=None, pretty=False):
    """
    Converts a dictionary to an UTF-8 encoded XML string.
    See also dict2et()
    """
    root = dict2et(datadict, roottag, listnames)
    
    xml = to_string(root, pretty=pretty)
    return xml.replace('<%s>' % roottag, '').replace('</%s>' % roottag, '')
    
def list2xml(datalist, roottag, elementname, pretty=False):
    """Converts a list to an UTF-8 encoded XML string.

    See also dict2et()
    """
    root = list2et(datalist, roottag, elementname)
    return to_string(root, pretty=pretty)


def to_string(root, encoding='utf-8', pretty=False):
    """Converts an ElementTree to a string"""

    if pretty:
        indent(root)

    tree = ET.ElementTree(root)
    fileobj = StringIO.StringIO()
    #fileobj.write('<?xml version="1.0" encoding="%s"?>' % encoding)
    if pretty:
        fileobj.write('\n')
    tree.write(fileobj, 'utf-8')
    return fileobj.getvalue()


# From http://effbot.org/zone/element-lib.htm
# prettyprint: Prints a tree with each node indented according to its depth. This is
# done by first indenting the tree (see below), and then serializing it as usual.
# indent: Adds whitespace to the tree, so that saving it as usual results in a prettyprinted tree.
# in-place prettyprint formatter

def indent(elem, level=0):
    """XML prettyprint: Prints a tree with each node indented according to its depth."""
    i = "\n" + level * " "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent(child, level + 1)
        if child:
            if not child.tail or not child.tail.strip():
                child.tail = i
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def test():
    """Simple selftest."""

    data = {"guid": "3104247-7",
            "menge": 7,
            "artnr": "14695",
            "batchnr": "3104247"}
    xmlstr = dict2xml(data, roottag='warenzugang')
    assert xmlstr == ('<?xml version="1.0" encoding="utf-8"?><warenzugang><artnr>14695</artnr>'
                      '<batchnr>3104247</batchnr><guid>3104247-7</guid><menge>7</menge></warenzugang>')

    data = {"kommiauftragsnr": 2103839,
     "anliefertermin": "2009-11-25",
     "fixtermin": True,
     "prioritaet": 7,
     "info_kunde": "Besuch H. Gerlach",
     "auftragsnr": 1025575,
     "kundenname": "Ute Zweihaus 400424990",
     "kundennr": "21548",
     "name1": "Uwe Zweihaus",
     "name2": "400424990",
     "name3": "",
     u"strasse": u"Bahnhofstr. 2",
     "land": "DE",
     "plz": "42499",
     "ort": u"Hucksenwagen",
     "positionen": [{"menge": 12,
                     "artnr": "14640/XL",
                     "posnr": 1},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3}],
     "versandeinweisungen": [{"guid": "2103839-XalE",
                              "bezeichner": "avisierung48h",
                              "anweisung": "48h vor Anlieferung unter 0900-LOGISTIK avisieren"},
                             {"guid": "2103839-GuTi",
                              "bezeichner": "abpackern140",
                              "anweisung": u"Paletten hochstens auf 140 cm Packen"}]
    }

    xmlstr = dict2xml(data, roottag='kommiauftrag')

    data = {"kommiauftragsnr": 2103839,
     "positionen": [{"menge": 4,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "23455326543222553"},
                    {"menge": 8,
                     "artnr": "14640/XL",
                     "posnr": 1,
                     "nve": "43255634634653546"},
                    {"menge": 4,
                     "artnr": "14640/03",
                     "posnr": 2,
                     "nve": "43255634634653546"},
                    {"menge": 2,
                     "artnr": "10105",
                     "posnr": 3,
                     "nve": "23455326543222553"}],
     "nves": [{"nve": "23455326543222553",
               "gewicht": 28256,
               "art": "paket"},
              {"nve": "43255634634653546",
               "gewicht": 28256,
                "art": "paket"}]}

    xmlstr = dict2xml(data, roottag='rueckmeldung')
    print xmlstr


VERSION = (0, 1, 6)


def get_version():
    version = '%s.%s.%s' % (VERSION[0], VERSION[1], VERSION[2])
    return version

__version__ = get_version()       

def nodeText(node):
    rc = []

    if hasattr(node, 'childNodes'):
        for cn in node.childNodes:
            if cn.nodeType == cn.TEXT_NODE:
                rc.append(cn.data)
            elif cn.nodeType == cn.CDATA_SECTION_NODE:
                rc.append(cn.data)    
        
    return ''.join(rc)

def tag(name, value):
    return "<%s>%s</%s>" % ( name, value, name )

class ebaybase(object):
    
    def __init__(self, debug=False, method='GET', proxy_host=None, timeout=20, proxy_port=80, **kwargs):                
        self.verb       = None
        self.debug      = debug
        self.method     = method
        self.timeout    = timeout
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port 
        self.spooled_calls = [];
        self._reset()
     
    def debug_callback(self, debug_type, debug_message):
        sys.stderr.write('type: ' + str(debug_type) + ' message'+str(debug_message) + "\n")
    
    def v(self, *args, **kwargs):
        
        args_a = [w for w in args]
        first  = args_a[0]
        args_a.remove(first)

        h = kwargs.get('mydict', {})
        if h:
            h = h.get(first, {})
        else:
            h = self.response_dict().get(first, {})
        
        if len(args) == 1:
            try:
                return h.get('value', None)
            except:
                return h
                
        last = args_a.pop()
        
        for a in args_a:
            h = h.get(a, {})

        h = h.get(last, {})
        
        try:
            return h.get('value', None)
        except:
            return h    
        
    def load_yaml(self, config_file):
            
        dirs = [ '.', os.environ.get('HOME'), '/etc' ]

        for mydir in dirs:
            myfile = "%s/%s" % (mydir, config_file)
            
            if os.path.exists( myfile ):
                try:
                    f = open( myfile, "r" ) 
                except IOError, e:
                    print "unable to open file %s" % e

                #print "using file %s" % myfile
                
                yData  = yaml.load( f.read() )
                domain = self.api_config.get('domain', '')
                
                self.api_config_append( yData.get(domain, {}) )
                return
    
    def api_config_append(self, config):
        for c in config:
            self.api_config[c] = config[c] 
        
    def getNodeText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    def _reset(self):
        self._response_content = None
        self._response_dom     = None
        self._response_obj     = None
        self._response_soup    = None
        self._response_dict    = None
        self._response_error   = None
        
    def do(self, verb, call_data=dict()):
        return self.execute(verb, call_data)
                    
    def execute(self, verb, data):
        self.verb = verb

        if type(data) == DictType:
            self.call_xml = dict2xml(data, roottag='TRASHME')
        elif type(data) == ListType:
            self.call_xml = list2xml(data, roottag='TRASHME')
        else:    
            self.call_xml = data

        self._reset()    
        self._response_content = self._execute_http_request()

        # remove xml namespace
        regex = re.compile('xmlns="[^"]+"')
        self._response_content = regex.sub( '', self._response_content )

    def response_soup(self):
        if not self._response_soup:
            self._response_soup = BeautifulStoneSoup(unicode(self._response_content))
        
        return self._response_soup
        
    def response_obj(self):
        if not self._response_obj:
            self._response_obj = make_struct(self.response_dict())
        
        return self._response_obj
            
    def response_dom(self):
        if not self._response_dom:
            dom = parseString((self._response_content or ("<%sResponse></%sResponse>" % (self.verb, self.verb))) )
            self._response_dom = dom.getElementsByTagName(self.verb+'Response')[0]
        
        return self._response_dom

    def response_dict(self):
        if not self._response_dict:
            mydict = xml2dict().fromstring(self._response_content)
            self._response_dict = mydict.get(self.verb+'Response', mydict)
            
        return self._response_dict
        
    def api_init(self,config_items):
        for config in config_items:
            self.api_config[config[0]] = config[1]
 
    def _execute_http_request(self):
        "performs the http post and returns the XML response body"
        try:
            curl = pycurl.Curl()
            
            if self.proxy_host:
                curl.setopt(pycurl.PROXY, str('%s:%d' % (self.proxy_host, self.proxy_port)))
            else:
                curl.setopt(pycurl.PROXY, '')

            # construct headers
            request_headers = self._build_request_headers()
            curl.setopt( pycurl.HTTPHEADER, [
                str( '%s: %s' % ( k, v ) ) for k, v in request_headers.items()
            ] )

            # construct URL & post data
            request_url = self.api_config.get('domain', None)
            
            if self.api_config.get('uri', None):
                request_url = "%s%s" % ( request_url, self.api_config.get('uri', None) )
            
            if self.api_config.get('https', None):
                request_url = "https://%s" % request_url
            
            if self.method == 'POST':
                request_xml = self._build_request_xml()
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, str(request_xml))
            
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.URL, str(request_url))
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            
            response_header = StringIO.StringIO()
            response_body   = StringIO.StringIO()

            curl.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
            curl.setopt(pycurl.TIMEOUT, self.timeout)

            curl.setopt(pycurl.HEADERFUNCTION, response_header.write)
            curl.setopt(pycurl.WRITEFUNCTION, response_body.write)

            if self.debug:
                sys.stderr.write("CURL Request: %s\n" % request_url)
                curl.setopt(pycurl.VERBOSE, 1)
                curl.setopt(pycurl.DEBUGFUNCTION, self.debug_callback)

            curl.perform()
            
            response_code   = curl.getinfo(pycurl.HTTP_CODE)
            response_status = response_header.getvalue().splitlines()[0]
            response_reason = re.match( r'^HTTP.+? +\d+ +(.*) *$', response_status ).group(1)
            response_data   = response_body.getvalue()
        
            if response_code != 200:
                print response_data
                self._response_error = "Error: %s" % response_reason
                raise Exception('%s' % response_reason)
            else:
                return response_data
            
        except Exception, e:
            self._response_error = "Exception: %s" % e
            raise Exception("%s" % e)
        
    def error(self):
        "builds and returns the api error message"

        str = []

        if self._response_error:
            str.append(self._response_error)

        for e in self.response_dom().getElementsByTagName("Errors"):

            if e.getElementsByTagName('ErrorClassification'):
                str.append('- Class: %s' % nodeText(e.getElementsByTagName('ErrorClassification')[0]))

            if e.getElementsByTagName('SeverityCode'):
                str.append('- Severity: %s' % nodeText(e.getElementsByTagName('SeverityCode')[0]))

            if e.getElementsByTagName('ErrorCode'):
                str.append('- Code: %s' % nodeText(e.getElementsByTagName('ErrorCode')[0]))

            if e.getElementsByTagName('ShortMessage'):
                str.append('- %s ' % nodeText(e.getElementsByTagName('ShortMessage')[0]))

            if e.getElementsByTagName('LongMessage'):
                str.append('- %s ' % nodeText(e.getElementsByTagName('LongMessage')[0]))

        if (len(str) > 0):
            return "%s error:\n%s\n" % (self.verb, "\n".join(str))

        return "\n".join(str)
            
class shopping(ebaybase):
    """
    Shopping backend for ebaysdk.
    http://developer.ebay.com/products/shopping/

    shopping(debug=False, domain='open.api.ebay.com', uri='/shopping', method='POST', https=False, siteid=0, response_encoding='XML', request_encoding='XML', config_file='ebay.yaml')
    
    >>> s = shopping()
    >>> s.execute('FindItemsAdvanced', {'CharityID': 3897})
    >>> print s.response_obj().Ack
    Success
    >>> print s.error()
    <BLANKLINE>
    """
    
    def __init__(self, 
        domain='open.api.ebay.com', 
        uri='/shopping',
        https=False,
        siteid=0,
        response_encoding='XML',
        request_encoding='XML',
        config_file='ebay.yaml',
        **kwargs ):

        ebaybase.__init__(self, method='POST', **kwargs)

        self.api_config = {
            'domain' : domain,
            'uri' : uri,
            'https' : https,
            'siteid' : siteid,
            'response_encoding' : response_encoding,
            'request_encoding' : request_encoding,
        }    

        self.load_yaml(config_file)

    def _build_request_headers(self):
        return {
            "X-EBAY-API-VERSION": self.api_config.get('version', ''),
            "X-EBAY-API-APP-ID": self.api_config.get('appid', ''),
            "X-EBAY-API-SITEID": self.api_config.get('siteid', ''),
            "X-EBAY-API-CALL-NAME": self.verb,
            "X-EBAY-API-REQUEST-ENCODING": "XML",
            "Content-Type": "text/xml"
        }

    def _build_request_xml(self):
        xml = "<?xml version='1.0' encoding='utf-8'?>"
        xml += "<" + self.verb + "Request xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
        xml += self.call_xml
        xml += "</" + self.verb + "Request>"

        return xml

class html(ebaybase):
    """
    HTML backend for ebaysdk.
    
    (self, debug=False, method='GET', proxy_host=None, timeout=20, proxy_port=80)
    
    >>> h = html()
    >>> h.execute('http://shop.ebay.com/i.html?rt=nc&_nkw=mytouch+slide&_dmpt=PDA_Accessories&_rss=1')
    >>> print h.response_obj().rss.channel.ttl
    60
    >>> title = h.response_dom().getElementsByTagName('title')[0]
    >>> print nodeText( title )
    mytouch slide
    >>> print title.toxml()
    <title><![CDATA[mytouch slide]]></title>
    >>> print h.error()
    None
    """

    def __init__(self, **kwargs):
        ebaybase.__init__(self, method='GET', **kwargs)

    def response_dom(self):
        if not self._response_dom:
            self._response_dom = parseString(self._response_content)

        return self._response_dom

    def response_dict(self):
        if not self._response_dict:
            self._response_dict = xml2dict().fromstring(self._response_content)
            
        return self._response_dict

    def execute(self, url, call_data=dict()):
        "execute(self, url, call_data=dict())"
        
        self.url = url
        self.call_data = call_data
 
        self._reset()    
        self._response_content = self._execute_http_request()

        # remove xml namespace
        regex = re.compile( 'xmlns="[^"]+"' )
        self._response_content = regex.sub( '', self._response_content )

    def _execute_http_request(self):
        "performs the http post and returns the XML response body"
        
        try:
            curl = pycurl.Curl()
            
            if self.proxy_host:
                curl.setopt(pycurl.PROXY, str('%s:%d' % (self.proxy_host, self.proxy_port)))
            else:
                curl.setopt(pycurl.PROXY, '')
            
            request_url = self.url
            if self.call_data and self.method == 'GET':
                request_url = request_url + '?' + urllib.urlencode(self.call_data)

            if self.method == 'POST':
                request_xml = self._build_request_xml()
                curl.setopt(pycurl.POST, True)
                curl.setopt(pycurl.POSTFIELDS, str(request_xml))
            
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.URL, str(request_url))
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            
            response_header = StringIO.StringIO()
            response_body   = StringIO.StringIO()

            curl.setopt(pycurl.CONNECTTIMEOUT, self.timeout)
            curl.setopt(pycurl.TIMEOUT, self.timeout)

            curl.setopt(pycurl.HEADERFUNCTION, response_header.write)
            curl.setopt(pycurl.WRITEFUNCTION, response_body.write)

            if self.debug:
                sys.stderr.write("CURL Request: %s\n" % request_url)
                curl.setopt(pycurl.VERBOSE, 1)
                curl.setopt(pycurl.DEBUGFUNCTION, self.debug_callback)

            curl.perform()
            
            response_code   = curl.getinfo(pycurl.HTTP_CODE)
            response_status = response_header.getvalue().splitlines()[0]
            response_reason = re.match( r'^HTTP.+? +\d+ +(.*) *$', response_status ).group(1)
            response_data   = response_body.getvalue()
        
            if response_code != 200:
                self._response_error = "Error: %s" % response_reason
                raise Exception('%s' % response_reason)
            else:
                return response_data
            
        except Exception, e:
            self._response_error = "Exception: %s" % e
            raise Exception("%s" % e)
        
    def error(self):
         "builds and returns the api error message"     
         return self._response_error
         
class trading(ebaybase):
    """
    Trading backend for the ebaysdk
    http://developer.ebay.com/products/trading/
    
    >>> t = trading()
    >>> t.execute('GetCharities', { 'CharityID': 3897 }) 
    >>> charity_name = ''
    >>> if len( t.response_dom().getElementsByTagName('Name') ) > 0:
    ...   charity_name = nodeText(t.response_dom().getElementsByTagName('Name')[0])
    >>> print charity_name 
    Sunshine Kids Foundation
    >>> print t.error()
    <BLANKLINE>
    """

    def __init__(self, 
        domain=None,
        uri=None,
        https=None,
        siteid=None,
        response_encoding=None,
        request_encoding=None,
        proxy_host=None,
        proxy_port=None,
        username=None,
        password=None,
        token=None,
        iaf_token=None,
        appid=None,
        certid=None,
        devid=None,
        version=None,
        config_file='ebay.yaml',
        **kwargs ):
        
        ebaybase.__init__(self, method='POST', **kwargs)

        self.api_config = {
            'domain' : 'api.ebay.com',
            'uri' : '/ws/api.dll',
            'https' : False,
            'siteid' : '0',
            'response_encoding' : 'XML',
            'request_encoding' : 'XML',
            'version' : '648',
        }

        self.load_yaml(config_file)        

        self.api_config['domain']=domain or self.api_config.get('domain')
        self.api_config['uri']=uri or self.api_config.get('uri')
        self.api_config['https']=https or self.api_config.get('https')
        self.api_config['siteid']=siteid or self.api_config.get('siteid')
        self.api_config['response_encoding']=response_encoding or self.api_config.get('response_encoding')
        self.api_config['request_encoding']=request_encoding or self.api_config.get('request_encoding')
        self.api_config['username']=username or self.api_config.get('username')
        self.api_config['password']=password or self.api_config.get('password')
        self.api_config['token']=token or self.api_config.get('token')
        self.api_config['iaf_token']=iaf_token or self.api_config.get('iaf_token')
        self.api_config['appid']=appid or self.api_config.get('appid')
        self.api_config['certid']=certid or self.api_config.get('certid')
        self.api_config['devid']=devid or self.api_config.get('devid')
        self.api_config['version']=version or self.api_config.get('compatability') or self.api_config.get('version')

    def _build_request_headers(self):
        headers = {
            "X-EBAY-API-COMPATIBILITY-LEVEL": self.api_config.get('version', ''),
            "X-EBAY-API-DEV-NAME": self.api_config.get('devid', ''),
            "X-EBAY-API-APP-NAME": self.api_config.get('appid',''),
            "X-EBAY-API-CERT-NAME": self.api_config.get('certid',''),
            "X-EBAY-API-SITEID": self.api_config.get('siteid',''),
            "X-EBAY-API-CALL-NAME": self.verb,
            "Content-Type": "text/xml"
        }
        if self.api_config.get('iaf_token', None):
            headers["X-EBAY-API-IAF-TOKEN"] = self.api_config.get('iaf_token')
        return headers

    def _build_request_xml(self):
        xml = "<?xml version='1.0' encoding='utf-8'?>"
        xml += "<" + self.verb + "Request xmlns=\"urn:ebay:apis:eBLBaseComponents\">"
        if not self.api_config.get('iaf_token', None):
            xml += "<RequesterCredentials>"
            if self.api_config.get('token', None):
                xml += "<eBayAuthToken>%s</eBayAuthToken>" % self.api_config.get('token')
            elif self.api_config.get('username', None):
                xml += "<Username>%s</Username>" % self.api_config.get('username', '')
                if self.api_config.get('password', None):
                    xml += "<Password>%s</Password>" % self.api_config.get('password', '')
            xml += "</RequesterCredentials>"
        xml += self.call_xml
        xml += "</" + self.verb + "Request>"
        return xml

class finding(ebaybase):
    """
    Finding backend for ebaysdk.
    http://developer.ebay.com/products/finding/
    
    >>> f = finding()
    >>> f.execute('findItemsAdvanced', {'keywords': 'shoes'})        
    >>> error = f.error()
    >>> print error
    <BLANKLINE>
    
    >>> if len( error ) <= 0:
    ...   print f.response_obj().itemSearchURL != ''
    ...   items = f.response_obj().searchResult.item    
    ...   print len(items)
    ...   print f.response_obj().ack
    True
    100
    Success
    
    """
    
    def __init__(self, 
        domain='svcs.ebay.com', 
        service='FindingService', 
        uri='/services/search/FindingService/v1',
        https=False,
        siteid='EBAY-US',
        response_encoding='XML',
        request_encoding='XML',
        config_file='ebay.yaml',
        **kwargs ):

        ebaybase.__init__(self, method='POST', **kwargs)

        self.api_config = {
            'domain'  : domain,
            'service' : service,
            'uri'     : uri,
            'https'   : https,
            'siteid'  : siteid,
            'response_encoding' : response_encoding,
            'request_encoding' : request_encoding,
        }    

        self.load_yaml(config_file)

    def _build_request_headers(self):
        return {
            "X-EBAY-SOA-SERVICE-NAME" : self.api_config.get('service',''),
            "X-EBAY-SOA-SERVICE-VERSION" : self.api_config.get('version',''),
            "X-EBAY-SOA-SECURITY-APPNAME"  : self.api_config.get('appid',''),
            "X-EBAY-SOA-GLOBAL-ID"  : self.api_config.get('siteid',''),
            "X-EBAY-SOA-OPERATION-NAME" : self.verb,
            "X-EBAY-SOA-REQUEST-DATA-FORMAT"  : self.api_config.get('request_encoding',''),
            "X-EBAY-SOA-RESPONSE-DATA-FORMAT" : self.api_config.get('response_encoding',''),
            "Content-Type" : "text/xml"
        }

    def _build_request_xml(self):
        xml = "<?xml version='1.0' encoding='utf-8'?>"
        xml += "<" + self.verb + "Request xmlns=\"http://www.ebay.com/marketplace/search/v1/services\">"
        xml += self.call_xml
        xml += "</" + self.verb + "Request>"

        return xml

