import scraperwiki

# Blank Python

"""
Stupid Python Trick - import modules over the web.
Author: Christian Wyglendowski
License: MIT (http://dowski.com/mit.txt)
"""

import httplib
import imp
import sys

def register_domain(name):
    WebImporter.registered_domains.add(name)
    parts = reversed(name.split('.'))
    whole = []
    for part in parts:
        whole.append(part)
        WebImporter.domain_modules.add(".".join(whole))

class WebImporter(object):
    domain_modules = set()
    registered_domains = set()

    def find_module(self, fullname, path=None):
        if fullname in self.domain_modules:
            return self
        if fullname.rsplit('.')[0] not in self.domain_modules:
            return None
        try:
            r = self._do_request(fullname, method="HEAD")
        except ValueError:
            return None
        else:
            r.close()
            if r.status == 200:
                return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = imp.new_module(fullname)
        mod.__loader__ = self
        sys.modules[fullname] = mod
        if fullname not in self.domain_modules:
            url = "http://%s%s" % self._get_host_and_path(fullname)
            mod.__file__ = url
            r = self._do_request(fullname)
            code = r.read()
            assert r.status == 200
            exec code in mod.__dict__
        else:
            mod.__file__ = "[fake module %r]" % fullname
            mod.__path__ = []
        return mod

    def _do_request(self, fullname, method="GET"):
        host, path = self._get_host_and_path(fullname)
        c = httplib.HTTPConnection(host)
        c.request(method, path)
        return c.getresponse()

    def _get_host_and_path(self, fullname):
        tld, domain, rest = fullname.split('.', 2)
        path = "/%s.py" % rest.replace('.', '/')
        return ".".join([domain, tld]), path

sys.meta_path = [WebImporter()]
register_domain('dowski.com')
from com.dowski import test
print test.fooimport scraperwiki

# Blank Python

"""
Stupid Python Trick - import modules over the web.
Author: Christian Wyglendowski
License: MIT (http://dowski.com/mit.txt)
"""

import httplib
import imp
import sys

def register_domain(name):
    WebImporter.registered_domains.add(name)
    parts = reversed(name.split('.'))
    whole = []
    for part in parts:
        whole.append(part)
        WebImporter.domain_modules.add(".".join(whole))

class WebImporter(object):
    domain_modules = set()
    registered_domains = set()

    def find_module(self, fullname, path=None):
        if fullname in self.domain_modules:
            return self
        if fullname.rsplit('.')[0] not in self.domain_modules:
            return None
        try:
            r = self._do_request(fullname, method="HEAD")
        except ValueError:
            return None
        else:
            r.close()
            if r.status == 200:
                return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = imp.new_module(fullname)
        mod.__loader__ = self
        sys.modules[fullname] = mod
        if fullname not in self.domain_modules:
            url = "http://%s%s" % self._get_host_and_path(fullname)
            mod.__file__ = url
            r = self._do_request(fullname)
            code = r.read()
            assert r.status == 200
            exec code in mod.__dict__
        else:
            mod.__file__ = "[fake module %r]" % fullname
            mod.__path__ = []
        return mod

    def _do_request(self, fullname, method="GET"):
        host, path = self._get_host_and_path(fullname)
        c = httplib.HTTPConnection(host)
        c.request(method, path)
        return c.getresponse()

    def _get_host_and_path(self, fullname):
        tld, domain, rest = fullname.split('.', 2)
        path = "/%s.py" % rest.replace('.', '/')
        return ".".join([domain, tld]), path

sys.meta_path = [WebImporter()]
register_domain('dowski.com')
from com.dowski import test
print test.foo