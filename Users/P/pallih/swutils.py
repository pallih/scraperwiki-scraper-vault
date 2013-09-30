import scraperwiki
import json
import random
import cgi, os
import requests
import urllib2
import urllib
import re
import lxml.html
#import lxml.html.soupparser
from lxml import etree
import datetime
import time
import base64
import imp, tempfile

'''
functions:

- Return user agent
- Return proxy - does not work atm.
- Extract emails
- Unserialize an XML document to a dictionary
- load the pynma library from github to send notifications to android devices using notifymyandroid.com - https://github.com/uskr/pynma
'''

#qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING"))) # This gives us the secret variables from the description

# SETUP

pynma_url = 'https://raw.github.com/uskr/pynma/master/pynma/pynma.py'


# known media file extensions
MEDIA_EXTENSIONS = ['ai', 'aif', 'aifc', 'aiff', 'asc', 'au', 'avi', 'bcpio', 'bin', 'c', 'cc', 'ccad', 'cdf', 'class', 'cpio', 'cpt', 'csh', 'css', 'csv', 'dcr', 'dir', 'dms', 'doc', 'drw', 'dvi', 'dwg', 'dxf', 'dxr', 'eps', 'etx', 'exe', 'ez', 'f', 'f90', 'fli', 'flv', 'gif', 'gtar', 'gz', 'h', 'hdf', 'hh', 'hqx', 'ice', 'ico', 'ief', 'iges', 'igs', 'ips', 'ipx', 'jpe', 'jpeg', 'jpg', 'js', 'kar', 'latex', 'lha', 'lsp', 'lzh', 'm', 'man', 'me', 'mesh', 'mid', 'midi', 'mif', 'mime', 'mov', 'movie', 'mp2', 'mp3', 'mpe', 'mpeg', 'mpg', 'mpga', 'ms', 'msh', 'nc', 'oda', 'pbm', 'pdb', 'pdf', 'pgm', 'pgn', 'png', 'pnm', 'pot', 'ppm', 'pps', 'ppt', 'ppz', 'pre', 'prt', 'ps', 'qt', 'ra', 'ram', 'ras', 'rgb', 'rm', 'roff', 'rpm', 'rtf', 'rtx', 'scm', 'set', 'sgm', 'sgml', 'sh', 'shar', 'silo', 'sit', 'skd', 'skm', 'skp', 'skt', 'smi', 'smil', 'snd', 'sol', 'spl', 'src', 'step', 'stl', 'stp', 'sv4cpio', 'sv4crc', 'swf', 't', 'tar', 'tcl', 'tex', 'texi', 'tif', 'tiff', 'tr', 'tsi', 'tsp', 'tsv', 'txt', 'unv', 'ustar', 'vcd', 'vda', 'viv', 'vivo', 'vrml', 'w2p', 'wav', 'wmv', 'wrl', 'xbm', 'xlc', 'xll', 'xlm', 'xls', 'xlw', 'xml', 'xpm', 'xsl', 'xwd', 'xyz', 'zip']

# Browsers
desktop = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21','Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.11 Safari/535.19','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3'
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'
'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1'
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'
'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)']

mobile = ['Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3','Nokia6630/1.0 (2.3.129) SymbianOS/8.0 Series60/2.6 Profile/MIDP-2.0 Configuration/CLDC-1.1','Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9','Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Opera/9.80 (Android 2.3.3; Linux; Opera Mobi/ADR-1111101157; U; es-ES) Presto/2.9.201 Version/11.50','Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)','HTC_Touch_3G Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)','Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+']


# Get page from Google cache
def gcache_get(url):
        """Get page from google cache
        """
        return requests.get('http://www.google.com/search?&q=cache%3A' + urllib.quote(url)).text


# Return user agent
def get_user_agent(browser_type='desktop'):
    '''Returns a user agent, either for a desktop browser (default) or a mobile browser.
    Format: {'User-Agent': 'USER-AGENT'}'''
    if browser_type == 'desktop':
        return {'User-Agent':str(random.choice(desktop))}
    elif browser_type == 'mobile':
        return {'User-Agent':str(random.choice(mobile))}


#Return proxy - does not work at the moment
def get_proxy(apikey= '1608634744e31cc0af5634a7cf6ae2e6520b3d60'):
    ''' Returns a list with number of proxies
    format: {'http':ip:port '''
    proxieslist = json.loads(scraperwiki.scrape('http://api.proxyswitcheroo.com/v1/proxies?format=json&api_key='+apikey+'&num_records=10&proxy_type=T&speed_rating=5&fresh_hours=3'))
    proxies = []
    for x in proxieslist['proxies']:
        proxies.append(x['host']+':'+x['port'])
    return {'http':str(random.choice(proxies))}

#Extract emails  - From webscraping library: http://code.google.com/p/webscraping/
def extract_emails(html):
    """Extract emails and look for common obfuscations
    >>> extract_emails('')
    []
    >>> extract_emails('hello richard@sitescraper.net world')
    ['richard@sitescraper.net']
    >>> extract_emails('hello richard@<!-- trick comment -->sitescraper.net world')
    ['richard@sitescraper.net']
    >>> extract_emails('hello richard AT sitescraper DOT net world')
    ['richard@sitescraper.net']
    """
    email_re = re.compile('([\w\.-]{1,64})@(\w[\w\.-]{1,255})\.(\w+)')
    # remove comments, which can obfuscate emails
    html = re.compile('<!--.*?-->', re.DOTALL).sub('', html).replace('mailto:', '')
    emails = []
    for user, domain, ext in email_re.findall(html):
        if ext.lower() not in MEDIA_EXTENSIONS and len(ext)>=2 and not re.compile('\d').search(ext) and domain.count('.')<=3:
            email = '%s@%s.%s' % (user, domain, ext)
            if email not in emails:
                emails.append(email)

    # look for obfuscated email
    for user, domain, ext in re.compile('([\w\.-]{1,64})\s?.?AT.?\s?([\w\.-]{1,255})\s?.?DOT.?\s?(\w+)', re.IGNORECASE).findall(html):
        if ext.lower() not in MEDIA_EXTENSIONS and len(ext)>=2 and not re.compile('\d').search(ext) and domain.count('.')<=3:
            email = '%s@%s.%s' % (user, domain, ext)
            if email not in emails:
                emails.append(email)
    return emails

# unserialize an XML document to a dictionary (containing dicts, strings or lists)
def from_xml(element):
    if len(element) > 0:
        outdict = {}
        if element.get('type') == 'list':
            value = []
            for i in element:
                value.append(from_xml(i))
            outdict[element[0].tag] = value
        else:
            for i in element:
                outdict[i.tag] = from_xml(i)
        return outdict
    else:
        return element.text

# return unicode string if not null, otherwise empty string
def xunc(s):
    return unicode(s) if s else u''

# serialise the contents of a dictionary as simple XML
def to_xml(element_name, data):
    element_name = re.sub('\s', '_', element_name) # replace any spaces in the tag name with underscores
    element = etree.Element(element_name)
    if isinstance (data, dict):
        keys = data.keys()
        keys.sort() # output is in alphab order 
        for key in keys: # output simple string elements first
            if not isinstance(data[key], list) and not isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
        for key in keys: # any lists and dicts come afterwards
            if isinstance(data[key], list): # lists stay in original order
                element.set('type', 'list')
                for i in data[key]:
                    element.append(to_xml(key, i))
            elif isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
    else:
        element.text = xunc(data)
    return element

# load the pynma library - based on julian's code to load librarys from github - https://scraperwiki.com/scrapers/github_import_experiment/edit/
modulecode = urllib.urlopen(pynma_url).read() + "\n"
modulefile = tempfile.NamedTemporaryFile(suffix='.py')
modulefile.write(modulecode)
modulefile.flush()
fp = open(modulefile.name)
pynma = imp.load_module("code", fp, modulefile.name, (".py", "U", 1))


import scraperwiki
import json
import random
import cgi, os
import requests
import urllib2
import urllib
import re
import lxml.html
#import lxml.html.soupparser
from lxml import etree
import datetime
import time
import base64
import imp, tempfile

'''
functions:

- Return user agent
- Return proxy - does not work atm.
- Extract emails
- Unserialize an XML document to a dictionary
- load the pynma library from github to send notifications to android devices using notifymyandroid.com - https://github.com/uskr/pynma
'''

#qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING"))) # This gives us the secret variables from the description

# SETUP

pynma_url = 'https://raw.github.com/uskr/pynma/master/pynma/pynma.py'


# known media file extensions
MEDIA_EXTENSIONS = ['ai', 'aif', 'aifc', 'aiff', 'asc', 'au', 'avi', 'bcpio', 'bin', 'c', 'cc', 'ccad', 'cdf', 'class', 'cpio', 'cpt', 'csh', 'css', 'csv', 'dcr', 'dir', 'dms', 'doc', 'drw', 'dvi', 'dwg', 'dxf', 'dxr', 'eps', 'etx', 'exe', 'ez', 'f', 'f90', 'fli', 'flv', 'gif', 'gtar', 'gz', 'h', 'hdf', 'hh', 'hqx', 'ice', 'ico', 'ief', 'iges', 'igs', 'ips', 'ipx', 'jpe', 'jpeg', 'jpg', 'js', 'kar', 'latex', 'lha', 'lsp', 'lzh', 'm', 'man', 'me', 'mesh', 'mid', 'midi', 'mif', 'mime', 'mov', 'movie', 'mp2', 'mp3', 'mpe', 'mpeg', 'mpg', 'mpga', 'ms', 'msh', 'nc', 'oda', 'pbm', 'pdb', 'pdf', 'pgm', 'pgn', 'png', 'pnm', 'pot', 'ppm', 'pps', 'ppt', 'ppz', 'pre', 'prt', 'ps', 'qt', 'ra', 'ram', 'ras', 'rgb', 'rm', 'roff', 'rpm', 'rtf', 'rtx', 'scm', 'set', 'sgm', 'sgml', 'sh', 'shar', 'silo', 'sit', 'skd', 'skm', 'skp', 'skt', 'smi', 'smil', 'snd', 'sol', 'spl', 'src', 'step', 'stl', 'stp', 'sv4cpio', 'sv4crc', 'swf', 't', 'tar', 'tcl', 'tex', 'texi', 'tif', 'tiff', 'tr', 'tsi', 'tsp', 'tsv', 'txt', 'unv', 'ustar', 'vcd', 'vda', 'viv', 'vivo', 'vrml', 'w2p', 'wav', 'wmv', 'wrl', 'xbm', 'xlc', 'xll', 'xlm', 'xls', 'xlw', 'xml', 'xpm', 'xsl', 'xwd', 'xyz', 'zip']

# Browsers
desktop = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21','Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.11 Safari/535.19','Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3'
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'
'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)'
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1'
'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)'
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'
'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)']

mobile = ['Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3','Nokia6630/1.0 (2.3.129) SymbianOS/8.0 Series60/2.6 Profile/MIDP-2.0 Configuration/CLDC-1.1','Mozilla/5.0 (Linux; U; Android 2.3; en-us) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9','Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Mozilla/5.0 (Linux; U; Android 2.3.4; fr-fr; HTC Desire Build/GRJ22) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1','Opera/9.80 (Android 2.3.3; Linux; Opera Mobi/ADR-1111101157; U; es-ES) Presto/2.9.201 Version/11.50','Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)','HTC_Touch_3G Mozilla/4.0 (compatible; MSIE 6.0; Windows CE; IEMobile 7.11)','Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+']


# Get page from Google cache
def gcache_get(url):
        """Get page from google cache
        """
        return requests.get('http://www.google.com/search?&q=cache%3A' + urllib.quote(url)).text


# Return user agent
def get_user_agent(browser_type='desktop'):
    '''Returns a user agent, either for a desktop browser (default) or a mobile browser.
    Format: {'User-Agent': 'USER-AGENT'}'''
    if browser_type == 'desktop':
        return {'User-Agent':str(random.choice(desktop))}
    elif browser_type == 'mobile':
        return {'User-Agent':str(random.choice(mobile))}


#Return proxy - does not work at the moment
def get_proxy(apikey= '1608634744e31cc0af5634a7cf6ae2e6520b3d60'):
    ''' Returns a list with number of proxies
    format: {'http':ip:port '''
    proxieslist = json.loads(scraperwiki.scrape('http://api.proxyswitcheroo.com/v1/proxies?format=json&api_key='+apikey+'&num_records=10&proxy_type=T&speed_rating=5&fresh_hours=3'))
    proxies = []
    for x in proxieslist['proxies']:
        proxies.append(x['host']+':'+x['port'])
    return {'http':str(random.choice(proxies))}

#Extract emails  - From webscraping library: http://code.google.com/p/webscraping/
def extract_emails(html):
    """Extract emails and look for common obfuscations
    >>> extract_emails('')
    []
    >>> extract_emails('hello richard@sitescraper.net world')
    ['richard@sitescraper.net']
    >>> extract_emails('hello richard@<!-- trick comment -->sitescraper.net world')
    ['richard@sitescraper.net']
    >>> extract_emails('hello richard AT sitescraper DOT net world')
    ['richard@sitescraper.net']
    """
    email_re = re.compile('([\w\.-]{1,64})@(\w[\w\.-]{1,255})\.(\w+)')
    # remove comments, which can obfuscate emails
    html = re.compile('<!--.*?-->', re.DOTALL).sub('', html).replace('mailto:', '')
    emails = []
    for user, domain, ext in email_re.findall(html):
        if ext.lower() not in MEDIA_EXTENSIONS and len(ext)>=2 and not re.compile('\d').search(ext) and domain.count('.')<=3:
            email = '%s@%s.%s' % (user, domain, ext)
            if email not in emails:
                emails.append(email)

    # look for obfuscated email
    for user, domain, ext in re.compile('([\w\.-]{1,64})\s?.?AT.?\s?([\w\.-]{1,255})\s?.?DOT.?\s?(\w+)', re.IGNORECASE).findall(html):
        if ext.lower() not in MEDIA_EXTENSIONS and len(ext)>=2 and not re.compile('\d').search(ext) and domain.count('.')<=3:
            email = '%s@%s.%s' % (user, domain, ext)
            if email not in emails:
                emails.append(email)
    return emails

# unserialize an XML document to a dictionary (containing dicts, strings or lists)
def from_xml(element):
    if len(element) > 0:
        outdict = {}
        if element.get('type') == 'list':
            value = []
            for i in element:
                value.append(from_xml(i))
            outdict[element[0].tag] = value
        else:
            for i in element:
                outdict[i.tag] = from_xml(i)
        return outdict
    else:
        return element.text

# return unicode string if not null, otherwise empty string
def xunc(s):
    return unicode(s) if s else u''

# serialise the contents of a dictionary as simple XML
def to_xml(element_name, data):
    element_name = re.sub('\s', '_', element_name) # replace any spaces in the tag name with underscores
    element = etree.Element(element_name)
    if isinstance (data, dict):
        keys = data.keys()
        keys.sort() # output is in alphab order 
        for key in keys: # output simple string elements first
            if not isinstance(data[key], list) and not isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
        for key in keys: # any lists and dicts come afterwards
            if isinstance(data[key], list): # lists stay in original order
                element.set('type', 'list')
                for i in data[key]:
                    element.append(to_xml(key, i))
            elif isinstance(data[key], dict):
                element.append(to_xml(key, data[key]))
    else:
        element.text = xunc(data)
    return element

# load the pynma library - based on julian's code to load librarys from github - https://scraperwiki.com/scrapers/github_import_experiment/edit/
modulecode = urllib.urlopen(pynma_url).read() + "\n"
modulefile = tempfile.NamedTemporaryFile(suffix='.py')
modulefile.write(modulecode)
modulefile.flush()
fp = open(modulefile.name)
pynma = imp.load_module("code", fp, modulefile.name, (".py", "U", 1))


