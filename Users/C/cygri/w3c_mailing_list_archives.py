# A scraper for the W3C's mailing list archives.
# 
# Scrapes a pre-configured selection of mailing lists.
#
# Keeps track of already scraped messages over
# multiple scraper runs, so it should only ever
# fetch each message once.

lists = ['public-rdb2rdf-wg', 'public-rdf-dawg']

import scraperwiki
import lxml.html
import re
import datetime
import rfc822

def parse(url):
    html = scraperwiki.scrape(url)
    # Hack: lxml trips over certain Unicode characters when they
    # appear in @href. They sometimes occur when an email subject
    # contained Unicode characters. We work around it by just
    # snipping a part out of the URL. Example:
    # http://lists.w3.org/Archives/Public/public-rdb2rdf-wg/2009Dec/0017.html
    html = re.sub('(<a href="mailto:[^"]+)\?Subject=[^"]*', '\g<1>', html)
    root = lxml.html.fromstring(html)
    root.make_links_absolute(url)
    return root

def get_archive(url):
    root = parse(url)
    archive = []
    for row in root.cssselect('tr'):
        cells = row.cssselect('td')
        if len(cells) == 0: continue
        archive.append(cells[0].cssselect('a')[0].get('href'))
    return archive

def get_messages(url):
    root = parse(url)
    messages = []
    for link in root.cssselect('.messages-list li a[href]'):
        messages.append(link.get('href'))
    return messages

def parse_receivers(s):
    splits = re.split('((?:"[^"]*"|[^,"]+)+)', s)
    result = []
    for i in range(len(splits)):
        if i % 2 == 0: continue
        result.append(splits[i].strip())
    return result

def get_message(list_id, url):
    root = parse(url)
#    print lxml.html.tostring(root)
    message = {}
    message['url'] = url
    message['list'] = list_id
    message['subject'] = root.cssselect('h1')[0].text_content()
    raw_from = root.cssselect('#from dfn')[0].tail
    if (raw_from == ': <'):
        message['from'] = None
    else:
        message['from'] = raw_from.replace(': ', '').replace(' <', '')
    message['from_email'] = re.search('^mailto:([^?]*)', root.cssselect('#from a')[0].get('href')).group(1)
    for dfn in root.cssselect('.links li'):
        if dfn.cssselect('dfn')[0].text == 'In reply to':
            message['in-reply-to'] = dfn.cssselect('a')[0].get('href')
    message['mid'] = root.cssselect('#message-id dfn')[0].tail.replace(': <', '').replace('>\n', '')
    date = root.cssselect('#date')[0].text_content().replace('Date: ', '')
    message['date'] = datetime.datetime.fromtimestamp(rfc822.mktime_tz(rfc822.parsedate_tz(date))).isoformat()
    try:
        message['to'] = parse_receivers(root.cssselect('#to')[0].text_content().replace('To: ', ''))
    except IndexError:
        message['to'] = []
    try:
        message['cc'] = parse_receivers(root.cssselect('#cc')[0].text_content().replace('cc: ', ''))
    except IndexError:
        message['cc'] = []
    # FIXME: Don't drop the whole message just because of one broken
    # Unicode char! Test case here:
    # http://lists.w3.org/Archives/Public/public-rdb2rdf-wg/2011Mar/0093.html
    try:
        message['body'] = root.cssselect('#body')[0].text_content()
    except UnicodeDecodeError:
        message['body'] = 'UnicodeDecodeError'
    message['links'] = []
    for a in root.cssselect('#body a[href]'):
        href = a.get('href')
        if href.startswith('mailto:'): continue
        message['links'].append(href)
    return message

def save_message(message):
    url = message['url']
    for receiver in message['to']:
        scraperwiki.sqlite.save(['url', 'receiver'], {'url': url, 'receiver': receiver}, 'message_to')
    for receiver in message['cc']:
        scraperwiki.sqlite.save(['url', 'receiver'], {'url': url, 'receiver': receiver}, 'message_cc')
    for link in message['links']:
        scraperwiki.sqlite.save(['url', 'link'], {'url': url, 'link': link}, 'message_links')
    del message['to']
    del message['cc']
    del message['links']
    scraperwiki.sqlite.save(['url'], message, 'messages')

def is_page_complete(page_url):
    return scraperwiki.sqlite.get_var(page_url) == 'complete'

def set_page_complete(page_url):
    scraperwiki.sqlite.save_var(page_url, 'complete')

def get_latest_done_msg(page_url):
    return scraperwiki.sqlite.get_var(page_url, None)

def set_latest_done_msg(page_url, msgnum):
    scraperwiki.sqlite.save_var(page_url, msgnum)

def scrape_list(list_id):
    url = 'http://lists.w3.org/Archives/Public/' + list_id + '/'
    
    pages = get_archive(url)
    print str(len(pages)) + ' archive pages for ' + list_id
    # Start with the last page so we can do incremental crawling
    pages.reverse()
    
    previous_page_url = None
    for page_url in pages:
        if is_page_complete(page_url):
            print 'Skipping page ' + page_url
            continue
        if previous_page_url:
            set_page_complete(previous_page_url)
            print 'Completed page ' + previous_page_url
        previous_page_url = page_url
    
        messages = get_messages(page_url)
        # Start with the last message so we can do incremental crawling
        messages.reverse()
        print str(len(messages)) + ' messages on page ' + page_url
    
        msg_done = get_latest_done_msg(page_url)
        if msg_done: print '... latest done: ' + msg_done
    
        for message_url in messages:
            msgnum = re.search('(\d\d\d\d).html$', message_url).group(1)
            if (msgnum <= msg_done):
                print 'Skipping message ' + message_url
                continue
    
            message = get_message(list_id, message_url)
            save_message(message)
            set_latest_done_msg(page_url, msgnum)
            print 'Saved: ' + message['date'] + (' ' + message['from'] if message['from'] else '') + ' <' + message['from_email'] + '>: ' + message['subject']

#print get_message('public-rdb2rdf-wg', 'http://lists.w3.org/Archives/Public/public-rdb2rdf-wg/2009Oct/0035.html')
for list_id in lists: scrape_list(list_id)