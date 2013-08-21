from scraperwiki.sqlite import save, select, execute, save_var, get_var, commit, show_tables
from scraperwiki import swimport
#from requests import session
import requests
from lxml.html import fromstring, tostring
import re
from time import time, sleep
keyify=swimport('keyify').keyify
randomsleep=swimport('randomsleep').randomsleep

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

    def first(self):
        # Query
        query = select('* from main.stack where rowid = (select min(rowid) from main.stack)')

        # Load
        instantiate = "%s(%s)" % (query[0]['classname'], '"""' + query[0]['url'] + '"""')
        print instantiate
        obj = eval(instantiate)

        return obj

    def pop0(self):
        obj = self.first()

        # Delete
        execute('delete from main.stack where rowid = (select min(rowid) from main.stack)')
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
            add_to_stack = stack.first().go()
        except Exception:
            raise
        else:
            stack.pop0()
            if add_to_stack != None:
                stack.extend(add_to_stack)

# --------------------------------------------------
# End Bucket-Wheel
# --------------------------------------------------



COLUMN_NAMES_MAP = {
    'images/Cancelled_Date.png': 'CancelledDate',
    'images/Town.png': 'Town',
    'images/Trading_Name.png': 'TradingName',
    'images/Reason.png': 'CancelledReason',
    'images/registrants_19.png': 'NCRNumber',
    'images/registrants_32.png': 'PhysicalAddress',
    'images/registrants_31.png': 'Fax',
    'images/Legal_Reg_No.png': 'LegalNumber',
    'images/registrants_38.png': 'Phone',
    'images/registrants_17.png': 'Name',
}

class Get(PageScraper):
    def __init__(self, url):
        self.url = url

    def load(self):
        randomsleep(2.5, 0.5)
        while True:
            try:
                return requests.get(self.url).text
            except requests.ConnectionError:
                randomsleep(20, 4)

class SearchResults(PageScraper):
    def __init__(self, hack):
        self.url = ''
        pass

    def load(self):
        url = 'http://www.ncr.org.za/register_of_registrants/cp.php'
        params = {
            'Registered': 'Registered',
            'name': '',
            'town': '',
            'regnum': '',
        }
        return requests.post(url, params).text

    def parse(self, text):
        delimeter = '<td height="66">'
        raw = [delimeter + td for td in text.split(delimeter)[1:]]
        return [Registrant(table) for table in raw]

class Registrant(PageScraper):
    def __init__(self, tabletext):
        self.tabletext = tabletext
        self.url = self.tabletext # Hack

    def load(self):
        return self.tabletext

    def parse(self, tabletext):
        html = fromstring(tostring(fromstring(tabletext).xpath('//table[@width="90%"]')[0]))
        tds = html.xpath('//td[img]')

        # Test img
        for td in tds:
            if len(td.xpath('img/@src')) != 1:
                print tostring(td)
                raise ValueError('We expact exactly one img/@src path inside the td.')

        # Get raw data
        data_img = {td.xpath('img/@src')[0]: td.xpath('following-sibling::td')[0].text_content() for td in tds}

        # Test column names
        if set(data_img.keys()) != set(COLUMN_NAMES_MAP.keys()):
            print data_img.keys()
            raise ValueError("The observed img srcs weren't as expected.")

        # Rename column names
        data = dict(zip([COLUMN_NAMES_MAP[k] for k in data_img.keys()], data_img.values()))

        # I could the button for whether it is registered,
        # but I already know from the search. 

        # Business premises link
        expected_onclick_prefix = "location.href='viewpremises.php?record="
        onclicks = html.xpath('//input[@value="View Business Premises"]/@onclick')

        # Test that there's only one
        if len(onclicks) != 1:
            raise ValueError('There is not exactly one input/@onclick.')
        onclick = onclicks[0]

        # Tests about the onclick syntax
        if onclick[:15] !="location.href='":
            print onclick
            raise ValueError('Value for @onclick does not start with a location.href assignment.')
        elif onclick[:len(expected_onclick_prefix)] != expected_onclick_prefix:
            print onclick
            raise ValueError('Value for @onclick does not start with a location.href=viewpremises.php?record= assignment.')
        elif onclick[-3:] !=" ' ":
            print onclick
            raise ValueError('Value for @onclick does not end with space, quote, space.')

        data['Record'] = int(onclick[len(expected_onclick_prefix):-3])
        data['ScraperRun'] = scraper_run
        save([], data, 'Registrant')
        return [BusinessPremises('http://www.ncr.org.za/register_of_registrants/viewpremises.php?record=%d' % data['Record'])]

class BusinessPremises(Get):
    def parse(self, text):
        html = fromstring(text)
        premises_found = int(re.findall(r'([0-9]+)\sBusiness Premises Found', text)[0])

        trs = html.xpath('//tr[td[img[@src="images/Trading_Name_and_Town.png"]]]/following-sibling::tr')

        if len(trs) != premises_found:
            raise ValueError('The page reports %d premises found, but I only found %d.' % (premises_found, len(trs)))

        data = []
        for tr in trs:
            name, premises_name_and_town = [td.text_content().strip() for td in tr.xpath('td')]
            row = {'name': name, 'col2raw': premises_name_and_town}
            if premises_name_and_town.count('-') == 1:
                premises_name, town = [t.strip() for t in premises_name_and_town.split('-')]
                row.update({'premises_name': premises_name, 'town': town,})
            else:
                row['enter_manually'] = 1

            row.update({'date_scraped': time(), 'ScraperRun': scraper_run, 'url': self.url, 'Record': int(self.url.split('=')[-1])})
            data.append(row)

        save([], data, 'BusinessPremises')

execute('CREATE TABLE IF NOT EXISTS Registrant (ScraperRun INTEGER, Record INTEGER)')
execute('CREATE INDEX IF NOT EXISTS RegistrantRecord ON Registrant(record)')
execute('CREATE TABLE IF NOT EXISTS BusinessPremises (ScraperRun INTEGER, Record INTEGER, FOREIGN KEY(Record) REFERENCES Registrant(Record))')
execute('CREATE INDEX IF NOT EXISTS BusinessPremisesRecord ON BusinessPremises(ScraperRun, Record)')
commit()

if "stack" not in show_tables() or select('count(*) as "c" from stack')[0]['c'] == 0:
    save_var('scraper_run', int(time()))

scraper_run = get_var('scraper_run', None)
if scraper_run == None:
    raise NameError('scraper_run is not defined.') 

seed([SearchResults(None)])
#seed([BusinessPremises('http://www.ncr.org.za/register_of_registrants/viewpremises.php?record=11296')])X