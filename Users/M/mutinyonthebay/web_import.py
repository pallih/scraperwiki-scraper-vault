import sys
import imp
import urllib2
import urlparse


class WebImporter(object):

    def __init__(self, path):
        url = urlparse.urlparse(path)
        if url.scheme not in ('http', 'https'):
            raise ImportError
        self.path = path
        self._cache = {}

    @classmethod
    def register(cls):
        sys.path_hooks.append(cls)

    def _get_source_and_filename(self, name):
        rv = self._cache.get(name)
        if rv is not None:
            return rv
        url_name = name.replace('.', '/')
        if url_name.endswith('.py'):
            urls = (url_name)
        else:
            urls = (url_name + '.py', url_name + '/__init__.py')
        for filename in urls:
            try:
                url = urlparse.urljoin(self.path, filename)
                try:
                    resp = urllib2.urlopen(url)
                except urllib2.URLError:
                    continue
                if resp.code == 404:
                    continue
                rv = resp.read(), url
                self._cache[name] = rv
                return rv
            except IOError:
                continue
        raise ImportError(name)

    def get_source(self, name):
        return self._get_source_and_filename(name)[0]

    def get_filename(self, name):
        return self._get_source_and_filename(name)[1]

    def find_module(self, name, path=None):
        try:
            self._get_source_and_filename(name)
        except ImportError:
            return None
        return self

    def load_module(self, name):
        source, filename = self._get_source_and_filename(name)
        sys.modules[name] = mod = imp.new_module(name)
        mod.__loader__ = self
        mod.__file__ = filename
        if filename.endswith('/__init__.py'):
            mod.__path__ = [filename.rsplit('/', 1)[0]]
        exec source in mod.__dict__
        return mod


def add_from_url(url):
    sys.path.insert(0, url)

WebImporter.register()

add_from_url('http://seagrass.goatchurch.org.uk/~expo/pdfminer-module/')

import pdfminer
print pdfminerimport sys
import imp
import urllib2
import urlparse


class WebImporter(object):

    def __init__(self, path):
        url = urlparse.urlparse(path)
        if url.scheme not in ('http', 'https'):
            raise ImportError
        self.path = path
        self._cache = {}

    @classmethod
    def register(cls):
        sys.path_hooks.append(cls)

    def _get_source_and_filename(self, name):
        rv = self._cache.get(name)
        if rv is not None:
            return rv
        url_name = name.replace('.', '/')
        if url_name.endswith('.py'):
            urls = (url_name)
        else:
            urls = (url_name + '.py', url_name + '/__init__.py')
        for filename in urls:
            try:
                url = urlparse.urljoin(self.path, filename)
                try:
                    resp = urllib2.urlopen(url)
                except urllib2.URLError:
                    continue
                if resp.code == 404:
                    continue
                rv = resp.read(), url
                self._cache[name] = rv
                return rv
            except IOError:
                continue
        raise ImportError(name)

    def get_source(self, name):
        return self._get_source_and_filename(name)[0]

    def get_filename(self, name):
        return self._get_source_and_filename(name)[1]

    def find_module(self, name, path=None):
        try:
            self._get_source_and_filename(name)
        except ImportError:
            return None
        return self

    def load_module(self, name):
        source, filename = self._get_source_and_filename(name)
        sys.modules[name] = mod = imp.new_module(name)
        mod.__loader__ = self
        mod.__file__ = filename
        if filename.endswith('/__init__.py'):
            mod.__path__ = [filename.rsplit('/', 1)[0]]
        exec source in mod.__dict__
        return mod


def add_from_url(url):
    sys.path.insert(0, url)

WebImporter.register()

add_from_url('http://seagrass.goatchurch.org.uk/~expo/pdfminer-module/')

import pdfminer
print pdfminer