from urllib2 import urlopen
from lxml.html import fromstring
from pickle import loads, dumps
from base64 import b64encode, b64decode
from scraperwiki.sqlite import save, select, execute, commit

JUSTPOPPED = None

class Stack:
    "A fancier stack, at some point"
    def __init__(self, startingstack):
        execute('create table if not exists stack (obj, blob);')
        commit()
        self.extend(startingstack)

    def __len__(self):
        return select('count(*) as c from stack')[0]['c']

    def pop(self):
        query = select('obj from stack where rowid = (select max(rowid) from stack)')
        obj = loads(b64decode(query[0]['obj']))
        JUSTPOPPED = obj
        return obj

    def extend(self, adding):
        save([], [{"obj": b64encode(dumps(obj))} for obj in adding], 'stack')

# Modules
class loaders:
    "This could be a separate file except that this is ScraperWiki."
    @staticmethod
    def get(url):
        return urlopen(url).read()

class parsers:
    @staticmethod
    def csv(text):
        assert false

class PageScraper:
    "The base page scraper class"
    def go(self):
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

def seed(stacklist):
    "Start everything."
    stack = Stack(stacklist)
    while len(stack) > 0:
        try:
            add_to_stack = stack.pop().go()
        except Exception:
            stack.extend([JUSTPOPPED])
            raise
        else:
            stack.extend(add_to_stack)

# Here are two ways of reusing code: Inheritance and mixins
class Get(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        loaders.get(self.url)

class Csv(Get):
    parse = parsers.csv

class GetLinks(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        return loaders.get(self.url)

    def parse(self, text):
        html = fromstring(text)
        links = html.xpath('//a/@href')
        for link in links:
            if link[0] == '/':
                link = 'http://thomaslevine.com' + link
        return map(GetLinks, links)


if __name__ == "scraper":
    execute('drop table if exists stack')
    commit()
    seed([GetLinks('http://thomaslevine.com')])from urllib2 import urlopen
from lxml.html import fromstring
from pickle import loads, dumps
from base64 import b64encode, b64decode
from scraperwiki.sqlite import save, select, execute, commit

JUSTPOPPED = None

class Stack:
    "A fancier stack, at some point"
    def __init__(self, startingstack):
        execute('create table if not exists stack (obj, blob);')
        commit()
        self.extend(startingstack)

    def __len__(self):
        return select('count(*) as c from stack')[0]['c']

    def pop(self):
        query = select('obj from stack where rowid = (select max(rowid) from stack)')
        obj = loads(b64decode(query[0]['obj']))
        JUSTPOPPED = obj
        return obj

    def extend(self, adding):
        save([], [{"obj": b64encode(dumps(obj))} for obj in adding], 'stack')

# Modules
class loaders:
    "This could be a separate file except that this is ScraperWiki."
    @staticmethod
    def get(url):
        return urlopen(url).read()

class parsers:
    @staticmethod
    def csv(text):
        assert false

class PageScraper:
    "The base page scraper class"
    def go(self):
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

def seed(stacklist):
    "Start everything."
    stack = Stack(stacklist)
    while len(stack) > 0:
        try:
            add_to_stack = stack.pop().go()
        except Exception:
            stack.extend([JUSTPOPPED])
            raise
        else:
            stack.extend(add_to_stack)

# Here are two ways of reusing code: Inheritance and mixins
class Get(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        loaders.get(self.url)

class Csv(Get):
    parse = parsers.csv

class GetLinks(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        return loaders.get(self.url)

    def parse(self, text):
        html = fromstring(text)
        links = html.xpath('//a/@href')
        for link in links:
            if link[0] == '/':
                link = 'http://thomaslevine.com' + link
        return map(GetLinks, links)


if __name__ == "scraper":
    execute('drop table if exists stack')
    commit()
    seed([GetLinks('http://thomaslevine.com')])