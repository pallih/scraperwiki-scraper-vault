from lxml.html import fromstring, tostring
from time import time, sleep
import requests
from scraperwiki.sqlite import save,save_var, get_var, select, commit, execute
import re

# --------------------------------------------------
# Begin Bucket-Wheel
# --------------------------------------------------
class Stack:
    "A fancier stack, at some point"
    def __init__(self, startingstack):
        try:
            assert self.__len__() > 0
        except:
            self.extend(startingstack)

    def __len__(self):
        return select('count(*) as c from main.stack')[0]['c']

    def last(self):
        # Query
        query = select('* from main.stack where rowid = (select max(rowid) from main.stack)')

        # Load
        instantiate = "%s(%s)" % (query[0]['classname'], '"""' + query[0]['offset'] + '"""')
        print instantiate
        obj = eval(instantiate)

        return obj

    def pop(self):
        obj = self.last()

        # Delete
        execute('delete from main.stack where rowid = (select max(rowid) from main.stack)')
        commit()

        return obj

    def extend(self, adding):
        save([], [{"classname": obj.__class__.__name__, "offset": obj.offset} for obj in adding], 'stack')

class PageScraper:
    "The base getter scraper class"
    def __init__(self, offset):
        self.offset = offset
    def go(self):
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

def seed(stacklist):
    "Start everything."
    stack = Stack(stacklist)

    while len(stack) > 0:
        try:
            add_to_stack = stack.last().go()
        except Exception:
            raise
        else:
            stack.pop()
            if add_to_stack != None:
                stack.extend(add_to_stack)

# --------------------------------------------------
# End Bucket-Wheel
# --------------------------------------------------

class Directory(PageScraper):
    def load(self):
        url = self.offset
        return requests.get(url).text
    def parse(self, text):
        onclicks = fromstring(text).xpath('id("bizdir_directory")/descendant::a/@onclick')
        offsets = [c.replace('bizdir_change_listings_page(', '').replace(')', '') for c in onclicks]
        return [Result(offset) for offset in offsets]

def element(node, xpath):
    out = node.xpath(xpath)
    if len(out) == 1:
        return out[0]
    else:
        raise ValueError('%d nodes returned (not exactly one)' % len(out))

class Result(PageScraper):
    URL = 'http://www.chicagoistheworld.org/notalone/wp-content/plugins/business-directory/requests.php'
    def load(self):
        sleep(2)
        params = {
            'offset': self.offset,
            'action': 'ChangePage',
            #rndval:1336868938020
        }
        return requests.post(self.URL, params).text
    def parse(self, text):
        text = '\n'.join(text.split('\n')[2:4]).replace("document.getElementById('bizdir_directory').innerHTML = '", '')
        text = re.sub(r"';\s*document.getElementById('bizdir_search').disabled = false;", '', text).replace("&nbsp;&nbsp;8</div>';", '&nbsp;&nbsp;8</div>').replace("\\'", '')
        html = fromstring(text)
        bizdir_directory = []
        for tr in html.cssselect('#bizdir_directory tr'):
            try:
                assert tr.xpath('count(td)') == 1
                name = element(tr, 'td/b').text_content()
                description = element(tr, 'td/p/text()')
                bizdir_directory.append({'name': name, 'description': description, 'pageOffset': self.offset, 'scraperrun': scraperrun})
            except:
                print tostring(tr)
                raise
        save(['scraperrun', 'pageOffset', 'name'], bizdir_directory, 'organizations')

scraperrun = get_var('scraperrun', time())
save_var('scraperrun', scraperrun)
seed([Directory('http://www.chicagoistheworld.org/notalone/directory-of-youth-organizations/')])
execute('DROP TABLE stack')
execute('DROP TABLE swvariables')
commit()from lxml.html import fromstring, tostring
from time import time, sleep
import requests
from scraperwiki.sqlite import save,save_var, get_var, select, commit, execute
import re

# --------------------------------------------------
# Begin Bucket-Wheel
# --------------------------------------------------
class Stack:
    "A fancier stack, at some point"
    def __init__(self, startingstack):
        try:
            assert self.__len__() > 0
        except:
            self.extend(startingstack)

    def __len__(self):
        return select('count(*) as c from main.stack')[0]['c']

    def last(self):
        # Query
        query = select('* from main.stack where rowid = (select max(rowid) from main.stack)')

        # Load
        instantiate = "%s(%s)" % (query[0]['classname'], '"""' + query[0]['offset'] + '"""')
        print instantiate
        obj = eval(instantiate)

        return obj

    def pop(self):
        obj = self.last()

        # Delete
        execute('delete from main.stack where rowid = (select max(rowid) from main.stack)')
        commit()

        return obj

    def extend(self, adding):
        save([], [{"classname": obj.__class__.__name__, "offset": obj.offset} for obj in adding], 'stack')

class PageScraper:
    "The base getter scraper class"
    def __init__(self, offset):
        self.offset = offset
    def go(self):
        textblob = self.load()
        morepages = self.parse(textblob)
        return morepages

def seed(stacklist):
    "Start everything."
    stack = Stack(stacklist)

    while len(stack) > 0:
        try:
            add_to_stack = stack.last().go()
        except Exception:
            raise
        else:
            stack.pop()
            if add_to_stack != None:
                stack.extend(add_to_stack)

# --------------------------------------------------
# End Bucket-Wheel
# --------------------------------------------------

class Directory(PageScraper):
    def load(self):
        url = self.offset
        return requests.get(url).text
    def parse(self, text):
        onclicks = fromstring(text).xpath('id("bizdir_directory")/descendant::a/@onclick')
        offsets = [c.replace('bizdir_change_listings_page(', '').replace(')', '') for c in onclicks]
        return [Result(offset) for offset in offsets]

def element(node, xpath):
    out = node.xpath(xpath)
    if len(out) == 1:
        return out[0]
    else:
        raise ValueError('%d nodes returned (not exactly one)' % len(out))

class Result(PageScraper):
    URL = 'http://www.chicagoistheworld.org/notalone/wp-content/plugins/business-directory/requests.php'
    def load(self):
        sleep(2)
        params = {
            'offset': self.offset,
            'action': 'ChangePage',
            #rndval:1336868938020
        }
        return requests.post(self.URL, params).text
    def parse(self, text):
        text = '\n'.join(text.split('\n')[2:4]).replace("document.getElementById('bizdir_directory').innerHTML = '", '')
        text = re.sub(r"';\s*document.getElementById('bizdir_search').disabled = false;", '', text).replace("&nbsp;&nbsp;8</div>';", '&nbsp;&nbsp;8</div>').replace("\\'", '')
        html = fromstring(text)
        bizdir_directory = []
        for tr in html.cssselect('#bizdir_directory tr'):
            try:
                assert tr.xpath('count(td)') == 1
                name = element(tr, 'td/b').text_content()
                description = element(tr, 'td/p/text()')
                bizdir_directory.append({'name': name, 'description': description, 'pageOffset': self.offset, 'scraperrun': scraperrun})
            except:
                print tostring(tr)
                raise
        save(['scraperrun', 'pageOffset', 'name'], bizdir_directory, 'organizations')

scraperrun = get_var('scraperrun', time())
save_var('scraperrun', scraperrun)
seed([Directory('http://www.chicagoistheworld.org/notalone/directory-of-youth-organizations/')])
execute('DROP TABLE stack')
execute('DROP TABLE swvariables')
commit()