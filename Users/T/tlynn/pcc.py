import scraperwiki.sqlite
import lxml.html
import base64
import re

# over-write a record that shouldn't have been there
scraperwiki.sqlite.save(['article-id'], {'article-id':6611, 'status':'deleted',
                                         'summary': '','title': '','publications': '', 'complainant': ''})

results_per_page = 100

page_num = 1

class Stop(Exception):
    pass

def only(seq):
    assert len(seq)==1
    return seq[0]

def extract_article_id(url):
    """Extracts and decodes the article ID from the URL."""
    blah, article_id = url.split('=', 1)
    return int(base64.urlsafe_b64decode(article_id))


try:
    while True:
        URL = ('http://www.pcc.org.uk/advanced_search.html'
               '?keywords=e&page=%d&num=%d&publication=x'
               '&decision=x&image.x=0&image.y=13') % (page_num, results_per_page)
        page_num += 1
        page = lxml.html.parse(URL).getroot()
        table = only(page.cssselect('table[width=510]')) # get table of articles
        found_some = False
        for td in table.cssselect('td'):
            links = td.cssselect('a[href^="/news/index.html?article="]') # looks for all links to articles, returns array
            if not links:
                continue
            found_some = True
            link = only(links)
            title = link.text # title of case - easy
            pattern = r'(.*?)\xa0\((.*?)\)$'
            m = re.match(pattern, title)
            if m:
                title, publications = m.groups() # returns a tuple of all the matches
            else:
                raise ValueError("Publication? %r" % title)
            status = None
            m = re.match('([A-Z][a-z]+) - ', title)
            if m:
                status = m.group(1)
                title = title[m.end():]
            else:
                title = title
            for vs in 'v', 'v.', 'versus', 'vs', 'vs.':
                vs = ' %s ' % vs
                if vs in title:
                    complainant, title = title.split(vs, 1)
                    break
            else:
                complainant = title
            url = link.attrib['href']
            summaries = [p.text for p in td.cssselect('p') if p.text and p.text.replace(u'\xa0', '').strip()]
            if not summaries:
                summaries = [br.tail for br in td.cssselect('br') if br.tail and br.tail.replace(u'\xa0', '').strip()]
            if summaries:
                summary = only(summaries)
            else:
                summary = None
            article_id = extract_article_id(url)
            data = {
                'url': 'http://www.pcc.org.uk' + url,
                'article-id': article_id,
                'summary': summary,
                'status': status,
                'title': title,
                'publications': publications,  # '/'-separated
                'complainant': complainant,
            }
            scraperwiki.sqlite.save(['article-id'], data)
            if article_id == 1767:
                raise Stop("just old PCC press releases after this point")
        if not found_some:
            raise Stop("no articles found at "+URL)

except Stop, e:
    print e
import scraperwiki.sqlite
import lxml.html
import base64
import re

# over-write a record that shouldn't have been there
scraperwiki.sqlite.save(['article-id'], {'article-id':6611, 'status':'deleted',
                                         'summary': '','title': '','publications': '', 'complainant': ''})

results_per_page = 100

page_num = 1

class Stop(Exception):
    pass

def only(seq):
    assert len(seq)==1
    return seq[0]

def extract_article_id(url):
    """Extracts and decodes the article ID from the URL."""
    blah, article_id = url.split('=', 1)
    return int(base64.urlsafe_b64decode(article_id))


try:
    while True:
        URL = ('http://www.pcc.org.uk/advanced_search.html'
               '?keywords=e&page=%d&num=%d&publication=x'
               '&decision=x&image.x=0&image.y=13') % (page_num, results_per_page)
        page_num += 1
        page = lxml.html.parse(URL).getroot()
        table = only(page.cssselect('table[width=510]')) # get table of articles
        found_some = False
        for td in table.cssselect('td'):
            links = td.cssselect('a[href^="/news/index.html?article="]') # looks for all links to articles, returns array
            if not links:
                continue
            found_some = True
            link = only(links)
            title = link.text # title of case - easy
            pattern = r'(.*?)\xa0\((.*?)\)$'
            m = re.match(pattern, title)
            if m:
                title, publications = m.groups() # returns a tuple of all the matches
            else:
                raise ValueError("Publication? %r" % title)
            status = None
            m = re.match('([A-Z][a-z]+) - ', title)
            if m:
                status = m.group(1)
                title = title[m.end():]
            else:
                title = title
            for vs in 'v', 'v.', 'versus', 'vs', 'vs.':
                vs = ' %s ' % vs
                if vs in title:
                    complainant, title = title.split(vs, 1)
                    break
            else:
                complainant = title
            url = link.attrib['href']
            summaries = [p.text for p in td.cssselect('p') if p.text and p.text.replace(u'\xa0', '').strip()]
            if not summaries:
                summaries = [br.tail for br in td.cssselect('br') if br.tail and br.tail.replace(u'\xa0', '').strip()]
            if summaries:
                summary = only(summaries)
            else:
                summary = None
            article_id = extract_article_id(url)
            data = {
                'url': 'http://www.pcc.org.uk' + url,
                'article-id': article_id,
                'summary': summary,
                'status': status,
                'title': title,
                'publications': publications,  # '/'-separated
                'complainant': complainant,
            }
            scraperwiki.sqlite.save(['article-id'], data)
            if article_id == 1767:
                raise Stop("just old PCC press releases after this point")
        if not found_some:
            raise Stop("no articles found at "+URL)

except Stop, e:
    print e
