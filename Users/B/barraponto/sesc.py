from urlparse import urlsplit,parse_qs
from urllib import urlencode
from lxml.html import parse
import re
import scraperwiki

def fix_charset(ugly_unicode_string):
    return unicode(ugly_unicode_string.strip().encode('iso-8859-1'), 'utf-8')

class SESCSchedule:
    baseurl = 'http://www.sescsp.org.br/sesc/programa_new/busca.cfm'

    basepage = parse(baseurl).getroot()

    units = {}
    for option in basepage.cssselect('select[name="unidade_id"] option'):
        value = int(option.get('value'))
        units[value] = fix_charset(option.text_content())

    def __init__(self, unit):
        # checks whether it is a valid unit
        if unit in SESCSchedule.units:
            self.unit = unit
            self.events = []
        else:
            # TODO: document the "unit doesn't exist" error
            raise

    def get_page_url(self, page):
        return SESCSchedule.baseurl + '?' + urlencode({'unidade_id': self.unit, 'page': page})

    def get_events(self, page):
        self.page_url = self.get_page_url(page)
        self.page_tree = parse(self.page_url).getroot()        
        entries = self.page_tree.cssselect('#box')
        if entries:
            print 'found {0} entries in page {1}'.format(len(entries), page)
            page_events = []
            for entry_count,entry in enumerate(entries):
                if entry.cssselect('.tit2'):
                    events = SESCProgram(entry, page).events
                elif entry.cssselect('.tit'):
                    events = [SESCEvent(entry, page).dictionaries]
                else:
                    events = []
                page_events.extend(events)
                print '{0} of {1} entries have been scraped'.format(entry_count, len(entries))
            # let the world know the scraper was succesful
            return page_events
        else:
            print 'no more events in unit {0} schedule'.format(self.unit)
            return 0
        print 'done scraping page {0}'.format(page)

    def __iter__(self, page=1):
        events = self.get_events(page)
        while events:
            yield events
            page += 1
            events = self.get_events(page)
        print 'iteration complete over {0} pages'.format(page)

class SESCProgram:
    def __init__(self, tree, page):
        self.program = fix_charset(tree.cssselect('.tit')[0].text_content()).rstrip(fix_charset(tree.cssselect('.tit font')[0].text_content()))
        self.program_id = re.search(r'[0-9]+', fix_charset(tree.cssselect('.tit')[0].get('onclick'))).group(),
        self.events = []

        for k,title in enumerate(tree.cssselect('.tit2')):
            self.events.append({
                'title': fix_charset(title[0].text_content()),
                'id': parse_qs(urlsplit(title[0].cssselect('a')[0].get('href')).query)['programacao_id'][0],
                'date_string': re.sub('\s+', ' ', fix_charset(tree.cssselect('.data tr')[2 * k].text_content())),
                'program': self.program,
                'program_id': self.program_id,
                'page': page # this will change as the source data is updated, here only for debug reasons
            })

class SESCEvent:
    baseurl = 'http://www.sescsp.org.br/sesc/programa_new/mostra_detalhe.cfm'

    def __init__(self, tree, page):
        self.title = fix_charset(tree.cssselect('.tit')[0].text_content())
        self.date_string = re.sub('\s+', ' ', fix_charset(tree.cssselect('.data td')[0].text_content()))
        self.id = parse_qs(urlsplit(tree.cssselect('.tit a')[0].get('href')).query)['programacao_id'][0]

        self.url = SESCEvent.baseurl + '?' + urlencode({'programacao_id': self.id})

        self.tree = parse(self.url).getroot()

        precos = [fix_charset(cell.text_content().strip()) for cell in self.tree.cssselect('.preco')]

        self.precos = zip(precos[1::2], precos[2::2])

        self.dictionaries = {'title': self.title, 'date_string': self.date_string, 'id': self.id, 'page': page, 'precos': self.precos}


# let's get Campinas (16) schedule

campinas = SESCSchedule(16)

for page,events in enumerate(campinas):
    print 'now saving page {0}...'.format(page)
    scraperwiki.sqlite.save(['id'], events)
    print 'done saving page {0}'.format(page)from urlparse import urlsplit,parse_qs
from urllib import urlencode
from lxml.html import parse
import re
import scraperwiki

def fix_charset(ugly_unicode_string):
    return unicode(ugly_unicode_string.strip().encode('iso-8859-1'), 'utf-8')

class SESCSchedule:
    baseurl = 'http://www.sescsp.org.br/sesc/programa_new/busca.cfm'

    basepage = parse(baseurl).getroot()

    units = {}
    for option in basepage.cssselect('select[name="unidade_id"] option'):
        value = int(option.get('value'))
        units[value] = fix_charset(option.text_content())

    def __init__(self, unit):
        # checks whether it is a valid unit
        if unit in SESCSchedule.units:
            self.unit = unit
            self.events = []
        else:
            # TODO: document the "unit doesn't exist" error
            raise

    def get_page_url(self, page):
        return SESCSchedule.baseurl + '?' + urlencode({'unidade_id': self.unit, 'page': page})

    def get_events(self, page):
        self.page_url = self.get_page_url(page)
        self.page_tree = parse(self.page_url).getroot()        
        entries = self.page_tree.cssselect('#box')
        if entries:
            print 'found {0} entries in page {1}'.format(len(entries), page)
            page_events = []
            for entry_count,entry in enumerate(entries):
                if entry.cssselect('.tit2'):
                    events = SESCProgram(entry, page).events
                elif entry.cssselect('.tit'):
                    events = [SESCEvent(entry, page).dictionaries]
                else:
                    events = []
                page_events.extend(events)
                print '{0} of {1} entries have been scraped'.format(entry_count, len(entries))
            # let the world know the scraper was succesful
            return page_events
        else:
            print 'no more events in unit {0} schedule'.format(self.unit)
            return 0
        print 'done scraping page {0}'.format(page)

    def __iter__(self, page=1):
        events = self.get_events(page)
        while events:
            yield events
            page += 1
            events = self.get_events(page)
        print 'iteration complete over {0} pages'.format(page)

class SESCProgram:
    def __init__(self, tree, page):
        self.program = fix_charset(tree.cssselect('.tit')[0].text_content()).rstrip(fix_charset(tree.cssselect('.tit font')[0].text_content()))
        self.program_id = re.search(r'[0-9]+', fix_charset(tree.cssselect('.tit')[0].get('onclick'))).group(),
        self.events = []

        for k,title in enumerate(tree.cssselect('.tit2')):
            self.events.append({
                'title': fix_charset(title[0].text_content()),
                'id': parse_qs(urlsplit(title[0].cssselect('a')[0].get('href')).query)['programacao_id'][0],
                'date_string': re.sub('\s+', ' ', fix_charset(tree.cssselect('.data tr')[2 * k].text_content())),
                'program': self.program,
                'program_id': self.program_id,
                'page': page # this will change as the source data is updated, here only for debug reasons
            })

class SESCEvent:
    baseurl = 'http://www.sescsp.org.br/sesc/programa_new/mostra_detalhe.cfm'

    def __init__(self, tree, page):
        self.title = fix_charset(tree.cssselect('.tit')[0].text_content())
        self.date_string = re.sub('\s+', ' ', fix_charset(tree.cssselect('.data td')[0].text_content()))
        self.id = parse_qs(urlsplit(tree.cssselect('.tit a')[0].get('href')).query)['programacao_id'][0]

        self.url = SESCEvent.baseurl + '?' + urlencode({'programacao_id': self.id})

        self.tree = parse(self.url).getroot()

        precos = [fix_charset(cell.text_content().strip()) for cell in self.tree.cssselect('.preco')]

        self.precos = zip(precos[1::2], precos[2::2])

        self.dictionaries = {'title': self.title, 'date_string': self.date_string, 'id': self.id, 'page': page, 'precos': self.precos}


# let's get Campinas (16) schedule

campinas = SESCSchedule(16)

for page,events in enumerate(campinas):
    print 'now saving page {0}...'.format(page)
    scraperwiki.sqlite.save(['id'], events)
    print 'done saving page {0}'.format(page)