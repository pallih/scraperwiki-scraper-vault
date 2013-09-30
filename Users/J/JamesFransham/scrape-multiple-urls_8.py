"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:


urls = """


http://www.economist.com/blogs/prospero/2012/06/quick-study-satoshi-kanazawa-intelligence
http://www.economist.com/blogs/prospero/2012/01/quick-study-alastair-smith-political-tyranny
http://www.economist.com/blogs/prospero/2012/06/ridley-scotts-prometheus


""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    cleaned = re.sub('<.*?>', '', html)  # remove tags
    #cleaned = ' '.join(cleaned.split())  # collapse whitespace
    return cleaned


for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        heading1 = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        heading1 = [gettext(heading) for heading in heading1]

        heading3 = re.findall("<span>(.*?)</span>", page, re.MULTILINE)
        heading3 = [gettext(heading) for heading in heading3]

        heading2 = re.findall("<time>(.)</time>", page, re.MULTILINE)
        heading2 = [gettext(heading) for heading in heading3]

        #for tag_elm in soup.find_all('div'):
        #print tag_elm.find('span', {'class' : 'ID2'})
        #<time class="date-created">Jan 24th 2013, 10:44</time>

        data = {'url': url, 'heading1': heading1, 'heading3':heading3, 'heading2':heading2}
        scraperwiki.sqlite.save(['url', 'heading1'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re


# The URLs we're going to scrape:


urls = """


http://www.economist.com/blogs/prospero/2012/06/quick-study-satoshi-kanazawa-intelligence
http://www.economist.com/blogs/prospero/2012/01/quick-study-alastair-smith-political-tyranny
http://www.economist.com/blogs/prospero/2012/06/ridley-scotts-prometheus


""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    """Return the text within html, removing any HTML tags it contained."""
    cleaned = re.sub('<.*?>', '', html)  # remove tags
    #cleaned = ' '.join(cleaned.split())  # collapse whitespace
    return cleaned


for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        heading1 = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        heading1 = [gettext(heading) for heading in heading1]

        heading3 = re.findall("<span>(.*?)</span>", page, re.MULTILINE)
        heading3 = [gettext(heading) for heading in heading3]

        heading2 = re.findall("<time>(.)</time>", page, re.MULTILINE)
        heading2 = [gettext(heading) for heading in heading3]

        #for tag_elm in soup.find_all('div'):
        #print tag_elm.find('span', {'class' : 'ID2'})
        #<time class="date-created">Jan 24th 2013, 10:44</time>

        data = {'url': url, 'heading1': heading1, 'heading3':heading3, 'heading2':heading2}
        scraperwiki.sqlite.save(['url', 'heading1'], data)   # each entry is identified by its url
