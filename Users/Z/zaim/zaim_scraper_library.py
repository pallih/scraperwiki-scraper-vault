""" Zaim's Scraper Library
"""

import mechanize
import logging
import sys

from lxml import etree
from lxml.html import soupparser


logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger('zaim_scraper_library')
log.setLevel(logging.INFO)


class Parser(object):
    selectors = {}

    def log(self, msg, *args, **kwargs):
        msg = '%s %s' % (self.__class__.__name__, msg)
        log.info(msg, *args, **kwargs)

    def parse(self, root):
        # NOTE: should make parser configurable?
        if isinstance(root, basestring):
            root = soupparser.fromstring(root)
        matches = {}
        for k in self.selectors:
            matches[k] = root.cssselect(self.selectors[k])
            self.log('"%s": %d matches', self.selectors[k], len(matches[k]))
        for e in self.elements(matches):
            try:
                yield self.transform(e)
            except AssertionError, err:
                self.log('error: %s', str(err))
                self.log('error: [HTML]%s[/HTML]', etree.tostring(e))
                continue

    def elements(self, matches):
        raise NotImplementedError

    def transform(self, elem):
        raise NotImplementedError


class Scraper(object):
    form_name = 'aspnetForm'
    form_data = {}

    def __init__(self, url):
        self._url = url
        self._mech = mechanize.Browser()
        self._response = None
        self._body = None
        self._info = None

    def log(self, msg, *args, **kwargs):
        msg = '%s %s' % (self._url, msg)
        log.info(msg, *args, **kwargs)

    def open(self):
        self.log('opening url')
        self._mech.open(self._url)
        self.setup_form()
        self.set_response(self._mech.response())

    def submit(self, form):
        self.setup_form()

        # set data from self.form_data defaults
        for k in self.form_data:
            try:
                control = self._mech.find_control(name=k)
            except mechanize.ControlNotFoundError:
                # auto create inputs
                self._mech.new_control('hidden', k, {'value':self.form_data[k]})
            else:
                self._mech[k] = self.form_data[k]

        # set data from `form` arg
        for k in form:
            self.log('setting input %s = %s', k, form[k])
            self._mech[k] = form[k]

        self.log('submitting "%s" form', self.form_name)
        self.set_response(self._mech.submit())
        return self._response

    def response(self):
        return self._response

    def body(self):
        return self._body

    def info(self):
        return self._info

    def set_response(self, res):
        self._response = res
        self._body = res.read()
        self._info = res.info()
        self._response.seek(0)

    def setup_form(self):
        self._mech.select_form(name=self.form_name)
        self._mech.set_all_readonly(False)

    def scrape(self):
        raise NotImplementedError
