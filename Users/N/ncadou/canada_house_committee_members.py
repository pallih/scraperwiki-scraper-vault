import scraperwiki
from datetime import datetime, date
from lxml import html
from urlparse import parse_qsl, urlparse

SCRAPE_PREVIOUS_SESSIONS = False
LANGS = dict(E='en', F='fr')
TEXT_MODE = 2

PARL_BASE_URL = 'http://www.parl.gc.ca'
BASE_URL = '/'.join([PARL_BASE_URL, 'CommitteeBusiness'])
INDEX_BASE_URL = '/'.join([BASE_URL, 'CommitteeList.aspx?Language=%s&Mode=%d'])

committees = dict()
last_run = datetime.utcnow()


def parse_all(*langs):
    for lang in langs:
        index_page = scraperwiki.scrape(INDEX_BASE_URL % (lang, TEXT_MODE))
        root = html.fromstring(index_page)
        sessions = root.cssselect('div[id="divParliamentSessionSwitcher"]')[0]
        sort_sessions = lambda (e, a, l, p): e.text_content()
        for (element, attribute, link, position) in sorted(sessions.iterlinks(), key=sort_sessions, reverse=True):
            if attribute == 'href' and BASE_URL in link:
                url = urlparse(link)
                query = dict(parse_qsl(url.query))
                session_id = '-'.join([query['Parl'], query['Ses']])
                text = element.text_content().replace(u'\xa0', u' ')
                dates = map(_to_date, text[text.index('(')+1:-1].split(' - '))
                if dates[1] and not SCRAPE_PREVIOUS_SESSIONS:
                    break
                parse_session(LANGS[lang], session_id, dates, link, root=None if dates[1] else root)


def parse_session(lang, session_id, dates, url, root=None):
    scraperwiki.sqlite.save(table_name='parl_session', unique_keys=['id'],
                            data=dict(id=session_id, start_date=dates[0], end_date=dates[1], last_run=last_run))
    print 'Session', session_id, dates, lang
    if not root:
        index_page = scraperwiki.scrape(url)
        root = html.fromstring(index_page)
    committee_list = root.cssselect('ul[class="CommitteeListItem"]')[0]
    for (element, attribute, url, position) in committee_list.iterlinks():
        url = _parl_url(url.replace('CommitteeHome', 'CommitteeMembership'))
        committee_id = _committee_id(url)
        name = element.text_content().replace(u'\xa0', u' ')
        if 'SubCommitteeItemText' in element.getparent().get('class'):
            parent_url = element.getparent().getparent().getparent().getparent().cssselect('a')[0].get('href')
            parent = _committee_id(parent_url)
        else:
            parent = None
        parse_committee(lang, session_id, committee_id, name, parent, url)


def parse_committee(lang, session_id, committee_id, name, parent, url):
    print 'SubCommittee' if parent else 'Committee', committee_id, name, parent, url
    data = committees.setdefault(committee_id, dict(id=committee_id, session_id=session_id, parent=parent, last_run=last_run))
    data['name_%s' % lang] = name
    scraperwiki.sqlite.save(table_name='committee', unique_keys=['id', 'session_id'], data=data)
    if lang != 'en':
        return
    page = scraperwiki.scrape(url)
    root = html.fromstring(page)
    roles = root.cssselect('ul[class="MemberRoles"]')
    if not roles:
        return
    roles = roles[0]
    chair = roles.xpath('.//span[contains(text(), "Chair")]/..')
    if chair:
        parse_members(session_id, committee_id, chair[0], chair=True)
    vice_chairs = roles.xpath('.//span[contains(text(), "Vice-Chairs")]/..')
    if vice_chairs:
        parse_members(session_id, committee_id, vice_chairs[0], vice_chair=True)
    members = roles.xpath('.//span[contains(text(), "Members")]/..')
    if members:
        parse_members(session_id, committee_id, members[0])


def parse_members(session_id, committee_id, section, **kwargs):
    for (element, attribute, url, position) in section.iterlinks():
        member_id = int(dict(parse_qsl(url[url.index('?')+1:]))['ResourceID'])
        member_name = element.text.strip()
        data = dict(id=member_id, session_id=session_id, committee_id=committee_id, name=member_name, last_run=last_run)
        data.update(kwargs)
        scraperwiki.sqlite.save(table_name='member', unique_keys=['id', 'session_id', 'committee_id'], data=data)
        print 'Member', kwargs.keys() or ['member'], member_name, member_id


def _to_date(text):
    if text.strip().endswith('sent'):
        return None
    else:
        return date(*map(int, text.split('-')))


def _committee_id(url):
    url_ = urlparse(url)
    query = dict(parse_qsl(url_.query))
    return query['Cmte']


def _parl_url(url):
    if url.startswith('/'):
        return PARL_BASE_URL + url
    return url


parse_all(*LANGS.keys())

import scraperwiki
from datetime import datetime, date
from lxml import html
from urlparse import parse_qsl, urlparse

SCRAPE_PREVIOUS_SESSIONS = False
LANGS = dict(E='en', F='fr')
TEXT_MODE = 2

PARL_BASE_URL = 'http://www.parl.gc.ca'
BASE_URL = '/'.join([PARL_BASE_URL, 'CommitteeBusiness'])
INDEX_BASE_URL = '/'.join([BASE_URL, 'CommitteeList.aspx?Language=%s&Mode=%d'])

committees = dict()
last_run = datetime.utcnow()


def parse_all(*langs):
    for lang in langs:
        index_page = scraperwiki.scrape(INDEX_BASE_URL % (lang, TEXT_MODE))
        root = html.fromstring(index_page)
        sessions = root.cssselect('div[id="divParliamentSessionSwitcher"]')[0]
        sort_sessions = lambda (e, a, l, p): e.text_content()
        for (element, attribute, link, position) in sorted(sessions.iterlinks(), key=sort_sessions, reverse=True):
            if attribute == 'href' and BASE_URL in link:
                url = urlparse(link)
                query = dict(parse_qsl(url.query))
                session_id = '-'.join([query['Parl'], query['Ses']])
                text = element.text_content().replace(u'\xa0', u' ')
                dates = map(_to_date, text[text.index('(')+1:-1].split(' - '))
                if dates[1] and not SCRAPE_PREVIOUS_SESSIONS:
                    break
                parse_session(LANGS[lang], session_id, dates, link, root=None if dates[1] else root)


def parse_session(lang, session_id, dates, url, root=None):
    scraperwiki.sqlite.save(table_name='parl_session', unique_keys=['id'],
                            data=dict(id=session_id, start_date=dates[0], end_date=dates[1], last_run=last_run))
    print 'Session', session_id, dates, lang
    if not root:
        index_page = scraperwiki.scrape(url)
        root = html.fromstring(index_page)
    committee_list = root.cssselect('ul[class="CommitteeListItem"]')[0]
    for (element, attribute, url, position) in committee_list.iterlinks():
        url = _parl_url(url.replace('CommitteeHome', 'CommitteeMembership'))
        committee_id = _committee_id(url)
        name = element.text_content().replace(u'\xa0', u' ')
        if 'SubCommitteeItemText' in element.getparent().get('class'):
            parent_url = element.getparent().getparent().getparent().getparent().cssselect('a')[0].get('href')
            parent = _committee_id(parent_url)
        else:
            parent = None
        parse_committee(lang, session_id, committee_id, name, parent, url)


def parse_committee(lang, session_id, committee_id, name, parent, url):
    print 'SubCommittee' if parent else 'Committee', committee_id, name, parent, url
    data = committees.setdefault(committee_id, dict(id=committee_id, session_id=session_id, parent=parent, last_run=last_run))
    data['name_%s' % lang] = name
    scraperwiki.sqlite.save(table_name='committee', unique_keys=['id', 'session_id'], data=data)
    if lang != 'en':
        return
    page = scraperwiki.scrape(url)
    root = html.fromstring(page)
    roles = root.cssselect('ul[class="MemberRoles"]')
    if not roles:
        return
    roles = roles[0]
    chair = roles.xpath('.//span[contains(text(), "Chair")]/..')
    if chair:
        parse_members(session_id, committee_id, chair[0], chair=True)
    vice_chairs = roles.xpath('.//span[contains(text(), "Vice-Chairs")]/..')
    if vice_chairs:
        parse_members(session_id, committee_id, vice_chairs[0], vice_chair=True)
    members = roles.xpath('.//span[contains(text(), "Members")]/..')
    if members:
        parse_members(session_id, committee_id, members[0])


def parse_members(session_id, committee_id, section, **kwargs):
    for (element, attribute, url, position) in section.iterlinks():
        member_id = int(dict(parse_qsl(url[url.index('?')+1:]))['ResourceID'])
        member_name = element.text.strip()
        data = dict(id=member_id, session_id=session_id, committee_id=committee_id, name=member_name, last_run=last_run)
        data.update(kwargs)
        scraperwiki.sqlite.save(table_name='member', unique_keys=['id', 'session_id', 'committee_id'], data=data)
        print 'Member', kwargs.keys() or ['member'], member_name, member_id


def _to_date(text):
    if text.strip().endswith('sent'):
        return None
    else:
        return date(*map(int, text.split('-')))


def _committee_id(url):
    url_ = urlparse(url)
    query = dict(parse_qsl(url_.query))
    return query['Cmte']


def _parl_url(url):
    if url.startswith('/'):
        return PARL_BASE_URL + url
    return url


parse_all(*LANGS.keys())

