from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save, select, execute, commit
from json import dumps

# The object that was just popped
justpopped = None

class Stack:
    "A fancier stack, at some point"
    def __init__(self, startingstack):
        try:
            assert self.__len__() > 0
        except:
            self.extend(startingstack)

    def __len__(self):
        return select('count(*) as c from stack')[0]['c']

    def pop(self):
        query = select('* from stack where rowid = (select max(rowid) from stack)')
        instantiate = "%s(%s)" % (query[0]['classname'], dumps(query[0]['url']))
        print instantiate
        obj = eval(instantiate)
        justpopped = obj
        return obj

    def extend(self, adding):
        #print adding[0].__class__.__name__
        print adding[0].url
        save([], [{"classname": obj.__class__.__name__, "url": obj.url} for obj in adding], 'stack')

class Get:
    "The base getter scraper class"
    def __init__(self, url):
        self.url = url

    def load(self):
        return urlopen(self.url).read()

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
            if justpopped != None:
                stack.extend([justpopped])
            raise
        else:
            stack.extend(add_to_stack)
