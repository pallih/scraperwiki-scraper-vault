from lxml.html import fromstring
#from lxml.etree import fromstring
from time import time
import requests
from scraperwiki.sqlite import save,save_var, get_var, select, commit, execute
from scraperwiki import swimport
options=swimport('options').options
keyify=swimport('keyify').keyify
randomsleep=swimport('randomsleep').randomsleep
from json import loads,dumps
strip_address = swimport('strip_address').strip_address

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
        instantiate = "%s(%s)" % (query[0]['classname'], '"""' + query[0]['url'] + '"""')
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
        save([], [{"classname": obj.__class__.__name__, "url": obj.url} for obj in adding], 'stack')

class PageScraper:
    "The base getter scraper class"
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

URLS={
  "main":"http://www.nedbank.co.za/website/content/map/branches.asp"
, "suburbs-base":"http://www.nedbank.co.za/website/content/map/getSuburbs.asp?q="
, "cities-base":"http://www.nedbank.co.za/website/content/map/getData.asp?q="
}

class Get(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        randomsleep()
        return requests.get(self.url).text

class Menu(Get):
    "Returns provinces"
    def parse(self, text):
        x=fromstring(text)
        provinces=options(x.xpath('id("province")')[0],valuename="provinceId",textname="provinceName",ignore_value="0")
        for province in provinces:
            province['provinceUrl'] = URLS['suburbs-base'] + province['provinceId']
            province['scraperrun'] = scraperrun

        save(['provinceUrl', 'scraperrun'], provinces, 'provinces')
        return [Province(p['provinceUrl']) for p in provinces]

class Province(Get):
    "Returns cities"
    def parse(self, text):
        html = fromstring(text)
        citiesParent = html.xpath('//select') #This should actually have an option child, but lxml fixes the wrong html
        assert len(citiesParent)==1
    
        cities=options(citiesParent[0],valuename="cityId",textname="cityName",ignore_value="0")
        for city in cities:
            city['provinceUrl'] = self.url
            city['cityUrl'] = URLS['cities-base'] + city['cityId']
            city['scraperrun'] = scraperrun

        save(['cityUrl', 'scraperrun'], cities, 'cities')
        return [City(c['cityUrl']) for c in cities]

class City(Get):
    "Returns branches"
    def parse(self, text):
        cleaned_text = text.replace('\n','').replace('\r','').replace('\t','')
        html = fromstring(cleaned_text)
        tds=html.xpath('//td[a]')
        branches=[branchinfo(td) for td in tds]
        for row in branches:
            row['cityUrl'] = self.url

            splitchar = '\n' if row['address'].count('\n') > 0 else ','
            splitaddress=row['address'].split(splitchar)

            l=len(splitaddress)
            if l==3:
                row['street-address'],row['subtown'],row['town2']=splitaddress
            elif l==2:
                row['street-address'],row['subtown']=splitaddress
            elif splitaddress == ['']:
                print 'Empty address'
            else:
                print row['map_Address_']
                print splitaddress
                raise ValueError('Weird address')

            if row.has_key('street-address'):
                row['street-address'] = row['street-address'].strip()

            row['address'] = strip_address(row['address'])
            row['scraperrun'] = scraperrun

        save(['scraperrun', 'cityUrl'], branches,'branches')

def branchinfo(td):
    keys=[keyify(key) for key in td.xpath('strong/text()')]
    l=len(keys)

    values=td.xpath('text()[position()>="%d"]' % l)
    address='\n'.join(td.xpath('text()[position()<"%d"]' % l))

    branch=dict(zip(keys,values))
    branch['address']=address

    maphref=td.xpath('a/attribute::href')[0]
    branch.update(parse_maphref(maphref))

    return branch

def parse_maphref(maphref):
    html=maphref.split("'")[1].replace('<br>','')
    x=fromstring(html)
    keys=["map_%s" % keyify(key) for key in x.xpath('strong/text()')]
    values=x.xpath('text()')
    return dict(zip(keys,values))

execute('CREATE TABLE IF NOT EXISTS provinces (provinceUrl TEXT )')
execute('CREATE TABLE IF NOT EXISTS cities (provinceUrl TEXT, cityUrl TEXT, FOREIGN KEY(provinceUrl) REFERENCES provinces(provinceUrl) )')
execute('CREATE TABLE IF NOT EXISTS branches (cityUrl TEXT, branchUrl TEXT, FOREIGN KEY(cityUrl) REFERENCES cities(cityUrl) )')
commit()

scraperrun = get_var('scraperrun', int(time()))
save_var('scraperrun', scraperrun)
seed([Menu(URLS['main'])])
execute('delete from swvariables where name = "scraperrun"')
commit()from lxml.html import fromstring
#from lxml.etree import fromstring
from time import time
import requests
from scraperwiki.sqlite import save,save_var, get_var, select, commit, execute
from scraperwiki import swimport
options=swimport('options').options
keyify=swimport('keyify').keyify
randomsleep=swimport('randomsleep').randomsleep
from json import loads,dumps
strip_address = swimport('strip_address').strip_address

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
        instantiate = "%s(%s)" % (query[0]['classname'], '"""' + query[0]['url'] + '"""')
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
        save([], [{"classname": obj.__class__.__name__, "url": obj.url} for obj in adding], 'stack')

class PageScraper:
    "The base getter scraper class"
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

URLS={
  "main":"http://www.nedbank.co.za/website/content/map/branches.asp"
, "suburbs-base":"http://www.nedbank.co.za/website/content/map/getSuburbs.asp?q="
, "cities-base":"http://www.nedbank.co.za/website/content/map/getData.asp?q="
}

class Get(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        randomsleep()
        return requests.get(self.url).text

class Menu(Get):
    "Returns provinces"
    def parse(self, text):
        x=fromstring(text)
        provinces=options(x.xpath('id("province")')[0],valuename="provinceId",textname="provinceName",ignore_value="0")
        for province in provinces:
            province['provinceUrl'] = URLS['suburbs-base'] + province['provinceId']
            province['scraperrun'] = scraperrun

        save(['provinceUrl', 'scraperrun'], provinces, 'provinces')
        return [Province(p['provinceUrl']) for p in provinces]

class Province(Get):
    "Returns cities"
    def parse(self, text):
        html = fromstring(text)
        citiesParent = html.xpath('//select') #This should actually have an option child, but lxml fixes the wrong html
        assert len(citiesParent)==1
    
        cities=options(citiesParent[0],valuename="cityId",textname="cityName",ignore_value="0")
        for city in cities:
            city['provinceUrl'] = self.url
            city['cityUrl'] = URLS['cities-base'] + city['cityId']
            city['scraperrun'] = scraperrun

        save(['cityUrl', 'scraperrun'], cities, 'cities')
        return [City(c['cityUrl']) for c in cities]

class City(Get):
    "Returns branches"
    def parse(self, text):
        cleaned_text = text.replace('\n','').replace('\r','').replace('\t','')
        html = fromstring(cleaned_text)
        tds=html.xpath('//td[a]')
        branches=[branchinfo(td) for td in tds]
        for row in branches:
            row['cityUrl'] = self.url

            splitchar = '\n' if row['address'].count('\n') > 0 else ','
            splitaddress=row['address'].split(splitchar)

            l=len(splitaddress)
            if l==3:
                row['street-address'],row['subtown'],row['town2']=splitaddress
            elif l==2:
                row['street-address'],row['subtown']=splitaddress
            elif splitaddress == ['']:
                print 'Empty address'
            else:
                print row['map_Address_']
                print splitaddress
                raise ValueError('Weird address')

            if row.has_key('street-address'):
                row['street-address'] = row['street-address'].strip()

            row['address'] = strip_address(row['address'])
            row['scraperrun'] = scraperrun

        save(['scraperrun', 'cityUrl'], branches,'branches')

def branchinfo(td):
    keys=[keyify(key) for key in td.xpath('strong/text()')]
    l=len(keys)

    values=td.xpath('text()[position()>="%d"]' % l)
    address='\n'.join(td.xpath('text()[position()<"%d"]' % l))

    branch=dict(zip(keys,values))
    branch['address']=address

    maphref=td.xpath('a/attribute::href')[0]
    branch.update(parse_maphref(maphref))

    return branch

def parse_maphref(maphref):
    html=maphref.split("'")[1].replace('<br>','')
    x=fromstring(html)
    keys=["map_%s" % keyify(key) for key in x.xpath('strong/text()')]
    values=x.xpath('text()')
    return dict(zip(keys,values))

execute('CREATE TABLE IF NOT EXISTS provinces (provinceUrl TEXT )')
execute('CREATE TABLE IF NOT EXISTS cities (provinceUrl TEXT, cityUrl TEXT, FOREIGN KEY(provinceUrl) REFERENCES provinces(provinceUrl) )')
execute('CREATE TABLE IF NOT EXISTS branches (cityUrl TEXT, branchUrl TEXT, FOREIGN KEY(cityUrl) REFERENCES cities(cityUrl) )')
commit()

scraperrun = get_var('scraperrun', int(time()))
save_var('scraperrun', scraperrun)
seed([Menu(URLS['main'])])
execute('delete from swvariables where name = "scraperrun"')
commit()