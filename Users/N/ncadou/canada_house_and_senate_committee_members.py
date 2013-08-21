import re
import urllib2

from datetime import datetime, date
from lxml import html
from urlparse import parse_qsl, urlparse

import scraperwiki

ABBR_RE = re.compile(r'^(.+) \(([A-Z0-9]{3,5})\)$')

SCRAPE_PREVIOUS_SESSIONS = False
LANGS = dict(E='en', F='fr')
TEXT_MODE = 2

PARL_BASE_URL = 'http://www.parl.gc.ca'
HOUSE_BASE_URL = '/'.join([PARL_BASE_URL, 'CommitteeBusiness'])
HOUSE_INDEX_URL = '/'.join([HOUSE_BASE_URL, 'CommitteeList.aspx?Language=%s&Mode=%d'])
JOINT_INDEX_URL = '&'.join([HOUSE_INDEX_URL, 'CmteInst=joint'])
SENATE_BASE_PATH = '/'.join(['SenCommitteeBusiness'])
SENATE_BASE_URL = '/'.join([PARL_BASE_URL, SENATE_BASE_PATH, 'Default.aspx'])
SENATE_INDEX_URL = '?'.join([SENATE_BASE_URL, 'Language=%s'])

committees = dict()
last_run = datetime.utcnow()


def parse_all(*langs):
    for lang in langs:
        parse_house_committees(lang)
        parse_senate_committees(lang)
        parse_joint_committees(lang)


def parse_house_committees(lang):
    sort_sessions = lambda (e, a, l, p): e.text_content()
    parse_committees(lang, HOUSE_INDEX_URL % (lang, TEXT_MODE), 'div[id="divParliamentSessionSwitcher"]',
                     sort_sessions, HOUSE_BASE_URL, parse_house_session)


def parse_senate_committees(lang):
    sort_sessions = lambda (e, a, l, p): e.text_content().split('(', 1)[1]
    parse_committees(lang, SENATE_INDEX_URL % lang, 'div[class="bannertext"] div[id="menu_child"]',
                     sort_sessions, SENATE_BASE_PATH, parse_senate_session)


def parse_joint_committees(lang):
    sort_sessions = lambda (e, a, l, p): e.text_content()
    parse_committees(lang, JOINT_INDEX_URL % (lang, TEXT_MODE), 'div[id="divParliamentSessionSwitcher"]',
                     sort_sessions, HOUSE_BASE_URL, parse_joint_session)


def parse_committees(lang, index_url, sessions_selector, sort_sessions, target_url, parse_session):
    index_page = scraperwiki.scrape(index_url)
    root = html.fromstring(index_page)
    sessions = root.cssselect(sessions_selector)[0]
    for (element, attribute, link, position) in sorted(sessions.iterlinks(), key=sort_sessions, reverse=True):
        if attribute == 'href' and target_url in link:
            url = urlparse(link)
            query = dict(parse_qsl(url.query))
            session_id = _session_id(query)
            text = element.text_content().replace(u'\xa0', u' ')
            dates = map(_to_date, text[text.index('(')+1:-1].split(' - '))
            if dates[1] and not SCRAPE_PREVIOUS_SESSIONS:
                break
            parse_session(LANGS[lang], session_id, dates, link, root=None if dates[1] else root)


def parse_house_session(lang, session_id, dates, url, root=None):
    member_url_fn = lambda url: _parl_url(url.replace('CommitteeHome', 'CommitteeMembership'))
    parse_session(lang, session_id, dates, url, '//ul[contains(@class, "CommitteeListItem")]', member_url_fn, 'Cmte', parse_house_committee, root)


def parse_senate_session(lang, session_id, dates, url, root=None):
    member_url_fn = lambda url: '/'.join([PARL_BASE_URL, SENATE_BASE_PATH, _parl_url(url.replace('CommitteeHome', 'CommitteeMembers'))])
    parse_session(lang, session_id, dates, url, '//ul[contains(@class, "committeelist")][1]', member_url_fn, 'comm_id', parse_senate_committee, root)


def parse_joint_session(lang, session_id, dates, url, root=None):
    member_url_fn = lambda url: _parl_url(url.replace('CommitteeHome', 'CommitteeMembership'))
    parse_session(lang, session_id, dates, url, '//ul[contains(@class, "CommitteeListItem")]', member_url_fn, 'Cmte', parse_joint_committee, root)


def parse_session(lang, session_id, dates, url, committees_xpath, member_url_fn, committee_id_param, parse_committee, root=None):
    scraperwiki.sqlite.save(table_name='parl_session', unique_keys=['id'],
                            data=dict(id=session_id, start_date=dates[0], end_date=dates[1], last_run=last_run))
    print 'Session', session_id, dates, lang
    if not root:
        index_page = scraperwiki.scrape(url)
        root = html.fromstring(index_page)
    committee_list = root.xpath(committees_xpath)[0]
    for (element, attribute, url, position) in committee_list.iterlinks():
        url = member_url_fn(url)
        committee_id = _committee_id(url, committee_id_param)
        name = element.text_content().replace(u'\xa0', u' ').strip()
        acronym = ABBR_RE.search(name).groups()[1]
        parent = None
        if 'SubCommitteeItemText' in element.getparent().get('class', ''):
            parent_url = element.getparent().getparent().getparent().getparent().cssselect('a')[0].get('href')
            parent = _committee_id(parent_url, committee_id_param)
        elif 'Subcommittee' in element.text:
            parent_url = element.xpath('../../preceding-sibling::node()[not(self::text())][1]/a/@href')[0]
            parent = _committee_id(parent_url, committee_id_param)
        parse_committee(lang, session_id, committee_id, acronym, name, parent, url)


def parse_house_committee(lang, session_id, committee_id, acronym, name, parent, url):
    parse_committee(lang, session_id, 'house', committee_id, acronym, name, parent, url, 'ul[class="MemberRoles"]',
                    './/span[contains(text(), "Chair")]/..',
                    './/span[contains(text(), "Vice-Chairs")]/..',
                    './/span[contains(text(), "Members")]/..',
                    parse_house_members)


def parse_senate_committee(lang, session_id, committee_id, acronym, name, parent, url):
    parse_committee(lang, session_id, 'senate', committee_id, acronym, name, parent, url, 'table[class="currentmembertable"]',
                    './/td/span[contains(text(), "Chair") and not(contains(text(), "Deputy"))]/..',
                    './/td/span[contains(text(), "Deputy Chair")]/..',
                    './/td[a and not(span[contains(@class, "redtitle")])]',
                    parse_senate_members)


def parse_joint_committee(lang, session_id, committee_id, acronym, name, parent, url):
    parse_committee(lang, session_id, 'joint', committee_id, acronym, name, parent, url, 'ul[class="MemberRoles"]',
                    './/span[contains(text(), "Chair")]/..',
                    './/span[contains(text(), "Vice-Chairs")]/..',
                    './/span[contains(text(), "Members")]/..',
                    parse_house_members)


def parse_committee(lang, session_id, committee_type, committee_id, acronym, name, parent, url, members_selector,
                     chairs_xpath, vice_chairs_xpath, members_xpath, parse_members):
    print 'SubCommittee' if parent else 'Committee', committee_id, name, parent, url
    data = committees.setdefault(committee_id, dict(type=committee_type, id=committee_id, acronym=acronym, session_id=session_id, parent=parent, last_run=last_run))
    data['name_%s' % lang] = name
    scraperwiki.sqlite.save(table_name='committee', unique_keys=['type', 'id', 'session_id'], data=data)
    if lang != 'en':
        return
    page = scraperwiki.scrape(url)
    root = html.fromstring(page)
    roles = root.cssselect(members_selector)
    if not roles:
        return
    roles = roles[0]
    chair = roles.xpath(chairs_xpath)
    if chair:
        parse_members(url, session_id, committee_type, committee_id, chair, chair=True)
    vice_chairs = roles.xpath(vice_chairs_xpath)
    if vice_chairs:
        parse_members(url, session_id, committee_type, committee_id, vice_chairs, vice_chair=True)
    members = roles.xpath(members_xpath)
    if members:
        parse_members(url, session_id, committee_type, committee_id, members)


def parse_senate_members(referer, session_id, committee_type, committee_id, section, **kwargs):
    from itertools import chain
    for element in [e for cell in section for e in cell.cssselect('a')]:
        url = element.get('href')
        member_id = int(dict(parse_qsl(url[url.index('?')+1:]))['senator_id'])
        member_name = element.text.strip()
        data = dict(type='senator', id=member_id, session_id=session_id,
                    committee_type=committee_type, committee_id=committee_id, name=member_name, last_run=last_run)
        data.update(kwargs)
        scraperwiki.sqlite.save(table_name='member', unique_keys=['type', 'id', 'session_id', 'committee_type', 'committee_id'], data=data)
        print 'Senator', kwargs.keys() or ['member'], member_name, member_id


def parse_house_members(referer, session_id, committee_type, committee_id, section, **kwargs):
    for (element, attribute, url, position) in section[0].iterlinks():
        member_id = int(dict(parse_qsl(url[url.index('?')+1:]))['ResourceID'])
        member_name = element.text.strip()
        member_type = _member_type(url, referer) if committee_type == 'joint' else 'mp'
        data = dict(type=member_type, id=member_id, session_id=session_id, committee_type=committee_type,
                    committee_id=committee_id, name=member_name, last_run=last_run)
        data.update(kwargs)
        scraperwiki.sqlite.save(table_name='member', unique_keys=['type', 'id', 'session_id', 'committee_type', 'committee_id'], data=data)
        print 'Member (%s)' % member_type, kwargs.keys() or ['member'], member_name, member_id


def _member_type(url, referer):
    if PARL_BASE_URL not in url:
        url = PARL_BASE_URL + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'ScraperWiki')
    req.add_header('Referer', referer) 
    f = urllib2.urlopen(req)
    page = f.read()
    f.close()
    if 'Senator Profile' in page:
        return 'senator'
    elif 'MP Profile' in page:
        return 'mp'


def _to_date(text):
    if text.strip().endswith('sent') or not text:
        return None
    else:
        return date(*map(int, text.split('-')))


def _committee_id(url, param):
    url_ = urlparse(url)
    query = dict(parse_qsl(url_.query))
    return query[param]


def _parl_url(url):
    if url.startswith('/'):
        return PARL_BASE_URL + url
    return url


def _session_id(query):
    if 'parl' in query:
        return '-'.join([query['parl'], query['ses']])
    elif 'Parl' in query:
        return '-'.join([query['Parl'], query['Ses']])


parse_all(*LANGS.keys())

