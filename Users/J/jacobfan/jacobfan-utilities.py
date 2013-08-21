import re
import time
import random
import datetime
import lxml.html
import unicodedata
import httplib
import urllib
import urllib2


#============== Utility Functions Begin ==============

def remove_html(string):
    return re.sub("<.*?>", "", string)

def clean(string):
    return safestr(clean_without_safestr(string))

def clean_without_safestr(string):
    return reduce_whitespaces(remove_html(string)).strip()

def reduce_whitespaces(string):
    return re.sub(r"(\n|\t|\r|\s)+"," ",string).strip()


def split_and_clean(string, delim=","):
    return delim.join(clean_list(string.split(delim)))

def clean_list(list):
    return [clean(item) for item in list]


def safestr(string):
    if isinstance(string, unicode):
        return unicode(unicodedata.normalize('NFKD', string).encode('ascii', 'ignore'), 'ascii')
    else:
        return string


def extract_multiple_line_text(node):
    breakline_placeholder = '62fce0d061ba7dea4972e37a54a012f8'
    p_nodes = node.xpath("p")
    br_nodes = node.xpath("br")
    for para in p_nodes:
        para.text = "%s%s" % (para.text, breakline_placeholder)

    for br in br_nodes:
        br.text = breakline_placeholder
    result = node.text_content()
    result = reduce_whitespaces(result.strip())
    result = result.replace(breakline_placeholder, "\n")

    for para in p_nodes:
        para.text = para.text.replace(breakline_placeholder, "")

    for br in br_nodes:
        br.text = br.text.replace(breakline_placeholder, "")

    return safestr(result)


def extract_node_text(node, is_clean=True):
    if not is_clean:
        clean_func = lambda a: a
    else:
        clean_func = clean
    return clean_func(node.text_content())

def extract_text(root_node, cssselector, is_multiple=False, empty_if_not_exist=False, is_clean=True):
    if not is_clean:
        clean_func = lambda a: a
    else:
        clean_func = clean
    selected_nodes = root_node.cssselect(cssselector)
    if selected_nodes:
        if is_multiple:
            return [clean_func(selected_node.text_content()) for selected_node in selected_nodes]
        else:
            return clean_func(selected_nodes[0].text_content())
    elif empty_if_not_exist:
        if is_multiple:
            return []
        else:
            return ""
    else:
        raise Exception("Failed to find a node which matches: %s" % cssselector)


def list_distinct(l):
    return list(set(l))


def limit_length(text, length):
    if len(text) > length:
        text = text[:length]
    return text


class Scrape:
    def __init__(self, headers=(), print_log=False, delay=(0.3, 1.5), proxy_config=None):
        self.headers = headers
        self.print_log = print_log
        self.delay = delay
        self.proxy_config = proxy_config
        if self.proxy_config:
            if self.proxy_config.get("username", None):
                username_password = "%(username)s:%(password)s@" % self.proxy_config
            else:
                username_password = ""
            print self.proxy_config
            self.proxy_config["proxies"]["http"] = self.proxy_config["proxies"]["http"] % username_password

        if not getattr(self, "cache", None):
            self.cache = None

    def __call__(self, url, params=None, headers=(), use_cache=True):
        if self.print_log:
            print "grab %s, %s, headers=%s" % (url, params, self.headers + headers)
        content = None
        if use_cache and self.cache:
            content = self.cache.get(url, params)

        if not content:
            time.sleep(random.uniform(self.delay[0], self.delay[1]))
            retry_times = 0
            done = False
            while not done:
                try:
                    if self.proxy_config:
                        proxy_handler = urllib2.ProxyHandler(self.proxy_config["proxies"])
                        proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
                        opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
                    else:
                        opener = urllib2.build_opener()
                    req = urllib2.Request(url)
                    for header in self.headers + headers:
                        req.headers[header[0]] = header[1]
                    if params:
                        r = opener.open(req, urllib.urlencode(params))
                    else:
                        r = opener.open(req)
                    content = r.read()
                    done = True
                except httplib.BadStatusLine, e:
                    print "BadStatusLine:", e
                    return None
                except urllib2.HTTPError, e:
                    print "HTTPError:", e
                    if str(e.code).startswith("5"):
                        if retry_times < 3:
                            retry_times += 1
                            time.sleep(5)
                        else:
                            raise
                    else:
                        return None

            if self.cache:
                self.cache.put(url, params, content)
        return content

scrape = Scrape()

def scrape2(url, params=None, headers=()):
    retry_times = 0
    while True:
        try:
            req = urllib2.Request(url)
            for header in headers:
                req.headers[header[0]] = header[1]
            if params:
                r = urllib2.urlopen(req, urllib.urlencode(params))
            else:
                r = urllib2.urlopen(req)
            final_url = r.geturl()
            content = r.read()
            return content, final_url
        except:
            if retry_times <= 3:
                retry_times += 1
                time.sleep(5)
            else:
                raise


def as_lxml_node(html_content, encoding="utf-8"):
    root = lxml.html.fromstring(unicode(html_content, encoding))
    return root


def detect_encoding(html_content):
    # TODO: make a better version which does not ignore Content-Type
    # http://stackoverflow.com/questions/2686709/encoding-in-python-with-lxml-complex-solution
    from bs4 import UnicodeDammit
    ud = UnicodeDammit(html_content, is_html=True)
    return ud.original_encoding


def detect_page_encoding(page_url):
    html_content = scrape(page_url)
    print detect_encoding(html_content), page_url


def parse_first_last_name(name, contact_num):
    result = {}
    names = name.split()
    if len(names) == 1:
        result["contact%dfirst" % contact_num] = names[0]
    elif len(names) >= 2:
        result["contact%dfirst" % contact_num] = " ".join(names[:-1])
        result["contact%dlast" % contact_num] = names[-1]
    return result


def initialize_my_data(fields, sourceurl):
    my_data = {}
    for field in fields:
        my_data[field] = ""
    my_data["datescraped"] = clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
    my_data["sourceurl"] = sourceurl
    return my_data

#============== Utility Functions End ==============

