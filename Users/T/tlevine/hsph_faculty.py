'''Bucket-Wheel demo

I've been thinking about a framework for web scrapers.
I've been calling it Bucket-Wheel.

Using Bucket-Wheel involves creating a class for each
different type of page during the scrape. For example,
you might have a page for the main index, a page for
the section index, a page for the subsection index and
so on) and managing them with a queue.

Each class has a load method and a parse method. The
former returns some sort of raw file (raw html for web
scrapers). The latter takes this raw file and returns
either nothing or a list of page type objects.

You instantiate an objects for the seminal pages and
push them to a queue. The queue is stored in the
database, so the script resumes nicely after a crash.
The script stops running when the queue is empty.

Here's an implementation of it and a demo of the use.
I had to do several weird things to get around
ScraperWiki's bizarities, so it is very disgusting
right now. In particular,

* I put Bucket-Wheel in the same file as the scraper
* I faked transaction management
* I didn't use proper adapters or converters.

Tom
'''
from time import sleep
from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save, select, execute, commit, show_tables
from json import dumps
from unidecode import unidecode


# --------------------------------------------------
# Begin Bucket-Wheel
# --------------------------------------------------

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
        # Query
        query = select('* from stack where rowid = (select max(rowid) from stack)')

        # Load
        instantiate = "%s(%s)" % (query[0]['classname'], dumps(query[0]['url']))
        print instantiate
        obj = eval(instantiate)

        # Delete
        execute('delete from stack where rowid = (select max(rowid) from stack)')
        commit()

        # Remember in case of error
        justpopped = obj

        return obj

    def extend(self, adding):
        save([], [{"classname": obj.__class__.__name__, "url": obj.url} for obj in adding], 'stack')

class PageScraper:
    def go(self):
        sleep(1)
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

class Get(PageScraper):
    "The base getter scraper class"
    def __init__(self, url):
        self.url = url

    def load(self):
        return urlopen(self.url).read()

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
            if add_to_stack != None:
                stack.extend(add_to_stack)

# --------------------------------------------------
# End Bucket-Wheel
# --------------------------------------------------


DOMAIN = 'http://www.hsph.harvard.edu'

class Index(Get):
    def parse(self, text):
        html = fromstring(text)
        hrefs = html.xpath('id("maincol")/descendant::ul[@class="landing"]/li/a/@href')
        urls = [DOMAIN + href for href in hrefs]
        return map(Faculty, urls)

class Faculty(Get):
    def parse(self, text):
        html = fromstring(text)
        try:
            individual = html.get_element_by_id('individual')
        except Exception, msg:
            data1 = {
                "url": self.url,
            }
            save([], {"url": self.url, "column": "individual", "msg": msg}, 'errors')
        else:
            data1 = {
                "url": self.url,
                "title": individual.cssselect('h2')[0].text,
                "contact": '\n'.join([div.text_content() for div in individual.xpath('div')])
            }

        try:
            data1["department"] = individual.cssselect('h3 > a')[0].text
        except Exception, msg:
            save([], {"url": self.url, "column": "department", "msg": msg}, 'errors')

        data2 = []
        for content_div in html.cssselect('#maincol > div.content'):
            try:
                key = content_div.xpath('h3')[0].text_content()
                value = content_div.xpath('div[@class="text"]')[0].text_content()
            except Exception, msg:
                save([], {"url": self.url, "column": "content_div", "msg": msg}, 'errors')
            else:
                data2.append({
                    "key": key,
                    "value": value,
                    "url": self.url
                })

        save(['url'], {"url": url, "plaintext": html.get_element_by_id('maincol').text_content()}, 'maincol')
        save(['url'], data1, 'faculty2')
        execute('CREATE TABLE IF NOT EXISTS descriptions ( url, key TEXT, value TEXT, FOREIGN KEY(url) REFERENCES faculty2(url))')
        save(['url'], data2, 'descriptions')

def clean_description_keys():
    KEY_GLOB_PAIRS = [
        ('affiliations', '*affiliations*'),
        ('courses', '*courses*'),
        ('research', '*research*'),
        ('research', '*interests*'),
        ('honors', '*honors*'),
        ('publications', '*publications*'),
        ('education', '*education*'),
        ('introduction', 'introduction*'),
        ('introduction', 'biography'),
    ]

    try:
        execute('ALTER TABLE descriptions ADD COLUMN key_cleaned TEXT')
    except:
        pass
    else:
        commit()

    for pair in KEY_GLOB_PAIRS:
        execute('UPDATE descriptions SET key_cleaned = "%s" WHERE lower(key) GLOB "%s" AND key_cleaned IS NULL' % pair)
        commit()

# Scraping
#seed([Index(DOMAIN + '/faculty/')])
#clean_description_keys()

# Topic modelling
from gensim import corpora, models, similarities
reference_person = 'http://www.hsph.harvard.edu/faculty/jack-dennerlein/'

def find_similar_research():
    research = select('url, value from maincol where url != ?;', [reference_person])
    research.extend(select('url, value from descriptions where url = ?;', [reference_person]))
    documents = [row['value'].strip() for row in research]
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    vec = corpus.pop() #The person being compared to
    
    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus])
    sims = index[tfidf[vec]]

    save(['url'], [{"url": row[0], "similarity": row[1][0]} for row in zip([row['url'] for row in research], list(enumerate(sims)))], 'similarity')

find_similar_research()'''Bucket-Wheel demo

I've been thinking about a framework for web scrapers.
I've been calling it Bucket-Wheel.

Using Bucket-Wheel involves creating a class for each
different type of page during the scrape. For example,
you might have a page for the main index, a page for
the section index, a page for the subsection index and
so on) and managing them with a queue.

Each class has a load method and a parse method. The
former returns some sort of raw file (raw html for web
scrapers). The latter takes this raw file and returns
either nothing or a list of page type objects.

You instantiate an objects for the seminal pages and
push them to a queue. The queue is stored in the
database, so the script resumes nicely after a crash.
The script stops running when the queue is empty.

Here's an implementation of it and a demo of the use.
I had to do several weird things to get around
ScraperWiki's bizarities, so it is very disgusting
right now. In particular,

* I put Bucket-Wheel in the same file as the scraper
* I faked transaction management
* I didn't use proper adapters or converters.

Tom
'''
from time import sleep
from urllib2 import urlopen
from lxml.html import fromstring
from scraperwiki.sqlite import save, select, execute, commit, show_tables
from json import dumps
from unidecode import unidecode


# --------------------------------------------------
# Begin Bucket-Wheel
# --------------------------------------------------

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
        # Query
        query = select('* from stack where rowid = (select max(rowid) from stack)')

        # Load
        instantiate = "%s(%s)" % (query[0]['classname'], dumps(query[0]['url']))
        print instantiate
        obj = eval(instantiate)

        # Delete
        execute('delete from stack where rowid = (select max(rowid) from stack)')
        commit()

        # Remember in case of error
        justpopped = obj

        return obj

    def extend(self, adding):
        save([], [{"classname": obj.__class__.__name__, "url": obj.url} for obj in adding], 'stack')

class PageScraper:
    def go(self):
        sleep(1)
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

class Get(PageScraper):
    "The base getter scraper class"
    def __init__(self, url):
        self.url = url

    def load(self):
        return urlopen(self.url).read()

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
            if add_to_stack != None:
                stack.extend(add_to_stack)

# --------------------------------------------------
# End Bucket-Wheel
# --------------------------------------------------


DOMAIN = 'http://www.hsph.harvard.edu'

class Index(Get):
    def parse(self, text):
        html = fromstring(text)
        hrefs = html.xpath('id("maincol")/descendant::ul[@class="landing"]/li/a/@href')
        urls = [DOMAIN + href for href in hrefs]
        return map(Faculty, urls)

class Faculty(Get):
    def parse(self, text):
        html = fromstring(text)
        try:
            individual = html.get_element_by_id('individual')
        except Exception, msg:
            data1 = {
                "url": self.url,
            }
            save([], {"url": self.url, "column": "individual", "msg": msg}, 'errors')
        else:
            data1 = {
                "url": self.url,
                "title": individual.cssselect('h2')[0].text,
                "contact": '\n'.join([div.text_content() for div in individual.xpath('div')])
            }

        try:
            data1["department"] = individual.cssselect('h3 > a')[0].text
        except Exception, msg:
            save([], {"url": self.url, "column": "department", "msg": msg}, 'errors')

        data2 = []
        for content_div in html.cssselect('#maincol > div.content'):
            try:
                key = content_div.xpath('h3')[0].text_content()
                value = content_div.xpath('div[@class="text"]')[0].text_content()
            except Exception, msg:
                save([], {"url": self.url, "column": "content_div", "msg": msg}, 'errors')
            else:
                data2.append({
                    "key": key,
                    "value": value,
                    "url": self.url
                })

        save(['url'], {"url": url, "plaintext": html.get_element_by_id('maincol').text_content()}, 'maincol')
        save(['url'], data1, 'faculty2')
        execute('CREATE TABLE IF NOT EXISTS descriptions ( url, key TEXT, value TEXT, FOREIGN KEY(url) REFERENCES faculty2(url))')
        save(['url'], data2, 'descriptions')

def clean_description_keys():
    KEY_GLOB_PAIRS = [
        ('affiliations', '*affiliations*'),
        ('courses', '*courses*'),
        ('research', '*research*'),
        ('research', '*interests*'),
        ('honors', '*honors*'),
        ('publications', '*publications*'),
        ('education', '*education*'),
        ('introduction', 'introduction*'),
        ('introduction', 'biography'),
    ]

    try:
        execute('ALTER TABLE descriptions ADD COLUMN key_cleaned TEXT')
    except:
        pass
    else:
        commit()

    for pair in KEY_GLOB_PAIRS:
        execute('UPDATE descriptions SET key_cleaned = "%s" WHERE lower(key) GLOB "%s" AND key_cleaned IS NULL' % pair)
        commit()

# Scraping
#seed([Index(DOMAIN + '/faculty/')])
#clean_description_keys()

# Topic modelling
from gensim import corpora, models, similarities
reference_person = 'http://www.hsph.harvard.edu/faculty/jack-dennerlein/'

def find_similar_research():
    research = select('url, value from maincol where url != ?;', [reference_person])
    research.extend(select('url, value from descriptions where url = ?;', [reference_person]))
    documents = [row['value'].strip() for row in research]
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    vec = corpus.pop() #The person being compared to
    
    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus])
    sims = index[tfidf[vec]]

    save(['url'], [{"url": row[0], "similarity": row[1][0]} for row in zip([row['url'] for row in research], list(enumerate(sims)))], 'similarity')

find_similar_research()