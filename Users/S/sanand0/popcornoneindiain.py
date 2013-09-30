"""
This scrapes the Bollywood movie cast from http://popcorn.oneindia.in/bollywood
"""

import scraperwiki
import urlparse
import lxml.html

def get_url(url):
    return scraperwiki.scrape(url)

def get_movies(url, all_pages=True):
    """
    Yields the (name, url) for each movie in the movie list page passed.
    all_pages = True makes it go through pagination and return ALL results
    """
    tree = lxml.html.fromstring(get_url(url))

    for link in tree.cssselect('a'):
        href = link.get('href')
        name = link.text_content()
        if href.startswith('/title/') and name != '':
            yield name, urlparse.urljoin(url, href)

    # Scrape the rest of the pages if requested
    if all_pages:
        for link in tree.cssselect('.paginationTable a'):
            if link.text_content().isdigit():
                next_url = urlparse.urljoin(url, link.get('href'))
                for name, movie_url in get_movies(next_url, all_pages=False):
                    yield name, movie_url

def get_cast(movie_url):
    """
    Yields the (name, url) for each actor in a movie
    """
    cast_url = movie_url.replace('/title/', '/movie-cast/')
    tree = lxml.html.fromstring(get_url(cast_url))
    for link in tree.cssselect('.galleryBox a'):
        href = link.get('href')
        if href.startswith('/artist/'):
            yield link.text_content(), urlparse.urljoin(cast_url, href)

for alphabet in list('GHIJKLMNOPQRSTUVWXYZ') + ['0-9']:
    for movie, movie_url in get_movies('http://popcorn.oneindia.in/browse/%s/2/browse-movies.html' % alphabet):
        for actor, actor_url in get_cast(movie_url):
            scraperwiki.sqlite.save(unique_keys=['movie_url', 'actor_url'], data={
                'movie': movie,
                'actor': actor,
                'movie_url': movie_url,
                'actor_url': actor_url
            })
"""
This scrapes the Bollywood movie cast from http://popcorn.oneindia.in/bollywood
"""

import scraperwiki
import urlparse
import lxml.html

def get_url(url):
    return scraperwiki.scrape(url)

def get_movies(url, all_pages=True):
    """
    Yields the (name, url) for each movie in the movie list page passed.
    all_pages = True makes it go through pagination and return ALL results
    """
    tree = lxml.html.fromstring(get_url(url))

    for link in tree.cssselect('a'):
        href = link.get('href')
        name = link.text_content()
        if href.startswith('/title/') and name != '':
            yield name, urlparse.urljoin(url, href)

    # Scrape the rest of the pages if requested
    if all_pages:
        for link in tree.cssselect('.paginationTable a'):
            if link.text_content().isdigit():
                next_url = urlparse.urljoin(url, link.get('href'))
                for name, movie_url in get_movies(next_url, all_pages=False):
                    yield name, movie_url

def get_cast(movie_url):
    """
    Yields the (name, url) for each actor in a movie
    """
    cast_url = movie_url.replace('/title/', '/movie-cast/')
    tree = lxml.html.fromstring(get_url(cast_url))
    for link in tree.cssselect('.galleryBox a'):
        href = link.get('href')
        if href.startswith('/artist/'):
            yield link.text_content(), urlparse.urljoin(cast_url, href)

for alphabet in list('GHIJKLMNOPQRSTUVWXYZ') + ['0-9']:
    for movie, movie_url in get_movies('http://popcorn.oneindia.in/browse/%s/2/browse-movies.html' % alphabet):
        for actor, actor_url in get_cast(movie_url):
            scraperwiki.sqlite.save(unique_keys=['movie_url', 'actor_url'], data={
                'movie': movie,
                'actor': actor,
                'movie_url': movie_url,
                'actor_url': actor_url
            })
