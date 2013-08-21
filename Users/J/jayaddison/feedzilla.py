import scraperwiki

from urllib2 import urlopen
from lxml.html import fromstring, tostring
import json
import dateutil.parser

from scraperwiki.sqlite import save, execute

scraperwiki.sqlite.execute("delete from swdata")          

# Gather articles from feedzilla API
raw = urlopen('http://api.feedzilla.com/v1/categories/3/articles.json').read()
js = json.loads(raw)

# Iterate through each article
for article in js['articles']:

    # Grab Feedzilla redirect page
    feedzilla_url = article['url']
    source_url = article['source_url']

    # Grab title
    article_title = article['title']

    # Extract publish date
    feedzilla_content = urlopen(feedzilla_url).read()
    date_text = article['publish_date']
    date = dateutil.parser.parse(date_text)

    # Find original article URL inside meta entries
    html = fromstring(feedzilla_content)
    metas = html.cssselect('meta')

    article_url = None
    for meta in metas:
        if meta.attrib.has_key('http-equiv') and meta.attrib['http-equiv'] == 'refresh':
            article_url = meta.attrib['content'][7:]

    if not article_url:
        continue

    # Filter out reviewjournal forum
    if article_url.startswith('http://eforum.reviewjournal.com'):
        continue

    # Gather original article content from source
    article_response = urlopen(article_url)

    article_url = article_response.geturl()
    article_raw = article_response.read()
    html = fromstring(article_raw)
    body = html.cssselect('body')[0]
    paras = body.cssselect('p')

    # Build up text from HTML paragraphs
    text = ''
    for para in paras:

        para_text = para.text_content() + '\n'

        # Skip paragraphs containing the string '()' (javascript)
        if '()' in para_text:
            continue

        text += para_text

    # Save data to sqlite
    row = {
        'url': article_url,
        'date': date,
        'title': article_title,
        'text': text
    }
    save(['url',], row)